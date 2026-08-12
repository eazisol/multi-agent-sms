"""Insights API schemas (MOD-450)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DashboardRefresh(BaseModel):
    project_id: UUID | None = None


class DashboardSnapshotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    scope_key: str
    project_id: UUID | None
    metrics: dict[str, Any]
    source_hash: str | None
    computed_at: datetime
    refreshed_at: datetime
    is_fresh: bool
    version: int
    created_at: datetime
    updated_at: datetime


class ProjectHealthUpsert(BaseModel):
    project_id: UUID
    health_status: str = Field(default="healthy", max_length=32)
    score: int = Field(default=100, ge=0, le=100)
    blockers_count: int = Field(default=0, ge=0)
    open_tickets: int = Field(default=0, ge=0)
    open_bugs: int = Field(default=0, ge=0)
    overdue_followups: int = Field(default=0, ge=0)
    notes: str | None = None
    expected_version: int | None = None


class ProjectHealthRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID
    health_status: str
    score: int
    blockers_count: int
    open_tickets: int
    open_bugs: int
    overdue_followups: int
    notes: str | None
    computed_at: datetime
    version: int
    created_at: datetime
    updated_at: datetime


class SavedFilterCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    module_key: str = Field(min_length=1, max_length=64)
    filter_json: str = Field(min_length=2)
    is_shared: bool = False


class SavedFilterRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    owner_actor_id: UUID
    name: str
    module_key: str
    filter_json: str
    is_shared: bool
    version: int
    created_at: datetime
    updated_at: datetime


class SearchIndexCreate(BaseModel):
    entity_type: str = Field(min_length=1, max_length=64)
    entity_id: UUID
    title: str = Field(min_length=1, max_length=255)
    body_preview: str = ""
    project_id: UUID | None = None
    classification: str = Field(default="internal", max_length=32)


class SearchDocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    entity_type: str
    entity_id: UUID
    title: str
    body_preview: str
    classification: str
    indexed_at: datetime
    created_at: datetime


class ActivityCreate(BaseModel):
    event_type: str = Field(min_length=1, max_length=64)
    entity_type: str = Field(min_length=1, max_length=64)
    summary: str = Field(min_length=1)
    entity_id: UUID | None = None
    project_id: UUID | None = None
    occurred_at: datetime | None = None


class ActivityEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    actor_id: UUID
    event_type: str
    entity_type: str
    entity_id: UUID | None
    summary: str
    occurred_at: datetime
    created_at: datetime


class ReportCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    report_type: str = Field(min_length=1, max_length=64)
    definition_json: str = Field(default="{}")
    status: str = Field(default="draft", max_length=32)


class ReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    report_type: str
    definition_json: str
    status: str
    version: int
    owner_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class ExportCreate(BaseModel):
    export_format: str = Field(default="json", max_length=16)
    report_id: UUID | None = None
    include_dashboard_metrics: bool = True


class ExportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    report_id: UUID | None
    export_format: str
    status: str
    payload_preview: str | None
    row_count: int
    requested_by_actor_id: UUID
    completed_at: datetime | None
    failure_reason: str | None
    created_at: datetime
    updated_at: datetime
