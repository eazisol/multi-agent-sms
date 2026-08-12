"""Traceability API schemas (MOD-460)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MustHaveCreate(BaseModel):
    requirement_id: UUID
    requirement_code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    project_id: UUID | None = None


class MustHaveRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    requirement_id: UUID
    requirement_code: str
    title: str
    created_by_actor_id: UUID
    created_at: datetime


class RequirementTicketLinkCreate(BaseModel):
    requirement_id: UUID
    ticket_id: UUID
    notes: str | None = None


class RequirementTicketLinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    requirement_id: UUID
    ticket_id: UUID
    notes: str | None
    created_by_actor_id: UUID
    created_at: datetime


class RequirementTestLinkCreate(BaseModel):
    requirement_id: UUID
    test_case_id: UUID
    notes: str | None = None


class RequirementTestLinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    requirement_id: UUID
    test_case_id: UUID
    notes: str | None
    created_by_actor_id: UUID
    created_at: datetime


class RequirementReleaseLinkCreate(BaseModel):
    requirement_id: UUID
    release_id: UUID
    notes: str | None = None


class RequirementReleaseLinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    requirement_id: UUID
    release_id: UUID
    notes: str | None
    created_by_actor_id: UUID
    created_at: datetime


class RequirementDocumentLinkCreate(BaseModel):
    requirement_id: UUID
    document_id: UUID
    notes: str | None = None


class RequirementDocumentLinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    requirement_id: UUID
    document_id: UUID
    notes: str | None
    created_by_actor_id: UUID
    created_at: datetime


class TicketTestLinkCreate(BaseModel):
    ticket_id: UUID
    test_case_id: UUID
    notes: str | None = None


class TicketTestLinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    ticket_id: UUID
    test_case_id: UUID
    notes: str | None
    created_by_actor_id: UUID
    created_at: datetime


class CoverageReport(BaseModel):
    organization_id: UUID
    project_id: UUID | None = None
    total_must_haves: int
    complete_count: int
    incomplete_count: int
    coverage_pct: float
    release_ready: bool
    incomplete_requirement_ids: list[UUID] = Field(default_factory=list)


class AuditCoverageReport(BaseModel):
    organization_id: UUID
    action_count: int
    audited_count: int
    coverage_pct: float
    complete: bool


class ManifestCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    project_id: UUID | None = None


class ManifestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    code: str
    title: str
    status: str
    item_count: int
    checksum: str | None
    sealed_at: datetime | None
    version: int
    created_by_actor_id: UUID
    updated_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class ManifestItemCreate(BaseModel):
    item_type: str = Field(min_length=1, max_length=32)
    item_id: UUID
    label: str | None = Field(default=None, max_length=255)


class ManifestItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    manifest_id: UUID
    item_type: str
    item_id: UUID
    label: str | None
    created_at: datetime


class ManifestSeal(BaseModel):
    expected_version: int | None = None


class ExportCreate(BaseModel):
    manifest_id: UUID
    export_format: str = Field(default="json", max_length=16)


class ExportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    manifest_id: UUID
    export_format: str
    status: str
    payload_preview: str | None
    reconciliation_hash: str | None
    requested_by_actor_id: UUID
    completed_at: datetime | None
    failure_reason: str | None
    created_at: datetime
