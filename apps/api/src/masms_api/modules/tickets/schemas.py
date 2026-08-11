"""Ticket API schemas (MOD-300)."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TicketCreate(BaseModel):
    project_id: UUID
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=2, max_length=255)
    description: str | None = None
    ticket_type: str = Field(default="story", max_length=32)
    priority: str = Field(default="medium", max_length=32)
    phase_id: UUID | None = None
    owner_actor_id: UUID | None = None
    queue_code: str | None = Field(default=None, max_length=64)
    estimate_points: Decimal | None = None
    acceptance_criteria: str | None = None
    definition_of_done: str | None = None
    requirement_id: UUID | None = None
    requirement_version_id: UUID | None = None


class TicketRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    phase_id: UUID | None
    code: str
    title: str
    description: str | None
    ticket_type: str
    status: str
    priority: str
    owner_actor_id: UUID | None
    queue_code: str | None
    estimate_points: Decimal | None
    acceptance_criteria: str | None
    definition_of_done: str | None
    blocked_reason: str | None
    version: int
    completed_at: datetime | None
    reopen_reason: str | None
    reopen_evidence_id: UUID | None
    reopened_by_actor_id: UUID | None
    reopened_at: datetime | None
    created_at: datetime
    updated_at: datetime


class TicketUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = None
    priority: str | None = Field(default=None, max_length=32)
    phase_id: UUID | None = None
    owner_actor_id: UUID | None = None
    queue_code: str | None = Field(default=None, max_length=64)
    estimate_points: Decimal | None = None
    acceptance_criteria: str | None = None
    definition_of_done: str | None = None
    expected_version: int


class TransitionRequest(BaseModel):
    next_status: str = Field(min_length=1, max_length=32)
    reason: str | None = None
    blocked_reason: str | None = None
    expected_version: int


class ReopenRequest(BaseModel):
    reason: str = Field(min_length=2)
    evidence_id: UUID
    next_status: str = Field(default="in_progress", max_length=32)
    expected_version: int


class SubtaskCreate(BaseModel):
    ticket_id: UUID
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=2, max_length=255)
    owner_actor_id: UUID | None = None
    sequence: int = Field(default=1, ge=1)


class SubtaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    ticket_id: UUID
    code: str
    title: str
    status: str
    owner_actor_id: UUID | None
    sequence: int
    created_at: datetime


class TicketDependencyCreate(BaseModel):
    project_id: UUID
    predecessor_ticket_id: UUID
    successor_ticket_id: UUID
    dependency_type: str = Field(default="finish_to_start", max_length=32)


class TicketDependencyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    predecessor_ticket_id: UUID
    successor_ticket_id: UUID
    dependency_type: str
    created_at: datetime


class RequirementLinkCreate(BaseModel):
    ticket_id: UUID
    requirement_id: UUID
    requirement_version_id: UUID | None = None


class RequirementLinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    ticket_id: UUID
    requirement_id: UUID
    requirement_version_id: UUID | None
    created_at: datetime


class EvidenceCreate(BaseModel):
    ticket_id: UUID
    evidence_type: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=2, max_length=255)
    uri_or_ref: str | None = Field(default=None, max_length=1024)
    summary: str | None = None


class EvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    ticket_id: UUID
    evidence_type: str
    title: str
    uri_or_ref: str | None
    summary: str | None
    created_at: datetime


class CheckCreate(BaseModel):
    ticket_id: UUID
    check_code: str = Field(min_length=1, max_length=64)
    label: str = Field(min_length=2, max_length=255)
    is_required: bool = True


class CheckRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    ticket_id: UUID
    check_code: str
    label: str
    is_required: bool
    is_satisfied: bool
    notes: str | None
    satisfied_by_actor_id: UUID | None
    satisfied_at: datetime | None
    created_at: datetime


class CheckSatisfy(BaseModel):
    notes: str | None = None
