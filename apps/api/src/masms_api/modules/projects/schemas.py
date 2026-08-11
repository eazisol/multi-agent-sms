"""Projects / SRS API schemas (MOD-240)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    code: str = Field(min_length=2, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    title: str = Field(min_length=2, max_length=255)
    client_id: UUID | None = None
    owner_actor_id: UUID | None = None


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    client_id: UUID | None
    code: str
    title: str
    status: str
    owner_actor_id: UUID
    created_at: datetime


class RequirementCreate(BaseModel):
    project_id: UUID
    requirement_code: str = Field(min_length=2, max_length=64)
    title: str = Field(min_length=2, max_length=255)


class RequirementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    requirement_code: str
    title: str
    status: str
    current_version_id: UUID | None
    created_at: datetime


class RequirementVersionCreate(BaseModel):
    requirement_id: UUID
    statement: str = Field(min_length=1)
    priority: str = Field(default="must_have", max_length=32)
    change_reason: str | None = None


class RequirementVersionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    requirement_id: UUID
    version_number: int
    statement: str
    priority: str
    status: str
    change_reason: str | None
    approved_by_actor_id: UUID | None
    approved_at: datetime | None
    created_at: datetime


class BusinessRuleCreate(BaseModel):
    requirement_version_id: UUID
    rule_code: str = Field(min_length=1, max_length=64)
    text: str = Field(min_length=1)


class BusinessRuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    requirement_version_id: UUID
    rule_code: str
    text: str
    created_at: datetime


class AcceptanceCriterionCreate(BaseModel):
    requirement_version_id: UUID
    criterion_code: str = Field(min_length=1, max_length=64)
    text: str = Field(min_length=1)


class AcceptanceCriterionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    requirement_version_id: UUID
    criterion_code: str
    text: str
    created_at: datetime


class AssumptionCreate(BaseModel):
    project_id: UUID
    assumption_code: str = Field(min_length=1, max_length=64)
    text: str = Field(min_length=1)
    requirement_version_id: UUID | None = None


class AssumptionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    requirement_version_id: UUID | None
    assumption_code: str
    text: str
    created_at: datetime


class ConstraintCreate(BaseModel):
    project_id: UUID
    constraint_code: str = Field(min_length=1, max_length=64)
    text: str = Field(min_length=1)
    requirement_version_id: UUID | None = None


class ConstraintRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    requirement_version_id: UUID | None
    constraint_code: str
    text: str
    created_at: datetime


class SrsBaselineCreate(BaseModel):
    project_id: UUID
    title: str = Field(min_length=2, max_length=255)
    summary: str = Field(min_length=1)
    requirement_version_ids: list[UUID] = Field(min_length=1)
    change_reason: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SrsBaselineRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    version_number: int
    title: str
    summary: str
    status: str
    requirement_version_ids: list[str]
    change_reason: str | None
    approved_by_actor_id: UUID | None
    approved_at: datetime | None
    created_at: datetime
