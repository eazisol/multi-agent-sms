"""Approval gate API schemas (MOD-330)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ApprovalStepSpec(BaseModel):
    role_code: str = Field(min_length=1, max_length=64)
    required_authority_level: int = Field(default=1, ge=1, le=10)
    assignee_actor_id: UUID | None = None
    order: int | None = Field(default=None, ge=1)


class ApprovalCreate(BaseModel):
    action_code: str = Field(min_length=3, max_length=128, pattern=r"^[a-z0-9_.]+$")
    title: str = Field(min_length=3, max_length=255)
    target_entity_type: str = Field(min_length=1, max_length=64)
    target_entity_id: UUID
    target_version: int = Field(ge=1)
    project_id: UUID | None = None
    workflow_code: str | None = Field(default=None, max_length=64)
    steps: list[ApprovalStepSpec] = Field(default_factory=list, max_length=20)
    recommendation_source_actor_id: UUID | None = None
    owner_actor_id: UUID | None = None


class ApprovalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    action_code: str
    title: str
    target_entity_type: str
    target_entity_id: UUID
    target_version: int
    workflow_code: str | None
    status: str
    current_step_order: int
    submitted_by_actor_id: UUID
    submitted_by_actor_kind: str
    recommendation_source_actor_id: UUID | None
    version: int
    superseded_by_id: UUID | None
    owner_actor_id: UUID
    created_at: datetime
    updated_at: datetime
    decided_at: datetime | None


class WorkflowRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    approval_id: UUID
    code: str
    title: str
    steps_json: list[Any]
    configuration_version_id: UUID | None
    created_at: datetime


class StepRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    approval_id: UUID
    step_order: int
    role_code: str
    required_authority_level: int
    status: str
    assignee_actor_id: UUID | None
    created_at: datetime


class DecisionCreate(BaseModel):
    decision: str = Field(pattern=r"^(approve|reject|withdraw)$")
    reason: str | None = None
    expected_version: int | None = None


class DecisionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    approval_id: UUID
    step_id: UUID
    decision: str
    actor_id: UUID
    actor_kind: str
    authority_mode: str
    delegation_id: UUID | None
    reason: str | None
    decided_at: datetime


class DelegationCreate(BaseModel):
    to_actor_id: UUID
    action_code: str = Field(min_length=3, max_length=128, pattern=r"^[a-z0-9_.*]+$")
    reason: str = Field(min_length=1)
    starts_at: datetime
    ends_at: datetime
    project_id: UUID | None = None


class DelegationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    from_actor_id: UUID
    to_actor_id: UUID
    action_code: str
    reason: str
    status: str
    starts_at: datetime
    ends_at: datetime
    created_at: datetime
    revoked_at: datetime | None


class EvidenceCreate(BaseModel):
    evidence_ref: str = Field(min_length=1, max_length=512)
    evidence_type: str = Field(default="reference", max_length=64)
    note: str | None = None


class EvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    approval_id: UUID
    evidence_type: str
    evidence_ref: str
    note: str | None
    created_by_actor_id: UUID
    created_at: datetime


class OverrideCreate(BaseModel):
    action_code: str = Field(min_length=3, max_length=128, pattern=r"^[a-z0-9_.]+$")
    target_entity_type: str = Field(min_length=1, max_length=64)
    target_entity_id: UUID
    target_version: int = Field(ge=1)
    reason: str = Field(min_length=1)
    authority_used: str = Field(min_length=1, max_length=128)
    project_id: UUID | None = None
    approval_id: UUID | None = None


class OverrideRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    approval_id: UUID | None
    action_code: str
    target_entity_type: str
    target_entity_id: UUID
    target_version: int
    reason: str
    authority_used: str
    retrospective_required: bool
    authorized_by_actor_id: UUID
    created_at: datetime


class GateCheckRequest(BaseModel):
    action_code: str = Field(min_length=3, max_length=128)
    target_entity_type: str = Field(min_length=1, max_length=64)
    target_entity_id: UUID
    target_version: int = Field(ge=1)


class GateCheckResponse(BaseModel):
    allowed: bool
    reason: str
    approval_id: UUID | None = None
    approval_status: str | None = None
