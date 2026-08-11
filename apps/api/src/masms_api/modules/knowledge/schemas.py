"""Knowledge API schemas (MOD-370)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    project_id: UUID | None = None
    classification: str = Field(default="internal", max_length=32)
    owner_actor_id: UUID | None = None


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    code: str
    title: str
    description: str | None
    status: str
    classification: str
    owner_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class VersionCreate(BaseModel):
    body_text: str = Field(min_length=1)
    change_summary: str | None = None
    effective_from: datetime | None = None
    effective_to: datetime | None = None


class VersionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    item_id: UUID
    version_number: int
    status: str
    body_text: str
    change_summary: str | None
    effective_from: datetime | None
    effective_to: datetime | None
    approved_by_actor_id: UUID | None
    version: int
    created_at: datetime
    updated_at: datetime


class ChunkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    item_id: UUID
    version_id: UUID
    chunk_index: int
    content_text: str
    token_estimate: int
    created_at: datetime


class EmbeddingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    chunk_id: UUID
    model_name: str
    dims: int
    vector_stub: list[Any]
    created_at: datetime


class PermissionCreate(BaseModel):
    effect: str = Field(default="allow", max_length=16)
    principal_type: str = Field(default="organization", max_length=32)
    principal_id: UUID | None = None
    project_id: UUID | None = None
    can_retrieve: bool = True
    can_manage: bool = False


class PermissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    item_id: UUID
    effect: str
    principal_type: str
    principal_id: UUID | None
    project_id: UUID | None
    can_retrieve: bool
    can_manage: bool
    created_at: datetime


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    project_id: UUID | None = None
    limit: int = Field(default=10, ge=1, le=50)


class CitationHit(BaseModel):
    item_id: UUID
    item_code: str
    item_title: str
    version_id: UUID
    version_number: int
    chunk_id: UUID
    chunk_index: int
    content_text: str
    score: float
    project_id: UUID | None
    source_citation: str


class SearchResponse(BaseModel):
    query: str
    items: list[CitationHit]
    stub: bool = True


class ConflictCreate(BaseModel):
    item_id_a: UUID
    version_id_a: UUID
    item_id_b: UUID
    version_id_b: UUID
    reason: str = Field(min_length=1)
    project_id: UUID | None = None


class ConflictResolve(BaseModel):
    status: str = Field(min_length=1, max_length=32)
    resolution_notes: str | None = None


class ConflictRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    item_id_a: UUID
    version_id_a: UUID
    item_id_b: UUID
    version_id_b: UUID
    status: str
    reason: str
    resolution_notes: str | None
    created_at: datetime
    resolved_at: datetime | None


class UsageLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    item_id: UUID
    version_id: UUID
    chunk_id: UUID | None
    query_text: str
    score: float | None
    actor_id: UUID
    created_at: datetime


class ActivateVersion(BaseModel):
    expected_version: int | None = None
