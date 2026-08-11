"""Query API schemas (MOD-210)."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class QuerySourceCreate(BaseModel):
    code: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    title: str = Field(min_length=2, max_length=255)
    channel: str = Field(default="email", max_length=64)


class QuerySourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    channel: str
    status: str
    created_at: datetime


class ClientQueryCreate(BaseModel):
    subject: str = Field(min_length=3, max_length=255)
    summary: str = Field(min_length=3)
    original_message: str | None = None
    client_id: UUID | None = None
    contact_id: UUID | None = None
    source_id: UUID | None = None
    owner_actor_id: UUID | None = None
    sla_hours: int = Field(default=24, ge=1, le=720)


class ClientQueryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    client_id: UUID | None
    contact_id: UUID | None
    project_id: UUID | None
    source_id: UUID | None
    subject: str
    summary: str
    status: str
    owner_actor_id: UUID
    classification: str | None
    sla_due_at: datetime | None
    first_responded_at: datetime | None
    sla_status: str
    opportunity_id: UUID | None
    version: int
    created_at: datetime


class QueryTransitionRequest(BaseModel):
    next_status: str = Field(min_length=2, max_length=32)
    reason: str | None = None
    classification: str | None = None
    rule_code: str | None = None


class FirstResponseRequest(BaseModel):
    responded_at: datetime | None = None
    note: str | None = None


class QualificationAnswerCreate(BaseModel):
    query_id: UUID
    question_key: str = Field(min_length=2, max_length=128, pattern=r"^[a-z0-9_]+$")
    question_text: str = Field(min_length=3, max_length=512)
    answer_text: str = Field(min_length=1)
    rationale: str | None = None


class QualificationAnswerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    query_id: UUID
    question_key: str
    question_text: str
    answer_text: str
    rationale: str | None
    answered_by_actor_id: UUID
    created_at: datetime


class ConvertQueryRequest(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    estimated_value: Decimal | None = None
    currency: str = Field(default="USD", min_length=3, max_length=3)
    conversion_notes: str | None = None


class OpportunityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    query_id: UUID
    client_id: UUID | None
    title: str
    status: str
    estimated_value: Decimal | None
    currency: str
    owner_actor_id: UUID
    conversion_notes: str | None
    version: int
    created_at: datetime


class QueryStatusHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    query_id: UUID
    previous_status: str
    next_status: str
    actor_id: UUID
    reason: str | None
    rule_code: str | None
    evidence_json: dict[str, Any]
    created_at: datetime
