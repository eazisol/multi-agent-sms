"""HTTP routes for MOD-330 approval gates."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.approvalgates.schemas import (
    ApprovalCreate,
    ApprovalRead,
    DecisionCreate,
    DecisionRead,
    DelegationCreate,
    DelegationRead,
    EvidenceCreate,
    EvidenceRead,
    GateCheckRequest,
    GateCheckResponse,
    OverrideCreate,
    OverrideRead,
    StepRead,
    WorkflowRead,
)
from masms_api.modules.approvalgates.service import ApprovalGatesService

router = APIRouter(prefix="/approvals", tags=["approvals"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> ApprovalGatesService:
    return ApprovalGatesService(db, ctx)


@router.post("", response_model=ApprovalRead, status_code=201)
def create_approval(
    body: ApprovalCreate, service: ApprovalGatesService = Depends(_service)
) -> ApprovalRead:
    return ApprovalRead.model_validate(service.create_approval(body))


@router.get("", response_model=list[ApprovalRead])
def list_approvals(
    status: str | None = Query(default=None),
    action_code: str | None = Query(default=None),
    service: ApprovalGatesService = Depends(_service),
) -> list[ApprovalRead]:
    rows = service.list_approvals(status=status, action_code=action_code)
    return [ApprovalRead.model_validate(r) for r in rows]


@router.post("/gate-check", response_model=GateCheckResponse)
def gate_check(
    body: GateCheckRequest, service: ApprovalGatesService = Depends(_service)
) -> GateCheckResponse:
    return service.check_gate(body)


@router.post("/gate-assert", response_model=GateCheckResponse)
def gate_assert(
    body: GateCheckRequest, service: ApprovalGatesService = Depends(_service)
) -> GateCheckResponse:
    return service.assert_gate(body)


@router.post("/delegations", response_model=DelegationRead, status_code=201)
def create_delegation(
    body: DelegationCreate, service: ApprovalGatesService = Depends(_service)
) -> DelegationRead:
    return DelegationRead.model_validate(service.create_delegation(body))


@router.get("/delegations", response_model=list[DelegationRead])
def list_delegations(
    service: ApprovalGatesService = Depends(_service),
) -> list[DelegationRead]:
    return [DelegationRead.model_validate(r) for r in service.list_delegations()]


@router.post("/delegations/{delegation_id}/revoke", response_model=DelegationRead)
def revoke_delegation(
    delegation_id: UUID, service: ApprovalGatesService = Depends(_service)
) -> DelegationRead:
    return DelegationRead.model_validate(service.revoke_delegation(delegation_id))


@router.post("/overrides", response_model=OverrideRead, status_code=201)
def create_override(
    body: OverrideCreate, service: ApprovalGatesService = Depends(_service)
) -> OverrideRead:
    return OverrideRead.model_validate(service.create_override(body))


@router.get("/{approval_id}", response_model=ApprovalRead)
def get_approval(
    approval_id: UUID, service: ApprovalGatesService = Depends(_service)
) -> ApprovalRead:
    return ApprovalRead.model_validate(service.get_approval(approval_id))


@router.get("/{approval_id}/workflow", response_model=WorkflowRead)
def get_workflow(
    approval_id: UUID, service: ApprovalGatesService = Depends(_service)
) -> WorkflowRead:
    return WorkflowRead.model_validate(service.get_workflow(approval_id))


@router.get("/{approval_id}/steps", response_model=list[StepRead])
def list_steps(
    approval_id: UUID, service: ApprovalGatesService = Depends(_service)
) -> list[StepRead]:
    return [StepRead.model_validate(r) for r in service.list_steps(approval_id)]


@router.get("/{approval_id}/decisions", response_model=list[DecisionRead])
def list_decisions(
    approval_id: UUID, service: ApprovalGatesService = Depends(_service)
) -> list[DecisionRead]:
    return [DecisionRead.model_validate(r) for r in service.list_decisions(approval_id)]


@router.post("/{approval_id}/decisions", response_model=DecisionRead)
def decide(
    approval_id: UUID,
    body: DecisionCreate,
    service: ApprovalGatesService = Depends(_service),
) -> DecisionRead:
    return DecisionRead.model_validate(service.decide(approval_id, body))


@router.post("/{approval_id}/supersede", response_model=ApprovalRead)
def supersede(
    approval_id: UUID,
    reason: str = Query(min_length=1),
    service: ApprovalGatesService = Depends(_service),
) -> ApprovalRead:
    return ApprovalRead.model_validate(service.supersede(approval_id, reason=reason))


@router.post("/{approval_id}/evidence", response_model=EvidenceRead, status_code=201)
def add_evidence(
    approval_id: UUID,
    body: EvidenceCreate,
    service: ApprovalGatesService = Depends(_service),
) -> EvidenceRead:
    return EvidenceRead.model_validate(service.add_evidence(approval_id, body))


@router.get("/{approval_id}/evidence", response_model=list[EvidenceRead])
def list_evidence(
    approval_id: UUID, service: ApprovalGatesService = Depends(_service)
) -> list[EvidenceRead]:
    return [EvidenceRead.model_validate(r) for r in service.list_evidence(approval_id)]
