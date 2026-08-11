"""Status engine API schemas (MOD-320)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class WorkflowBindingCreate(BaseModel):
    entity_type: str = Field(min_length=1, max_length=64)
    workflow_code: str = Field(min_length=1, max_length=64)
    project_id: UUID | None = None
    priority: int = Field(default=100, ge=0, le=10_000)


class WorkflowBindingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    entity_type: str
    project_id: UUID | None
    workflow_code: str
    priority: int
    status: str
    created_by_actor_id: UUID
    created_at: datetime


class EntityStateInit(BaseModel):
    entity_type: str = Field(min_length=1, max_length=64)
    entity_id: UUID
    project_id: UUID | None = None
    initial_status_code: str = Field(min_length=1, max_length=64)
    workflow_code: str | None = Field(default=None, max_length=64)


class EntityStateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    entity_type: str
    entity_id: UUID
    project_id: UUID | None
    workflow_code: str
    status_code: str
    configuration_version_id: UUID | None
    version: int
    on_hold: bool
    updated_by_actor_id: UUID
    updated_at: datetime
    created_at: datetime


class TransitionApply(BaseModel):
    entity_type: str = Field(min_length=1, max_length=64)
    entity_id: UUID
    to_status_code: str = Field(min_length=1, max_length=64)
    reason: str | None = None
    evidence_ref: str | None = Field(default=None, max_length=512)
    approval_id: UUID | None = None
    expected_version: int | None = None
    fields: dict[str, Any] = Field(default_factory=dict)


class StatusHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    entity_type: str
    entity_id: UUID
    project_id: UUID | None
    workflow_code: str
    from_status_code: str
    to_status_code: str
    reason: str | None
    evidence_ref: str | None
    approval_id: UUID | None
    actor_id: UUID
    actor_kind: str
    rule_id: UUID | None
    payload_json: dict[str, Any]
    recorded_at: datetime


class AvailableAction(BaseModel):
    to_status_code: str
    requires_reason: bool
    requires_approval: bool
    rule_id: UUID


class AvailableActionsRead(BaseModel):
    entity_type: str
    entity_id: UUID
    workflow_code: str
    status_code: str
    on_hold: bool
    actions: list[AvailableAction]


class HoldCreate(BaseModel):
    entity_type: str = Field(min_length=1, max_length=64)
    entity_id: UUID
    reason: str = Field(min_length=1)
    responsible_actor_id: UUID | None = None
    due_at: datetime | None = None


class HoldRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    entity_type: str
    entity_id: UUID
    project_id: UUID | None
    status_code_at_hold: str
    reason: str
    responsible_actor_id: UUID
    due_at: datetime | None
    status: str
    created_by_actor_id: UUID
    created_at: datetime
    released_at: datetime | None
    released_by_actor_id: UUID | None


class HoldRelease(BaseModel):
    note: str | None = None


class ReopenApply(BaseModel):
    entity_type: str = Field(min_length=1, max_length=64)
    entity_id: UUID
    to_status_code: str = Field(min_length=1, max_length=64)
    reason: str = Field(min_length=1)
    evidence_ref: str | None = Field(default=None, max_length=512)
    expected_version: int | None = None


class ReopenRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    entity_type: str
    entity_id: UUID
    project_id: UUID | None
    from_status_code: str
    to_status_code: str
    reason: str
    evidence_ref: str | None
    authorized_by_actor_id: UUID
    created_at: datetime


class ResolveWorkflowRead(BaseModel):
    entity_type: str
    project_id: UUID | None
    workflow_code: str
    binding_id: UUID | None
    configuration_version_id: UUID | None
