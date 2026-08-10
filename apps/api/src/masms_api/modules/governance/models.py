"""SQLAlchemy models for MOD-000 governance entities."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON, Uuid

from masms_api.db import Base


class SourceBaseline(Base):
    __tablename__ = "gov_source_baselines"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "baseline_key",
            "version",
            name="uq_gov_source_baselines_org_key_version",
        ),
        Index("ix_gov_source_baselines_org_status", "organization_id", "approval_status"),
    )

    id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[Any | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    baseline_key: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    artifact_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    document_version: Mapped[str] = mapped_column(String(64), nullable=False)
    classification: Mapped[str] = mapped_column(String(32), nullable=False, default="internal")
    approval_status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    effective_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    supersedes_id: Mapped[Any | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("gov_source_baselines.id"), nullable=True
    )
    content_sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    owner_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_by_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    updated_by_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class RequirementMapping(Base):
    __tablename__ = "gov_requirement_mappings"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "requirement_id",
            "module_id",
            "mapping_role",
            name="uq_gov_requirement_mappings_unique",
        ),
        Index("ix_gov_requirement_mappings_req", "organization_id", "requirement_id"),
    )

    id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[Any | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    requirement_id: Mapped[str] = mapped_column(String(64), nullable=False)
    requirement_title: Mapped[str] = mapped_column(String(255), nullable=False)
    module_id: Mapped[str] = mapped_column(String(32), nullable=False)
    mapping_role: Mapped[str] = mapped_column(String(32), nullable=False, default="primary")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    owner_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_by_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    updated_by_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class ArchitectureDecision(Base):
    __tablename__ = "gov_architecture_decisions"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "adr_key",
            "version",
            name="uq_gov_architecture_decisions_org_key_version",
        ),
    )

    id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[Any | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    adr_key: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="proposed")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    context: Mapped[str] = mapped_column(Text, nullable=False)
    decision: Mapped[str] = mapped_column(Text, nullable=False)
    consequences: Mapped[str] = mapped_column(Text, nullable=False)
    security_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    document_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    owner_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_by_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    updated_by_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class GovernanceChangeRequest(Base):
    __tablename__ = "gov_change_requests"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "change_request_key",
            "version",
            name="uq_gov_change_requests_org_key_version",
        ),
        UniqueConstraint(
            "organization_id",
            "idempotency_key",
            name="uq_gov_change_requests_org_idempotency",
        ),
        Index(
            "ix_gov_change_requests_target",
            "organization_id",
            "target_entity_type",
            "target_entity_id",
        ),
    )

    id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[Any | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    change_request_key: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    impact: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    target_entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    target_entity_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    target_version: Mapped[int] = mapped_column(Integer, nullable=False)
    proposed_version: Mapped[int] = mapped_column(Integer, nullable=False)
    priority: Mapped[str] = mapped_column(String(32), nullable=False, default="normal")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    idempotency_key: Mapped[str | None] = mapped_column(String(128), nullable=True)
    owner_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_by_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    updated_by_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class GovernanceApprovalRecord(Base):
    __tablename__ = "gov_approval_records"
    __table_args__ = (
        Index(
            "ix_gov_approval_records_target",
            "organization_id",
            "target_entity_type",
            "target_entity_id",
            "target_version",
        ),
    )

    id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[Any | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    target_entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    target_entity_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    target_version: Mapped[int] = mapped_column(Integer, nullable=False)
    decision: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="decided")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    approver_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    authority_level: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    correlation_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    owner_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_by_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    updated_by_actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class GovernanceAuditEvent(Base):
    __tablename__ = "gov_audit_events"
    __table_args__ = (
        Index("ix_gov_audit_events_org_created", "organization_id", "created_at"),
    )

    id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[Any | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    actor_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    actor_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    entity_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(String(64), nullable=False, default="api")
    correlation_id: Mapped[Any] = mapped_column(Uuid(as_uuid=True), nullable=False)
    payload_redacted: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
