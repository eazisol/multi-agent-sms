"""Governance HTTP routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.governance.schemas import (
    AdrCreate,
    AdrRead,
    AdrTransition,
    ApprovalCreate,
    ApprovalRead,
    BaselineCreate,
    BaselineRead,
    BaselineTransition,
    BaselineUpdate,
    ChangeRequestCreate,
    ChangeRequestRead,
    ChangeRequestTransition,
    RequirementMappingCreate,
    RequirementMappingRead,
)
from masms_api.modules.governance.service import GovernanceService

router = APIRouter(prefix="/governance", tags=["governance"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> GovernanceService:
    return GovernanceService(db, ctx)


@router.post("/baselines", response_model=BaselineRead, status_code=201)
def create_baseline(
    body: BaselineCreate, service: GovernanceService = Depends(_service)
) -> BaselineRead:
    return BaselineRead.model_validate(service.create_baseline(body))


@router.get("/baselines", response_model=list[BaselineRead])
def list_baselines(service: GovernanceService = Depends(_service)) -> list[BaselineRead]:
    return [BaselineRead.model_validate(row) for row in service.list_baselines()]


@router.get("/baselines/{baseline_id}", response_model=BaselineRead)
def get_baseline(
    baseline_id: UUID, service: GovernanceService = Depends(_service)
) -> BaselineRead:
    return BaselineRead.model_validate(service.get_baseline(baseline_id))


@router.patch("/baselines/{baseline_id}", response_model=BaselineRead)
def update_baseline(
    baseline_id: UUID,
    body: BaselineUpdate,
    service: GovernanceService = Depends(_service),
) -> BaselineRead:
    return BaselineRead.model_validate(service.update_baseline(baseline_id, body))


@router.post("/baselines/{baseline_id}/transitions", response_model=BaselineRead)
def transition_baseline(
    baseline_id: UUID,
    body: BaselineTransition,
    service: GovernanceService = Depends(_service),
) -> BaselineRead:
    return BaselineRead.model_validate(service.transition_baseline(baseline_id, body))


@router.post("/requirement-mappings", response_model=RequirementMappingRead, status_code=201)
def create_requirement_mapping(
    body: RequirementMappingCreate, service: GovernanceService = Depends(_service)
) -> RequirementMappingRead:
    return RequirementMappingRead.model_validate(service.create_requirement_mapping(body))


@router.get("/requirement-mappings", response_model=list[RequirementMappingRead])
def list_requirement_mappings(
    service: GovernanceService = Depends(_service),
) -> list[RequirementMappingRead]:
    return [
        RequirementMappingRead.model_validate(row) for row in service.list_requirement_mappings()
    ]


@router.post("/architecture-decisions", response_model=AdrRead, status_code=201)
def create_adr(body: AdrCreate, service: GovernanceService = Depends(_service)) -> AdrRead:
    return AdrRead.model_validate(service.create_adr(body))


@router.get("/architecture-decisions", response_model=list[AdrRead])
def list_adrs(service: GovernanceService = Depends(_service)) -> list[AdrRead]:
    return [AdrRead.model_validate(row) for row in service.list_adrs()]


@router.post("/architecture-decisions/{adr_id}/transitions", response_model=AdrRead)
def transition_adr(
    adr_id: UUID, body: AdrTransition, service: GovernanceService = Depends(_service)
) -> AdrRead:
    return AdrRead.model_validate(service.transition_adr(adr_id, body))


@router.post("/change-requests", response_model=ChangeRequestRead, status_code=201)
def create_change_request(
    body: ChangeRequestCreate, service: GovernanceService = Depends(_service)
) -> ChangeRequestRead:
    return ChangeRequestRead.model_validate(service.create_change_request(body))


@router.get("/change-requests", response_model=list[ChangeRequestRead])
def list_change_requests(
    service: GovernanceService = Depends(_service),
) -> list[ChangeRequestRead]:
    return [ChangeRequestRead.model_validate(row) for row in service.list_change_requests()]


@router.post("/change-requests/{change_request_id}/transitions", response_model=ChangeRequestRead)
def transition_change_request(
    change_request_id: UUID,
    body: ChangeRequestTransition,
    service: GovernanceService = Depends(_service),
) -> ChangeRequestRead:
    return ChangeRequestRead.model_validate(
        service.transition_change_request(change_request_id, body)
    )


@router.post("/approvals", response_model=ApprovalRead, status_code=201)
def create_approval(
    body: ApprovalCreate, service: GovernanceService = Depends(_service)
) -> ApprovalRead:
    return ApprovalRead.model_validate(service.create_approval(body))


@router.get("/approvals", response_model=list[ApprovalRead])
def list_approvals(service: GovernanceService = Depends(_service)) -> list[ApprovalRead]:
    return [ApprovalRead.model_validate(row) for row in service.list_approvals()]
