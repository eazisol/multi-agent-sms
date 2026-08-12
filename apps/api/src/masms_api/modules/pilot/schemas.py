"""API schemas for MOD-630 controlled pilot and production sign-off records."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PilotPlanCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    status: str = Field(default="draft", min_length=1, max_length=32)
    start_at: datetime | None = None
    end_at: datetime | None = None
    owner_actor_id: UUID | None = None


class PilotPlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    status: str
    start_at: datetime | None
    end_at: datetime | None
    version: int
    owner_actor_id: UUID
    created_by_actor_id: UUID
    updated_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class PilotUserCreate(BaseModel):
    actor_id: UUID
    role_label: str = Field(min_length=1, max_length=128)


class PilotUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    plan_id: UUID
    actor_id: UUID
    role_label: str
    approved_production_use: bool
    approved_at: datetime | None
    created_by_actor_id: UUID
    created_at: datetime


class TrainingRecordCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    audience: str = Field(min_length=1, max_length=255)
    status: str = Field(default="planned", min_length=1, max_length=32)


class TrainingRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    plan_id: UUID
    title: str
    audience: str
    status: str
    completed_at: datetime | None
    created_by_actor_id: UUID
    created_at: datetime


class SupportReadinessCreate(BaseModel):
    checklist_item: str = Field(min_length=1, max_length=255)
    ready: bool = False
    notes: str | None = None


class SupportReadinessRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    plan_id: UUID
    checklist_item: str
    ready: bool
    notes: str | None
    created_by_actor_id: UUID
    created_at: datetime


class KnownLimitationCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    summary: str = Field(min_length=1)
    severity: str = Field(min_length=1, max_length=32)
    status: str = Field(default="open", min_length=1, max_length=32)


class KnownLimitationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    plan_id: UUID
    code: str
    summary: str
    severity: str
    status: str
    created_by_actor_id: UUID
    created_at: datetime


class AcceptanceTestCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    severity: str = Field(min_length=1, max_length=32)
    result: str = Field(min_length=1, max_length=32)


class AcceptanceTestResultUpdate(BaseModel):
    result: str = Field(min_length=1, max_length=32)


class AcceptanceTestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    plan_id: UUID
    code: str
    title: str
    severity: str
    result: str
    created_by_actor_id: UUID
    created_at: datetime


class FinalSignoffCreate(BaseModel):
    plan_id: UUID
    function_code: str = Field(min_length=1, max_length=32)
    evidence: str = Field(default="")


class FinalSignoffSign(BaseModel):
    evidence: str = Field(min_length=1)


class FinalSignoffRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    plan_id: UUID
    function_code: str
    status: str
    evidence: str
    signed_by_actor_id: UUID | None
    signed_at: datetime | None
    created_by_actor_id: UUID
    created_at: datetime


class ProductionDeploymentCreate(BaseModel):
    plan_id: UUID
    human_approval_evidence: str = Field(min_length=0)
    environment: str = Field(default="production", min_length=1, max_length=32)


class ProductionDeploymentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    plan_id: UUID
    environment: str
    status: str
    human_approval_evidence: str
    created_by_actor_id: UUID
    created_at: datetime


class RollbackCreate(BaseModel):
    reason: str = Field(min_length=1)


class RollbackRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    deployment_id: UUID
    reason: str
    status: str
    created_by_actor_id: UUID
    created_at: datetime


class AcceptanceGateRead(BaseModel):
    plan_id: UUID
    critical_high_failed_count: int
    gate_passed: bool


class PilotApprovalGateRead(BaseModel):
    plan_id: UUID
    registered_count: int
    approved_count: int
    pending_count: int
    gate_passed: bool


class ReadinessGateRead(BaseModel):
    plan_id: UUID
    required_functions: list[str]
    signed_functions: list[str]
    gate_passed: bool
