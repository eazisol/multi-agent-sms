"""Roadmap API schemas (MOD-260)."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PhaseCreate(BaseModel):
    project_id: UUID
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=2, max_length=255)
    sequence: int = Field(default=1, ge=1)
    owner_actor_id: UUID | None = None
    planned_start: date | None = None
    planned_end: date | None = None


class PhaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    code: str
    title: str
    sequence: int
    status: str
    owner_actor_id: UUID
    planned_start: date | None
    planned_end: date | None
    completed_at: datetime | None
    created_at: datetime


class MilestoneCreate(BaseModel):
    phase_id: UUID
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=2, max_length=255)
    owner_actor_id: UUID
    target_date: date
    requires_approval: bool = True


class MilestoneRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    phase_id: UUID
    code: str
    title: str
    owner_actor_id: UUID
    target_date: date
    status: str
    requires_approval: bool
    approved_by_actor_id: UUID | None
    approved_at: datetime | None
    created_at: datetime


class DeliverableCreate(BaseModel):
    phase_id: UUID
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=2, max_length=255)
    milestone_id: UUID | None = None


class DeliverableRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    phase_id: UUID
    milestone_id: UUID | None
    code: str
    title: str
    status: str
    created_at: datetime


class PhaseDependencyCreate(BaseModel):
    project_id: UUID
    predecessor_phase_id: UUID
    successor_phase_id: UUID
    dependency_type: str = Field(default="finish_to_start", max_length=32)


class PhaseDependencyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    predecessor_phase_id: UUID
    successor_phase_id: UUID
    dependency_type: str
    created_at: datetime


class RequirementPhaseMapCreate(BaseModel):
    project_id: UUID
    requirement_id: UUID
    phase_id: UUID


class RequirementPhaseMapRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    requirement_id: UUID
    phase_id: UUID
    created_at: datetime


class BaselineCreate(BaseModel):
    project_id: UUID
    title: str = Field(min_length=2, max_length=255)


class BaselineRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    version_number: int
    title: str
    status: str
    approved_by_actor_id: UUID | None
    approved_at: datetime | None
    created_at: datetime


class ForecastCreate(BaseModel):
    project_id: UUID
    phase_id: UUID | None = None
    forecast_type: str = Field(default="completion", max_length=32)
    predicted_date: date | None = None
    predicted_value: Decimal | None = None
    confidence: Decimal = Field(default=Decimal("0.5000"), ge=0, le=1)
    notes: str | None = None


class ForecastRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    phase_id: UUID | None
    forecast_type: str
    predicted_date: date | None
    predicted_value: Decimal | None
    confidence: Decimal
    notes: str | None
    created_at: datetime
