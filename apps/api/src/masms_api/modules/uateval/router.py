"""HTTP routes for MOD-620 UAT evaluation."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.uateval.schemas import (
    AcceptanceEvidenceAccept,
    AcceptanceEvidenceCreate,
    AcceptanceEvidenceRead,
    AgentEvaluationCreate,
    AgentEvaluationRead,
    AgentQualityRead,
    E2eTestCreate,
    E2eTestRead,
    ExpectedDecisionCreate,
    ExpectedDecisionRead,
    RoleUatCreate,
    RoleUatRead,
    SampleGateRead,
    SampleProjectRead,
    SeedScriptCreate,
    SeedScriptRead,
)
from masms_api.modules.uateval.service import UatEvalService

router = APIRouter(prefix="/uat", tags=["uat"])


class SampleProjectPage(BaseModel):
    items: list[SampleProjectRead]
    page: PageMeta = Field(description="Pagination metadata")


class SeedScriptPage(BaseModel):
    items: list[SeedScriptRead]
    page: PageMeta = Field(description="Pagination metadata")


class ExpectedDecisionPage(BaseModel):
    items: list[ExpectedDecisionRead]
    page: PageMeta = Field(description="Pagination metadata")


class AgentEvaluationPage(BaseModel):
    items: list[AgentEvaluationRead]
    page: PageMeta = Field(description="Pagination metadata")


class E2eTestPage(BaseModel):
    items: list[E2eTestRead]
    page: PageMeta = Field(description="Pagination metadata")


class RoleUatPage(BaseModel):
    items: list[RoleUatRead]
    page: PageMeta = Field(description="Pagination metadata")


class AcceptanceEvidencePage(BaseModel):
    items: list[AcceptanceEvidenceRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> UatEvalService:
    return UatEvalService(db, ctx)


@router.post("/sample-projects/seed", response_model=list[SampleProjectRead])
def seed_sample_projects(service: UatEvalService = Depends(_service)) -> list[SampleProjectRead]:
    return [SampleProjectRead.model_validate(item) for item in service.seed_sample_projects()]


@router.get("/sample-projects", response_model=SampleProjectPage)
def list_sample_projects(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: UatEvalService = Depends(_service),
) -> SampleProjectPage:
    items, page = service.list_sample_projects(limit=limit, offset=offset)
    return SampleProjectPage(
        items=[SampleProjectRead.model_validate(item) for item in items], page=page
    )


@router.get("/sample-projects/{code}", response_model=SampleProjectRead)
def get_sample_project(
    code: str, service: UatEvalService = Depends(_service)
) -> SampleProjectRead:
    return SampleProjectRead.model_validate(service.get_sample_project(code))


@router.post("/sample-projects/{code}/pass", response_model=SampleProjectRead)
def mark_sample_passed(
    code: str, service: UatEvalService = Depends(_service)
) -> SampleProjectRead:
    return SampleProjectRead.model_validate(service.mark_sample_passed(code))


@router.get("/sample-gate", response_model=SampleGateRead)
def sample_gate(service: UatEvalService = Depends(_service)) -> SampleGateRead:
    return SampleGateRead.model_validate(service.sample_gate())


@router.get("/agent-quality", response_model=AgentQualityRead)
def agent_quality(service: UatEvalService = Depends(_service)) -> AgentQualityRead:
    return AgentQualityRead.model_validate(service.agent_quality())


@router.post("/seed-scripts", response_model=SeedScriptRead, status_code=201)
def create_seed_script(
    body: SeedScriptCreate, service: UatEvalService = Depends(_service)
) -> SeedScriptRead:
    return SeedScriptRead.model_validate(service.create_seed_script(body))


@router.get("/seed-scripts", response_model=SeedScriptPage)
def list_seed_scripts(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: UatEvalService = Depends(_service),
) -> SeedScriptPage:
    items, page = service.list_seed_scripts(limit=limit, offset=offset)
    return SeedScriptPage(
        items=[SeedScriptRead.model_validate(item) for item in items], page=page
    )


@router.get("/seed-scripts/{seed_script_id}", response_model=SeedScriptRead)
def get_seed_script(
    seed_script_id: UUID, service: UatEvalService = Depends(_service)
) -> SeedScriptRead:
    return SeedScriptRead.model_validate(service.get_seed_script(seed_script_id))


@router.post("/expected-decisions", response_model=ExpectedDecisionRead, status_code=201)
def create_expected_decision(
    body: ExpectedDecisionCreate, service: UatEvalService = Depends(_service)
) -> ExpectedDecisionRead:
    return ExpectedDecisionRead.model_validate(service.create_expected_decision(body))


@router.get("/expected-decisions", response_model=ExpectedDecisionPage)
def list_expected_decisions(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: UatEvalService = Depends(_service),
) -> ExpectedDecisionPage:
    items, page = service.list_expected_decisions(limit=limit, offset=offset)
    return ExpectedDecisionPage(
        items=[ExpectedDecisionRead.model_validate(item) for item in items], page=page
    )


@router.post("/agent-evaluations", response_model=AgentEvaluationRead, status_code=201)
def create_agent_evaluation(
    body: AgentEvaluationCreate, service: UatEvalService = Depends(_service)
) -> AgentEvaluationRead:
    return AgentEvaluationRead.model_validate(service.create_agent_evaluation(body))


@router.get("/agent-evaluations", response_model=AgentEvaluationPage)
def list_agent_evaluations(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: UatEvalService = Depends(_service),
) -> AgentEvaluationPage:
    items, page = service.list_agent_evaluations(limit=limit, offset=offset)
    return AgentEvaluationPage(
        items=[AgentEvaluationRead.model_validate(item) for item in items], page=page
    )


@router.post("/e2e-tests", response_model=E2eTestRead, status_code=201)
def create_e2e_test(
    body: E2eTestCreate, service: UatEvalService = Depends(_service)
) -> E2eTestRead:
    return E2eTestRead.model_validate(service.create_e2e_test(body))


@router.get("/e2e-tests", response_model=E2eTestPage)
def list_e2e_tests(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: UatEvalService = Depends(_service),
) -> E2eTestPage:
    items, page = service.list_e2e_tests(limit=limit, offset=offset)
    return E2eTestPage(items=[E2eTestRead.model_validate(item) for item in items], page=page)


@router.post("/role-uat", response_model=RoleUatRead, status_code=201)
def create_role_uat(
    body: RoleUatCreate, service: UatEvalService = Depends(_service)
) -> RoleUatRead:
    return RoleUatRead.model_validate(service.create_role_uat(body))


@router.get("/role-uat", response_model=RoleUatPage)
def list_role_uat(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: UatEvalService = Depends(_service),
) -> RoleUatPage:
    items, page = service.list_role_uat(limit=limit, offset=offset)
    return RoleUatPage(items=[RoleUatRead.model_validate(item) for item in items], page=page)


@router.post("/acceptance-evidence", response_model=AcceptanceEvidenceRead, status_code=201)
def create_acceptance_evidence(
    body: AcceptanceEvidenceCreate, service: UatEvalService = Depends(_service)
) -> AcceptanceEvidenceRead:
    return AcceptanceEvidenceRead.model_validate(service.create_acceptance_evidence(body))


@router.get("/acceptance-evidence", response_model=AcceptanceEvidencePage)
def list_acceptance_evidence(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: UatEvalService = Depends(_service),
) -> AcceptanceEvidencePage:
    items, page = service.list_acceptance_evidence(limit=limit, offset=offset)
    return AcceptanceEvidencePage(
        items=[AcceptanceEvidenceRead.model_validate(item) for item in items], page=page
    )


@router.post("/acceptance-evidence/{evidence_id}/accept", response_model=AcceptanceEvidenceRead)
def accept_evidence(
    evidence_id: UUID,
    body: AcceptanceEvidenceAccept | None = None,
    service: UatEvalService = Depends(_service),
) -> AcceptanceEvidenceRead:
    return AcceptanceEvidenceRead.model_validate(
        service.accept_evidence(evidence_id, body or AcceptanceEvidenceAccept())
    )
