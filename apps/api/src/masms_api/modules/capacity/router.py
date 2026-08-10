"""HTTP routes for MOD-130 capacity / workforce."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.capacity.schemas import (
    ActorSkillCreate,
    ActorSkillRead,
    AssignmentEvaluateRequest,
    AssignmentEvaluateResponse,
    AvailabilityCreate,
    AvailabilityRead,
    BusinessCalendarCreate,
    BusinessCalendarRead,
    CapacityAllocationCreate,
    CapacityAllocationRead,
    HolidayCreate,
    HolidayRead,
    LeavePeriodCreate,
    LeavePeriodRead,
    OnCallCreate,
    OnCallRead,
    SkillCreate,
    SkillRead,
    SlaBusinessDayRequest,
    SlaBusinessDayResponse,
)
from masms_api.modules.capacity.service import CapacityService

router = APIRouter(prefix="/capacity", tags=["capacity"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> CapacityService:
    return CapacityService(db, ctx)


@router.post("/skills", response_model=SkillRead, status_code=201)
def create_skill(body: SkillCreate, service: CapacityService = Depends(_service)) -> SkillRead:
    return SkillRead.model_validate(service.create_skill(body))


@router.post("/actor-skills", response_model=ActorSkillRead, status_code=201)
def assign_skill(
    body: ActorSkillCreate, service: CapacityService = Depends(_service)
) -> ActorSkillRead:
    return ActorSkillRead.model_validate(service.assign_actor_skill(body))


@router.post("/availability", response_model=AvailabilityRead, status_code=201)
def create_availability(
    body: AvailabilityCreate, service: CapacityService = Depends(_service)
) -> AvailabilityRead:
    return AvailabilityRead.model_validate(service.create_availability(body))


@router.post("/allocations", response_model=CapacityAllocationRead, status_code=201)
def create_allocation(
    body: CapacityAllocationCreate, service: CapacityService = Depends(_service)
) -> CapacityAllocationRead:
    return CapacityAllocationRead.model_validate(service.create_capacity(body))


@router.post("/calendars", response_model=BusinessCalendarRead, status_code=201)
def create_calendar(
    body: BusinessCalendarCreate, service: CapacityService = Depends(_service)
) -> BusinessCalendarRead:
    return BusinessCalendarRead.model_validate(service.create_calendar(body))


@router.post("/holidays", response_model=HolidayRead, status_code=201)
def create_holiday(
    body: HolidayCreate, service: CapacityService = Depends(_service)
) -> HolidayRead:
    return HolidayRead.model_validate(service.create_holiday(body))


@router.post("/leave", response_model=LeavePeriodRead, status_code=201)
def create_leave(
    body: LeavePeriodCreate, service: CapacityService = Depends(_service)
) -> LeavePeriodRead:
    return LeavePeriodRead.model_validate(service.create_leave(body))


@router.post("/oncall", response_model=OnCallRead, status_code=201)
def create_oncall(body: OnCallCreate, service: CapacityService = Depends(_service)) -> OnCallRead:
    return OnCallRead.model_validate(service.create_oncall(body))


@router.post("/evaluate-assignment", response_model=AssignmentEvaluateResponse)
def evaluate_assignment(
    body: AssignmentEvaluateRequest, service: CapacityService = Depends(_service)
) -> AssignmentEvaluateResponse:
    return service.evaluate_assignment(body)


@router.post("/sla/business-days", response_model=SlaBusinessDayResponse)
def sla_business_days(
    body: SlaBusinessDayRequest, service: CapacityService = Depends(_service)
) -> SlaBusinessDayResponse:
    return service.add_business_days(body)
