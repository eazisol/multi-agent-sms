"""Notifications application service (MOD-440)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.notifications import domain
from masms_api.modules.notifications.models import (
    Notification,
    NotificationDeadLetter,
    NotificationDelivery,
    NotificationDigest,
    NotificationPreference,
    NotificationRetry,
    NotificationTemplate,
)
from masms_api.modules.notifications.schemas import (
    DigestCreate,
    MarkRead,
    NotificationCreate,
    PreferenceUpsert,
    ProcessDigest,
    SimulateDeliver,
    TemplateCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class NotificationService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_notification(self, data: NotificationCreate) -> Notification:
        domain.assert_channel(data.channel)
        domain.assert_priority(data.priority)
        domain.assert_type(data.notification_type)
        key = data.idempotency_key.strip() if data.idempotency_key else None
        if key:
            existing = self.db.scalar(
                select(Notification).where(
                    Notification.organization_id == self.ctx.organization_id,
                    Notification.idempotency_key == key,
                )
            )
            if existing is not None:
                raise ConflictError(
                    f"Notification with idempotency_key '{key}' already exists"
                )
        row = Notification(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            recipient_actor_id=data.recipient_actor_id,
            notification_type=data.notification_type,
            channel=data.channel,
            title=data.title.strip(),
            body=data.body,
            related_entity_type=data.related_entity_type,
            related_entity_id=data.related_entity_id,
            priority=data.priority,
            status="pending",
            scheduled_at=data.scheduled_at,
            idempotency_key=key,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="ntf_notification_create",
            entity_type="ntf_notification",
            entity_id=row.id,
            payload={
                "notification_type": row.notification_type,
                "channel": row.channel,
                "priority": row.priority,
                "idempotency_key": key,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="ntf_notification",
            aggregate_id=row.id,
            event_type="notification.created",
            payload={
                "notification_id": str(row.id),
                "notification_type": row.notification_type,
                "channel": row.channel,
            },
            correlation_id=self.ctx.correlation_id,
            project_id=data.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def get_notification(self, notification_id: UUID) -> Notification:
        row = self.db.get(Notification, notification_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Notification not found")
        return row

    def list_notifications(
        self,
        *,
        status: str | None = None,
        channel: str | None = None,
        recipient_actor_id: UUID | None = None,
        q: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Notification], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(Notification).where(
            Notification.organization_id == self.ctx.organization_id
        )
        if status:
            stmt = stmt.where(Notification.status == status)
        if channel:
            stmt = stmt.where(Notification.channel == channel)
        if recipient_actor_id is not None:
            stmt = stmt.where(Notification.recipient_actor_id == recipient_actor_id)
        if q:
            like = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(Notification.title.ilike(like), Notification.body.ilike(like))
            )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(Notification.updated_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def mark_read(self, notification_id: UUID, data: MarkRead) -> Notification:
        row = self.get_notification(notification_id)
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        if row.status not in {"sent", "delivered", "read"}:
            domain.assert_notification_transition(
                from_status=row.status, to_status="read"
            )
        if row.status != "read":
            if row.status in {"pending", "queued", "failed"}:
                raise ValidationAppError(
                    f"Cannot mark notification as read from status '{row.status}'"
                )
            row.status = "read"
            row.read_at = datetime.now(UTC)
            row.version += 1
            row.updated_by_actor_id = self.ctx.actor_id
            row.updated_at = datetime.now(UTC)
            self.obs.write_audit(
                action="ntf_notification_mark_read",
                entity_type="ntf_notification",
                entity_id=row.id,
                payload={"status": row.status},
            )
            enqueue_outbox(
                self.db,
                organization_id=self.ctx.organization_id,
                aggregate_type="ntf_notification",
                aggregate_id=row.id,
                event_type="notification.read",
                payload={"notification_id": str(row.id)},
                correlation_id=self.ctx.correlation_id,
                project_id=row.project_id,
            )
            self.uow.commit()
            self.db.refresh(row)
        return row

    def _next_attempt_number(self, notification_id: UUID) -> int:
        current = self.db.scalar(
            select(func.max(NotificationDelivery.attempt_number)).where(
                NotificationDelivery.organization_id == self.ctx.organization_id,
                NotificationDelivery.notification_id == notification_id,
            )
        )
        return int(current or 0) + 1

    def _move_to_dead_letter(
        self, row: Notification, *, reason: str, last_error: str | None
    ) -> None:
        domain.assert_notification_transition(
            from_status=row.status, to_status="dead_lettered"
        )
        row.status = "dead_lettered"
        row.failure_reason = last_error or reason
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        row.updated_at = datetime.now(UTC)
        dl = NotificationDeadLetter(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            notification_id=row.id,
            reason=reason,
            last_error=last_error,
            attempt_count=row.retry_count,
            status="open",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(dl)
        self.obs.write_audit(
            action="ntf_dead_letter_open",
            entity_type="ntf_dead_letter",
            entity_id=dl.id,
            payload={"notification_id": str(row.id), "attempt_count": row.retry_count},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="ntf_dead_letter",
            aggregate_id=dl.id,
            event_type="notification.dead_lettered",
            payload={"notification_id": str(row.id), "dead_letter_id": str(dl.id)},
            correlation_id=self.ctx.correlation_id,
            project_id=row.project_id,
        )

    def simulate_deliver(
        self, notification_id: UUID, data: SimulateDeliver
    ) -> Notification:
        row = self.get_notification(notification_id)
        if row.status in {"read", "cancelled", "dead_lettered"}:
            raise ValidationAppError(
                f"Cannot deliver notification in status '{row.status}'"
            )
        prefs = self.list_preferences(actor_id=row.recipient_actor_id)
        if domain.is_delivery_suppressed(prefs, row):
            raise ValidationAppError("Delivery suppressed by recipient preference")

        attempt = self._next_attempt_number(notification_id)
        now = datetime.now(UTC)
        if data.succeed:
            delivery = NotificationDelivery(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                notification_id=row.id,
                channel=row.channel,
                status="succeeded",
                attempt_number=attempt,
                provider_ref="local-sim",
                error_message=None,
                created_by_actor_id=self.ctx.actor_id,
            )
            self.uow.add(delivery)
            if row.status not in {"sent", "delivered"}:
                domain.assert_notification_transition(
                    from_status=row.status, to_status="delivered"
                )
            row.status = "delivered"
            row.sent_at = row.sent_at or now
            row.delivered_at = now
            row.failure_reason = None
            row.version += 1
            row.updated_by_actor_id = self.ctx.actor_id
            row.updated_at = now
            self.obs.write_audit(
                action="ntf_delivery_succeeded",
                entity_type="ntf_notification",
                entity_id=row.id,
                payload={"attempt_number": attempt, "provider_ref": "local-sim"},
            )
            enqueue_outbox(
                self.db,
                organization_id=self.ctx.organization_id,
                aggregate_type="ntf_notification",
                aggregate_id=row.id,
                event_type="notification.delivered",
                payload={"notification_id": str(row.id), "attempt_number": attempt},
                correlation_id=self.ctx.correlation_id,
                project_id=row.project_id,
            )
        else:
            err = data.error_message or "Simulated delivery failure"
            delivery = NotificationDelivery(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                notification_id=row.id,
                channel=row.channel,
                status="failed",
                attempt_number=attempt,
                provider_ref="local-sim",
                error_message=err,
                created_by_actor_id=self.ctx.actor_id,
            )
            self.uow.add(delivery)
            row.retry_count = attempt
            row.failure_reason = err
            row.updated_by_actor_id = self.ctx.actor_id
            row.updated_at = now
            if attempt >= domain.MAX_DELIVERY_ATTEMPTS:
                self._move_to_dead_letter(
                    row, reason="Max delivery attempts exhausted", last_error=err
                )
            else:
                if row.status != "failed":
                    domain.assert_notification_transition(
                        from_status=row.status, to_status="failed"
                    )
                row.status = "failed"
                row.version += 1
                retry = NotificationRetry(
                    id=uuid4(),
                    organization_id=self.ctx.organization_id,
                    notification_id=row.id,
                    delivery_id=delivery.id,
                    attempt_number=attempt,
                    scheduled_at=now,
                    status="executed",
                    reason=err,
                )
                self.uow.add(retry)
                self.obs.write_audit(
                    action="ntf_delivery_failed",
                    entity_type="ntf_notification",
                    entity_id=row.id,
                    payload={"attempt_number": attempt, "error_message": err},
                )
                enqueue_outbox(
                    self.db,
                    organization_id=self.ctx.organization_id,
                    aggregate_type="ntf_notification",
                    aggregate_id=row.id,
                    event_type="notification.delivery_failed",
                    payload={
                        "notification_id": str(row.id),
                        "attempt_number": attempt,
                    },
                    correlation_id=self.ctx.correlation_id,
                    project_id=row.project_id,
                )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def retry_delivery(self, notification_id: UUID) -> Notification:
        row = self.get_notification(notification_id)
        if row.status != "failed":
            raise ValidationAppError("Only failed notifications can be retried")
        if row.retry_count >= domain.MAX_DELIVERY_ATTEMPTS:
            self._move_to_dead_letter(
                row,
                reason="Retry exhausted",
                last_error=row.failure_reason,
            )
            self.uow.commit()
            self.db.refresh(row)
            return row
        now = datetime.now(UTC)
        retry = NotificationRetry(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            notification_id=row.id,
            delivery_id=None,
            attempt_number=row.retry_count + 1,
            scheduled_at=now,
            status="scheduled",
            reason="manual_retry",
        )
        self.uow.add(retry)
        domain.assert_notification_transition(from_status=row.status, to_status="pending")
        row.status = "pending"
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        row.updated_at = now
        self.obs.write_audit(
            action="ntf_delivery_retry",
            entity_type="ntf_notification",
            entity_id=row.id,
            payload={"attempt_number": retry.attempt_number},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="ntf_notification",
            aggregate_id=row.id,
            event_type="notification.retry_scheduled",
            payload={"notification_id": str(row.id)},
            correlation_id=self.ctx.correlation_id,
            project_id=row.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def upsert_preference(self, data: PreferenceUpsert) -> NotificationPreference:
        domain.assert_channel(data.channel)
        domain.assert_type(data.notification_type)
        domain.assert_preference_allows_mute(
            notification_type=data.notification_type, enabled=data.enabled
        )
        existing = self.db.scalar(
            select(NotificationPreference).where(
                NotificationPreference.organization_id == self.ctx.organization_id,
                NotificationPreference.actor_id == data.actor_id,
                NotificationPreference.channel == data.channel,
                NotificationPreference.notification_type == data.notification_type,
            )
        )
        now = datetime.now(UTC)
        if existing is None:
            row = NotificationPreference(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                actor_id=data.actor_id,
                channel=data.channel,
                notification_type=data.notification_type,
                enabled=data.enabled,
                quiet_hours_start=data.quiet_hours_start,
                quiet_hours_end=data.quiet_hours_end,
                updated_by_actor_id=self.ctx.actor_id,
            )
            self.uow.add(row)
            action = "ntf_preference_create"
        else:
            domain.assert_expected_version(
                current=existing.version, expected=data.expected_version
            )
            existing.enabled = data.enabled
            existing.quiet_hours_start = data.quiet_hours_start
            existing.quiet_hours_end = data.quiet_hours_end
            existing.version += 1
            existing.updated_by_actor_id = self.ctx.actor_id
            existing.updated_at = now
            row = existing
            action = "ntf_preference_update"
        self.obs.write_audit(
            action=action,
            entity_type="ntf_preference",
            entity_id=row.id,
            payload={
                "channel": row.channel,
                "notification_type": row.notification_type,
                "enabled": row.enabled,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="ntf_preference",
            aggregate_id=row.id,
            event_type="notification.preference_upserted",
            payload={
                "preference_id": str(row.id),
                "notification_type": row.notification_type,
                "enabled": row.enabled,
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_preferences(
        self, *, actor_id: UUID | None = None
    ) -> list[NotificationPreference]:
        stmt = select(NotificationPreference).where(
            NotificationPreference.organization_id == self.ctx.organization_id
        )
        if actor_id is not None:
            stmt = stmt.where(NotificationPreference.actor_id == actor_id)
        return list(
            self.db.scalars(stmt.order_by(NotificationPreference.updated_at.desc()))
        )

    def create_template(self, data: TemplateCreate) -> NotificationTemplate:
        domain.assert_channel(data.channel)
        domain.assert_type(data.notification_type)
        existing = self.db.scalar(
            select(NotificationTemplate).where(
                NotificationTemplate.organization_id == self.ctx.organization_id,
                NotificationTemplate.code == data.code,
            )
        )
        if existing is not None:
            raise ConflictError(f"Template code '{data.code}' already exists")
        row = NotificationTemplate(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code.strip(),
            channel=data.channel,
            subject=data.subject.strip(),
            body_template=data.body_template,
            notification_type=data.notification_type,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="ntf_template_create",
            entity_type="ntf_template",
            entity_id=row.id,
            payload={"code": row.code},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="ntf_template",
            aggregate_id=row.id,
            event_type="notification.template_created",
            payload={"template_id": str(row.id), "code": row.code},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_templates(self) -> list[NotificationTemplate]:
        return list(
            self.db.scalars(
                select(NotificationTemplate)
                .where(NotificationTemplate.organization_id == self.ctx.organization_id)
                .order_by(NotificationTemplate.code.asc())
            )
        )

    def list_dead_letters(
        self, *, status: str | None = None, limit: int = 20, offset: int = 0
    ) -> tuple[list[NotificationDeadLetter], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(NotificationDeadLetter).where(
            NotificationDeadLetter.organization_id == self.ctx.organization_id
        )
        if status:
            stmt = stmt.where(NotificationDeadLetter.status == status)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(NotificationDeadLetter.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def replay_dead_letter(self, dead_letter_id: UUID) -> NotificationDeadLetter:
        dl = self.db.get(NotificationDeadLetter, dead_letter_id)
        if dl is None or dl.organization_id != self.ctx.organization_id:
            raise NotFoundError("Dead letter not found")
        if dl.status != "open":
            raise ValidationAppError(
                f"Dead letter status '{dl.status}' cannot be replayed"
            )
        row = self.get_notification(dl.notification_id)
        domain.assert_notification_transition(
            from_status=row.status, to_status="pending"
        )
        now = datetime.now(UTC)
        row.status = "pending"
        row.retry_count = 0
        row.failure_reason = None
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        row.updated_at = now
        dl.status = "replayed"
        dl.replayed_at = now
        dl.updated_at = now
        self.uow.add(
            NotificationRetry(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                notification_id=row.id,
                delivery_id=None,
                attempt_number=1,
                scheduled_at=now,
                status="scheduled",
                reason="dead_letter_replay",
            )
        )
        self.obs.write_audit(
            action="ntf_dead_letter_replay",
            entity_type="ntf_dead_letter",
            entity_id=dl.id,
            payload={"notification_id": str(row.id), "status": "pending"},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="ntf_dead_letter",
            aggregate_id=dl.id,
            event_type="notification.dead_letter_replayed",
            payload={
                "dead_letter_id": str(dl.id),
                "notification_id": str(row.id),
            },
            correlation_id=self.ctx.correlation_id,
            project_id=row.project_id,
        )
        self.uow.commit()
        self.db.refresh(dl)
        return dl

    def create_digest(self, data: DigestCreate) -> NotificationDigest:
        domain.assert_channel(data.channel)
        row = NotificationDigest(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            recipient_actor_id=data.recipient_actor_id,
            channel=data.channel,
            status="pending",
            window_start=data.window_start,
            window_end=data.window_end,
            item_count=data.item_count,
            summary=data.summary,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="ntf_digest_create",
            entity_type="ntf_digest",
            entity_id=row.id,
            payload={"channel": row.channel},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="ntf_digest",
            aggregate_id=row.id,
            event_type="notification.digest_created",
            payload={"digest_id": str(row.id)},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_digests(
        self, *, status: str | None = None, limit: int = 20, offset: int = 0
    ) -> tuple[list[NotificationDigest], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(NotificationDigest).where(
            NotificationDigest.organization_id == self.ctx.organization_id
        )
        if status:
            stmt = stmt.where(NotificationDigest.status == status)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(NotificationDigest.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def process_digest(
        self, digest_id: UUID, data: ProcessDigest
    ) -> NotificationDigest:
        row = self.db.get(NotificationDigest, digest_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Digest not found")
        if row.status == "processed":
            return row
        now = datetime.now(UTC)
        row.status = "processed"
        if data.item_count is not None:
            row.item_count = data.item_count
        if data.summary is not None:
            row.summary = data.summary
        row.processed_at = now
        row.updated_at = now
        self.obs.write_audit(
            action="ntf_digest_process",
            entity_type="ntf_digest",
            entity_id=row.id,
            payload={"item_count": row.item_count},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="ntf_digest",
            aggregate_id=row.id,
            event_type="notification.digest_processed",
            payload={"digest_id": str(row.id)},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row
