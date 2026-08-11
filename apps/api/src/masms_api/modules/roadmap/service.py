"""Roadmap application service (MOD-260)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from masms_api.errors import ForbiddenError, NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.projects.models import Project, ProjectRequirement
from masms_api.modules.roadmap import domain
from masms_api.modules.roadmap.models import (
    Deliverable,
    Forecast,
    Milestone,
    Phase,
    PhaseDependency,
    ProjectPlanBaseline,
    RequirementPhaseMap,
)
from masms_api.modules.roadmap.schemas import (
    BaselineCreate,
    DeliverableCreate,
    ForecastCreate,
    MilestoneCreate,
    PhaseCreate,
    PhaseDependencyCreate,
    RequirementPhaseMapCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class RoadmapService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_phase(self, data: PhaseCreate) -> Phase:
        project = self._get_project(data.project_id)
        row = Phase(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=project.id,
            code=data.code,
            title=data.title,
            sequence=data.sequence,
            status="planned",
            owner_actor_id=data.owner_actor_id or self.ctx.actor_id,
            planned_start=data.planned_start,
            planned_end=data.planned_end,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="phase_create",
            entity_type="pm_phase",
            entity_id=row.id,
            payload={"code": data.code},
            project_id=project.id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_milestone(self, data: MilestoneCreate) -> Milestone:
        phase = self._get_phase(data.phase_id)
        domain.assert_milestone_fields(
            owner_actor_id=data.owner_actor_id,
            target_date=data.target_date,
            status="planned",
        )
        row = Milestone(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=phase.project_id,
            phase_id=phase.id,
            code=data.code,
            title=data.title,
            owner_actor_id=data.owner_actor_id,
            target_date=data.target_date,
            status="planned",
            requires_approval=data.requires_approval,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="milestone_create",
            entity_type="pm_milestone",
            entity_id=row.id,
            payload={"code": data.code, "requires_approval": data.requires_approval},
            project_id=phase.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def approve_milestone(self, milestone_id: UUID) -> Milestone:
        row = self._get_milestone(milestone_id)
        if not row.requires_approval:
            raise ValidationAppError("Milestone does not require approval")
        if row.status == "completed":
            raise ForbiddenError("Completed milestones cannot be re-approved")
        row.approved_by_actor_id = self.ctx.actor_id
        row.approved_at = datetime.now(UTC)
        if row.status == "planned":
            row.status = "in_progress"
        self.uow.add(row)
        self.obs.write_audit(
            action="milestone_approve",
            entity_type="pm_milestone",
            entity_id=row.id,
            project_id=row.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def complete_milestone(self, milestone_id: UUID) -> Milestone:
        row = self._get_milestone(milestone_id)
        domain.assert_can_complete_milestone(
            status=row.status,
            owner_actor_id=row.owner_actor_id,
            target_date=row.target_date,
            requires_approval=row.requires_approval,
            approved=row.approved_by_actor_id is not None,
        )
        row.status = "completed"
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_deliverable(self, data: DeliverableCreate) -> Deliverable:
        phase = self._get_phase(data.phase_id)
        if data.milestone_id is not None:
            milestone = self._get_milestone(data.milestone_id)
            if milestone.phase_id != phase.id:
                raise ValidationAppError("Milestone does not belong to phase")
        row = Deliverable(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=phase.project_id,
            phase_id=phase.id,
            milestone_id=data.milestone_id,
            code=data.code,
            title=data.title,
            status="planned",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_dependency(self, data: PhaseDependencyCreate) -> PhaseDependency:
        project = self._get_project(data.project_id)
        predecessor = self._get_phase(data.predecessor_phase_id)
        successor = self._get_phase(data.successor_phase_id)
        if predecessor.project_id != project.id or successor.project_id != project.id:
            raise ValidationAppError("Both phases must belong to the project")
        domain.assert_no_self_dependency(predecessor.id, successor.id)
        row = PhaseDependency(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=project.id,
            predecessor_phase_id=predecessor.id,
            successor_phase_id=successor.id,
            dependency_type=data.dependency_type,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def map_requirement(self, data: RequirementPhaseMapCreate) -> RequirementPhaseMap:
        project = self._get_project(data.project_id)
        phase = self._get_phase(data.phase_id)
        if phase.project_id != project.id:
            raise ValidationAppError("Phase does not belong to project")
        requirement = self.db.scalar(
            select(ProjectRequirement).where(ProjectRequirement.id == data.requirement_id)
        )
        if (
            requirement is None
            or requirement.organization_id != self.ctx.organization_id
            or requirement.project_id != project.id
        ):
            raise NotFoundError("Requirement not found on project")
        if requirement.status != "approved":
            raise ValidationAppError("Only approved requirements can be mapped to phases")
        row = RequirementPhaseMap(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=project.id,
            requirement_id=requirement.id,
            phase_id=phase.id,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="requirement_phase_map",
            entity_type="pm_requirement_phase_map",
            entity_id=row.id,
            payload={"requirement_id": str(requirement.id), "phase_id": str(phase.id)},
            project_id=project.id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def complete_phase(self, phase_id: UUID) -> Phase:
        phase = self._get_phase(phase_id)
        preds = list(
            self.db.scalars(
                select(PhaseDependency).where(PhaseDependency.successor_phase_id == phase.id)
            )
        )
        unfinished: list[str] = []
        for dep in preds:
            pred = self._get_phase(dep.predecessor_phase_id)
            if pred.status != "completed":
                unfinished.append(pred.code)
        domain.assert_can_complete_phase(
            status=phase.status, unfinished_predecessor_codes=unfinished
        )
        siblings = list(
            self.db.scalars(
                select(Phase).where(
                    Phase.project_id == phase.project_id,
                    Phase.id != phase.id,
                    Phase.status != "completed",
                )
            )
        )
        domain.assert_sibling_independence(
            completing_phase_id=phase.id,
            sibling_incomplete_ids=[s.id for s in siblings],
        )
        phase.status = "completed"
        phase.completed_at = datetime.now(UTC)
        self.uow.add(phase)
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="pm_phase",
            aggregate_id=phase.id,
            event_type="roadmap.phase.completed",
            payload={"code": phase.code},
            correlation_id=self.ctx.correlation_id,
        )
        self.obs.write_audit(
            action="phase_complete",
            entity_type="pm_phase",
            entity_id=phase.id,
            payload={"code": phase.code},
            project_id=phase.project_id,
        )
        self.uow.commit()
        self.uow.refresh(phase)
        return phase

    def create_baseline(self, data: BaselineCreate) -> ProjectPlanBaseline:
        project = self._get_project(data.project_id)
        phases = list(
            self.db.scalars(select(Phase).where(Phase.project_id == project.id))
        )
        next_version = (
            self.db.scalar(
                select(func.max(ProjectPlanBaseline.version_number)).where(
                    ProjectPlanBaseline.project_id == project.id
                )
            )
            or 0
        ) + 1
        snapshot = {
            "phase_ids": [str(p.id) for p in phases],
            "phase_codes": [p.code for p in phases],
        }
        row = ProjectPlanBaseline(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=project.id,
            version_number=next_version,
            title=data.title,
            status="draft",
            snapshot_json=snapshot,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def approve_baseline(self, baseline_id: UUID) -> ProjectPlanBaseline:
        row = self._get_baseline(baseline_id)
        if row.status != "draft":
            raise ForbiddenError("Only draft baselines can be approved")
        approved_reqs = {
            r.id
            for r in self.db.scalars(
                select(ProjectRequirement).where(
                    ProjectRequirement.project_id == row.project_id,
                    ProjectRequirement.status == "approved",
                )
            )
        }
        mapped = {
            m.requirement_id
            for m in self.db.scalars(
                select(RequirementPhaseMap).where(
                    RequirementPhaseMap.project_id == row.project_id
                )
            )
        }
        domain.assert_approved_requirements_mapped(
            approved_requirement_ids=approved_reqs,
            mapped_requirement_ids=mapped,
        )
        for prior in self.db.scalars(
            select(ProjectPlanBaseline).where(
                ProjectPlanBaseline.project_id == row.project_id,
                ProjectPlanBaseline.status == "approved",
                ProjectPlanBaseline.id != row.id,
            )
        ):
            prior.status = "superseded"
            self.uow.add(prior)
        row.status = "approved"
        row.approved_by_actor_id = self.ctx.actor_id
        row.approved_at = datetime.now(UTC)
        self.uow.add(row)
        self.obs.write_audit(
            action="baseline_approve",
            entity_type="pm_project_baseline",
            entity_id=row.id,
            payload={"version_number": row.version_number},
            project_id=row.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_forecast(self, data: ForecastCreate) -> Forecast:
        project = self._get_project(data.project_id)
        if data.phase_id is not None:
            phase = self._get_phase(data.phase_id)
            if phase.project_id != project.id:
                raise ValidationAppError("Phase does not belong to project")
        row = Forecast(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=project.id,
            phase_id=data.phase_id,
            forecast_type=data.forecast_type,
            predicted_date=data.predicted_date,
            predicted_value=data.predicted_value,
            confidence=data.confidence,
            notes=data.notes,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_phases(self, project_id: UUID) -> list[Phase]:
        self._get_project(project_id)
        return list(
            self.db.scalars(
                select(Phase)
                .where(
                    Phase.organization_id == self.ctx.organization_id,
                    Phase.project_id == project_id,
                )
                .order_by(Phase.sequence, Phase.code)
            )
        )

    def list_milestones(
        self, project_id: UUID, *, phase_id: UUID | None = None
    ) -> list[Milestone]:
        self._get_project(project_id)
        stmt = select(Milestone).where(
            Milestone.organization_id == self.ctx.organization_id,
            Milestone.project_id == project_id,
        )
        if phase_id is not None:
            self._get_phase(phase_id)
            stmt = stmt.where(Milestone.phase_id == phase_id)
        stmt = stmt.order_by(Milestone.target_date.asc(), Milestone.code.asc())
        return list(self.db.scalars(stmt).all())

    def _get_project(self, project_id: UUID) -> Project:
        row = self.db.scalar(select(Project).where(Project.id == project_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Project not found")
        ctx_client = self.ctx.tenant.client_id
        if ctx_client and row.client_id and row.client_id != ctx_client:
            raise ForbiddenError("Cross-client access denied")
        return row

    def _get_phase(self, phase_id: UUID) -> Phase:
        row = self.db.scalar(select(Phase).where(Phase.id == phase_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Phase not found")
        self._get_project(row.project_id)
        return row

    def _get_milestone(self, milestone_id: UUID) -> Milestone:
        row = self.db.scalar(select(Milestone).where(Milestone.id == milestone_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Milestone not found")
        self._get_project(row.project_id)
        return row

    def _get_baseline(self, baseline_id: UUID) -> ProjectPlanBaseline:
        row = self.db.scalar(
            select(ProjectPlanBaseline).where(ProjectPlanBaseline.id == baseline_id)
        )
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Project baseline not found")
        self._get_project(row.project_id)
        return row
