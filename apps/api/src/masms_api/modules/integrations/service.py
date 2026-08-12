"""Integration framework application service (MOD-500)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.integrations import domain
from masms_api.modules.integrations.models import (
    ConnectionHealth,
    ExternalMapping,
    InboxEvent,
    IntegrationConnection,
    IntegrationOutboxEvent,
    SyncCursor,
    WebhookEvent,
)
from masms_api.modules.integrations.schemas import (
    ConnectionCreate,
    ConnectionHealthRecord,
    ExternalMappingCreate,
    InboxReceive,
    IntegrationOutboxCreate,
    SyncCursorUpsert,
    WebhookReceive,
)
from masms_api.observability.writer import ObservabilityWriter


class IntegrationsService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def _audit(
        self,
        *,
        action: str,
        entity_type: str,
        entity_id: UUID,
        payload: dict[str, Any] | None = None,
    ) -> None:
        self.obs.write_audit(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload,
        )

    def _get_connection(self, connection_id: UUID) -> IntegrationConnection:
        row = self.db.get(IntegrationConnection, connection_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Integration connection not found")
        return row

    def create_connection(self, data: ConnectionCreate) -> IntegrationConnection:
        domain.assert_provider(data.provider)
        domain.assert_no_raw_secrets(data.model_dump())
        credential_ref = data.credential_ref
        if data.auth_type != "none" and not credential_ref:
            credential_ref = domain.default_credential_ref(
                organization_id=str(self.ctx.organization_id),
                code=data.code.strip(),
            )
        domain.assert_credential_ref(data.auth_type, credential_ref)

        existing = self.db.scalar(
            select(IntegrationConnection).where(
                IntegrationConnection.organization_id == self.ctx.organization_id,
                IntegrationConnection.code == data.code.strip(),
            )
        )
        if existing is not None:
            raise ConflictError(f"Connection code '{data.code}' already exists")

        owner = data.owner_actor_id or self.ctx.actor_id
        row = IntegrationConnection(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code.strip(),
            provider=data.provider,
            auth_type=data.auth_type,
            status="draft",
            credential_ref=credential_ref,
            scopes_json=data.scopes_json,
            metadata_json=data.metadata_json,
            owner_actor_id=owner,
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        audit_payload = {
            "code": row.code,
            "provider": row.provider,
            "auth_type": row.auth_type,
            "credential_ref": row.credential_ref,
        }
        self._audit(
            action="ig_connection_create",
            entity_type="ig_connection",
            entity_id=row.id,
            payload=audit_payload,
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="ig_connection",
            aggregate_id=row.id,
            event_type="integrations.connection.created",
            payload={"connection_id": str(row.id), "code": row.code, "provider": row.provider},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_connections(
        self,
        *,
        status: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[IntegrationConnection], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(IntegrationConnection).where(
            IntegrationConnection.organization_id == self.ctx.organization_id
        )
        if status:
            stmt = stmt.where(IntegrationConnection.status == status)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(IntegrationConnection.updated_at.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def get_connection(self, connection_id: UUID) -> IntegrationConnection:
        return self._get_connection(connection_id)

    def _transition_connection(
        self,
        connection_id: UUID,
        *,
        target_status: str,
        expected_version: int | None,
        action: str,
    ) -> IntegrationConnection:
        row = self._get_connection(connection_id)
        domain.assert_expected_version(current=row.version, expected=expected_version)
        domain.assert_connection_transition(row.status, target_status)
        row.status = target_status
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self._audit(
            action=action,
            entity_type="ig_connection",
            entity_id=row.id,
            payload={"status": target_status, "version": row.version},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="ig_connection",
            aggregate_id=row.id,
            event_type=f"integrations.connection.{target_status}",
            payload={"connection_id": str(row.id), "status": target_status},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def activate_connection(
        self, connection_id: UUID, *, expected_version: int | None = None
    ) -> IntegrationConnection:
        return self._transition_connection(
            connection_id,
            target_status="active",
            expected_version=expected_version,
            action="ig_connection_activate",
        )

    def pause_connection(
        self, connection_id: UUID, *, expected_version: int | None = None
    ) -> IntegrationConnection:
        return self._transition_connection(
            connection_id,
            target_status="paused",
            expected_version=expected_version,
            action="ig_connection_pause",
        )

    def receive_webhook(self, data: WebhookReceive) -> WebhookEvent:
        self._get_connection(data.connection_id)
        existing = self.db.scalar(
            select(WebhookEvent).where(
                WebhookEvent.organization_id == self.ctx.organization_id,
                WebhookEvent.connection_id == data.connection_id,
                WebhookEvent.external_event_id == data.external_event_id,
            )
        )
        if existing is not None:
            raise ConflictError(
                f"Webhook event '{data.external_event_id}' already received"
            )

        row = WebhookEvent(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            connection_id=data.connection_id,
            external_event_id=data.external_event_id,
            event_type=data.event_type,
            payload_json=domain.redact_payload(data.payload),
            status="received",
        )
        self.uow.add(row)
        self._audit(
            action="ig_webhook_receive",
            entity_type="ig_webhook_event",
            entity_id=row.id,
            payload={
                "connection_id": str(data.connection_id),
                "external_event_id": data.external_event_id,
                "event_type": data.event_type,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="ig_webhook_event",
            aggregate_id=row.id,
            event_type="integrations.webhook.received",
            payload={
                "connection_id": str(data.connection_id),
                "external_event_id": data.external_event_id,
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def upsert_sync_cursor(self, data: SyncCursorUpsert) -> SyncCursor:
        self._get_connection(data.connection_id)
        row = self.db.scalar(
            select(SyncCursor).where(
                SyncCursor.organization_id == self.ctx.organization_id,
                SyncCursor.connection_id == data.connection_id,
                SyncCursor.stream_key == data.stream_key,
            )
        )
        if row is None:
            row = SyncCursor(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                connection_id=data.connection_id,
                stream_key=data.stream_key,
                cursor_value=data.cursor_value,
            )
            self.uow.add(row)
            action = "ig_sync_cursor_create"
        else:
            row.cursor_value = data.cursor_value
            action = "ig_sync_cursor_update"
        self._audit(
            action=action,
            entity_type="ig_sync_cursor",
            entity_id=row.id,
            payload={
                "connection_id": str(data.connection_id),
                "stream_key": data.stream_key,
            },
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def get_sync_cursor(
        self, *, connection_id: UUID, stream_key: str
    ) -> SyncCursor:
        self._get_connection(connection_id)
        row = self.db.scalar(
            select(SyncCursor).where(
                SyncCursor.organization_id == self.ctx.organization_id,
                SyncCursor.connection_id == connection_id,
                SyncCursor.stream_key == stream_key,
            )
        )
        if row is None:
            raise NotFoundError("Sync cursor not found")
        return row

    def create_mapping(self, data: ExternalMappingCreate) -> ExternalMapping:
        self._get_connection(data.connection_id)
        existing_internal = self.db.scalar(
            select(ExternalMapping).where(
                ExternalMapping.organization_id == self.ctx.organization_id,
                ExternalMapping.connection_id == data.connection_id,
                ExternalMapping.internal_entity_type == data.internal_entity_type,
                ExternalMapping.internal_entity_id == data.internal_entity_id,
            )
        )
        if existing_internal is not None:
            raise ConflictError("Internal entity mapping already exists")
        existing_external = self.db.scalar(
            select(ExternalMapping).where(
                ExternalMapping.organization_id == self.ctx.organization_id,
                ExternalMapping.connection_id == data.connection_id,
                ExternalMapping.external_entity_type == data.external_entity_type,
                ExternalMapping.external_entity_id == data.external_entity_id,
            )
        )
        if existing_external is not None:
            raise ConflictError("External entity mapping already exists")

        row = ExternalMapping(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            connection_id=data.connection_id,
            internal_entity_type=data.internal_entity_type,
            internal_entity_id=data.internal_entity_id,
            external_entity_type=data.external_entity_type,
            external_entity_id=data.external_entity_id,
        )
        self.uow.add(row)
        self._audit(
            action="ig_mapping_create",
            entity_type="ig_external_mapping",
            entity_id=row.id,
            payload={
                "connection_id": str(data.connection_id),
                "internal_entity_type": data.internal_entity_type,
                "external_entity_id": data.external_entity_id,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="ig_external_mapping",
            aggregate_id=row.id,
            event_type="integrations.mapping.created",
            payload={"mapping_id": str(row.id), "connection_id": str(data.connection_id)},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_mappings(
        self,
        *,
        connection_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[ExternalMapping], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(ExternalMapping).where(
            ExternalMapping.organization_id == self.ctx.organization_id
        )
        if connection_id is not None:
            stmt = stmt.where(ExternalMapping.connection_id == connection_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(ExternalMapping.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def enqueue_ig_outbox(self, data: IntegrationOutboxCreate) -> IntegrationOutboxEvent:
        self._get_connection(data.connection_id)
        row = IntegrationOutboxEvent(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            connection_id=data.connection_id,
            event_type=data.event_type,
            payload_json=domain.redact_payload(data.payload),
            status="pending",
            attempt_count=0,
        )
        self.uow.add(row)
        self._audit(
            action="ig_outbox_enqueue",
            entity_type="ig_outbox_event",
            entity_id=row.id,
            payload={
                "connection_id": str(data.connection_id),
                "event_type": data.event_type,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="ig_outbox_event",
            aggregate_id=row.id,
            event_type="integrations.outbox.enqueued",
            payload={"outbox_id": str(row.id), "connection_id": str(data.connection_id)},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_ig_outbox(
        self,
        *,
        connection_id: UUID | None = None,
        status: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[IntegrationOutboxEvent], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(IntegrationOutboxEvent).where(
            IntegrationOutboxEvent.organization_id == self.ctx.organization_id
        )
        if connection_id is not None:
            stmt = stmt.where(IntegrationOutboxEvent.connection_id == connection_id)
        if status:
            stmt = stmt.where(IntegrationOutboxEvent.status == status)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(IntegrationOutboxEvent.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def relay_ig_outbox(
        self, outbox_id: UUID, *, force_fail: bool = False
    ) -> IntegrationOutboxEvent:
        row = self.db.get(IntegrationOutboxEvent, outbox_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Integration outbox event not found")
        if row.status not in {"pending", "failed"}:
            raise ConflictError("Outbox event is not relayable")

        row.attempt_count += 1
        now = datetime.now(UTC)
        if force_fail:
            row.status = "failed"
            row.last_error = "Simulated relay failure"
            self._record_health_failure(row.connection_id, row.last_error)
        else:
            row.status = "sent"
            row.sent_at = now
            row.last_error = None
            self._record_health_success(row.connection_id)

        self._audit(
            action="ig_outbox_relay",
            entity_type="ig_outbox_event",
            entity_id=row.id,
            payload={"status": row.status, "attempt_count": row.attempt_count},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def receive_inbox(self, data: InboxReceive) -> InboxEvent:
        self._get_connection(data.connection_id)
        existing = self.db.scalar(
            select(InboxEvent).where(
                InboxEvent.organization_id == self.ctx.organization_id,
                InboxEvent.connection_id == data.connection_id,
                InboxEvent.external_event_id == data.external_event_id,
            )
        )
        if existing is not None:
            raise ConflictError(
                f"Inbox event '{data.external_event_id}' already received"
            )

        row = InboxEvent(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            connection_id=data.connection_id,
            external_event_id=data.external_event_id,
            event_type=data.event_type,
            payload_json=domain.redact_payload(data.payload),
            status="pending",
        )
        self.uow.add(row)
        self._audit(
            action="ig_inbox_receive",
            entity_type="ig_inbox_event",
            entity_id=row.id,
            payload={
                "connection_id": str(data.connection_id),
                "external_event_id": data.external_event_id,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="ig_inbox_event",
            aggregate_id=row.id,
            event_type="integrations.inbox.received",
            payload={
                "connection_id": str(data.connection_id),
                "external_event_id": data.external_event_id,
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_inbox(
        self,
        *,
        connection_id: UUID | None = None,
        status: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[InboxEvent], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(InboxEvent).where(
            InboxEvent.organization_id == self.ctx.organization_id
        )
        if connection_id is not None:
            stmt = stmt.where(InboxEvent.connection_id == connection_id)
        if status:
            stmt = stmt.where(InboxEvent.status == status)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(InboxEvent.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def process_inbox(
        self, inbox_id: UUID, *, force_fail: bool = False
    ) -> InboxEvent:
        row = self.db.get(InboxEvent, inbox_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Inbox event not found")
        if row.status != "pending":
            raise ConflictError("Inbox event already processed")

        now = datetime.now(UTC)
        mapping_count_before = self.db.scalar(
            select(func.count()).select_from(
                select(ExternalMapping)
                .where(
                    ExternalMapping.organization_id == self.ctx.organization_id,
                    ExternalMapping.connection_id == row.connection_id,
                )
                .subquery()
            )
        ) or 0

        if force_fail:
            row.status = "failed"
            row.failure_reason = "Simulated processing failure"
            row.processed_at = now
            self._record_health_failure(row.connection_id, row.failure_reason)
            self._audit(
                action="ig_inbox_process_failed",
                entity_type="ig_inbox_event",
                entity_id=row.id,
                payload={"failure_reason": row.failure_reason},
            )
            self.uow.commit()
            self.db.refresh(row)
            mapping_count_after = self.db.scalar(
                select(func.count()).select_from(
                    select(ExternalMapping)
                    .where(
                        ExternalMapping.organization_id == self.ctx.organization_id,
                        ExternalMapping.connection_id == row.connection_id,
                    )
                    .subquery()
                )
            ) or 0
            if mapping_count_after != mapping_count_before:
                raise ValidationAppError("Mapping count changed on failed inbox process")
            return row

        payload: dict[str, Any] = {}
        if row.payload_json:
            try:
                parsed = json.loads(row.payload_json)
                if isinstance(parsed, dict):
                    payload = parsed
            except json.JSONDecodeError:
                payload = {}

        row.status = "processed"
        row.processed_at = now
        if domain.mapping_fields_present(payload):
            mapping = ExternalMapping(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                connection_id=row.connection_id,
                internal_entity_type=str(payload["internal_entity_type"]),
                internal_entity_id=str(payload["internal_entity_id"]),
                external_entity_type=str(payload["external_entity_type"]),
                external_entity_id=str(payload["external_entity_id"]),
            )
            self.uow.add(mapping)
            self._audit(
                action="ig_mapping_create_from_inbox",
                entity_type="ig_external_mapping",
                entity_id=mapping.id,
                payload={
                    "inbox_id": str(row.id),
                    "external_entity_id": mapping.external_entity_id,
                },
            )

        self._record_health_success(row.connection_id)
        self._audit(
            action="ig_inbox_process",
            entity_type="ig_inbox_event",
            entity_id=row.id,
            payload={"status": "processed"},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def _get_or_create_health(self, connection_id: UUID) -> ConnectionHealth:
        row = self.db.scalar(
            select(ConnectionHealth).where(
                ConnectionHealth.organization_id == self.ctx.organization_id,
                ConnectionHealth.connection_id == connection_id,
            )
        )
        if row is None:
            row = ConnectionHealth(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                connection_id=connection_id,
                health_status="healthy",
                failure_count=0,
            )
            self.uow.add(row)
        elif row.failure_count is None:
            row.failure_count = 0
        return row

    def _record_health_success(self, connection_id: UUID) -> None:
        health = self._get_or_create_health(connection_id)
        now = datetime.now(UTC)
        health.health_status = "healthy"
        health.last_success_at = now
        health.checked_at = now
        health.last_error = None

    def _record_health_failure(self, connection_id: UUID, error: str) -> None:
        health = self._get_or_create_health(connection_id)
        now = datetime.now(UTC)
        health.failure_count = (health.failure_count or 0) + 1
        health.last_failure_at = now
        health.last_error = error
        health.checked_at = now
        health.health_status = "degraded" if health.failure_count < 3 else "down"

    def record_health(
        self, connection_id: UUID, data: ConnectionHealthRecord
    ) -> ConnectionHealth:
        self._get_connection(connection_id)
        if data.health_status not in domain.HEALTH_STATUSES:
            raise ValidationAppError(f"Invalid health_status '{data.health_status}'")
        health = self._get_or_create_health(connection_id)
        health.health_status = data.health_status
        health.last_error = data.last_error
        health.checked_at = datetime.now(UTC)
        self._audit(
            action="ig_health_record",
            entity_type="ig_connection_health",
            entity_id=health.id,
            payload={"health_status": data.health_status},
        )
        self.uow.commit()
        self.db.refresh(health)
        return health

    def get_health(self, connection_id: UUID) -> ConnectionHealth:
        self._get_connection(connection_id)
        row = self.db.scalar(
            select(ConnectionHealth).where(
                ConnectionHealth.organization_id == self.ctx.organization_id,
                ConnectionHealth.connection_id == connection_id,
            )
        )
        if row is None:
            raise NotFoundError("Connection health not found")
        return row

    def check_health(self, connection_id: UUID) -> ConnectionHealth:
        conn = self._get_connection(connection_id)
        health = self._get_or_create_health(connection_id)
        now = datetime.now(UTC)
        health.checked_at = now
        if conn.status == "active":
            health.health_status = "healthy"
        elif conn.status == "error":
            health.health_status = "down"
        else:
            health.health_status = "degraded"
        self.uow.commit()
        self.db.refresh(health)
        return health
