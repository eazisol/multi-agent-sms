"""Comms API schemas (MOD-220)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ConversationCreate(BaseModel):
    subject: str = Field(min_length=2, max_length=255)
    related_entity_type: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    related_entity_id: UUID
    channel: str = Field(default="email", max_length=32)
    direction: str = Field(default="external", max_length=16)
    classification: str = Field(default="internal", max_length=32)
    client_id: UUID | None = None
    project_id: UUID | None = None


class ConversationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    client_id: UUID | None
    project_id: UUID | None
    subject: str
    channel: str
    direction: str
    related_entity_type: str
    related_entity_id: UUID
    status: str
    classification: str
    created_at: datetime


class MessageCreate(BaseModel):
    conversation_id: UUID
    body: str = Field(min_length=1)
    classification: str | None = None


class MessageUpdateBody(BaseModel):
    body: str = Field(min_length=1)


class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    conversation_id: UUID
    sender_actor_id: UUID
    body: str
    status: str
    classification: str
    requires_approval: bool
    approved_by_actor_id: UUID | None
    approved_at: datetime | None
    sent_at: datetime | None
    revision_number: int
    created_at: datetime


class MessageRevisionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    message_id: UUID
    revision_number: int
    body: str
    edited_by_actor_id: UUID
    created_at: datetime


class RecipientCreate(BaseModel):
    message_id: UUID
    address: str = Field(min_length=3, max_length=320)
    role: str = Field(default="to", max_length=16)
    actor_id: UUID | None = None
    contact_id: UUID | None = None


class RecipientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    message_id: UUID
    role: str
    address: str
    actor_id: UUID | None
    contact_id: UUID | None
    created_at: datetime


class DeliveryReceiptCreate(BaseModel):
    message_id: UUID
    recipient_id: UUID
    status: str = Field(default="queued", max_length=32)
    provider_ref: str | None = None
    detail: str | None = None


class DeliveryReceiptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    message_id: UUID
    recipient_id: UUID
    status: str
    provider_ref: str | None
    detail: str | None
    created_at: datetime
    updated_at: datetime


class AttachmentLinkCreate(BaseModel):
    message_id: UUID
    file_ref: str = Field(min_length=2, max_length=512)
    filename: str = Field(min_length=1, max_length=255)
    content_type: str = Field(default="application/octet-stream", max_length=128)
    size_bytes: int = Field(default=0, ge=0)
    classification: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AttachmentLinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    message_id: UUID
    file_ref: str
    filename: str
    content_type: str
    size_bytes: int
    classification: str
    created_at: datetime
