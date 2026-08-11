"""Client API schemas (MOD-200)."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ClientCreate(BaseModel):
    code: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_-]+$")
    legal_name: str = Field(min_length=2, max_length=255)
    trading_name: str | None = None
    owner_actor_id: UUID | None = None
    industry: str | None = None
    website: str | None = None
    notes: str | None = None


class ClientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    legal_name: str
    trading_name: str | None
    status: str
    owner_actor_id: UUID
    industry: str | None
    website: str | None
    version: int
    created_at: datetime


class ContactCreate(BaseModel):
    client_id: UUID
    full_name: str = Field(min_length=2, max_length=255)
    email: str = Field(min_length=3, max_length=320, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    phone: str | None = None
    job_title: str | None = None
    authority_level: str = Field(default="general", max_length=64)
    is_primary: bool = False


class ContactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    client_id: UUID
    full_name: str
    email: str
    phone: str | None
    job_title: str | None
    authority_level: str
    is_primary: bool
    status: str
    version: int
    created_at: datetime


class ProjectContactCreate(BaseModel):
    client_id: UUID
    project_id: UUID
    contact_id: UUID
    role_label: str = Field(default="contact", max_length=64)


class ProjectContactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    client_id: UUID
    project_id: UUID
    contact_id: UUID
    role_label: str
    status: str
    created_at: datetime


class CommunicationPreferenceCreate(BaseModel):
    contact_id: UUID
    channel: str = Field(min_length=2, max_length=32, pattern=r"^[a-z0-9_]+$")
    opted_in: bool = True
    quiet_hours_start: str | None = None
    quiet_hours_end: str | None = None
    timezone: str = Field(default="UTC", max_length=64)


class CommunicationPreferenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    contact_id: UUID
    channel: str
    opted_in: bool
    quiet_hours_start: str | None
    quiet_hours_end: str | None
    timezone: str
    status: str
    created_at: datetime


class DuplicateSuggestionCreate(BaseModel):
    left_client_id: UUID
    right_client_id: UUID
    score: float = Field(ge=0, le=100)
    reason: str = Field(min_length=3, max_length=255)


class DuplicateSuggestionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    left_client_id: UUID
    right_client_id: UUID
    score: Decimal
    reason: str
    status: str
    created_at: datetime
    resolved_at: datetime | None


class MergeClientsRequest(BaseModel):
    surviving_client_id: UUID
    merged_client_id: UUID
    duplicate_suggestion_id: UUID | None = None
    reason: str = Field(min_length=3, max_length=255)


class MergeHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    surviving_client_id: UUID
    merged_client_id: UUID
    duplicate_suggestion_id: UUID | None
    merged_snapshot: dict[str, Any]
    reason: str
    merged_by_actor_id: UUID
    created_at: datetime
