"""Change-control API schemas (MOD-420)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RiskCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    project_id: UUID | None = None
    risk_level: str = Field(default="medium", max_length=16)


class RiskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    code: str
    title: str
    description: str | None
    risk_level: str
    status: str
    owner_actor_id: UUID
    version: int
    created_at: datetime
    updated_at: datetime


class RiskReviewCreate(BaseModel):
    outcome: str = Field(min_length=1, max_length=32)
    notes: str | None = None
    expected_version: int | None = None


class RiskReviewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    risk_id: UUID
    outcome: str
    notes: str | None
    reviewed_by_actor_id: UUID
    created_at: datetime


class ChangeRequestCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    project_id: UUID | None = None
    change_type: str = Field(default="scope", max_length=64)
    rationale: str | None = None


class ChangeRequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    code: str
    title: str
    description: str | None
    change_type: str
    status: str
    rationale: str | None
    decision_evidence: str | None
    owner_actor_id: UUID
    version: int
    created_at: datetime
    updated_at: datetime


class ImpactCreate(BaseModel):
    summary: str = Field(min_length=1)
    affected_areas: list[str] = Field(default_factory=list)
    estimated_effort_hours: int | None = Field(default=None, ge=0)
    expected_version: int | None = None


class ImpactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    change_request_id: UUID
    summary: str
    affected_areas: list[Any]
    estimated_effort_hours: int | None
    created_by_actor_id: UUID
    created_at: datetime


class SubmitForApproval(BaseModel):
    expected_version: int | None = None


class ApprovalCreate(BaseModel):
    decision: str = Field(min_length=1, max_length=32)
    rationale: str = Field(min_length=1)
    evidence: str | None = None
    expected_version: int | None = None


class ApprovalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    change_request_id: UUID
    decision: str
    rationale: str
    evidence: str | None
    decided_by_actor_id: UUID
    created_at: datetime


class BaselineUpdateCreate(BaseModel):
    artifact_type: str = Field(min_length=1, max_length=64)
    artifact_id: UUID
    from_version: int | None = None
    to_version: int = Field(ge=1)
    ticket_id: UUID | None = None
    notes: str | None = None


class BaselineUpdateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    change_request_id: UUID
    artifact_type: str
    artifact_id: UUID
    from_version: int | None
    to_version: int
    ticket_id: UUID | None
    notes: str | None
    created_by_actor_id: UUID
    created_at: datetime


class DevelopmentGateResult(BaseModel):
    change_request_id: UUID
    status: str
    allowed: bool
    reason: str
