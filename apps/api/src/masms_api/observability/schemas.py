"""Observability query schemas and read APIs."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from masms_api.kernel.pagination import PageMeta


class AuditLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    actor_id: UUID
    actor_kind: str
    action: str
    entity_type: str
    entity_id: UUID
    entity_version: int | None
    correlation_id: UUID
    payload_redacted: dict[str, Any]
    created_at: datetime


class ActivityEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    activity_type: str
    summary: str
    actor_id: UUID
    correlation_id: UUID
    created_at: datetime


class StatusHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    entity_type: str
    entity_id: UUID
    previous_status: str | None
    next_status: str
    actor_id: UUID
    correlation_id: UUID
    created_at: datetime


class AgentRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    agent_name: str
    status: str
    actor_id: UUID
    correlation_id: UUID
    started_at: datetime
    finished_at: datetime | None


class IntegrationEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    provider: str
    direction: str
    event_type: str
    status: str
    correlation_id: UUID
    created_at: datetime


class AuditLogPage(BaseModel):
    items: list[AuditLogRead]
    page: PageMeta


class ActivityEventPage(BaseModel):
    items: list[ActivityEventRead]
    page: PageMeta


class AgentRunCreate(BaseModel):
    agent_name: str = Field(min_length=2, max_length=128)
    input_summary: dict[str, Any] = Field(default_factory=dict)


class AgentRunFinish(BaseModel):
    status: str = Field(min_length=2, max_length=32)
    output_summary: dict[str, Any] = Field(default_factory=dict)
    error_summary: str | None = None
