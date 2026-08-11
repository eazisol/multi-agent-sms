"""Projects / requirements / SRS application service (MOD-240)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from masms_api.errors import ForbiddenError, NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.projects import domain
from masms_api.modules.projects.models import (
    AcceptanceCriterion,
    Assumption,
    BusinessRule,
    Project,
    ProjectConstraint,
    ProjectRequirement,
    RequirementVersion,
    SrsBaseline,
)
from masms_api.modules.projects.schemas import (
    AcceptanceCriterionCreate,
    AssumptionCreate,
    BusinessRuleCreate,
    ConstraintCreate,
    ProjectCreate,
    RequirementCreate,
    RequirementVersionCreate,
    SrsBaselineCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class ProjectsService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_project(self, data: ProjectCreate) -> Project:
        client_id = data.client_id or self.ctx.tenant.client_id
        if self.ctx.tenant.client_id and client_id and client_id != self.ctx.tenant.client_id:
            raise ForbiddenError("Cross-client access denied")
        row = Project(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            client_id=client_id,
            code=data.code,
            title=data.title,
            status="active",
            owner_actor_id=data.owner_actor_id or self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="project_create",
            entity_type="prj_project",
            entity_id=row.id,
            payload={"code": data.code},
            project_id=row.id,
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="prj_project",
            aggregate_id=row.id,
            event_type="projects.project.created",
            payload={"code": data.code},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_projects(
        self,
        *,
        status: str | None = None,
        q: str | None = None,
        client_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Project], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [Project.organization_id == self.ctx.organization_id]
        ctx_client = self.ctx.tenant.client_id
        if ctx_client is not None:
            filters.append(Project.client_id == ctx_client)
        elif client_id is not None:
            filters.append(Project.client_id == client_id)
        if status:
            filters.append(Project.status == status)
        if q and q.strip():
            like = f"%{q.strip()}%"
            filters.append(or_(Project.code.ilike(like), Project.title.ilike(like)))
        total = self.db.scalar(select(func.count()).select_from(Project).where(*filters)) or 0
        rows = list(
            self.db.scalars(
                select(Project)
                .where(*filters)
                .order_by(Project.created_at.desc())
                .offset(offset)
                .limit(limit)
            )
        )
        return rows, build_page_meta(limit=limit, offset=offset, total=int(total))

    def get_project(self, project_id: UUID) -> Project:
        return self._get_project(project_id)

    def create_requirement(self, data: RequirementCreate) -> ProjectRequirement:
        project = self._get_project(data.project_id)
        domain.assert_requirement_code(data.requirement_code)
        row = ProjectRequirement(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=project.id,
            requirement_code=data.requirement_code.strip(),
            title=data.title,
            status="draft",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="requirement_create",
            entity_type="prj_requirement",
            entity_id=row.id,
            payload={"requirement_code": row.requirement_code},
            project_id=project.id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_requirement_version(self, data: RequirementVersionCreate) -> RequirementVersion:
        requirement = self._get_requirement(data.requirement_id)
        domain.assert_priority(data.priority)
        next_version = (
            self.db.scalar(
                select(func.max(RequirementVersion.version_number)).where(
                    RequirementVersion.requirement_id == requirement.id
                )
            )
            or 0
        ) + 1
        domain.assert_change_reason_for_new_version(
            version_number=next_version, change_reason=data.change_reason
        )
        row = RequirementVersion(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=requirement.project_id,
            requirement_id=requirement.id,
            version_number=next_version,
            statement=data.statement,
            priority=data.priority,
            status="draft",
            change_reason=data.change_reason,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="requirement_version_create",
            entity_type="prj_requirement_version",
            entity_id=row.id,
            payload={"version_number": next_version},
            project_id=requirement.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def add_business_rule(self, data: BusinessRuleCreate) -> BusinessRule:
        version = self._get_requirement_version(data.requirement_version_id)
        domain.assert_version_editable(version.status)
        row = BusinessRule(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=version.project_id,
            requirement_version_id=version.id,
            rule_code=data.rule_code,
            text=data.text,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def add_acceptance_criterion(self, data: AcceptanceCriterionCreate) -> AcceptanceCriterion:
        version = self._get_requirement_version(data.requirement_version_id)
        domain.assert_version_editable(version.status)
        row = AcceptanceCriterion(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=version.project_id,
            requirement_version_id=version.id,
            criterion_code=data.criterion_code,
            text=data.text,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def add_assumption(self, data: AssumptionCreate) -> Assumption:
        project = self._get_project(data.project_id)
        if data.requirement_version_id is not None:
            version = self._get_requirement_version(data.requirement_version_id)
            if version.project_id != project.id:
                raise ValidationAppError("requirement_version does not belong to project")
            domain.assert_version_editable(version.status)
        row = Assumption(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=project.id,
            requirement_version_id=data.requirement_version_id,
            assumption_code=data.assumption_code,
            text=data.text,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def add_constraint(self, data: ConstraintCreate) -> ProjectConstraint:
        project = self._get_project(data.project_id)
        if data.requirement_version_id is not None:
            version = self._get_requirement_version(data.requirement_version_id)
            if version.project_id != project.id:
                raise ValidationAppError("requirement_version does not belong to project")
            domain.assert_version_editable(version.status)
        row = ProjectConstraint(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=project.id,
            requirement_version_id=data.requirement_version_id,
            constraint_code=data.constraint_code,
            text=data.text,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def approve_requirement_version(self, version_id: UUID) -> RequirementVersion:
        version = self._get_requirement_version(version_id)
        requirement = self._get_requirement(version.requirement_id)
        ac_count = self.db.scalar(
            select(func.count()).select_from(AcceptanceCriterion).where(
                AcceptanceCriterion.requirement_version_id == version.id
            )
        ) or 0
        domain.assert_can_approve_requirement_version(
            status=version.status,
            requirement_code=requirement.requirement_code,
            acceptance_criteria_count=int(ac_count),
        )
        prior = list(
            self.db.scalars(
                select(RequirementVersion).where(
                    RequirementVersion.requirement_id == requirement.id,
                    RequirementVersion.status == "approved",
                    RequirementVersion.id != version.id,
                )
            )
        )
        for old in prior:
            old.status = "superseded"
            self.uow.add(old)
        version.status = "approved"
        version.approved_by_actor_id = self.ctx.actor_id
        version.approved_at = datetime.now(UTC)
        requirement.status = "approved"
        requirement.current_version_id = version.id
        self.uow.add(version)
        self.uow.add(requirement)
        self.obs.write_audit(
            action="requirement_version_approve",
            entity_type="prj_requirement_version",
            entity_id=version.id,
            payload={
                "requirement_code": requirement.requirement_code,
                "acceptance_criteria_count": int(ac_count),
            },
            project_id=version.project_id,
        )
        self.uow.commit()
        self.uow.refresh(version)
        return version

    def create_srs_baseline(self, data: SrsBaselineCreate) -> SrsBaseline:
        project = self._get_project(data.project_id)
        next_version = (
            self.db.scalar(
                select(func.max(SrsBaseline.version_number)).where(
                    SrsBaseline.project_id == project.id
                )
            )
            or 0
        ) + 1
        domain.assert_change_reason_for_new_version(
            version_number=next_version, change_reason=data.change_reason
        )
        approved_count = 0
        for vid in data.requirement_version_ids:
            version = self._get_requirement_version(vid)
            if version.project_id != project.id:
                raise ValidationAppError("requirement_version does not belong to project")
            if version.status == "approved":
                approved_count += 1
        if approved_count < 1:
            raise ValidationAppError(
                "SRS baseline must include at least one approved requirement version"
            )
        row = SrsBaseline(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=project.id,
            version_number=next_version,
            title=data.title,
            summary=data.summary,
            status="draft",
            requirement_version_ids=[str(v) for v in data.requirement_version_ids],
            change_reason=data.change_reason,
            metadata_json=data.metadata,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="srs_baseline_create",
            entity_type="prj_srs_baseline",
            entity_id=row.id,
            payload={"version_number": next_version},
            project_id=project.id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def approve_srs_baseline(self, baseline_id: UUID) -> SrsBaseline:
        row = self._get_srs(baseline_id)
        approved_count = 0
        for vid in row.requirement_version_ids or []:
            version = self._get_requirement_version(UUID(str(vid)))
            if version.status == "approved":
                approved_count += 1
        domain.assert_can_approve_srs(
            status=row.status, approved_requirement_version_count=approved_count
        )
        prior = list(
            self.db.scalars(
                select(SrsBaseline).where(
                    SrsBaseline.project_id == row.project_id,
                    SrsBaseline.status == "approved",
                    SrsBaseline.id != row.id,
                )
            )
        )
        for old in prior:
            old.status = "superseded"
            self.uow.add(old)
        row.status = "approved"
        row.approved_by_actor_id = self.ctx.actor_id
        row.approved_at = datetime.now(UTC)
        self.uow.add(row)
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="prj_srs_baseline",
            aggregate_id=row.id,
            event_type="projects.srs.approved",
            payload={"version_number": row.version_number},
            correlation_id=self.ctx.correlation_id,
        )
        self.obs.write_audit(
            action="srs_baseline_approve",
            entity_type="prj_srs_baseline",
            entity_id=row.id,
            payload={"version_number": row.version_number},
            project_id=row.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_requirements(self, project_id: UUID) -> list[ProjectRequirement]:
        self._get_project(project_id)
        return list(
            self.db.scalars(
                select(ProjectRequirement)
                .where(
                    ProjectRequirement.organization_id == self.ctx.organization_id,
                    ProjectRequirement.project_id == project_id,
                )
                .order_by(ProjectRequirement.requirement_code)
            )
        )

    def _get_project(self, project_id: UUID) -> Project:
        row = self.db.scalar(select(Project).where(Project.id == project_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Project not found")
        ctx_client = self.ctx.tenant.client_id
        if ctx_client and row.client_id and row.client_id != ctx_client:
            raise ForbiddenError("Cross-client access denied")
        return row

    def _get_requirement(self, requirement_id: UUID) -> ProjectRequirement:
        row = self.db.scalar(
            select(ProjectRequirement).where(ProjectRequirement.id == requirement_id)
        )
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Requirement not found")
        self._get_project(row.project_id)
        return row

    def _get_requirement_version(self, version_id: UUID) -> RequirementVersion:
        row = self.db.scalar(
            select(RequirementVersion).where(RequirementVersion.id == version_id)
        )
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Requirement version not found")
        self._get_project(row.project_id)
        return row

    def _get_srs(self, baseline_id: UUID) -> SrsBaseline:
        row = self.db.scalar(select(SrsBaseline).where(SrsBaseline.id == baseline_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("SRS baseline not found")
        self._get_project(row.project_id)
        return row
