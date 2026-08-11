"""HTTP routes for MOD-420 change control."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.changecontrol.schemas import (
    ApprovalCreate,
    ApprovalRead,
    BaselineUpdateCreate,
    BaselineUpdateRead,
    ChangeRequestCreate,
    ChangeRequestRead,
    DevelopmentGateResult,
    ImpactCreate,
    ImpactRead,
    RiskCreate,
    RiskRead,
    RiskReviewCreate,
    RiskReviewRead,
    SubmitForApproval,
)
from masms_api.modules.changecontrol.service import ChangeControlService

router = APIRouter(prefix="/change-control", tags=["change-control"])


class RiskPage(BaseModel):
    items: list[RiskRead]
    page: PageMeta = Field(description="Pagination metadata")


class ChangeRequestPage(BaseModel):
    items: list[ChangeRequestRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> ChangeControlService:
    return ChangeControlService(db, ctx)


@router.post("/risks", response_model=RiskRead, status_code=201)
def create_risk(body: RiskCreate, service: ChangeControlService = Depends(_service)) -> RiskRead:
    return RiskRead.model_validate(service.create_risk(body))


@router.get("/risks", response_model=RiskPage)
def list_risks(
    status: str | None = Query(default=None),
    project_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ChangeControlService = Depends(_service),
) -> RiskPage:
    items, page = service.list_risks(
        status=status, project_id=project_id, limit=limit, offset=offset
    )
    return RiskPage(items=[RiskRead.model_validate(r) for r in items], page=page)


@router.post("/risks/{risk_id}/reviews", response_model=RiskReviewRead, status_code=201)
def review_risk(
    risk_id: UUID,
    body: RiskReviewCreate,
    service: ChangeControlService = Depends(_service),
) -> RiskReviewRead:
    return RiskReviewRead.model_validate(service.review_risk(risk_id, body))


@router.get("/risks/{risk_id}/reviews", response_model=list[RiskReviewRead])
def list_risk_reviews(
    risk_id: UUID, service: ChangeControlService = Depends(_service)
) -> list[RiskReviewRead]:
    return [RiskReviewRead.model_validate(r) for r in service.list_risk_reviews(risk_id)]


@router.post("/change-requests", response_model=ChangeRequestRead, status_code=201)
def create_cr(
    body: ChangeRequestCreate, service: ChangeControlService = Depends(_service)
) -> ChangeRequestRead:
    return ChangeRequestRead.model_validate(service.create_change_request(body))


@router.get("/change-requests", response_model=ChangeRequestPage)
def list_crs(
    status: str | None = Query(default=None),
    project_id: UUID | None = Query(default=None),
    q: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ChangeControlService = Depends(_service),
) -> ChangeRequestPage:
    items, page = service.list_change_requests(
        status=status, project_id=project_id, q=q, limit=limit, offset=offset
    )
    return ChangeRequestPage(
        items=[ChangeRequestRead.model_validate(r) for r in items], page=page
    )


@router.get("/change-requests/{cr_id}", response_model=ChangeRequestRead)
def get_cr(cr_id: UUID, service: ChangeControlService = Depends(_service)) -> ChangeRequestRead:
    return ChangeRequestRead.model_validate(service.get_change_request(cr_id))


@router.get(
    "/change-requests/{cr_id}/development-gate",
    response_model=DevelopmentGateResult,
)
def development_gate(
    cr_id: UUID, service: ChangeControlService = Depends(_service)
) -> DevelopmentGateResult:
    return service.development_gate(cr_id)


@router.post(
    "/change-requests/{cr_id}/impacts",
    response_model=ImpactRead,
    status_code=201,
)
def add_impact(
    cr_id: UUID,
    body: ImpactCreate,
    service: ChangeControlService = Depends(_service),
) -> ImpactRead:
    return ImpactRead.model_validate(service.add_impact(cr_id, body))


@router.get("/change-requests/{cr_id}/impacts", response_model=list[ImpactRead])
def list_impacts(
    cr_id: UUID, service: ChangeControlService = Depends(_service)
) -> list[ImpactRead]:
    return [ImpactRead.model_validate(r) for r in service.list_impacts(cr_id)]


@router.post("/change-requests/{cr_id}/submit", response_model=ChangeRequestRead)
def submit_cr(
    cr_id: UUID,
    body: SubmitForApproval | None = None,
    service: ChangeControlService = Depends(_service),
) -> ChangeRequestRead:
    payload = body or SubmitForApproval()
    return ChangeRequestRead.model_validate(service.submit_for_approval(cr_id, payload))


@router.post(
    "/change-requests/{cr_id}/approvals",
    response_model=ApprovalRead,
    status_code=201,
)
def decide_cr(
    cr_id: UUID,
    body: ApprovalCreate,
    service: ChangeControlService = Depends(_service),
) -> ApprovalRead:
    return ApprovalRead.model_validate(service.decide(cr_id, body))


@router.get("/change-requests/{cr_id}/approvals", response_model=list[ApprovalRead])
def list_approvals(
    cr_id: UUID, service: ChangeControlService = Depends(_service)
) -> list[ApprovalRead]:
    return [ApprovalRead.model_validate(r) for r in service.list_approvals(cr_id)]


@router.post(
    "/change-requests/{cr_id}/baseline-updates",
    response_model=BaselineUpdateRead,
    status_code=201,
)
def apply_baseline(
    cr_id: UUID,
    body: BaselineUpdateCreate,
    service: ChangeControlService = Depends(_service),
) -> BaselineUpdateRead:
    return BaselineUpdateRead.model_validate(service.apply_baseline_update(cr_id, body))


@router.get(
    "/change-requests/{cr_id}/baseline-updates",
    response_model=list[BaselineUpdateRead],
)
def list_baselines(
    cr_id: UUID, service: ChangeControlService = Depends(_service)
) -> list[BaselineUpdateRead]:
    return [BaselineUpdateRead.model_validate(r) for r in service.list_baseline_updates(cr_id)]
