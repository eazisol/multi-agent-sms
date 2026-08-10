"""Capacity API schemas (MOD-130)."""

from __future__ import annotations

from datetime import date, datetime, time
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SkillCreate(BaseModel):
    code: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    title: str = Field(min_length=2, max_length=255)
    category: str = Field(default="general", max_length=64)
    description: str | None = None


class SkillRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    category: str
    status: str
    created_at: datetime


class ActorSkillCreate(BaseModel):
    actor_id: UUID
    skill_id: UUID
    proficiency: int = Field(default=3, ge=1, le=5)


class ActorSkillRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    actor_id: UUID
    skill_id: UUID
    proficiency: int
    status: str
    created_at: datetime


class AvailabilityCreate(BaseModel):
    actor_id: UUID
    weekday: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    timezone: str = Field(default="UTC", max_length=64)


class AvailabilityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    actor_id: UUID
    weekday: int
    start_time: time
    end_time: time
    timezone: str
    status: str
    created_at: datetime


class CapacityAllocationCreate(BaseModel):
    actor_id: UUID
    allocation_pct: Decimal = Field(gt=0, le=100)
    project_id: UUID | None = None
    effective_from: date
    effective_to: date | None = None


class CapacityAllocationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    actor_id: UUID
    project_id: UUID | None
    allocation_pct: Decimal
    status: str
    effective_from: date
    effective_to: date | None
    created_at: datetime


class BusinessCalendarCreate(BaseModel):
    code: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    title: str = Field(min_length=2, max_length=255)
    timezone: str = Field(default="UTC", max_length=64)


class BusinessCalendarRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    timezone: str
    status: str
    created_at: datetime


class HolidayCreate(BaseModel):
    calendar_id: UUID
    holiday_date: date
    title: str = Field(min_length=2, max_length=255)


class HolidayRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    calendar_id: UUID
    holiday_date: date
    title: str
    status: str
    created_at: datetime


class LeavePeriodCreate(BaseModel):
    actor_id: UUID
    leave_type: str = Field(default="annual", max_length=64)
    starts_on: date
    ends_on: date
    notes: str | None = None


class LeavePeriodRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    actor_id: UUID
    leave_type: str
    starts_on: date
    ends_on: date
    status: str
    created_at: datetime


class OnCallCreate(BaseModel):
    actor_id: UUID
    rotation_name: str = Field(min_length=2, max_length=128)
    starts_at: datetime
    ends_at: datetime


class OnCallRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    actor_id: UUID
    rotation_name: str
    starts_at: datetime
    ends_at: datetime
    status: str
    created_at: datetime


class AssignmentEvaluateRequest(BaseModel):
    actor_id: UUID
    skill_code: str | None = None
    min_proficiency: int = Field(default=3, ge=1, le=5)
    project_id: UUID | None = None
    as_of: date | None = None
    calendar_id: UUID | None = None
    deadline: date | None = None


class AssignmentEvaluateResponse(BaseModel):
    eligible: bool
    reasons: list[str]
    remaining_capacity_pct: Decimal | None = None
    deadline_is_business_day: bool | None = None


class SlaBusinessDayRequest(BaseModel):
    calendar_id: UUID
    start_date: date
    business_days: int = Field(ge=0, le=365)


class SlaBusinessDayResponse(BaseModel):
    due_date: date
    calendar_timezone: str
