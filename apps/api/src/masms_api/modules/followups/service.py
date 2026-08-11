"""Follow-ups application service (MOD-340)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.configadmin import domain as config_domain
from masms_api.modules.configadmin.models import ConfigurationVersion
from masms_api.modules.followups import domain
from masms_api.modules.followups.models import (
    BusinessDeadline,
    ClosureEvidence,
    EscalationEvent,
    FollowUp,
    FollowUpLink,
    ReminderEvent,
    SlaPause,
)
from masms_api.modules.followups.schemas import (
    ChildLinkCreate,
    ClosureEvidenceCreate,
    FollowUpCreate,
    ProcessOverdueResult,
    SlaPauseCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class FollowUpService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create(self, data: FollowUpCreate) -> FollowUp:
        rule_version_id = data.rule_version_id or self._effective_config_id()
        now = datetime.now(UTC)
        if data.due_at is not None:
            due_at = data.due_at if data.due_at.tzinfo else data.due_at.replace(tzinfo=UTC)
            wall = due_at
            offset_hours = max(1, int((due_at - now).total_seconds() // 3600) or 1)
        else:
            wall = now + timedelta(hours=data.due_offset_hours)
            due_at = domain.add_business_hours(start=now, hours=data.due_offset_hours)
            offset_hours = data.due_offset_hours

        domain.assert_required_fields(
            owner_actor_id=data.owner_actor_id,
            due_at=due_at,
            rule_version_id=rule_version_id,
            closure_condition=data.closure_condition,
            required_response=data.required_response,
        )

        parent_id = data.parent_followup_id
        return_to = data.return_to_followup_id
        if parent_id is not None:
            parent = self._get(parent_id)
            domain.assert_open(parent.status)
            if return_to is None:
                return_to = parent.id

        row = FollowUp(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            title=data.title,
            direction=data.direction,
            source_entity_type=data.source_entity_type,
            source_entity_id=data.source_entity_id,
            source_actor_id=self.ctx.actor_id,
            recipient_actor_id=data.recipient_actor_id,
            owner_actor_id=data.owner_actor_id,
            required_response=data.required_response.strip(),
            closure_condition=data.closure_condition.strip(),
            status="open",
            due_at=due_at,
            rule_version_id=rule_version_id,
            reminder_offset_hours=data.reminder_offset_hours,
            escalation_after_hours=data.escalation_after_hours,
            escalate_to_role_code=data.escalate_to_role_code or "PM",
            parent_followup_id=parent_id,
            return_to_followup_id=return_to,
            sla_paused=False,
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)

        deadline = BusinessDeadline(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            followup_id=row.id,
            calendar_code=data.calendar_code,
            due_offset_hours=offset_hours,
            wall_clock_due_at=wall,
            business_due_at=due_at,
            computed_at=now,
        )
        self.uow.add(deadline)

        reminder = ReminderEvent(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            followup_id=row.id,
            scheduled_for=due_at - timedelta(hours=data.reminder_offset_hours),
            status="scheduled",
            channel="in_app",
        )
        self.uow.add(reminder)

        if parent_id is not None:
            self.uow.add(
                FollowUpLink(
                    id=uuid4(),
                    organization_id=self.ctx.organization_id,
                    parent_followup_id=parent_id,
                    child_followup_id=row.id,
                    link_type="child",
                    mandatory=True,
                    return_route="parent",
                    created_by_actor_id=self.ctx.actor_id,
                )
            )

        self.obs.write_audit(
            action="flu_create",
            entity_type="flu_followup",
            entity_id=row.id,
            payload={
                "due_at": due_at.isoformat(),
                "owner_actor_id": str(row.owner_actor_id),
                "rule_version_id": str(rule_version_id) if rule_version_id else None,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="flu_followup",
            aggregate_id=row.id,
            event_type="followup.created",
            payload={"title": row.title, "due_at": due_at.isoformat()},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def get(self, followup_id: UUID) -> FollowUp:
        return self._get(followup_id)

    def list_open(self) -> list[FollowUp]:
        return list(
            self.db.scalars(
                select(FollowUp)
                .where(
                    FollowUp.organization_id == self.ctx.organization_id,
                    FollowUp.status == "open",
                )
                .order_by(FollowUp.due_at.asc())
            ).all()
        )

    def link_child(self, parent_id: UUID, data: ChildLinkCreate) -> FollowUpLink:
        parent = self._get(parent_id)
        child = self._get(data.child_followup_id)
        domain.assert_open(parent.status)
        domain.assert_open(child.status)
        existing = self.db.scalar(
            select(FollowUpLink).where(
                FollowUpLink.organization_id == self.ctx.organization_id,
                FollowUpLink.parent_followup_id == parent_id,
                FollowUpLink.child_followup_id == data.child_followup_id,
            )
        )
        if existing is not None:
            raise ConflictError("Parent-child link already exists")

        child.parent_followup_id = parent_id
        if child.return_to_followup_id is None:
            child.return_to_followup_id = parent_id
        child.updated_by_actor_id = self.ctx.actor_id
        child.version += 1
        self.uow.add(child)

        link = FollowUpLink(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            parent_followup_id=parent_id,
            child_followup_id=data.child_followup_id,
            link_type=data.link_type,
            mandatory=data.mandatory,
            return_route=data.return_route,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(link)
        self.obs.write_audit(
            action="flu_link_child",
            entity_type="flu_followup",
            entity_id=parent_id,
            payload={
                "child_followup_id": str(data.child_followup_id),
                "return_route": data.return_route,
            },
        )
        self.uow.commit()
        self.uow.refresh(link)
        return link

    def list_links(self, parent_id: UUID) -> list[FollowUpLink]:
        self._get(parent_id)
        return list(
            self.db.scalars(
                select(FollowUpLink).where(
                    FollowUpLink.organization_id == self.ctx.organization_id,
                    FollowUpLink.parent_followup_id == parent_id,
                )
            ).all()
        )

    def list_reminders(self, followup_id: UUID) -> list[ReminderEvent]:
        self._get(followup_id)
        return list(
            self.db.scalars(
                select(ReminderEvent)
                .where(
                    ReminderEvent.organization_id == self.ctx.organization_id,
                    ReminderEvent.followup_id == followup_id,
                )
                .order_by(ReminderEvent.scheduled_for.asc())
            ).all()
        )

    def list_escalations(self, followup_id: UUID) -> list[EscalationEvent]:
        self._get(followup_id)
        return list(
            self.db.scalars(
                select(EscalationEvent)
                .where(
                    EscalationEvent.organization_id == self.ctx.organization_id,
                    EscalationEvent.followup_id == followup_id,
                )
                .order_by(EscalationEvent.triggered_at.asc())
            ).all()
        )

    def get_deadline(self, followup_id: UUID) -> BusinessDeadline:
        self._get(followup_id)
        row = self.db.scalar(
            select(BusinessDeadline).where(
                BusinessDeadline.organization_id == self.ctx.organization_id,
                BusinessDeadline.followup_id == followup_id,
            )
        )
        if row is None:
            raise NotFoundError("Business deadline not found")
        return row

    def pause_sla(self, followup_id: UUID, data: SlaPauseCreate) -> SlaPause:
        row = self._get(followup_id)
        domain.assert_open(row.status)
        domain.assert_pause_fields(
            reason=data.reason, next_action=data.next_action, review_at=data.review_at
        )
        if row.sla_paused:
            raise ConflictError("SLA already paused")

        review = data.review_at if data.review_at.tzinfo else data.review_at.replace(tzinfo=UTC)
        pause = SlaPause(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            followup_id=followup_id,
            reason=data.reason.strip(),
            responsible_actor_id=data.responsible_actor_id or self.ctx.actor_id,
            next_action=data.next_action.strip(),
            review_at=review,
            status="open",
            created_by_actor_id=self.ctx.actor_id,
        )
        row.sla_paused = True
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self.uow.add(row)
        self.uow.add(pause)
        self.obs.write_audit(
            action="flu_sla_pause",
            entity_type="flu_followup",
            entity_id=followup_id,
            payload={"pause_id": str(pause.id), "reason": pause.reason},
        )
        self.uow.commit()
        self.uow.refresh(pause)
        return pause

    def resume_sla(self, followup_id: UUID) -> SlaPause:
        row = self._get(followup_id)
        pause = self.db.scalar(
            select(SlaPause).where(
                SlaPause.organization_id == self.ctx.organization_id,
                SlaPause.followup_id == followup_id,
                SlaPause.status == "open",
            )
        )
        if pause is None:
            raise NotFoundError("Open SLA pause not found")
        pause.status = "resumed"
        pause.resumed_at = datetime.now(UTC)
        pause.resumed_by_actor_id = self.ctx.actor_id
        row.sla_paused = False
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self.uow.add(pause)
        self.uow.add(row)
        self.obs.write_audit(
            action="flu_sla_resume",
            entity_type="flu_followup",
            entity_id=followup_id,
            payload={"pause_id": str(pause.id)},
        )
        self.uow.commit()
        self.uow.refresh(pause)
        return pause

    def add_closure_evidence(
        self, followup_id: UUID, data: ClosureEvidenceCreate
    ) -> ClosureEvidence:
        self._get(followup_id)
        domain.assert_closure_evidence(data.evidence_ref)
        evidence = ClosureEvidence(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            followup_id=followup_id,
            evidence_ref=data.evidence_ref.strip(),
            evidence_type=data.evidence_type,
            note=data.note,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(evidence)
        self.obs.write_audit(
            action="flu_closure_evidence",
            entity_type="flu_followup",
            entity_id=followup_id,
            payload={"evidence_id": str(evidence.id)},
        )
        self.uow.commit()
        self.uow.refresh(evidence)
        return evidence

    def close(self, followup_id: UUID) -> FollowUp:
        row = self._get(followup_id)
        domain.assert_open(row.status)
        unresolved = self._unresolved_mandatory_children(followup_id)
        domain.assert_can_close_parent(unresolved_mandatory_children=unresolved)
        evidence_count = len(
            list(
                self.db.scalars(
                    select(ClosureEvidence).where(
                        ClosureEvidence.organization_id == self.ctx.organization_id,
                        ClosureEvidence.followup_id == followup_id,
                    )
                ).all()
            )
        )
        if evidence_count < 1:
            raise ValidationAppError("Closure requires at least one evidence record")

        row.status = "closed"
        row.closed_at = datetime.now(UTC)
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self.uow.add(row)
        self.obs.write_audit(
            action="flu_close",
            entity_type="flu_followup",
            entity_id=followup_id,
            payload={
                "return_to_followup_id": (
                    str(row.return_to_followup_id) if row.return_to_followup_id else None
                )
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="flu_followup",
            aggregate_id=row.id,
            event_type="followup.closed",
            payload={
                "return_to_followup_id": str(row.return_to_followup_id)
                if row.return_to_followup_id
                else None
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def process_overdue(self, followup_id: UUID) -> ProcessOverdueResult:
        """AC-002: create reminder/escalation events when configured thresholds met."""
        row = self._get(followup_id)
        domain.assert_open(row.status)
        if row.sla_paused:
            return ProcessOverdueResult(
                followup_id=followup_id, reminders_created=0, escalations_created=0
            )

        now = datetime.now(UTC)
        reminders_created = 0
        escalations_created = 0

        if domain.reminder_due(
            due_at=row.due_at, offset_hours=row.reminder_offset_hours, now=now
        ):
            pending = self.db.scalar(
                select(ReminderEvent).where(
                    ReminderEvent.organization_id == self.ctx.organization_id,
                    ReminderEvent.followup_id == followup_id,
                    ReminderEvent.status == "scheduled",
                )
            )
            if pending is not None:
                pending.status = "sent"
                pending.triggered_at = now
                self.uow.add(pending)
                reminders_created = 1
            else:
                sent_exists = self.db.scalar(
                    select(ReminderEvent).where(
                        ReminderEvent.organization_id == self.ctx.organization_id,
                        ReminderEvent.followup_id == followup_id,
                        ReminderEvent.status == "sent",
                    )
                )
                if sent_exists is None:
                    evt = ReminderEvent(
                        id=uuid4(),
                        organization_id=self.ctx.organization_id,
                        followup_id=followup_id,
                        scheduled_for=now,
                        status="sent",
                        channel="in_app",
                        triggered_at=now,
                    )
                    self.uow.add(evt)
                    reminders_created = 1

        if domain.escalation_due(
            due_at=row.due_at, after_hours=row.escalation_after_hours, now=now
        ):
            existing = self.db.scalar(
                select(EscalationEvent).where(
                    EscalationEvent.organization_id == self.ctx.organization_id,
                    EscalationEvent.followup_id == followup_id,
                    EscalationEvent.status == "open",
                )
            )
            if existing is None:
                esc = EscalationEvent(
                    id=uuid4(),
                    organization_id=self.ctx.organization_id,
                    followup_id=followup_id,
                    escalate_to_role_code=row.escalate_to_role_code or "PM",
                    escalate_to_actor_id=None,
                    reason="Follow-up overdue beyond escalation window",
                    status="open",
                    triggered_at=now,
                    created_by_actor_id=self.ctx.actor_id,
                )
                self.uow.add(esc)
                escalations_created = 1

        if reminders_created or escalations_created:
            self.obs.write_audit(
                action="flu_process_overdue",
                entity_type="flu_followup",
                entity_id=followup_id,
                payload={
                    "reminders_created": reminders_created,
                    "escalations_created": escalations_created,
                },
            )
            enqueue_outbox(
                self.db,
                organization_id=self.ctx.organization_id,
                aggregate_type="flu_followup",
                aggregate_id=followup_id,
                event_type="followup.overdue_processed",
                payload={
                    "reminders_created": reminders_created,
                    "escalations_created": escalations_created,
                },
                correlation_id=self.ctx.correlation_id,
            )
            self.uow.commit()

        return ProcessOverdueResult(
            followup_id=followup_id,
            reminders_created=reminders_created,
            escalations_created=escalations_created,
        )

    def _unresolved_mandatory_children(self, parent_id: UUID) -> int:
        links = list(
            self.db.scalars(
                select(FollowUpLink).where(
                    FollowUpLink.organization_id == self.ctx.organization_id,
                    FollowUpLink.parent_followup_id == parent_id,
                    FollowUpLink.mandatory.is_(True),
                )
            ).all()
        )
        count = 0
        for link in links:
            child = self.db.scalar(
                select(FollowUp).where(
                    FollowUp.id == link.child_followup_id,
                    FollowUp.organization_id == self.ctx.organization_id,
                )
            )
            if child is not None and child.status != "closed":
                count += 1
        return count

    def _get(self, followup_id: UUID) -> FollowUp:
        row = self.db.scalar(
            select(FollowUp).where(
                FollowUp.id == followup_id,
                FollowUp.organization_id == self.ctx.organization_id,
            )
        )
        if row is None:
            raise NotFoundError("Follow-up not found")
        return row

    def _effective_config_id(self) -> UUID | None:
        row = self.db.scalar(
            select(ConfigurationVersion).where(
                ConfigurationVersion.organization_id == self.ctx.organization_id,
                ConfigurationVersion.status == config_domain.STATUS_EFFECTIVE,
            )
        )
        return row.id if row else None
