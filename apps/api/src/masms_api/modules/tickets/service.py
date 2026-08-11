"""Ticket application service (MOD-300)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, ForbiddenError, NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.projects.models import Project, ProjectRequirement
from masms_api.modules.roadmap.models import Phase
from masms_api.modules.tickets import domain
from masms_api.modules.tickets.models import (
    DoneCheck,
    ReadinessCheck,
    Subtask,
    Ticket,
    TicketDependency,
    TicketEvidence,
    TicketRequirementLink,
)
from masms_api.modules.tickets.schemas import (
    CheckCreate,
    CheckSatisfy,
    EvidenceCreate,
    ReopenRequest,
    RequirementLinkCreate,
    SubtaskCreate,
    TicketCreate,
    TicketDependencyCreate,
    TicketUpdate,
    TransitionRequest,
)
from masms_api.observability.writer import ObservabilityWriter


class TicketService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_ticket(self, data: TicketCreate) -> Ticket:
        project = self._get_project(data.project_id)
        if data.phase_id is not None:
            self._get_phase(data.phase_id, project.id)
        row = Ticket(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=project.id,
            phase_id=data.phase_id,
            code=data.code,
            title=data.title,
            description=data.description,
            ticket_type=data.ticket_type,
            status=domain.STATUS_BACKLOG,
            priority=data.priority,
            owner_actor_id=data.owner_actor_id,
            queue_code=data.queue_code,
            estimate_points=data.estimate_points,
            acceptance_criteria=data.acceptance_criteria,
            definition_of_done=data.definition_of_done,
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.db.flush()
        for code, label in domain.DEFAULT_READINESS_CHECKS:
            self.uow.add(
                ReadinessCheck(
                    id=uuid4(),
                    organization_id=self.ctx.organization_id,
                    project_id=project.id,
                    ticket_id=row.id,
                    check_code=code,
                    label=label,
                    is_required=True,
                    is_satisfied=False,
                    created_by_actor_id=self.ctx.actor_id,
                )
            )
        for code, label in domain.DEFAULT_DONE_CHECKS:
            self.uow.add(
                DoneCheck(
                    id=uuid4(),
                    organization_id=self.ctx.organization_id,
                    project_id=project.id,
                    ticket_id=row.id,
                    check_code=code,
                    label=label,
                    is_required=True,
                    is_satisfied=False,
                    created_by_actor_id=self.ctx.actor_id,
                )
            )
        if data.requirement_id is not None:
            self._link_requirement(
                ticket=row,
                requirement_id=data.requirement_id,
                requirement_version_id=data.requirement_version_id,
                commit=False,
            )
        self.obs.write_audit(
            action="ticket_create",
            entity_type="tkt_ticket",
            entity_id=row.id,
            payload={"code": data.code},
            project_id=project.id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def update_ticket(self, ticket_id: UUID, data: TicketUpdate) -> Ticket:
        row = self._get_ticket(ticket_id)
        self._assert_version(row, data.expected_version)
        if row.status == domain.STATUS_DONE:
            raise ForbiddenError("Done tickets are immutable; reopen first")
        if data.title is not None:
            row.title = data.title
        if data.description is not None:
            row.description = data.description
        if data.priority is not None:
            row.priority = data.priority
        if data.phase_id is not None:
            self._get_phase(data.phase_id, row.project_id)
            row.phase_id = data.phase_id
        if data.owner_actor_id is not None:
            row.owner_actor_id = data.owner_actor_id
        if data.queue_code is not None:
            row.queue_code = data.queue_code
        if data.estimate_points is not None:
            row.estimate_points = data.estimate_points
        if data.acceptance_criteria is not None:
            row.acceptance_criteria = data.acceptance_criteria
        if data.definition_of_done is not None:
            row.definition_of_done = data.definition_of_done
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self.uow.add(row)
        self.obs.write_audit(
            action="ticket_update",
            entity_type="tkt_ticket",
            entity_id=row.id,
            payload={"version": row.version},
            project_id=row.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def get_ticket(self, ticket_id: UUID) -> Ticket:
        return self._get_ticket(ticket_id)

    def list_tickets(
        self,
        project_id: UUID,
        *,
        status: str | None = None,
        q: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Ticket], PageMeta]:
        self._get_project(project_id)
        limit, offset = normalize_paging(limit, offset)
        filters = [
            Ticket.organization_id == self.ctx.organization_id,
            Ticket.project_id == project_id,
        ]
        if status:
            filters.append(Ticket.status == status)
        if q and q.strip():
            like = f"%{q.strip()}%"
            filters.append(or_(Ticket.code.ilike(like), Ticket.title.ilike(like)))
        total = self.db.scalar(select(func.count()).select_from(Ticket).where(*filters)) or 0
        rows = list(
            self.db.scalars(
                select(Ticket)
                .where(*filters)
                .order_by(Ticket.code)
                .offset(offset)
                .limit(limit)
            )
        )
        return rows, build_page_meta(limit=limit, offset=offset, total=int(total))

    def transition(self, ticket_id: UUID, data: TransitionRequest) -> Ticket:
        row = self._get_ticket(ticket_id)
        self._assert_version(row, data.expected_version)
        nxt = data.next_status.strip().lower()
        if nxt == domain.STATUS_READY:
            return self._mark_ready(row)
        if nxt == domain.STATUS_DONE:
            return self._mark_done(row)
        domain.assert_allowed_transition(row.status, nxt)
        if nxt == domain.STATUS_BLOCKED and not (
            data.blocked_reason and data.blocked_reason.strip()
        ):
            raise ValidationAppError("Blocked transition requires a reason")
        row.status = nxt
        if nxt == domain.STATUS_BLOCKED:
            row.blocked_reason = data.blocked_reason
        elif row.blocked_reason and nxt != domain.STATUS_BLOCKED:
            row.blocked_reason = None
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self.uow.add(row)
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tkt_ticket",
            aggregate_id=row.id,
            event_type="ticket.status.changed",
            payload={"code": row.code, "status": row.status, "reason": data.reason},
            correlation_id=self.ctx.correlation_id,
        )
        self.obs.write_audit(
            action="ticket_transition",
            entity_type="tkt_ticket",
            entity_id=row.id,
            payload={"status": row.status, "reason": data.reason},
            project_id=row.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def reopen(self, ticket_id: UUID, data: ReopenRequest) -> Ticket:
        row = self._get_ticket(ticket_id)
        self._assert_version(row, data.expected_version)
        evidence = self._get_evidence(data.evidence_id)
        if evidence.ticket_id != row.id:
            raise ValidationAppError("Evidence must belong to the ticket")
        next_status = data.next_status.strip().lower()
        domain.assert_can_reopen(
            status=row.status,
            actor_kind=self.ctx.actor_kind,
            reopen_reason=data.reason,
            evidence_id=data.evidence_id,
        )
        domain.assert_allowed_transition(domain.STATUS_DONE, next_status)
        row.status = next_status
        row.completed_at = None
        row.reopen_reason = data.reason
        row.reopen_evidence_id = data.evidence_id
        row.reopened_by_actor_id = self.ctx.actor_id
        row.reopened_at = datetime.now(UTC)
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self.uow.add(row)
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tkt_ticket",
            aggregate_id=row.id,
            event_type="ticket.reopened",
            payload={"code": row.code, "status": row.status},
            correlation_id=self.ctx.correlation_id,
        )
        self.obs.write_audit(
            action="ticket_reopen",
            entity_type="tkt_ticket",
            entity_id=row.id,
            payload={"reason": data.reason, "evidence_id": str(data.evidence_id)},
            project_id=row.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_subtask(self, data: SubtaskCreate) -> Subtask:
        ticket = self._get_ticket(data.ticket_id)
        row = Subtask(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=ticket.project_id,
            ticket_id=ticket.id,
            code=data.code,
            title=data.title,
            status="open",
            owner_actor_id=data.owner_actor_id,
            sequence=data.sequence,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="subtask_create",
            entity_type="tkt_subtask",
            entity_id=row.id,
            payload={"code": data.code},
            project_id=ticket.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_dependency(self, data: TicketDependencyCreate) -> TicketDependency:
        project = self._get_project(data.project_id)
        predecessor = self._get_ticket(data.predecessor_ticket_id)
        successor = self._get_ticket(data.successor_ticket_id)
        if predecessor.project_id != project.id or successor.project_id != project.id:
            raise ValidationAppError("Both tickets must belong to the project")
        domain.assert_no_self_dependency(predecessor.id, successor.id)
        row = TicketDependency(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=project.id,
            predecessor_ticket_id=predecessor.id,
            successor_ticket_id=successor.id,
            dependency_type=data.dependency_type,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def link_requirement(self, data: RequirementLinkCreate) -> TicketRequirementLink:
        ticket = self._get_ticket(data.ticket_id)
        return self._link_requirement(
            ticket=ticket,
            requirement_id=data.requirement_id,
            requirement_version_id=data.requirement_version_id,
            commit=True,
        )

    def add_evidence(self, data: EvidenceCreate) -> TicketEvidence:
        ticket = self._get_ticket(data.ticket_id)
        row = TicketEvidence(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=ticket.project_id,
            ticket_id=ticket.id,
            evidence_type=data.evidence_type,
            title=data.title,
            uri_or_ref=data.uri_or_ref,
            summary=data.summary,
            metadata_json={},
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="ticket_evidence_add",
            entity_type="tkt_ticket_evidence",
            entity_id=row.id,
            payload={"type": data.evidence_type},
            project_id=ticket.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def add_readiness_check(self, data: CheckCreate) -> ReadinessCheck:
        ticket = self._get_ticket(data.ticket_id)
        row = ReadinessCheck(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=ticket.project_id,
            ticket_id=ticket.id,
            check_code=data.check_code,
            label=data.label,
            is_required=data.is_required,
            is_satisfied=False,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def satisfy_readiness_check(
        self, check_id: UUID, data: CheckSatisfy
    ) -> ReadinessCheck:
        row = self.db.scalar(select(ReadinessCheck).where(ReadinessCheck.id == check_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Readiness check not found")
        row.is_satisfied = True
        row.notes = data.notes
        row.satisfied_by_actor_id = self.ctx.actor_id
        row.satisfied_at = datetime.now(UTC)
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def add_done_check(self, data: CheckCreate) -> DoneCheck:
        ticket = self._get_ticket(data.ticket_id)
        row = DoneCheck(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=ticket.project_id,
            ticket_id=ticket.id,
            check_code=data.check_code,
            label=data.label,
            is_required=data.is_required,
            is_satisfied=False,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def satisfy_done_check(self, check_id: UUID, data: CheckSatisfy) -> DoneCheck:
        row = self.db.scalar(select(DoneCheck).where(DoneCheck.id == check_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Done check not found")
        row.is_satisfied = True
        row.notes = data.notes
        row.satisfied_by_actor_id = self.ctx.actor_id
        row.satisfied_at = datetime.now(UTC)
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_readiness_checks(self, ticket_id: UUID) -> list[ReadinessCheck]:
        self._get_ticket(ticket_id)
        return list(
            self.db.scalars(
                select(ReadinessCheck).where(ReadinessCheck.ticket_id == ticket_id)
            ).all()
        )

    def list_done_checks(self, ticket_id: UUID) -> list[DoneCheck]:
        self._get_ticket(ticket_id)
        return list(
            self.db.scalars(select(DoneCheck).where(DoneCheck.ticket_id == ticket_id)).all()
        )

    def _mark_ready(self, row: Ticket) -> Ticket:
        links = self.db.scalars(
            select(TicketRequirementLink).where(TicketRequirementLink.ticket_id == row.id)
        ).all()
        checks = self.db.scalars(
            select(ReadinessCheck).where(ReadinessCheck.ticket_id == row.id)
        ).all()
        unsatisfied = [
            c.check_code for c in checks if c.is_required and not c.is_satisfied
        ]
        domain.assert_can_become_ready(
            status=row.status,
            description=row.description,
            acceptance_criteria=row.acceptance_criteria,
            priority=row.priority,
            estimate_points=row.estimate_points,
            definition_of_done=row.definition_of_done,
            phase_id=row.phase_id,
            has_requirement_link=bool(links),
            owner_actor_id=row.owner_actor_id,
            queue_code=row.queue_code,
            unsatisfied_required_checks=unsatisfied,
        )
        row.status = domain.STATUS_READY
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self.uow.add(row)
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tkt_ticket",
            aggregate_id=row.id,
            event_type="ticket.ready",
            payload={"code": row.code},
            correlation_id=self.ctx.correlation_id,
        )
        self.obs.write_audit(
            action="ticket_ready",
            entity_type="tkt_ticket",
            entity_id=row.id,
            payload={"code": row.code},
            project_id=row.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def _mark_done(self, row: Ticket) -> Ticket:
        checks = self.db.scalars(
            select(DoneCheck).where(DoneCheck.ticket_id == row.id)
        ).all()
        unsatisfied = [
            c.check_code for c in checks if c.is_required and not c.is_satisfied
        ]
        domain.assert_can_complete(
            status=row.status, unsatisfied_required_checks=unsatisfied
        )
        row.status = domain.STATUS_DONE
        row.completed_at = datetime.now(UTC)
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self.uow.add(row)
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tkt_ticket",
            aggregate_id=row.id,
            event_type="ticket.done",
            payload={"code": row.code},
            correlation_id=self.ctx.correlation_id,
        )
        self.obs.write_audit(
            action="ticket_done",
            entity_type="tkt_ticket",
            entity_id=row.id,
            payload={"code": row.code},
            project_id=row.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def _link_requirement(
        self,
        *,
        ticket: Ticket,
        requirement_id: UUID,
        requirement_version_id: UUID | None,
        commit: bool,
    ) -> TicketRequirementLink:
        requirement = self.db.scalar(
            select(ProjectRequirement).where(ProjectRequirement.id == requirement_id)
        )
        if (
            requirement is None
            or requirement.organization_id != self.ctx.organization_id
            or requirement.project_id != ticket.project_id
        ):
            raise NotFoundError("Requirement not found on project")
        row = TicketRequirementLink(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=ticket.project_id,
            ticket_id=ticket.id,
            requirement_id=requirement.id,
            requirement_version_id=requirement_version_id,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="ticket_requirement_link",
            entity_type="tkt_requirement_link",
            entity_id=row.id,
            payload={"requirement_id": str(requirement.id)},
            project_id=ticket.project_id,
        )
        if commit:
            self.uow.commit()
            self.uow.refresh(row)
        return row

    def _assert_version(self, row: Ticket, expected: int) -> None:
        if row.version != expected:
            raise ConflictError("Ticket version conflict; refresh and retry")

    def _get_project(self, project_id: UUID) -> Project:
        row = self.db.scalar(select(Project).where(Project.id == project_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Project not found")
        ctx_client = self.ctx.tenant.client_id
        if ctx_client and row.client_id and row.client_id != ctx_client:
            raise ForbiddenError("Cross-client access denied")
        return row

    def _get_phase(self, phase_id: UUID, project_id: UUID) -> Phase:
        row = self.db.scalar(select(Phase).where(Phase.id == phase_id))
        if (
            row is None
            or row.organization_id != self.ctx.organization_id
            or row.project_id != project_id
        ):
            raise NotFoundError("Phase not found on project")
        return row

    def _get_ticket(self, ticket_id: UUID) -> Ticket:
        row = self.db.scalar(select(Ticket).where(Ticket.id == ticket_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Ticket not found")
        return row

    def _get_evidence(self, evidence_id: UUID) -> TicketEvidence:
        row = self.db.scalar(select(TicketEvidence).where(TicketEvidence.id == evidence_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Evidence not found")
        return row
