"""Assignment application service (MOD-310)."""

from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from typing import TypedDict
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, ForbiddenError, NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.access.models import ProjectMember
from masms_api.modules.assignments import domain
from masms_api.modules.assignments.models import (
    AllocationHistory,
    Assignment,
    AssignmentAcknowledgment,
    AssignmentRecommendation,
    ReassignmentHistory,
)
from masms_api.modules.assignments.schemas import (
    AcknowledgeRequest,
    AssignmentCreate,
    ReassignRequest,
    RecommendRequest,
)
from masms_api.modules.capacity.models import ActorSkill, CapacityAllocation, LeavePeriod, Skill
from masms_api.modules.projects.models import Project
from masms_api.modules.tickets.models import Ticket
from masms_api.observability.writer import ObservabilityWriter

ACTIVE_STATUSES = frozenset({"pending_ack", "acknowledged"})


class _Eligibility(TypedDict):
    is_member: bool
    eligible: bool
    reasons: list[str]
    remaining_capacity_pct: Decimal | None
    proficiency: int | None


class AssignmentService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_assignment(self, data: AssignmentCreate) -> Assignment:
        ticket = self._get_ticket(data.ticket_id)
        existing = self._active_assignment(ticket.id)
        if existing is not None:
            raise ConflictError("Ticket already has an active assignment; reassign instead")

        eligibility = self._evaluate_candidate(
            project_id=ticket.project_id,
            actor_id=data.assignee_actor_id,
            skill_code=data.required_skill_code,
            min_proficiency=data.min_proficiency,
        )
        domain.assert_project_authorized(is_member=eligibility["is_member"])
        domain.assert_actor_available(
            eligible=eligibility["eligible"],
            reasons=eligibility["reasons"],
            allow_override=data.allow_override,
            override_reason=data.override_reason,
        )
        is_override = data.allow_override and not eligibility["eligible"]

        row = Assignment(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=ticket.project_id,
            ticket_id=ticket.id,
            assignee_actor_id=data.assignee_actor_id,
            role_code=data.role_code,
            status="pending_ack",
            required_skill_code=data.required_skill_code,
            min_proficiency=data.min_proficiency,
            override_reason=data.override_reason if is_override else None,
            is_override=is_override,
            recommendation_id=data.recommendation_id,
            assigned_by_actor_id=self.ctx.actor_id,
            version=1,
        )
        self.uow.add(row)
        self.db.flush()
        self._record_allocation(
            ticket=ticket,
            assignment_id=row.id,
            actor_id=data.assignee_actor_id,
            allocation_pct=data.allocation_pct,
            event_type="overridden" if is_override else "allocated",
            reason=data.override_reason if is_override else None,
        )
        ticket.owner_actor_id = data.assignee_actor_id
        if ticket.status in {"backlog", "ready"}:
            ticket.status = "assigned"
            ticket.version += 1
        ticket.updated_by_actor_id = self.ctx.actor_id
        self.uow.add(ticket)
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="asg_assignment",
            aggregate_id=row.id,
            event_type="assignment.created",
            payload={"ticket_id": str(ticket.id), "assignee": str(data.assignee_actor_id)},
            correlation_id=self.ctx.correlation_id,
        )
        self.obs.write_audit(
            action="assignment_create",
            entity_type="asg_assignment",
            entity_id=row.id,
            payload={"is_override": is_override},
            project_id=ticket.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def recommend(self, data: RecommendRequest) -> list[AssignmentRecommendation]:
        ticket = self._get_ticket(data.ticket_id)
        # supersede prior proposed recommendations
        prior = self.db.scalars(
            select(AssignmentRecommendation).where(
                AssignmentRecommendation.ticket_id == ticket.id,
                AssignmentRecommendation.status == "proposed",
            )
        ).all()
        for item in prior:
            item.status = "superseded"
            self.uow.add(item)

        scored: list[tuple[UUID, Decimal, bool, list[str], Decimal | None]] = []
        for actor_id in data.candidate_actor_ids:
            result = self._evaluate_candidate(
                project_id=ticket.project_id,
                actor_id=actor_id,
                skill_code=data.required_skill_code,
                min_proficiency=data.min_proficiency,
            )
            score = domain.score_candidate(
                eligible=result["eligible"],
                remaining_capacity_pct=result["remaining_capacity_pct"],
                proficiency=result["proficiency"],
                min_proficiency=data.min_proficiency,
            )
            scored.append(
                (
                    actor_id,
                    score,
                    result["eligible"],
                    result["reasons"],
                    result["remaining_capacity_pct"],
                )
            )
        scored.sort(key=lambda x: x[1], reverse=True)

        rows: list[AssignmentRecommendation] = []
        for rank, (actor_id, score, eligible, reasons, remaining) in enumerate(scored, start=1):
            row = AssignmentRecommendation(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                project_id=ticket.project_id,
                ticket_id=ticket.id,
                candidate_actor_id=actor_id,
                score=score,
                rank=rank,
                eligible=eligible,
                reasons_json=reasons,
                remaining_capacity_pct=remaining,
                status="proposed",
                created_by_actor_id=self.ctx.actor_id,
            )
            self.uow.add(row)
            rows.append(row)
        self.obs.write_audit(
            action="assignment_recommend",
            entity_type="tkt_ticket",
            entity_id=ticket.id,
            payload={"candidates": len(rows)},
            project_id=ticket.project_id,
        )
        self.uow.commit()
        for row in rows:
            self.uow.refresh(row)
        return rows

    def acknowledge(
        self, assignment_id: UUID, data: AcknowledgeRequest
    ) -> AssignmentAcknowledgment:
        assignment = self._get_assignment(assignment_id)
        if assignment.status not in ACTIVE_STATUSES:
            raise ValidationAppError("Only active assignments can be acknowledged")
        if assignment.assignee_actor_id != self.ctx.actor_id and self.ctx.actor_kind != "system":
            raise ForbiddenError("Only the assignee may acknowledge this assignment")
        existing = self.db.scalar(
            select(AssignmentAcknowledgment).where(
                AssignmentAcknowledgment.assignment_id == assignment.id
            )
        )
        if existing is not None:
            raise ConflictError("Assignment already acknowledged")

        status = "declined" if data.decline else "acknowledged"
        row = AssignmentAcknowledgment(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=assignment.project_id,
            assignment_id=assignment.id,
            actor_id=self.ctx.actor_id,
            status=status,
            note=data.note,
        )
        self.uow.add(row)
        if status == "acknowledged":
            assignment.status = "acknowledged"
        else:
            assignment.status = "closed"
            assignment.closed_at = datetime.now(UTC)
        assignment.version += 1
        self.uow.add(assignment)
        self.obs.write_audit(
            action="assignment_acknowledge",
            entity_type="asg_acknowledgment",
            entity_id=row.id,
            payload={"status": status},
            project_id=assignment.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def reassign(self, assignment_id: UUID, data: ReassignRequest) -> Assignment:
        current = self._get_assignment(assignment_id)
        if current.version != data.expected_version:
            raise ConflictError("Assignment version conflict; refresh and retry")
        if current.status not in ACTIVE_STATUSES:
            raise ValidationAppError("Only active assignments can be reassigned")
        ticket = self._get_ticket(current.ticket_id)

        eligibility = self._evaluate_candidate(
            project_id=ticket.project_id,
            actor_id=data.new_assignee_actor_id,
            skill_code=data.required_skill_code,
            min_proficiency=data.min_proficiency,
        )
        domain.assert_project_authorized(is_member=eligibility["is_member"])
        domain.assert_actor_available(
            eligible=eligibility["eligible"],
            reasons=eligibility["reasons"],
            allow_override=data.allow_override,
            override_reason=data.override_reason,
        )
        is_override = data.allow_override and not eligibility["eligible"]

        current.status = "closed"
        current.closed_at = datetime.now(UTC)
        current.version += 1
        self.uow.add(current)
        self._record_allocation(
            ticket=ticket,
            assignment_id=current.id,
            actor_id=current.assignee_actor_id,
            allocation_pct=Decimal("0"),
            event_type="released",
            reason=data.reason,
        )

        new_row = Assignment(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=ticket.project_id,
            ticket_id=ticket.id,
            assignee_actor_id=data.new_assignee_actor_id,
            role_code=data.role_code,
            status="pending_ack",
            required_skill_code=data.required_skill_code,
            min_proficiency=data.min_proficiency,
            override_reason=data.override_reason if is_override else None,
            is_override=is_override,
            assigned_by_actor_id=self.ctx.actor_id,
            version=1,
        )
        self.uow.add(new_row)
        self.db.flush()
        self._record_allocation(
            ticket=ticket,
            assignment_id=new_row.id,
            actor_id=data.new_assignee_actor_id,
            allocation_pct=data.allocation_pct,
            event_type="overridden" if is_override else "allocated",
            reason=data.override_reason if is_override else data.reason,
        )
        history = ReassignmentHistory(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=ticket.project_id,
            ticket_id=ticket.id,
            from_assignment_id=current.id,
            to_assignment_id=new_row.id,
            from_actor_id=current.assignee_actor_id,
            to_actor_id=data.new_assignee_actor_id,
            reason=data.reason,
            is_override=is_override,
            recorded_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(history)
        ticket.owner_actor_id = data.new_assignee_actor_id
        ticket.updated_by_actor_id = self.ctx.actor_id
        ticket.version += 1
        self.uow.add(ticket)
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="asg_assignment",
            aggregate_id=new_row.id,
            event_type="assignment.reassigned",
            payload={"from": str(current.assignee_actor_id), "to": str(data.new_assignee_actor_id)},
            correlation_id=self.ctx.correlation_id,
        )
        self.obs.write_audit(
            action="assignment_reassign",
            entity_type="asg_reassignment_history",
            entity_id=history.id,
            payload={"reason": data.reason, "is_override": is_override},
            project_id=ticket.project_id,
        )
        self.uow.commit()
        self.uow.refresh(new_row)
        return new_row

    def list_for_ticket(self, ticket_id: UUID) -> list[Assignment]:
        self._get_ticket(ticket_id)
        return list(
            self.db.scalars(
                select(Assignment)
                .where(Assignment.ticket_id == ticket_id)
                .order_by(Assignment.created_at.desc())
            ).all()
        )

    def list_recommendations(self, ticket_id: UUID) -> list[AssignmentRecommendation]:
        self._get_ticket(ticket_id)
        return list(
            self.db.scalars(
                select(AssignmentRecommendation)
                .where(AssignmentRecommendation.ticket_id == ticket_id)
                .order_by(AssignmentRecommendation.rank)
            ).all()
        )

    def list_allocation_history(self, ticket_id: UUID) -> list[AllocationHistory]:
        self._get_ticket(ticket_id)
        return list(
            self.db.scalars(
                select(AllocationHistory)
                .where(AllocationHistory.ticket_id == ticket_id)
                .order_by(AllocationHistory.recorded_at)
            ).all()
        )

    def list_reassignment_history(self, ticket_id: UUID) -> list[ReassignmentHistory]:
        self._get_ticket(ticket_id)
        return list(
            self.db.scalars(
                select(ReassignmentHistory)
                .where(ReassignmentHistory.ticket_id == ticket_id)
                .order_by(ReassignmentHistory.recorded_at)
            ).all()
        )

    def _record_allocation(
        self,
        *,
        ticket: Ticket,
        assignment_id: UUID,
        actor_id: UUID,
        allocation_pct: Decimal,
        event_type: str,
        reason: str | None,
    ) -> None:
        self.uow.add(
            AllocationHistory(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                project_id=ticket.project_id,
                ticket_id=ticket.id,
                assignment_id=assignment_id,
                actor_id=actor_id,
                allocation_pct=allocation_pct,
                event_type=event_type,
                reason=reason,
                recorded_by_actor_id=self.ctx.actor_id,
            )
        )

    def _evaluate_candidate(
        self,
        *,
        project_id: UUID,
        actor_id: UUID,
        skill_code: str | None,
        min_proficiency: int,
    ) -> _Eligibility:
        reasons: list[str] = []
        as_of = date.today()
        member = self.db.scalar(
            select(ProjectMember).where(
                ProjectMember.organization_id == self.ctx.organization_id,
                ProjectMember.project_id == project_id,
                ProjectMember.actor_id == actor_id,
                ProjectMember.status == "active",
            )
        )
        is_member = member is not None
        if not is_member:
            reasons.append("not a project member")

        proficiency: int | None = None
        if skill_code:
            skill = self.db.scalar(
                select(Skill).where(
                    Skill.organization_id == self.ctx.organization_id,
                    Skill.code == skill_code,
                    Skill.status == "active",
                )
            )
            if skill is None:
                reasons.append(f"skill '{skill_code}' not found")
            else:
                link = self.db.scalar(
                    select(ActorSkill).where(
                        ActorSkill.organization_id == self.ctx.organization_id,
                        ActorSkill.actor_id == actor_id,
                        ActorSkill.skill_id == skill.id,
                        ActorSkill.status == "active",
                    )
                )
                if link is None or link.proficiency < min_proficiency:
                    reasons.append("skill proficiency below required minimum")
                else:
                    proficiency = link.proficiency

        allocations = list(
            self.db.scalars(
                select(CapacityAllocation).where(
                    CapacityAllocation.organization_id == self.ctx.organization_id,
                    CapacityAllocation.actor_id == actor_id,
                    CapacityAllocation.status == "active",
                    CapacityAllocation.effective_from <= as_of,
                )
            )
        )
        used = Decimal("0")
        for alloc in allocations:
            if alloc.effective_to is not None and alloc.effective_to < as_of:
                continue
            if alloc.project_id not in {None, project_id}:
                continue
            used += Decimal(alloc.allocation_pct)
        remaining = Decimal("100") - used
        if remaining < 0:
            reasons.append("capacity over-allocated")

        leave = self.db.scalar(
            select(LeavePeriod).where(
                LeavePeriod.organization_id == self.ctx.organization_id,
                LeavePeriod.actor_id == actor_id,
                LeavePeriod.status == "approved",
                LeavePeriod.starts_on <= as_of,
                LeavePeriod.ends_on >= as_of,
            )
        )
        if leave is not None:
            reasons.append("actor is on leave")

        return {
            "is_member": is_member,
            "eligible": len(reasons) == 0,
            "reasons": reasons,
            "remaining_capacity_pct": remaining,
            "proficiency": proficiency,
        }

    def _active_assignment(self, ticket_id: UUID) -> Assignment | None:
        return self.db.scalar(
            select(Assignment).where(
                Assignment.ticket_id == ticket_id,
                Assignment.status.in_(tuple(ACTIVE_STATUSES)),
            )
        )

    def _get_ticket(self, ticket_id: UUID) -> Ticket:
        row = self.db.scalar(select(Ticket).where(Ticket.id == ticket_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Ticket not found")
        project = self.db.scalar(select(Project).where(Project.id == row.project_id))
        if project is None or project.organization_id != self.ctx.organization_id:
            raise NotFoundError("Project not found")
        ctx_client = self.ctx.tenant.client_id
        if ctx_client and project.client_id and project.client_id != ctx_client:
            raise ForbiddenError("Cross-client access denied")
        return row

    def _get_assignment(self, assignment_id: UUID) -> Assignment:
        row = self.db.scalar(select(Assignment).where(Assignment.id == assignment_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Assignment not found")
        return row
