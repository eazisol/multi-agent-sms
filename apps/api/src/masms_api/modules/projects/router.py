"""HTTP routes for MOD-240 projects and SRS."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.projects.schemas import (
    AcceptanceCriterionCreate,
    AcceptanceCriterionRead,
    AssumptionCreate,
    AssumptionRead,
    BusinessRuleCreate,
    BusinessRuleRead,
    ConstraintCreate,
    ConstraintRead,
    ProjectCreate,
    ProjectRead,
    RequirementCreate,
    RequirementRead,
    RequirementVersionCreate,
    RequirementVersionRead,
    SrsBaselineCreate,
    SrsBaselineRead,
)
from masms_api.modules.projects.service import ProjectsService

router = APIRouter(prefix="/projects", tags=["projects"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> ProjectsService:
    return ProjectsService(db, ctx)


@router.post("", response_model=ProjectRead, status_code=201)
def create_project(
    body: ProjectCreate, service: ProjectsService = Depends(_service)
) -> ProjectRead:
    return ProjectRead.model_validate(service.create_project(body))


@router.get("", response_model=list[ProjectRead])
def list_projects(
    status: str | None = Query(default=None),
    q: str | None = Query(default=None),
    client_id: UUID | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    service: ProjectsService = Depends(_service),
) -> list[ProjectRead]:
    rows = service.list_projects(
        status=status, q=q, client_id=client_id, limit=limit, offset=offset
    )
    return [ProjectRead.model_validate(r) for r in rows]


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(
    project_id: UUID, service: ProjectsService = Depends(_service)
) -> ProjectRead:
    return ProjectRead.model_validate(service.get_project(project_id))


@router.post("/requirements", response_model=RequirementRead, status_code=201)
def create_requirement(
    body: RequirementCreate, service: ProjectsService = Depends(_service)
) -> RequirementRead:
    return RequirementRead.model_validate(service.create_requirement(body))


@router.get("/{project_id}/requirements", response_model=list[RequirementRead])
def list_requirements(
    project_id: UUID, service: ProjectsService = Depends(_service)
) -> list[RequirementRead]:
    return [RequirementRead.model_validate(r) for r in service.list_requirements(project_id)]


@router.post("/requirement-versions", response_model=RequirementVersionRead, status_code=201)
def create_requirement_version(
    body: RequirementVersionCreate, service: ProjectsService = Depends(_service)
) -> RequirementVersionRead:
    return RequirementVersionRead.model_validate(service.create_requirement_version(body))


@router.post(
    "/requirement-versions/{version_id}/approve",
    response_model=RequirementVersionRead,
)
def approve_requirement_version(
    version_id: UUID, service: ProjectsService = Depends(_service)
) -> RequirementVersionRead:
    return RequirementVersionRead.model_validate(
        service.approve_requirement_version(version_id)
    )


@router.post("/business-rules", response_model=BusinessRuleRead, status_code=201)
def add_business_rule(
    body: BusinessRuleCreate, service: ProjectsService = Depends(_service)
) -> BusinessRuleRead:
    return BusinessRuleRead.model_validate(service.add_business_rule(body))


@router.post("/acceptance-criteria", response_model=AcceptanceCriterionRead, status_code=201)
def add_acceptance_criterion(
    body: AcceptanceCriterionCreate, service: ProjectsService = Depends(_service)
) -> AcceptanceCriterionRead:
    return AcceptanceCriterionRead.model_validate(service.add_acceptance_criterion(body))


@router.post("/assumptions", response_model=AssumptionRead, status_code=201)
def add_assumption(
    body: AssumptionCreate, service: ProjectsService = Depends(_service)
) -> AssumptionRead:
    return AssumptionRead.model_validate(service.add_assumption(body))


@router.post("/constraints", response_model=ConstraintRead, status_code=201)
def add_constraint(
    body: ConstraintCreate, service: ProjectsService = Depends(_service)
) -> ConstraintRead:
    return ConstraintRead.model_validate(service.add_constraint(body))


@router.post("/srs-baselines", response_model=SrsBaselineRead, status_code=201)
def create_srs_baseline(
    body: SrsBaselineCreate, service: ProjectsService = Depends(_service)
) -> SrsBaselineRead:
    return SrsBaselineRead.model_validate(service.create_srs_baseline(body))


@router.post("/srs-baselines/{baseline_id}/approve", response_model=SrsBaselineRead)
def approve_srs_baseline(
    baseline_id: UUID, service: ProjectsService = Depends(_service)
) -> SrsBaselineRead:
    return SrsBaselineRead.model_validate(service.approve_srs_baseline(baseline_id))
