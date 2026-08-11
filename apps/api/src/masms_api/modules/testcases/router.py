"""HTTP routes for MOD-400 test cases / coverage."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.testcases.schemas import (
    CaseCreate,
    CaseRead,
    CoverageCreate,
    CoverageRead,
    CoverageSummary,
    EvidenceRead,
    PlanCreate,
    PlanRead,
    RunComplete,
    RunCreate,
    RunRead,
    StepCreate,
    StepRead,
    SuiteCreate,
    SuiteRead,
)
from masms_api.modules.testcases.service import TestcaseService

router = APIRouter(prefix="/test-cases", tags=["test-cases"])


class CasePage(BaseModel):
    items: list[CaseRead]
    page: PageMeta = Field(description="Pagination metadata")


class RunPage(BaseModel):
    items: list[RunRead]
    page: PageMeta = Field(description="Pagination metadata")


class ApproveBody(BaseModel):
    expected_version: int | None = None


class CoverageSummaryRequest(BaseModel):
    must_have_requirement_ids: list[UUID] = Field(default_factory=list)


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> TestcaseService:
    return TestcaseService(db, ctx)


@router.post("/cases", response_model=CaseRead, status_code=201)
def create_case(
    body: CaseCreate,
    service: TestcaseService = Depends(_service),
) -> CaseRead:
    return CaseRead.model_validate(service.create_case(body))


@router.get("/cases", response_model=CasePage)
def list_cases(
    status: str | None = Query(default=None),
    case_type: str | None = Query(default=None),
    project_id: UUID | None = Query(default=None),
    q: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: TestcaseService = Depends(_service),
) -> CasePage:
    items, page = service.list_cases(
        status=status,
        case_type=case_type,
        project_id=project_id,
        q=q,
        limit=limit,
        offset=offset,
    )
    return CasePage(items=[CaseRead.model_validate(r) for r in items], page=page)


@router.get("/cases/{case_id}", response_model=CaseRead)
def get_case(
    case_id: UUID,
    service: TestcaseService = Depends(_service),
) -> CaseRead:
    return CaseRead.model_validate(service.get_case(case_id))


@router.post("/cases/{case_id}/approve", response_model=CaseRead)
def approve_case(
    case_id: UUID,
    body: ApproveBody | None = None,
    service: TestcaseService = Depends(_service),
) -> CaseRead:
    expected = body.expected_version if body else None
    return CaseRead.model_validate(service.approve_case(case_id, expected_version=expected))


@router.get("/cases/{case_id}/steps", response_model=list[StepRead])
def list_steps(
    case_id: UUID,
    service: TestcaseService = Depends(_service),
) -> list[StepRead]:
    return [StepRead.model_validate(r) for r in service.list_steps(case_id)]


@router.post("/cases/{case_id}/steps", response_model=list[StepRead], status_code=201)
def add_steps(
    case_id: UUID,
    body: list[StepCreate],
    service: TestcaseService = Depends(_service),
) -> list[StepRead]:
    return [StepRead.model_validate(r) for r in service.add_steps(case_id, body)]


@router.post("/suites", response_model=SuiteRead, status_code=201)
def create_suite(
    body: SuiteCreate,
    service: TestcaseService = Depends(_service),
) -> SuiteRead:
    return SuiteRead.model_validate(service.create_suite(body))


@router.get("/suites", response_model=list[SuiteRead])
def list_suites(
    service: TestcaseService = Depends(_service),
) -> list[SuiteRead]:
    return [SuiteRead.model_validate(r) for r in service.list_suites()]


@router.post("/plans", response_model=PlanRead, status_code=201)
def create_plan(
    body: PlanCreate,
    service: TestcaseService = Depends(_service),
) -> PlanRead:
    return PlanRead.model_validate(service.create_plan(body))


@router.get("/plans", response_model=list[PlanRead])
def list_plans(
    service: TestcaseService = Depends(_service),
) -> list[PlanRead]:
    return [PlanRead.model_validate(r) for r in service.list_plans()]


@router.post("/runs", response_model=RunRead, status_code=201)
def start_run(
    body: RunCreate,
    service: TestcaseService = Depends(_service),
) -> RunRead:
    return RunRead.model_validate(service.start_run(body))


@router.post("/runs/{run_id}/complete", response_model=RunRead)
def complete_run(
    run_id: UUID,
    body: RunComplete,
    service: TestcaseService = Depends(_service),
) -> RunRead:
    return RunRead.model_validate(service.complete_run(run_id, body))


@router.get("/runs", response_model=RunPage)
def list_runs(
    status: str | None = Query(default=None),
    case_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: TestcaseService = Depends(_service),
) -> RunPage:
    items, page = service.list_runs(status=status, case_id=case_id, limit=limit, offset=offset)
    return RunPage(items=[RunRead.model_validate(r) for r in items], page=page)


@router.get("/runs/{run_id}/evidence", response_model=list[EvidenceRead])
def list_evidence(
    run_id: UUID,
    service: TestcaseService = Depends(_service),
) -> list[EvidenceRead]:
    return [EvidenceRead.model_validate(r) for r in service.list_evidence(run_id)]


@router.post(
    "/cases/{case_id}/coverage",
    response_model=CoverageRead,
    status_code=201,
)
def link_coverage(
    case_id: UUID,
    body: CoverageCreate,
    service: TestcaseService = Depends(_service),
) -> CoverageRead:
    return CoverageRead.model_validate(service.link_coverage(case_id, body))


@router.get("/coverage", response_model=list[CoverageRead])
def list_coverage(
    case_id: UUID | None = Query(default=None),
    service: TestcaseService = Depends(_service),
) -> list[CoverageRead]:
    return [CoverageRead.model_validate(r) for r in service.list_coverage(case_id)]


@router.post("/coverage/summary", response_model=CoverageSummary)
def coverage_summary(
    body: CoverageSummaryRequest | None = None,
    service: TestcaseService = Depends(_service),
) -> CoverageSummary:
    ids = body.must_have_requirement_ids if body else []
    return service.coverage_summary(must_have_requirement_ids=ids)
