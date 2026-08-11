"""Configuration API schemas (MOD-140)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ConfigurationVersionCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    change_reason: str | None = None
    based_on_version_id: UUID | None = None


class ConfigurationVersionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    version_number: int
    title: str
    status: str
    based_on_version_id: UUID | None
    change_reason: str | None
    approved_by_actor_id: UUID | None
    approved_at: datetime | None
    effective_at: datetime | None
    superseded_at: datetime | None
    rolled_back_at: datetime | None
    created_at: datetime


class WorkflowCreate(BaseModel):
    configuration_version_id: UUID
    code: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    title: str = Field(min_length=2, max_length=255)
    entity_type: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    description: str | None = None


class WorkflowRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    configuration_version_id: UUID
    code: str
    title: str
    entity_type: str
    status: str
    created_at: datetime


class StatusCreate(BaseModel):
    configuration_version_id: UUID
    workflow_definition_id: UUID
    code: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    title: str = Field(min_length=2, max_length=255)
    is_terminal: bool = False
    sort_order: int = 0


class StatusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    configuration_version_id: UUID
    workflow_definition_id: UUID
    code: str
    title: str
    is_terminal: bool
    sort_order: int
    status: str
    created_at: datetime


class TransitionCreate(BaseModel):
    configuration_version_id: UUID
    workflow_definition_id: UUID
    from_status_code: str = Field(min_length=2, max_length=64)
    to_status_code: str = Field(min_length=2, max_length=64)
    requires_reason: bool = False
    requires_approval: bool = False


class TransitionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    configuration_version_id: UUID
    workflow_definition_id: UUID
    from_status_code: str
    to_status_code: str
    requires_reason: bool
    requires_approval: bool
    status: str
    created_at: datetime


class FollowUpRuleCreate(BaseModel):
    configuration_version_id: UUID
    workflow_code: str = Field(min_length=2, max_length=64)
    trigger_status_code: str = Field(min_length=2, max_length=64)
    due_offset_hours: int = Field(default=24, ge=0, le=8760)
    required_response: str = Field(min_length=2, max_length=255)


class FollowUpRuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    configuration_version_id: UUID
    workflow_code: str
    trigger_status_code: str
    due_offset_hours: int
    required_response: str
    status: str
    created_at: datetime


class ReminderRuleCreate(BaseModel):
    configuration_version_id: UUID
    workflow_code: str = Field(min_length=2, max_length=64)
    offset_hours_before_due: int = Field(default=4, ge=0, le=8760)
    channel: str = Field(default="in_app", max_length=32)


class ReminderRuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    configuration_version_id: UUID
    workflow_code: str
    offset_hours_before_due: int
    channel: str
    status: str
    created_at: datetime


class EscalationRuleCreate(BaseModel):
    configuration_version_id: UUID
    workflow_code: str = Field(min_length=2, max_length=64)
    after_hours_overdue: int = Field(default=24, ge=0, le=8760)
    escalate_to_role_code: str = Field(min_length=2, max_length=64)


class EscalationRuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    configuration_version_id: UUID
    workflow_code: str
    after_hours_overdue: int
    escalate_to_role_code: str
    status: str
    created_at: datetime


class ApprovalWorkflowCreate(BaseModel):
    configuration_version_id: UUID
    code: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    title: str = Field(min_length=2, max_length=255)
    action_code: str = Field(min_length=3, max_length=128, pattern=r"^[a-z0-9_.]+$")
    steps: list[dict[str, Any]] = Field(default_factory=list)


class ApprovalWorkflowRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    configuration_version_id: UUID
    code: str
    title: str
    action_code: str
    steps_json: list[dict[str, Any]]
    status: str
    created_at: datetime


class LiveTransitionCheckRequest(BaseModel):
    workflow_code: str = Field(min_length=2, max_length=64)
    from_status_code: str = Field(min_length=2, max_length=64)
    to_status_code: str = Field(min_length=2, max_length=64)


class LiveTransitionCheckResponse(BaseModel):
    allowed: bool
    configuration_version_id: UUID | None
    configuration_status: str | None
    reason: str
