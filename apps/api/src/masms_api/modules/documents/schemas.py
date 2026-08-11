"""Documents API schemas (MOD-250)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TemplateCreate(BaseModel):
    code: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    title: str = Field(min_length=2, max_length=255)


class TemplateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    status: str
    created_at: datetime


class TemplateVersionCreate(BaseModel):
    template_id: UUID
    body_markdown: str = Field(min_length=1)


class TemplateVersionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    template_id: UUID
    version_number: int
    status: str
    body_markdown: str
    published_at: datetime | None
    created_at: datetime


class DocumentCreate(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    classification: str = Field(default="internal", max_length=32)
    client_id: UUID | None = None
    project_id: UUID | None = None
    template_id: UUID | None = None
    owner_actor_id: UUID | None = None


class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    client_id: UUID | None
    project_id: UUID | None
    title: str
    classification: str
    status: str
    owner_actor_id: UUID
    template_id: UUID | None
    current_version_id: UUID | None
    created_at: datetime


class DocumentVersionCreate(BaseModel):
    document_id: UUID
    storage_key: str = Field(min_length=2, max_length=512)
    filename: str = Field(min_length=1, max_length=255)
    content_type: str = Field(default="application/octet-stream", max_length=128)
    size_bytes: int = Field(default=0, ge=0)
    checksum_sha256: str | None = Field(default=None, max_length=64)


class DocumentVersionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    document_id: UUID
    version_number: int
    status: str
    owner_actor_id: UUID
    storage_key: str
    filename: str
    content_type: str
    size_bytes: int
    checksum_sha256: str | None
    effective_at: datetime | None
    indexing_allowed: bool
    created_at: datetime


class AttachmentCreate(BaseModel):
    document_version_id: UUID
    storage_key: str = Field(min_length=2, max_length=512)
    filename: str = Field(min_length=1, max_length=255)
    content_type: str = Field(default="application/octet-stream", max_length=128)
    size_bytes: int = Field(default=0, ge=0)


class AttachmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    document_version_id: UUID
    storage_key: str
    filename: str
    content_type: str
    size_bytes: int
    created_at: datetime


class PermissionCreate(BaseModel):
    document_id: UUID
    grantee_actor_id: UUID
    can_download: bool = False
    can_preview: bool = False
    can_extract_text: bool = False
    can_use_embeddings: bool = False


class PermissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    document_id: UUID
    grantee_actor_id: UUID
    can_download: bool
    can_preview: bool
    can_extract_text: bool
    can_use_embeddings: bool
    created_at: datetime


class ScanResultCreate(BaseModel):
    document_version_id: UUID
    verdict: str = Field(min_length=3, max_length=32)
    engine: str = Field(default="stub", max_length=64)
    detail: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ScanResultRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    document_version_id: UUID
    engine: str
    verdict: str
    detail: str | None
    scanned_at: datetime
    created_at: datetime


class MarkAvailableRequest(BaseModel):
    effective_at: datetime


class AccessCheckRequest(BaseModel):
    document_version_id: UUID
    actor_id: UUID
    action: str = Field(min_length=3, max_length=32)


class AccessCheckRead(BaseModel):
    allowed: bool
    action: str
    document_version_id: UUID
    version_status: str
