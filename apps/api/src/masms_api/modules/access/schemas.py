"""Access API schemas (MOD-120)."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PermissionCreate(BaseModel):
    code: str = Field(min_length=3, max_length=128, pattern=r"^[a-z0-9_.]+$")
    module_key: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    action_key: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    title: str = Field(min_length=2, max_length=255)
    description: str | None = None


class PermissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    module_key: str
    action_key: str
    title: str
    status: str
    created_at: datetime


class RolePermissionCreate(BaseModel):
    role_id: UUID
    permission_id: UUID


class RolePermissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    role_id: UUID
    permission_id: UUID
    status: str
    created_at: datetime


class ProjectMemberCreate(BaseModel):
    project_id: UUID
    actor_id: UUID
    client_id: UUID | None = None
    role_code: str = Field(default="member", max_length=64)
    access_level: str = Field(default="standard", max_length=32)
    effective_from: datetime | None = None
    effective_to: datetime | None = None


class ProjectMemberRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    client_id: UUID | None
    project_id: UUID
    actor_id: UUID
    role_code: str
    access_level: str
    status: str
    effective_from: datetime
    effective_to: datetime | None
    created_at: datetime


class ModuleAccessCreate(BaseModel):
    actor_id: UUID
    module_key: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    project_id: UUID | None = None
    access_level: str = Field(default="read", max_length=32)


class ModuleAccessRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    actor_id: UUID
    module_key: str
    project_id: UUID | None
    access_level: str
    status: str
    created_at: datetime


class DocumentAccessCreate(BaseModel):
    document_ref: str = Field(min_length=2, max_length=255)
    classification: str = Field(default="internal", max_length=32)
    actor_id: UUID | None = None
    role_code: str | None = Field(default=None, max_length=64)
    access_level: str = Field(default="read", max_length=32)


class DocumentAccessRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    document_ref: str
    classification: str
    actor_id: UUID | None
    role_code: str | None
    access_level: str
    status: str
    created_at: datetime


class ApprovalAuthorityCreate(BaseModel):
    action_code: str = Field(min_length=3, max_length=128, pattern=r"^[a-z0-9_.]+$")
    authority_actor_id: UUID | None = None
    authority_role_code: str | None = Field(default=None, max_length=64)
    client_id: UUID | None = None
    project_id: UUID | None = None
    environment: str = Field(default="all", max_length=32)
    amount_threshold: Decimal | None = None
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    delegated_from_authority_id: UUID | None = None


class ApprovalAuthorityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    action_code: str
    authority_actor_id: UUID | None
    authority_role_code: str | None
    client_id: UUID | None
    project_id: UUID | None
    environment: str
    amount_threshold: Decimal | None
    status: str
    effective_from: datetime
    effective_to: datetime | None
    created_at: datetime


class AccessReviewCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    due_at: datetime
    owner_actor_id: UUID
    summary: str | None = None


class AccessReviewComplete(BaseModel):
    summary: str | None = None
    findings: dict[str, Any] = Field(default_factory=dict)


class AccessReviewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    title: str
    status: str
    due_at: datetime
    owner_actor_id: UUID
    summary: str | None
    findings_json: dict[str, Any]
    completed_at: datetime | None
    version: int
    created_at: datetime


class PermissionCheckRequest(BaseModel):
    permission_code: str = Field(min_length=3, max_length=128)
    role_id: UUID | None = None
    project_id: UUID | None = None


class PermissionCheckResponse(BaseModel):
    allowed: bool
    permission_code: str
    reason: str
