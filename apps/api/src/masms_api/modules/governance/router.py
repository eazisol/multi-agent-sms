"""Governance HTTP routes."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.governance.schemas import (
    AdrCreate,
    AdrPage,
    AdrRead,
    AdrTransition,
    ApprovalCreate,
    ApprovalPage,
    ApprovalRead,
    AuditEventPage,
    AuditEventRead,
    BaselineCreate,
    BaselinePage,
    BaselineRead,
    BaselineTransition,
    BaselineUpdate,
    ChangeRequestCreate,
    ChangeRequestPage,
    ChangeRequestRead,
    ChangeRequestTransition,
    ProblemDetails,
    RequirementMappingCreate,
    RequirementMappingPage,
    RequirementMappingRead,
)
from masms_api.modules.governance.service import GovernanceService

router = APIRouter(prefix="/governance", tags=["governance"])

ERROR_RESPONSES: dict[int | str, dict[str, Any]] = {
    403: {"model": ProblemDetails, "description": "Forbidden"},
    404: {"model": ProblemDetails, "description": "Not found"},
    409: {
        "model": ProblemDetails,
        "description": "Conflict / invalid transition / approval required",
    },
    422: {"model": ProblemDetails, "description": "Validation error"},
}


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> GovernanceService:
    return GovernanceService(db, ctx)


@router.post(
    "/baselines",
    response_model=BaselineRead,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
    summary="Create source baseline",
)
def create_baseline(
    body: BaselineCreate, service: GovernanceService = Depends(_service)
) -> BaselineRead:
    return BaselineRead.model_validate(service.create_baseline(body))


@router.get(
    "/baselines",
    response_model=BaselinePage,
    responses=ERROR_RESPONSES,
    summary="List source baselines",
)
def list_baselines(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status_filter: str | None = Query(default=None, alias="status"),
    q: str | None = Query(default=None, max_length=128),
    sort: str = Query(default="baseline_key"),
    service: GovernanceService = Depends(_service),
) -> BaselinePage:
    rows, page = service.list_baselines(
        limit=limit, offset=offset, status=status_filter, q=q, sort=sort
    )
    return BaselinePage(items=[BaselineRead.model_validate(row) for row in rows], page=page)


@router.get(
    "/baselines/{baseline_id}",
    response_model=BaselineRead,
    responses=ERROR_RESPONSES,
    summary="Get source baseline",
)
def get_baseline(
    baseline_id: UUID, service: GovernanceService = Depends(_service)
) -> BaselineRead:
    return BaselineRead.model_validate(service.get_baseline(baseline_id))


@router.get(
    "/baselines/{baseline_id}/history",
    response_model=AuditEventPage,
    responses=ERROR_RESPONSES,
    summary="List source baseline audit history",
)
def list_baseline_history(
    baseline_id: UUID,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: GovernanceService = Depends(_service),
) -> AuditEventPage:
    rows, page = service.list_baseline_history(baseline_id, limit=limit, offset=offset)
    return AuditEventPage(items=[AuditEventRead.model_validate(row) for row in rows], page=page)


@router.patch(
    "/baselines/{baseline_id}",
    response_model=BaselineRead,
    responses=ERROR_RESPONSES,
    summary="Update mutable source baseline",
)
def update_baseline(
    baseline_id: UUID,
    body: BaselineUpdate,
    service: GovernanceService = Depends(_service),
) -> BaselineRead:
    return BaselineRead.model_validate(service.update_baseline(baseline_id, body))


@router.post(
    "/baselines/{baseline_id}/transitions",
    response_model=BaselineRead,
    responses=ERROR_RESPONSES,
    summary="Transition source baseline status",
)
def transition_baseline(
    baseline_id: UUID,
    body: BaselineTransition,
    service: GovernanceService = Depends(_service),
) -> BaselineRead:
    return BaselineRead.model_validate(service.transition_baseline(baseline_id, body))


@router.post(
    "/requirement-mappings",
    response_model=RequirementMappingRead,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
)
def create_requirement_mapping(
    body: RequirementMappingCreate, service: GovernanceService = Depends(_service)
) -> RequirementMappingRead:
    return RequirementMappingRead.model_validate(service.create_requirement_mapping(body))


@router.get(
    "/requirement-mappings",
    response_model=RequirementMappingPage,
    responses=ERROR_RESPONSES,
)
def list_requirement_mappings(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    q: str | None = Query(default=None, max_length=128),
    service: GovernanceService = Depends(_service),
) -> RequirementMappingPage:
    rows, page = service.list_requirement_mappings(limit=limit, offset=offset, q=q)
    return RequirementMappingPage(
        items=[RequirementMappingRead.model_validate(row) for row in rows],
        page=page,
    )


@router.post(
    "/architecture-decisions",
    response_model=AdrRead,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
)
def create_adr(body: AdrCreate, service: GovernanceService = Depends(_service)) -> AdrRead:
    return AdrRead.model_validate(service.create_adr(body))


@router.get("/architecture-decisions", response_model=AdrPage, responses=ERROR_RESPONSES)
def list_adrs(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status_filter: str | None = Query(default=None, alias="status"),
    service: GovernanceService = Depends(_service),
) -> AdrPage:
    rows, page = service.list_adrs(limit=limit, offset=offset, status=status_filter)
    return AdrPage(items=[AdrRead.model_validate(row) for row in rows], page=page)


@router.post(
    "/architecture-decisions/{adr_id}/transitions",
    response_model=AdrRead,
    responses=ERROR_RESPONSES,
)
def transition_adr(
    adr_id: UUID, body: AdrTransition, service: GovernanceService = Depends(_service)
) -> AdrRead:
    return AdrRead.model_validate(service.transition_adr(adr_id, body))


@router.post(
    "/change-requests",
    response_model=ChangeRequestRead,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
)
def create_change_request(
    body: ChangeRequestCreate, service: GovernanceService = Depends(_service)
) -> ChangeRequestRead:
    return ChangeRequestRead.model_validate(service.create_change_request(body))


@router.get("/change-requests", response_model=ChangeRequestPage, responses=ERROR_RESPONSES)
def list_change_requests(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status_filter: str | None = Query(default=None, alias="status"),
    service: GovernanceService = Depends(_service),
) -> ChangeRequestPage:
    rows, page = service.list_change_requests(limit=limit, offset=offset, status=status_filter)
    return ChangeRequestPage(
        items=[ChangeRequestRead.model_validate(row) for row in rows],
        page=page,
    )


@router.post(
    "/change-requests/{change_request_id}/transitions",
    response_model=ChangeRequestRead,
    responses=ERROR_RESPONSES,
)
def transition_change_request(
    change_request_id: UUID,
    body: ChangeRequestTransition,
    service: GovernanceService = Depends(_service),
) -> ChangeRequestRead:
    return ChangeRequestRead.model_validate(
        service.transition_change_request(change_request_id, body)
    )


@router.post(
    "/approvals",
    response_model=ApprovalRead,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
)
def create_approval(
    body: ApprovalCreate, service: GovernanceService = Depends(_service)
) -> ApprovalRead:
    return ApprovalRead.model_validate(service.create_approval(body))


@router.get("/approvals", response_model=ApprovalPage, responses=ERROR_RESPONSES)
def list_approvals(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: GovernanceService = Depends(_service),
) -> ApprovalPage:
    rows, page = service.list_approvals(limit=limit, offset=offset)
    return ApprovalPage(items=[ApprovalRead.model_validate(row) for row in rows], page=page)
