"""Pydantic schemas for governance API."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from masms_api.kernel.pagination import PageMeta


class BaselineCreate(BaseModel):
    baseline_key: str = Field(min_length=3, max_length=64)
    title: str = Field(min_length=3, max_length=255)
    artifact_path: str = Field(min_length=1, max_length=1024)
    document_version: str = Field(min_length=1, max_length=64)
    classification: str = Field(default="internal", max_length=32)
    content_sha256: str | None = Field(default=None, max_length=64)
    metadata: dict[str, Any] = Field(default_factory=dict)


class BaselineUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=255)
    artifact_path: str | None = Field(default=None, min_length=1, max_length=1024)
    document_version: str | None = Field(default=None, min_length=1, max_length=64)
    classification: str | None = Field(default=None, max_length=32)
    expected_version: int = Field(ge=1)
    metadata: dict[str, Any] | None = None


class BaselineTransition(BaseModel):
    target_status: str
    expected_version: int = Field(ge=1)
    reason: str | None = None


class BaselineRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": "00000000-0000-4000-8000-000000000301",
                    "organization_id": "00000000-0000-4000-8000-000000000001",
                    "baseline_key": "BL-SRS-001",
                    "title": "MVP SRS",
                    "artifact_path": (
                        "Docs/Multi_Agent_Software_House_Management_System_MVP_SRS_v1.0.md"
                    ),
                    "document_version": "v1.0",
                    "classification": "internal",
                    "approval_status": "draft",
                    "version": 1,
                    "created_at": "2026-08-10T12:00:00Z",
                    "updated_at": "2026-08-10T12:00:00Z",
                }
            ]
        },
    )

    id: UUID
    organization_id: UUID
    baseline_key: str
    title: str
    artifact_path: str
    document_version: str
    classification: str
    approval_status: str
    version: int
    created_at: datetime
    updated_at: datetime


class RequirementMappingCreate(BaseModel):
    requirement_id: str = Field(min_length=3, max_length=64)
    requirement_title: str = Field(min_length=3, max_length=255)
    module_id: str = Field(min_length=3, max_length=32)
    mapping_role: str = Field(default="primary", max_length=32)
    notes: str | None = None


class RequirementMappingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    requirement_id: str
    requirement_title: str
    module_id: str
    mapping_role: str
    notes: str | None
    status: str
    version: int


class AdrCreate(BaseModel):
    adr_key: str = Field(min_length=3, max_length=64)
    title: str = Field(min_length=3, max_length=255)
    context: str = Field(min_length=3)
    decision: str = Field(min_length=3)
    consequences: str = Field(min_length=3)
    security_notes: str | None = None
    document_path: str | None = None


class AdrTransition(BaseModel):
    target_status: str
    expected_version: int = Field(ge=1)
    reason: str | None = None


class AdrRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    adr_key: str
    title: str
    status: str
    version: int
    context: str
    decision: str
    consequences: str
    security_notes: str | None
    document_path: str | None


class ChangeRequestCreate(BaseModel):
    change_request_key: str = Field(min_length=3, max_length=64)
    title: str = Field(min_length=3, max_length=255)
    summary: str = Field(min_length=3)
    rationale: str = Field(min_length=3)
    impact: dict[str, Any] = Field(default_factory=dict)
    target_entity_type: str
    target_entity_id: UUID
    target_version: int = Field(ge=1)
    proposed_version: int = Field(ge=1)
    priority: str = "normal"
    idempotency_key: str | None = Field(default=None, max_length=128)


class ChangeRequestTransition(BaseModel):
    target_status: str
    expected_version: int = Field(ge=1)
    reason: str | None = None


class ChangeRequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    change_request_key: str
    title: str
    summary: str
    rationale: str
    impact: dict[str, Any]
    target_entity_type: str
    target_entity_id: UUID
    target_version: int
    proposed_version: int
    priority: str
    status: str
    version: int


class ApprovalCreate(BaseModel):
    target_entity_type: str
    target_entity_id: UUID
    target_version: int = Field(ge=1)
    decision: str
    authority_level: int = Field(ge=1, le=5)
    reason: str | None = None


class ApprovalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    target_entity_type: str
    target_entity_id: UUID
    target_version: int
    decision: str
    status: str
    approver_actor_id: UUID
    authority_level: int
    reason: str | None
    decided_at: datetime
    correlation_id: UUID


class AuditEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    actor_id: UUID
    actor_kind: str
    action: str
    entity_type: str
    entity_id: UUID
    entity_version: int | None
    reason: str | None
    source: str
    correlation_id: UUID
    created_at: datetime


class BaselinePage(BaseModel):
    items: list[BaselineRead]
    page: PageMeta


class RequirementMappingPage(BaseModel):
    items: list[RequirementMappingRead]
    page: PageMeta


class AdrPage(BaseModel):
    items: list[AdrRead]
    page: PageMeta


class ChangeRequestPage(BaseModel):
    items: list[ChangeRequestRead]
    page: PageMeta


class ApprovalPage(BaseModel):
    items: list[ApprovalRead]
    page: PageMeta


class AuditEventPage(BaseModel):
    items: list[AuditEventRead]
    page: PageMeta


class ProblemDetails(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "type": "https://masms.local/problems/forbidden",
                    "title": "forbidden",
                    "status": 403,
                    "detail": "Only human actors may approve or reject governance records",
                    "code": "forbidden",
                    "message": "Only human actors may approve or reject governance records",
                    "correlation_id": "00000000-0000-4000-8000-000000000999",
                    "details": None,
                },
                {
                    "type": "https://masms.local/problems/conflict",
                    "title": "conflict",
                    "status": 409,
                    "detail": "Stale version; refresh and retry",
                    "code": "conflict",
                    "message": "Stale version; refresh and retry",
                    "correlation_id": "00000000-0000-4000-8000-000000000999",
                    "details": None,
                },
            ]
        }
    )

    type: str
    title: str
    status: int
    detail: str
    code: str
    message: str
    correlation_id: UUID | None = None
    details: list[dict[str, Any]] | None = None
