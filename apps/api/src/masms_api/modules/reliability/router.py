"""HTTP routes for MOD-610 reliability."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.reliability.schemas import (
    ApiSloRead,
    DashboardSloRead,
    DrRunbookApprove,
    DrRunbookCreate,
    DrRunbookRead,
    IndexReviewCreate,
    IndexReviewRead,
    IntegrationFailureTestCreate,
    IntegrationFailureTestRead,
    PerformanceTestCreate,
    PerformanceTestRead,
    ResilienceTestCreate,
    ResilienceTestRead,
    SloDashboardRead,
    SloDashboardUpsert,
    WorkflowReplayAction,
    WorkflowReplayCreate,
    WorkflowReplayFail,
    WorkflowReplayRead,
)
from masms_api.modules.reliability.service import ReliabilityService

router = APIRouter(prefix="/reliability", tags=["reliability"])


class PerformanceTestPage(BaseModel):
    items: list[PerformanceTestRead]
    page: PageMeta = Field(description="Pagination metadata")


class ResilienceTestPage(BaseModel):
    items: list[ResilienceTestRead]
    page: PageMeta = Field(description="Pagination metadata")


class IndexReviewPage(BaseModel):
    items: list[IndexReviewRead]
    page: PageMeta = Field(description="Pagination metadata")


class SloDashboardPage(BaseModel):
    items: list[SloDashboardRead]
    page: PageMeta = Field(description="Pagination metadata")


class WorkflowReplayPage(BaseModel):
    items: list[WorkflowReplayRead]
    page: PageMeta = Field(description="Pagination metadata")


class IntegrationFailureTestPage(BaseModel):
    items: list[IntegrationFailureTestRead]
    page: PageMeta = Field(description="Pagination metadata")


class DrRunbookPage(BaseModel):
    items: list[DrRunbookRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> ReliabilityService:
    return ReliabilityService(db, ctx)


@router.get("/api-slo", response_model=ApiSloRead)
def api_slo(service: ReliabilityService = Depends(_service)) -> ApiSloRead:
    return ApiSloRead.model_validate(service.api_slo())


@router.get("/dashboard-slo", response_model=DashboardSloRead)
def dashboard_slo(service: ReliabilityService = Depends(_service)) -> DashboardSloRead:
    return DashboardSloRead.model_validate(service.dashboard_slo())


@router.post("/performance-tests", response_model=PerformanceTestRead, status_code=201)
def create_performance_test(
    body: PerformanceTestCreate, service: ReliabilityService = Depends(_service)
) -> PerformanceTestRead:
    return PerformanceTestRead.model_validate(service.create_performance_test(body))


@router.get("/performance-tests", response_model=PerformanceTestPage)
def list_performance_tests(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ReliabilityService = Depends(_service),
) -> PerformanceTestPage:
    items, page = service.list_performance_tests(limit=limit, offset=offset)
    return PerformanceTestPage(
        items=[PerformanceTestRead.model_validate(item) for item in items], page=page
    )


@router.post("/resilience-tests", response_model=ResilienceTestRead, status_code=201)
def create_resilience_test(
    body: ResilienceTestCreate, service: ReliabilityService = Depends(_service)
) -> ResilienceTestRead:
    return ResilienceTestRead.model_validate(service.create_resilience_test(body))


@router.get("/resilience-tests", response_model=ResilienceTestPage)
def list_resilience_tests(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ReliabilityService = Depends(_service),
) -> ResilienceTestPage:
    items, page = service.list_resilience_tests(limit=limit, offset=offset)
    return ResilienceTestPage(
        items=[ResilienceTestRead.model_validate(item) for item in items], page=page
    )


@router.post("/index-reviews", response_model=IndexReviewRead, status_code=201)
def create_index_review(
    body: IndexReviewCreate, service: ReliabilityService = Depends(_service)
) -> IndexReviewRead:
    return IndexReviewRead.model_validate(service.create_index_review(body))


@router.get("/index-reviews", response_model=IndexReviewPage)
def list_index_reviews(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ReliabilityService = Depends(_service),
) -> IndexReviewPage:
    items, page = service.list_index_reviews(limit=limit, offset=offset)
    return IndexReviewPage(
        items=[IndexReviewRead.model_validate(item) for item in items], page=page
    )


@router.post("/slo-dashboards", response_model=SloDashboardRead, status_code=201)
def upsert_slo_dashboard(
    body: SloDashboardUpsert, service: ReliabilityService = Depends(_service)
) -> SloDashboardRead:
    return SloDashboardRead.model_validate(service.upsert_slo_dashboard(body))


@router.get("/slo-dashboards", response_model=SloDashboardPage)
def list_slo_dashboards(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ReliabilityService = Depends(_service),
) -> SloDashboardPage:
    items, page = service.list_slo_dashboards(limit=limit, offset=offset)
    return SloDashboardPage(
        items=[SloDashboardRead.model_validate(item) for item in items], page=page
    )


@router.post("/replays", response_model=WorkflowReplayRead, status_code=201)
def create_replay(
    body: WorkflowReplayCreate, service: ReliabilityService = Depends(_service)
) -> WorkflowReplayRead:
    return WorkflowReplayRead.model_validate(service.create_replay(body))


@router.get("/replays", response_model=WorkflowReplayPage)
def list_replays(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ReliabilityService = Depends(_service),
) -> WorkflowReplayPage:
    items, page = service.list_replays(limit=limit, offset=offset)
    return WorkflowReplayPage(
        items=[WorkflowReplayRead.model_validate(item) for item in items], page=page
    )


@router.post("/replays/{replay_id}/fail", response_model=WorkflowReplayRead)
def fail_replay(
    replay_id: UUID,
    body: WorkflowReplayFail | None = None,
    service: ReliabilityService = Depends(_service),
) -> WorkflowReplayRead:
    return WorkflowReplayRead.model_validate(
        service.fail_replay(replay_id, body or WorkflowReplayFail())
    )


@router.post("/replays/{replay_id}/resume", response_model=WorkflowReplayRead)
def resume_replay(
    replay_id: UUID,
    body: WorkflowReplayAction | None = None,
    service: ReliabilityService = Depends(_service),
) -> WorkflowReplayRead:
    return WorkflowReplayRead.model_validate(
        service.resume_replay(replay_id, body or WorkflowReplayAction())
    )


@router.post("/replays/{replay_id}/complete", response_model=WorkflowReplayRead)
def complete_replay(
    replay_id: UUID,
    body: WorkflowReplayAction | None = None,
    service: ReliabilityService = Depends(_service),
) -> WorkflowReplayRead:
    return WorkflowReplayRead.model_validate(
        service.complete_replay(replay_id, body or WorkflowReplayAction())
    )


@router.post(
    "/integration-failure-tests",
    response_model=IntegrationFailureTestRead,
    status_code=201,
)
def create_integration_failure_test(
    body: IntegrationFailureTestCreate, service: ReliabilityService = Depends(_service)
) -> IntegrationFailureTestRead:
    return IntegrationFailureTestRead.model_validate(
        service.create_integration_failure_test(body)
    )


@router.get("/integration-failure-tests", response_model=IntegrationFailureTestPage)
def list_integration_failure_tests(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ReliabilityService = Depends(_service),
) -> IntegrationFailureTestPage:
    items, page = service.list_integration_failure_tests(limit=limit, offset=offset)
    return IntegrationFailureTestPage(
        items=[IntegrationFailureTestRead.model_validate(item) for item in items],
        page=page,
    )


@router.post(
    "/integration-failure-tests/{test_id}/recover",
    response_model=IntegrationFailureTestRead,
)
def mark_integration_recovered(
    test_id: UUID, service: ReliabilityService = Depends(_service)
) -> IntegrationFailureTestRead:
    return IntegrationFailureTestRead.model_validate(
        service.mark_integration_recovered(test_id)
    )


@router.post("/dr-runbooks", response_model=DrRunbookRead, status_code=201)
def create_dr_runbook(
    body: DrRunbookCreate, service: ReliabilityService = Depends(_service)
) -> DrRunbookRead:
    return DrRunbookRead.model_validate(service.create_dr_runbook(body))


@router.get("/dr-runbooks", response_model=DrRunbookPage)
def list_dr_runbooks(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ReliabilityService = Depends(_service),
) -> DrRunbookPage:
    items, page = service.list_dr_runbooks(limit=limit, offset=offset)
    return DrRunbookPage(
        items=[DrRunbookRead.model_validate(item) for item in items], page=page
    )


@router.post("/dr-runbooks/{runbook_id}/approve", response_model=DrRunbookRead)
def approve_dr_runbook(
    runbook_id: UUID,
    body: DrRunbookApprove | None = None,
    service: ReliabilityService = Depends(_service),
) -> DrRunbookRead:
    return DrRunbookRead.model_validate(
        service.approve_dr_runbook(runbook_id, body or DrRunbookApprove())
    )
