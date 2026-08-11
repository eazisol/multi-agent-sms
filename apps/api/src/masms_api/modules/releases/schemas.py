"""Releases API schemas (MOD-430)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ReleaseCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    project_id: UUID | None = None
    version_label: str = Field(default="0.1.0", max_length=64)
    items: list["ReleaseItemCreate"] = Field(default_factory=list)


class ReleaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    code: str
    title: str
    description: str | None
    status: str
    version_label: str
    approval_evidence: str | None
    approved_by_actor_id: UUID | None
    approved_at: datetime | None
    owner_actor_id: UUID
    version: int
    created_at: datetime
    updated_at: datetime


class ReleaseItemCreate(BaseModel):
    link_type: str = Field(min_length=1, max_length=32)
    linked_entity_id: UUID
    notes: str | None = None


class ReleaseItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    release_id: UUID
    link_type: str
    linked_entity_id: UUID
    notes: str | None
    created_at: datetime


class SubmitApproval(BaseModel):
    expected_version: int | None = None


class ApproveRelease(BaseModel):
    evidence: str = Field(min_length=1)
    expected_version: int | None = None


class DeploymentCreate(BaseModel):
    environment_code: str = Field(min_length=1, max_length=64)
    build_ref: str | None = None
    expected_version: int | None = None


class DeploymentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    release_id: UUID
    environment_code: str
    status: str
    build_ref: str | None
    requested_by_actor_id: UUID
    started_at: datetime | None
    finished_at: datetime | None
    created_at: datetime


class DeploymentCheckCreate(BaseModel):
    check_name: str = Field(min_length=1, max_length=128)
    result: str = Field(min_length=1, max_length=16)
    evidence: str | None = None


class DeploymentCheckRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    deployment_id: UUID
    check_name: str
    result: str
    evidence: str | None
    created_at: datetime


class BackupCreate(BaseModel):
    backup_ref: str = Field(min_length=1, max_length=255)
    confirmed: bool = True
    notes: str | None = None


class BackupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    release_id: UUID
    backup_ref: str
    confirmed: bool
    notes: str | None
    confirmed_by_actor_id: UUID
    created_at: datetime


class MigrationPlanCreate(BaseModel):
    plan_text: str = Field(min_length=1)
    alembic_revision: str | None = None


class MigrationPlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    release_id: UUID
    plan_text: str
    alembic_revision: str | None
    created_by_actor_id: UUID
    created_at: datetime


class RollbackCreate(BaseModel):
    reason: str = Field(min_length=1)
    evidence: str | None = None
    deployment_id: UUID | None = None
    expected_version: int | None = None


class RollbackRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    release_id: UUID
    deployment_id: UUID | None
    reason: str
    evidence: str | None
    created_by_actor_id: UUID
    created_at: datetime


class CompletionReportCreate(BaseModel):
    summary: str = Field(min_length=1)
    client_accepted: bool = False
    internal_accepted: bool = False
    client_acceptance_notes: str | None = None
    internal_acceptance_notes: str | None = None
    expected_version: int | None = None


class CompletionReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    release_id: UUID
    summary: str
    client_accepted: bool
    internal_accepted: bool
    client_acceptance_notes: str | None
    internal_acceptance_notes: str | None
    created_at: datetime
    updated_at: datetime


class TraceabilitySummary(BaseModel):
    release_id: UUID
    link_types_present: list[str]
    missing_link_types: list[str]
    item_count: int


ReleaseCreate.model_rebuild()
