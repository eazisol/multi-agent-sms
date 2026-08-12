"""Gmail integration API schemas (MOD-510)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from masms_api.modules.gmail import domain


class ConnectionCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    email_address: str = Field(min_length=3, max_length=255)
    credential_ref: str | None = Field(default=None, max_length=255)
    scopes_json: str | None = None
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
    email_address: str
    credential_ref: str | None
    status: str
    scopes_json: str | None
    history_id: str | None
    owner_actor_id: UUID
    version: int
    created_by_actor_id: UUID
    updated_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class ConnectionTransition(BaseModel):
    expected_version: int | None = None


class HistoryCursorUpsert(BaseModel):
    connection_id: UUID
    cursor_key: str = Field(default=domain.DEFAULT_CURSOR_KEY, max_length=128)
    cursor_value: str = Field(min_length=1)


class HistoryCursorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connection_id: UUID
    cursor_key: str
    cursor_value: str
    updated_at: datetime


class InboundProcess(BaseModel):
    connection_id: UUID
    gmail_message_id: str = Field(min_length=1, max_length=128)
    gmail_thread_id: str = Field(min_length=1, max_length=128)
    subject: str = Field(default="", max_length=512)
    from_email: str = Field(min_length=3, max_length=255)
    snippet: str | None = None
    query_id: UUID | None = None
    client_id: UUID | None = None

    @model_validator(mode="before")
    @classmethod
    def reject_raw_secrets(cls, data: Any) -> Any:
        if isinstance(data, dict):
            domain.assert_no_raw_secrets(data)
        return data


class InboundProcessResult(BaseModel):
    thread_mapping_id: UUID
    message_mapping_id: UUID
    query_id: UUID
    internal_thread_id: UUID
    idempotent: bool = False


class PushReceive(BaseModel):
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


class PushReceiveResult(BaseModel):
    external_event_id: str
    event_type: str
    status: str
    inbound: InboundProcessResult | None = None
    idempotent: bool = False


class ThreadMappingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connection_id: UUID
    gmail_thread_id: str
    internal_thread_id: UUID
    query_id: UUID | None
    client_id: UUID | None
    created_at: datetime


class MessageMappingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connection_id: UUID
    gmail_message_id: str
    internal_message_id: UUID | None
    thread_mapping_id: UUID
    direction: str
    subject: str | None
    snippet: str | None
    status: str
    created_at: datetime


class AttachmentImportCreate(BaseModel):
    gmail_attachment_id: str = Field(min_length=1, max_length=128)
    file_name: str = Field(min_length=1, max_length=512)
    mime_type: str | None = Field(default=None, max_length=128)

    @model_validator(mode="before")
    @classmethod
    def reject_raw_secrets(cls, data: Any) -> Any:
        if isinstance(data, dict):
            domain.assert_no_raw_secrets(data)
        return data


class AttachmentImportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connection_id: UUID
    message_mapping_id: UUID
    gmail_attachment_id: str
    file_name: str
    mime_type: str | None
    storage_ref: str
    status: str
    created_at: datetime


class DraftCreate(BaseModel):
    connection_id: UUID
    thread_mapping_id: UUID | None = None
    to_addresses: str = Field(min_length=3)
    subject: str = Field(min_length=1, max_length=512)
    body_preview: str | None = None

    @model_validator(mode="before")
    @classmethod
    def reject_raw_secrets(cls, data: Any) -> Any:
        if isinstance(data, dict):
            domain.assert_no_raw_secrets(data)
        return data


class DraftRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connection_id: UUID
    draft_id: UUID
    thread_mapping_id: UUID | None
    to_addresses: str
    subject: str
    body_preview: str | None
    status: str
    reviewer_actor_id: UUID | None
    review_notes: str | None
    version: int
    created_by_actor_id: UUID
    updated_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class DraftReject(BaseModel):
    review_notes: str | None = None
    expected_version: int | None = None


class DraftTransition(BaseModel):
    expected_version: int | None = None


class ApprovedSendRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    connection_id: UUID
    draft_review_id: UUID
    message_mapping_id: UUID | None
    external_send_id: str
    status: str
    sent_at: datetime | None
    failure_reason: str | None
    created_by_actor_id: UUID
    created_at: datetime


class SendApprovedResult(BaseModel):
    approved_send: ApprovedSendRead
    message_mapping: MessageMappingRead
