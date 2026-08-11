"""Notifications API schemas (MOD-440)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class NotificationCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    body: str = Field(min_length=1)
    recipient_actor_id: UUID
    notification_type: str = Field(min_length=1, max_length=64)
    channel: str = Field(default="in_app", max_length=32)
    priority: str = Field(default="normal", max_length=16)
    project_id: UUID | None = None
    related_entity_type: str | None = Field(default=None, max_length=64)
    related_entity_id: UUID | None = None
    scheduled_at: datetime | None = None
    idempotency_key: str | None = Field(default=None, max_length=128)


class NotificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    recipient_actor_id: UUID
    notification_type: str
    channel: str
    title: str
    body: str
    related_entity_type: str | None
    related_entity_id: UUID | None
    priority: str
    status: str
    scheduled_at: datetime | None
    sent_at: datetime | None
    delivered_at: datetime | None
    read_at: datetime | None
    failure_reason: str | None
    retry_count: int
    idempotency_key: str | None
    version: int
    created_at: datetime
    updated_at: datetime


class SimulateDeliver(BaseModel):
    succeed: bool = True
    error_message: str | None = None


class MarkRead(BaseModel):
    expected_version: int | None = None


class PreferenceUpsert(BaseModel):
    actor_id: UUID
    channel: str = Field(min_length=1, max_length=32)
    notification_type: str = Field(min_length=1, max_length=64)
    enabled: bool = True
    quiet_hours_start: str | None = Field(default=None, max_length=5)
    quiet_hours_end: str | None = Field(default=None, max_length=5)
    expected_version: int | None = None


class PreferenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    actor_id: UUID
    channel: str
    notification_type: str
    enabled: bool
    quiet_hours_start: str | None
    quiet_hours_end: str | None
    version: int
    updated_at: datetime
    created_at: datetime


class TemplateCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    channel: str = Field(min_length=1, max_length=32)
    subject: str = Field(min_length=1, max_length=255)
    body_template: str = Field(min_length=1)
    notification_type: str = Field(min_length=1, max_length=64)


class TemplateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    channel: str
    subject: str
    body_template: str
    notification_type: str
    version: int
    created_at: datetime
    updated_at: datetime


class DeliveryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    notification_id: UUID
    channel: str
    status: str
    attempt_number: int
    provider_ref: str | None
    error_message: str | None
    created_at: datetime


class DeadLetterRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    notification_id: UUID
    reason: str
    last_error: str | None
    attempt_count: int
    status: str
    replayed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class DigestCreate(BaseModel):
    recipient_actor_id: UUID
    channel: str = Field(default="email", max_length=32)
    window_start: datetime | None = None
    window_end: datetime | None = None
    summary: str | None = None
    item_count: int = 0


class DigestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    recipient_actor_id: UUID
    channel: str
    status: str
    window_start: datetime | None
    window_end: datetime | None
    item_count: int
    summary: str | None
    processed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class ProcessDigest(BaseModel):
    item_count: int | None = None
    summary: str | None = None
