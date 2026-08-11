"""HTTP routes for MOD-260 project phases and roadmaps."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.roadmap.schemas import (
    BaselineCreate,
    BaselineRead,
    DeliverableCreate,
    DeliverableRead,
    ForecastCreate,
    ForecastRead,
    MilestoneCreate,
    MilestoneRead,
    PhaseCreate,
    PhaseDependencyCreate,
    PhaseDependencyRead,
    PhaseRead,
    RequirementPhaseMapCreate,
    RequirementPhaseMapRead,
)
from masms_api.modules.roadmap.service import RoadmapService

router = APIRouter(prefix="/roadmap", tags=["roadmap"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> RoadmapService:
    return RoadmapService(db, ctx)


@router.post("/phases", response_model=PhaseRead, status_code=201)
def create_phase(
    body: PhaseCreate, service: RoadmapService = Depends(_service)
) -> PhaseRead:
    return PhaseRead.model_validate(service.create_phase(body))


@router.get("/projects/{project_id}/phases", response_model=list[PhaseRead])
def list_phases(
    project_id: UUID, service: RoadmapService = Depends(_service)
) -> list[PhaseRead]:
    return [PhaseRead.model_validate(p) for p in service.list_phases(project_id)]


@router.get("/projects/{project_id}/milestones", response_model=list[MilestoneRead])
def list_milestones(
    project_id: UUID,
    phase_id: UUID | None = Query(default=None),
    service: RoadmapService = Depends(_service),
) -> list[MilestoneRead]:
    return [
        MilestoneRead.model_validate(m)
        for m in service.list_milestones(project_id, phase_id=phase_id)
    ]


@router.post("/phases/{phase_id}/complete", response_model=PhaseRead)
def complete_phase(
    phase_id: UUID, service: RoadmapService = Depends(_service)
) -> PhaseRead:
    return PhaseRead.model_validate(service.complete_phase(phase_id))


@router.post("/milestones", response_model=MilestoneRead, status_code=201)
def create_milestone(
    body: MilestoneCreate, service: RoadmapService = Depends(_service)
) -> MilestoneRead:
    return MilestoneRead.model_validate(service.create_milestone(body))


@router.post("/milestones/{milestone_id}/approve", response_model=MilestoneRead)
def approve_milestone(
    milestone_id: UUID, service: RoadmapService = Depends(_service)
) -> MilestoneRead:
    return MilestoneRead.model_validate(service.approve_milestone(milestone_id))


@router.post("/milestones/{milestone_id}/complete", response_model=MilestoneRead)
def complete_milestone(
    milestone_id: UUID, service: RoadmapService = Depends(_service)
) -> MilestoneRead:
    return MilestoneRead.model_validate(service.complete_milestone(milestone_id))


@router.post("/deliverables", response_model=DeliverableRead, status_code=201)
def create_deliverable(
    body: DeliverableCreate, service: RoadmapService = Depends(_service)
) -> DeliverableRead:
    return DeliverableRead.model_validate(service.create_deliverable(body))


@router.post("/phase-dependencies", response_model=PhaseDependencyRead, status_code=201)
def create_dependency(
    body: PhaseDependencyCreate, service: RoadmapService = Depends(_service)
) -> PhaseDependencyRead:
    return PhaseDependencyRead.model_validate(service.create_dependency(body))


@router.post("/requirement-maps", response_model=RequirementPhaseMapRead, status_code=201)
def map_requirement(
    body: RequirementPhaseMapCreate, service: RoadmapService = Depends(_service)
) -> RequirementPhaseMapRead:
    return RequirementPhaseMapRead.model_validate(service.map_requirement(body))


@router.post("/baselines", response_model=BaselineRead, status_code=201)
def create_baseline(
    body: BaselineCreate, service: RoadmapService = Depends(_service)
) -> BaselineRead:
    return BaselineRead.model_validate(service.create_baseline(body))


@router.post("/baselines/{baseline_id}/approve", response_model=BaselineRead)
def approve_baseline(
    baseline_id: UUID, service: RoadmapService = Depends(_service)
) -> BaselineRead:
    return BaselineRead.model_validate(service.approve_baseline(baseline_id))


@router.post("/forecasts", response_model=ForecastRead, status_code=201)
def create_forecast(
    body: ForecastCreate, service: RoadmapService = Depends(_service)
) -> ForecastRead:
    return ForecastRead.model_validate(service.create_forecast(body))
