"""Integration framework API schemas (MOD-500)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from masms_api.modules.integrations import domain


class ConnectionCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    provider: str = Field(min_length=1, max_length=32)
    auth_type: str = Field(default="oauth2", max_length=16)
    credential_ref: str | None = Field(default=None, max_length=255)
    scopes_json: str | None = None
    metadata_json: str | None = None
    owner_actor_id: UUID | None = None

    @model_validator(mode="before")
    @classmethod
    def reject_raw_secrets(cls, data: Any) -> Any:
        if isinstance(data, dict):
            domain.assert_no_raw_secrets(data)
        return data


class ConnectionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    provider: str
    auth_type: str
    status: str
    credential_ref: str | None
    scopes_json: str | None
    metadata_json: str | None
    owner_actor_id: UUID
    version: int
    created_by_actor_id: UUID
    updated_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class ConnectionTransition(BaseModel):
    expected_version: int | None = None


class WebhookReceive(BaseModel):
    connection_id: UUID
    external_event_id: str = Field(min_length=1, max_length=128)
    event_type: str = Field(min_length=1, max_length=64)
    payload: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def reject_raw_secrets(cls, data: Any) -> Any:
        if isinstance(data, dict):
            domain.assert_no_raw_secrets(data)
        return data


class WebhookEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connection_id: UUID
    external_event_id: str
    event_type: str
    payload_json: str | None
    status: str
    failure_reason: str | None
    received_at: datetime
    processed_at: datetime | None
    created_at: datetime


class SyncCursorUpsert(BaseModel):
    connection_id: UUID
    stream_key: str = Field(min_length=1, max_length=128)
    cursor_value: str = Field(min_length=1)


class SyncCursorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connection_id: UUID
    stream_key: str
    cursor_value: str
    updated_at: datetime


class ExternalMappingCreate(BaseModel):
    connection_id: UUID
    internal_entity_type: str = Field(min_length=1, max_length=64)
    internal_entity_id: str = Field(min_length=1, max_length=128)
    external_entity_type: str = Field(min_length=1, max_length=64)
    external_entity_id: str = Field(min_length=1, max_length=128)


class ExternalMappingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connection_id: UUID
    internal_entity_type: str
    internal_entity_id: str
    external_entity_type: str
    external_entity_id: str
    created_at: datetime


class IntegrationOutboxCreate(BaseModel):
    connection_id: UUID
    event_type: str = Field(min_length=1, max_length=64)
    payload: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def reject_raw_secrets(cls, data: Any) -> Any:
        if isinstance(data, dict):
            domain.assert_no_raw_secrets(data)
        return data


class IntegrationOutboxRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connection_id: UUID
    event_type: str
    payload_json: str | None
    status: str
    attempt_count: int
    last_error: str | None
    created_at: datetime
    sent_at: datetime | None


class OutboxRelayRequest(BaseModel):
    force_fail: bool = False


class InboxReceive(BaseModel):
    connection_id: UUID
    external_event_id: str = Field(min_length=1, max_length=128)
    event_type: str = Field(min_length=1, max_length=64)
    payload: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def reject_raw_secrets(cls, data: Any) -> Any:
        if isinstance(data, dict):
            domain.assert_no_raw_secrets(data)
        return data


class InboxEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connection_id: UUID
    external_event_id: str
    event_type: str
    payload_json: str | None
    status: str
    failure_reason: str | None
    created_at: datetime
    processed_at: datetime | None


class InboxProcessRequest(BaseModel):
    force_fail: bool = False


class ConnectionHealthRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connection_id: UUID
    health_status: str
    last_success_at: datetime | None
    last_failure_at: datetime | None
    failure_count: int
    last_error: str | None
    checked_at: datetime
    updated_at: datetime


class ConnectionHealthRecord(BaseModel):
    health_status: str = Field(default="healthy", max_length=32)
    last_error: str | None = None
