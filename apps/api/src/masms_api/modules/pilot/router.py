"""HTTP routes for MOD-630 controlled pilot and production sign-off records."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.pilot.schemas import (
    AcceptanceGateRead,
    AcceptanceTestCreate,
    AcceptanceTestRead,
    AcceptanceTestResultUpdate,
    FinalSignoffCreate,
    FinalSignoffRead,
    FinalSignoffSign,
    KnownLimitationCreate,
    KnownLimitationRead,
    PilotApprovalGateRead,
    PilotPlanCreate,
    PilotPlanRead,
    PilotUserCreate,
    PilotUserRead,
    ProductionDeploymentCreate,
    ProductionDeploymentRead,
    ReadinessGateRead,
    RollbackCreate,
    RollbackRead,
    SupportReadinessCreate,
    SupportReadinessRead,
    TrainingRecordCreate,
    TrainingRecordRead,
)
from masms_api.modules.pilot.service import PilotService

router = APIRouter(prefix="/pilot", tags=["pilot"])


class PilotPlanPage(BaseModel):
    items: list[PilotPlanRead]
    page: PageMeta = Field(description="Pagination metadata")


class PilotUserPage(BaseModel):
    items: list[PilotUserRead]
    page: PageMeta = Field(description="Pagination metadata")


class TrainingRecordPage(BaseModel):
    items: list[TrainingRecordRead]
    page: PageMeta = Field(description="Pagination metadata")


class SupportReadinessPage(BaseModel):
    items: list[SupportReadinessRead]
    page: PageMeta = Field(description="Pagination metadata")


class KnownLimitationPage(BaseModel):
    items: list[KnownLimitationRead]
    page: PageMeta = Field(description="Pagination metadata")


class AcceptanceTestPage(BaseModel):
    items: list[AcceptanceTestRead]
    page: PageMeta = Field(description="Pagination metadata")


class FinalSignoffPage(BaseModel):
    items: list[FinalSignoffRead]
    page: PageMeta = Field(description="Pagination metadata")


class ProductionDeploymentPage(BaseModel):
    items: list[ProductionDeploymentRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> PilotService:
    return PilotService(db, ctx)


@router.get("/acceptance-gate", response_model=AcceptanceGateRead)
def acceptance_gate(
    plan_id: UUID = Query(...),
    service: PilotService = Depends(_service),
) -> AcceptanceGateRead:
    return AcceptanceGateRead.model_validate(service.acceptance_gate(plan_id))


@router.get("/pilot-approval-gate", response_model=PilotApprovalGateRead)
def pilot_approval_gate(
    plan_id: UUID = Query(...),
    service: PilotService = Depends(_service),
) -> PilotApprovalGateRead:
    return PilotApprovalGateRead.model_validate(service.pilot_approval_gate(plan_id))


@router.get("/readiness-gate", response_model=ReadinessGateRead)
def readiness_gate(
    plan_id: UUID = Query(...),
    service: PilotService = Depends(_service),
) -> ReadinessGateRead:
    return ReadinessGateRead.model_validate(service.readiness_gate(plan_id))


@router.post("/plans", response_model=PilotPlanRead, status_code=201)
def create_plan(
    body: PilotPlanCreate, service: PilotService = Depends(_service)
) -> PilotPlanRead:
    return PilotPlanRead.model_validate(service.create_plan(body))


@router.get("/plans", response_model=PilotPlanPage)
def list_plans(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: PilotService = Depends(_service),
) -> PilotPlanPage:
    items, page = service.list_plans(limit=limit, offset=offset)
    return PilotPlanPage(items=[PilotPlanRead.model_validate(item) for item in items], page=page)


@router.get("/plans/{plan_id}", response_model=PilotPlanRead)
def get_plan(plan_id: UUID, service: PilotService = Depends(_service)) -> PilotPlanRead:
    return PilotPlanRead.model_validate(service.get_plan(plan_id))


@router.post("/plans/{plan_id}/users", response_model=PilotUserRead, status_code=201)
def add_user(
    plan_id: UUID, body: PilotUserCreate, service: PilotService = Depends(_service)
) -> PilotUserRead:
    return PilotUserRead.model_validate(service.add_user(plan_id, body))


@router.get("/plans/{plan_id}/users", response_model=PilotUserPage)
def list_users(
    plan_id: UUID,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: PilotService = Depends(_service),
) -> PilotUserPage:
    items, page = service.list_users(plan_id, limit=limit, offset=offset)
    return PilotUserPage(items=[PilotUserRead.model_validate(item) for item in items], page=page)


@router.post("/plans/{plan_id}/users/{user_id}/approve", response_model=PilotUserRead)
def approve_user(
    plan_id: UUID, user_id: UUID, service: PilotService = Depends(_service)
) -> PilotUserRead:
    return PilotUserRead.model_validate(service.approve_user(plan_id, user_id))


@router.post("/plans/{plan_id}/training", response_model=TrainingRecordRead, status_code=201)
def create_training(
    plan_id: UUID, body: TrainingRecordCreate, service: PilotService = Depends(_service)
) -> TrainingRecordRead:
    return TrainingRecordRead.model_validate(service.create_training(plan_id, body))


@router.get("/plans/{plan_id}/training", response_model=TrainingRecordPage)
def list_training(
    plan_id: UUID,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: PilotService = Depends(_service),
) -> TrainingRecordPage:
    items, page = service.list_training(plan_id, limit=limit, offset=offset)
    return TrainingRecordPage(
        items=[TrainingRecordRead.model_validate(item) for item in items], page=page
    )


@router.post("/plans/{plan_id}/support", response_model=SupportReadinessRead, status_code=201)
def create_support(
    plan_id: UUID, body: SupportReadinessCreate, service: PilotService = Depends(_service)
) -> SupportReadinessRead:
    return SupportReadinessRead.model_validate(service.create_support(plan_id, body))


@router.get("/plans/{plan_id}/support", response_model=SupportReadinessPage)
def list_support(
    plan_id: UUID,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: PilotService = Depends(_service),
) -> SupportReadinessPage:
    items, page = service.list_support(plan_id, limit=limit, offset=offset)
    return SupportReadinessPage(
        items=[SupportReadinessRead.model_validate(item) for item in items], page=page
    )


@router.post("/plans/{plan_id}/limitations", response_model=KnownLimitationRead, status_code=201)
def create_limitation(
    plan_id: UUID, body: KnownLimitationCreate, service: PilotService = Depends(_service)
) -> KnownLimitationRead:
    return KnownLimitationRead.model_validate(service.create_limitation(plan_id, body))


@router.get("/plans/{plan_id}/limitations", response_model=KnownLimitationPage)
def list_limitations(
    plan_id: UUID,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: PilotService = Depends(_service),
) -> KnownLimitationPage:
    items, page = service.list_limitations(plan_id, limit=limit, offset=offset)
    return KnownLimitationPage(
        items=[KnownLimitationRead.model_validate(item) for item in items], page=page
    )


@router.post(
    "/plans/{plan_id}/acceptance-tests", response_model=AcceptanceTestRead, status_code=201
)
def create_acceptance_test(
    plan_id: UUID, body: AcceptanceTestCreate, service: PilotService = Depends(_service)
) -> AcceptanceTestRead:
    return AcceptanceTestRead.model_validate(service.create_acceptance_test(plan_id, body))


@router.get("/plans/{plan_id}/acceptance-tests", response_model=AcceptanceTestPage)
def list_acceptance_tests(
    plan_id: UUID,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: PilotService = Depends(_service),
) -> AcceptanceTestPage:
    items, page = service.list_acceptance_tests(plan_id, limit=limit, offset=offset)
    return AcceptanceTestPage(
        items=[AcceptanceTestRead.model_validate(item) for item in items], page=page
    )


@router.post(
    "/plans/{plan_id}/acceptance-tests/{test_id}/result", response_model=AcceptanceTestRead
)
def update_acceptance_result(
    plan_id: UUID,
    test_id: UUID,
    body: AcceptanceTestResultUpdate,
    service: PilotService = Depends(_service),
) -> AcceptanceTestRead:
    return AcceptanceTestRead.model_validate(
        service.update_acceptance_result(plan_id, test_id, body)
    )


@router.post("/signoffs", response_model=FinalSignoffRead, status_code=201)
def create_signoff(
    body: FinalSignoffCreate, service: PilotService = Depends(_service)
) -> FinalSignoffRead:
    return FinalSignoffRead.model_validate(service.create_signoff(body))


@router.get("/signoffs", response_model=FinalSignoffPage)
def list_signoffs(
    plan_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: PilotService = Depends(_service),
) -> FinalSignoffPage:
    items, page = service.list_signoffs(plan_id=plan_id, limit=limit, offset=offset)
    return FinalSignoffPage(
        items=[FinalSignoffRead.model_validate(item) for item in items], page=page
    )


@router.post("/signoffs/{signoff_id}/sign", response_model=FinalSignoffRead)
def sign_off(
    signoff_id: UUID,
    body: FinalSignoffSign,
    service: PilotService = Depends(_service),
) -> FinalSignoffRead:
    return FinalSignoffRead.model_validate(service.sign_off(signoff_id, body))


@router.post("/deployments", response_model=ProductionDeploymentRead, status_code=201)
def record_deployment(
    body: ProductionDeploymentCreate, service: PilotService = Depends(_service)
) -> ProductionDeploymentRead:
    return ProductionDeploymentRead.model_validate(service.record_deployment(body))


@router.get("/deployments", response_model=ProductionDeploymentPage)
def list_deployments(
    plan_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: PilotService = Depends(_service),
) -> ProductionDeploymentPage:
    items, page = service.list_deployments(plan_id=plan_id, limit=limit, offset=offset)
    return ProductionDeploymentPage(
        items=[ProductionDeploymentRead.model_validate(item) for item in items], page=page
    )


@router.post("/deployments/{deployment_id}/rollback", response_model=RollbackRead)
def record_rollback(
    deployment_id: UUID,
    body: RollbackCreate,
    service: PilotService = Depends(_service),
) -> RollbackRead:
    return RollbackRead.model_validate(service.record_rollback(deployment_id, body))
