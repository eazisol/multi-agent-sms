"""Bugs API schemas (MOD-410)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BugCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    project_id: UUID | None = None
    severity: str = Field(default="medium", max_length=16)
    blocks_release: bool | None = None
    links: list[LinkCreate] = Field(default_factory=list)


class BugRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    code: str
    title: str
    description: str | None
    severity: str
    status: str
    blocks_release: bool
    rejection_reason: str | None
    rejection_evidence: str | None
    reopen_reason: str | None
    owner_actor_id: UUID
    assignee_actor_id: UUID | None
    version: int
    created_at: datetime
    updated_at: datetime


class BugReject(BaseModel):
    reason: str = Field(min_length=1)
    evidence: str = Field(min_length=1)
    expected_version: int | None = None


class BugReopen(BaseModel):
    reason: str = Field(min_length=1)
    expected_version: int | None = None


class BugTransition(BaseModel):
    status: str = Field(min_length=1, max_length=32)
    expected_version: int | None = None
    reason: str | None = None


class LinkCreate(BaseModel):
    link_type: str = Field(min_length=1, max_length=32)
    linked_entity_id: UUID
    notes: str | None = None


class LinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    bug_id: UUID
    link_type: str
    linked_entity_id: UUID
    notes: str | None
    created_at: datetime


class AssignmentCreate(BaseModel):
    assignee_actor_id: UUID
    reason: str | None = None


class AssignmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    bug_id: UUID
    assignee_actor_id: UUID
    assigned_by_actor_id: UUID
    reason: str | None
    effective_from: datetime
    effective_to: datetime | None
    created_at: datetime


class FixCreate(BaseModel):
    summary: str = Field(min_length=1)
    build_ref: str | None = None
    expected_version: int | None = None


class FixRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    bug_id: UUID
    summary: str
    build_ref: str | None
    status: str
    submitted_by_actor_id: UUID
    created_at: datetime


class RetestCreate(BaseModel):
    result: str = Field(min_length=1, max_length=16)
    evidence_text: str | None = None
    environment_code: str = Field(default="local", max_length=64)
    build_ref: str | None = None
    fix_submission_id: UUID | None = None
    expected_version: int | None = None


class RetestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    bug_id: UUID
    fix_submission_id: UUID | None
    result: str
    evidence_text: str | None
    environment_code: str
    build_ref: str | None
    tested_by_actor_id: UUID
    created_at: datetime


class KnownIssueCreate(BaseModel):
    reason: str = Field(min_length=1)
    release_ref: str | None = None


class KnownIssueDecide(BaseModel):
    status: str = Field(min_length=1, max_length=32)
    expected_bug_version: int | None = None


class KnownIssueRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    bug_id: UUID
    reason: str
    release_ref: str | None
    status: str
    approved_by_actor_id: UUID | None
    created_by_actor_id: UUID
    created_at: datetime
    decided_at: datetime | None


class SeveritySlaUpsert(BaseModel):
    severity: str = Field(min_length=1, max_length=16)
    response_hours: int = Field(ge=1)
    resolve_hours: int = Field(ge=1)
    blocks_release: bool = False


class SeveritySlaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    severity: str
    response_hours: int
    resolve_hours: int
    blocks_release: bool
    created_at: datetime
    updated_at: datetime


class ReleaseGateResult(BaseModel):
    project_id: UUID | None
    release_allowed: bool
    blocking_bug_ids: list[UUID]
    blocking_codes: list[str]


class BugHistory(BaseModel):
    bug: BugRead
    links: list[LinkRead]
    assignments: list[AssignmentRead]
    fixes: list[FixRead]
    retests: list[RetestRead]
    known_issues: list[KnownIssueRead]


BugCreate.model_rebuild()
