"""Orchestrator API schemas (MOD-350)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DefinitionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    description: str | None
    status: str
    created_at: datetime


class VersionCreate(BaseModel):
    definition_json: dict[str, Any] = Field(default_factory=dict)
    temporal_workflow_type: str | None = Field(default=None, max_length=128)


class VersionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    definition_id: UUID
    version_number: int
    status: str
    definition_json: dict[str, Any]
    temporal_workflow_type: str
    created_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class InstanceCreate(BaseModel):
    workflow_code: str = Field(min_length=1, max_length=64)
    related_entity_type: str = Field(min_length=1, max_length=64)
    related_entity_id: UUID
    project_id: UUID | None = None
    owner_actor_id: UUID | None = None
    input_json: dict[str, Any] = Field(default_factory=dict)
    workflow_version_id: UUID | None = None


class InstanceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    workflow_code: str
    workflow_version_id: UUID
    related_entity_type: str
    related_entity_id: UUID
    status: str
    temporal_run_id: str | None
    temporal_workflow_id: str | None
    owner_actor_id: UUID
    correlation_id: UUID
    input_json: dict[str, Any]
    version: int
    created_at: datetime
    updated_at: datetime
    closed_at: datetime | None


class SignalCreate(BaseModel):
    signal_name: str = Field(min_length=1, max_length=128)
    payload_json: dict[str, Any] = Field(default_factory=dict)
    idempotency_key: str = Field(min_length=1, max_length=128)


class SignalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    instance_id: UUID
    signal_name: str
    payload_json: dict[str, Any]
    idempotency_key: str
    status: str
    actor_id: UUID
    created_at: datetime


class FailureCreate(BaseModel):
    failure_code: str = Field(min_length=1, max_length=64)
    message: str = Field(min_length=1)
    retryable: bool = True
    attempt: int = Field(default=1, ge=1)
    details_json: dict[str, Any] = Field(default_factory=dict)
    mark_instance_failed: bool = True
    expected_version: int | None = None


class FailureRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    instance_id: UUID
    failure_code: str
    message: str
    retryable: bool
    attempt: int
    details_json: dict[str, Any]
    created_at: datetime


class InterventionCreate(BaseModel):
    reason: str = Field(min_length=1)
    action_code: str = Field(min_length=1, max_length=64)
    notes: str | None = None


class InterventionResolve(BaseModel):
    notes: str | None = None
    expected_version: int | None = None


class InterventionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    instance_id: UUID
    reason: str
    action_code: str
    notes: str | None
    status: str
    decided_by_actor_id: UUID | None
    created_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None
