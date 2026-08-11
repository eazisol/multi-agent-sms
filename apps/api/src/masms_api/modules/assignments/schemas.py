"""Assignment API schemas (MOD-310)."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AssignmentCreate(BaseModel):
    ticket_id: UUID
    assignee_actor_id: UUID
    role_code: str = Field(default="developer", max_length=64)
    required_skill_code: str | None = Field(default=None, max_length=64)
    min_proficiency: int = Field(default=1, ge=1, le=5)
    allocation_pct: Decimal = Field(default=Decimal("25.00"), gt=0, le=100)
    allow_override: bool = False
    override_reason: str | None = None
    recommendation_id: UUID | None = None


class AssignmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    ticket_id: UUID
    assignee_actor_id: UUID
    role_code: str
    status: str
    required_skill_code: str | None
    min_proficiency: int
    override_reason: str | None
    is_override: bool
    recommendation_id: UUID | None
    assigned_by_actor_id: UUID
    version: int
    created_at: datetime
    closed_at: datetime | None


class RecommendRequest(BaseModel):
    ticket_id: UUID
    candidate_actor_ids: list[UUID] = Field(min_length=1, max_length=50)
    required_skill_code: str | None = Field(default=None, max_length=64)
    min_proficiency: int = Field(default=1, ge=1, le=5)


class RecommendationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    ticket_id: UUID
    candidate_actor_id: UUID
    score: Decimal
    rank: int
    eligible: bool
    reasons_json: list[object]
    remaining_capacity_pct: Decimal | None
    status: str
    created_at: datetime


class AcknowledgeRequest(BaseModel):
    note: str | None = None
    decline: bool = False


class AcknowledgmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    assignment_id: UUID
    actor_id: UUID
    status: str
    note: str | None
    acknowledged_at: datetime


class ReassignRequest(BaseModel):
    new_assignee_actor_id: UUID
    reason: str = Field(min_length=2)
    role_code: str = Field(default="developer", max_length=64)
    required_skill_code: str | None = Field(default=None, max_length=64)
    min_proficiency: int = Field(default=1, ge=1, le=5)
    allocation_pct: Decimal = Field(default=Decimal("25.00"), gt=0, le=100)
    allow_override: bool = False
    override_reason: str | None = None
    expected_version: int


class AllocationHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    ticket_id: UUID
    assignment_id: UUID
    actor_id: UUID
    allocation_pct: Decimal
    event_type: str
    reason: str | None
    recorded_by_actor_id: UUID
    recorded_at: datetime


class ReassignmentHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    ticket_id: UUID
    from_assignment_id: UUID | None
    to_assignment_id: UUID
    from_actor_id: UUID | None
    to_actor_id: UUID
    reason: str
    is_override: bool
    recorded_by_actor_id: UUID
    recorded_at: datetime
