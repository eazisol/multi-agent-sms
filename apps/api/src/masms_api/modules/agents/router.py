"""HTTP routes for MOD-360 agent runtime registry."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.agents.schemas import (
    ContextProfileCreate,
    ContextProfileRead,
    DefinitionRead,
    EvaluationCreate,
    EvaluationRead,
    FailRun,
    PromptVersionCreate,
    PromptVersionRead,
    ReviewCreate,
    ReviewRead,
    RunCreate,
    RunRead,
    ToolPolicyCreate,
    ToolPolicyRead,
)
from masms_api.modules.agents.service import AgentRuntimeService

router = APIRouter(prefix="/agent-runtime", tags=["agent-runtime"])


class RunPage(BaseModel):
    items: list[RunRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> AgentRuntimeService:
    return AgentRuntimeService(db, ctx)


@router.get("/definitions", response_model=list[DefinitionRead])
def list_definitions(
    service: AgentRuntimeService = Depends(_service),
) -> list[DefinitionRead]:
    return [DefinitionRead.model_validate(r) for r in service.list_definitions()]


@router.post(
    "/definitions/{code}/prompt-versions",
    response_model=PromptVersionRead,
    status_code=201,
)
def create_prompt_version(
    code: str,
    body: PromptVersionCreate,
    service: AgentRuntimeService = Depends(_service),
) -> PromptVersionRead:
    return PromptVersionRead.model_validate(service.create_prompt_version(code, body))


@router.get("/prompt-versions", response_model=list[PromptVersionRead])
def list_prompt_versions(
    definition_id: UUID | None = Query(default=None),
    service: AgentRuntimeService = Depends(_service),
) -> list[PromptVersionRead]:
    return [
        PromptVersionRead.model_validate(r)
        for r in service.list_prompt_versions(definition_id)
    ]


@router.post("/prompt-versions/{version_id}/activate", response_model=PromptVersionRead)
def activate_prompt_version(
    version_id: UUID,
    service: AgentRuntimeService = Depends(_service),
) -> PromptVersionRead:
    return PromptVersionRead.model_validate(service.activate_prompt_version(version_id))


@router.post(
    "/definitions/{code}/tool-policies",
    response_model=ToolPolicyRead,
    status_code=201,
)
def create_tool_policy(
    code: str,
    body: ToolPolicyCreate,
    service: AgentRuntimeService = Depends(_service),
) -> ToolPolicyRead:
    return ToolPolicyRead.model_validate(service.create_tool_policy(code, body))


@router.get("/tool-policies", response_model=list[ToolPolicyRead])
def list_tool_policies(
    definition_id: UUID | None = Query(default=None),
    service: AgentRuntimeService = Depends(_service),
) -> list[ToolPolicyRead]:
    return [
        ToolPolicyRead.model_validate(r) for r in service.list_tool_policies(definition_id)
    ]


@router.post(
    "/definitions/{code}/context-profiles",
    response_model=ContextProfileRead,
    status_code=201,
)
def create_context_profile(
    code: str,
    body: ContextProfileCreate,
    service: AgentRuntimeService = Depends(_service),
) -> ContextProfileRead:
    return ContextProfileRead.model_validate(service.create_context_profile(code, body))


@router.get("/context-profiles", response_model=list[ContextProfileRead])
def list_context_profiles(
    definition_id: UUID | None = Query(default=None),
    service: AgentRuntimeService = Depends(_service),
) -> list[ContextProfileRead]:
    return [
        ContextProfileRead.model_validate(r)
        for r in service.list_context_profiles(definition_id)
    ]


@router.post("/runs", response_model=RunRead, status_code=201)
def start_run(
    body: RunCreate,
    service: AgentRuntimeService = Depends(_service),
) -> RunRead:
    return RunRead.model_validate(service.start_run(body))


@router.get("/runs", response_model=RunPage)
def list_runs(
    status: str | None = Query(default=None),
    q: str | None = Query(default=None),
    agent_code: str | None = Query(default=None),
    project_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: AgentRuntimeService = Depends(_service),
) -> RunPage:
    items, page = service.list_runs(
        status=status,
        q=q,
        agent_code=agent_code,
        project_id=project_id,
        limit=limit,
        offset=offset,
    )
    return RunPage(items=[RunRead.model_validate(r) for r in items], page=page)


@router.get("/runs/{run_id}", response_model=RunRead)
def get_run(
    run_id: UUID,
    service: AgentRuntimeService = Depends(_service),
) -> RunRead:
    return RunRead.model_validate(service.get_run(run_id))


@router.post("/runs/{run_id}/fail", response_model=RunRead)
def fail_run(
    run_id: UUID,
    body: FailRun,
    service: AgentRuntimeService = Depends(_service),
) -> RunRead:
    return RunRead.model_validate(service.fail_run(run_id, body))


@router.post("/runs/{run_id}/reviews", response_model=ReviewRead, status_code=201)
def submit_review(
    run_id: UUID,
    body: ReviewCreate,
    service: AgentRuntimeService = Depends(_service),
) -> ReviewRead:
    return ReviewRead.model_validate(service.submit_review(run_id, body))


@router.get("/runs/{run_id}/reviews", response_model=list[ReviewRead])
def list_reviews(
    run_id: UUID,
    service: AgentRuntimeService = Depends(_service),
) -> list[ReviewRead]:
    return [ReviewRead.model_validate(r) for r in service.list_reviews(run_id)]


@router.post(
    "/runs/{run_id}/evaluations",
    response_model=EvaluationRead,
    status_code=201,
)
def create_evaluation(
    run_id: UUID,
    body: EvaluationCreate,
    service: AgentRuntimeService = Depends(_service),
) -> EvaluationRead:
    return EvaluationRead.model_validate(service.create_evaluation(run_id, body))


@router.get("/runs/{run_id}/evaluations", response_model=list[EvaluationRead])
def list_evaluations(
    run_id: UUID,
    service: AgentRuntimeService = Depends(_service),
) -> list[EvaluationRead]:
    return [EvaluationRead.model_validate(r) for r in service.list_evaluations(run_id)]
