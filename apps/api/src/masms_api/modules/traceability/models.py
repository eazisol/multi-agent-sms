"""Traceability persistence models (MOD-460)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from masms_api.db import Base


class RequirementTicketLink(Base):
    __tablename__ = "tr_requirement_ticket_links"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "requirement_id",
            "ticket_id",
            name="uq_tr_req_ticket_links_org_req_ticket",
        ),
        Index("ix_tr_req_ticket_links_org_req", "organization_id", "requirement_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    requirement_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    ticket_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class RequirementTestLink(Base):
    __tablename__ = "tr_requirement_test_links"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "requirement_id",
            "test_case_id",
            name="uq_tr_req_test_links_org_req_test",
        ),
        Index("ix_tr_req_test_links_org_req", "organization_id", "requirement_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    requirement_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    test_case_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class RequirementReleaseLink(Base):
    __tablename__ = "tr_requirement_release_links"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "requirement_id",
            "release_id",
            name="uq_tr_req_release_links_org_req_release",
        ),
        Index("ix_tr_req_release_links_org_req", "organization_id", "requirement_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    requirement_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    release_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class RequirementDocumentLink(Base):
    __tablename__ = "tr_requirement_document_links"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "requirement_id",
            "document_id",
            name="uq_tr_req_document_links_org_req_doc",
        ),
        Index("ix_tr_req_document_links_org_req", "organization_id", "requirement_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    requirement_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    document_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class TicketTestLink(Base):
    __tablename__ = "tr_ticket_test_links"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "ticket_id",
            "test_case_id",
            name="uq_tr_ticket_test_links_org_ticket_test",
        ),
        Index("ix_tr_ticket_test_links_org_ticket", "organization_id", "ticket_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    ticket_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    test_case_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class EvidenceManifest(Base):
    __tablename__ = "tr_evidence_manifests"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "code",
            name="uq_tr_evidence_manifests_org_code",
        ),
        Index("ix_tr_evidence_manifests_org_status", "organization_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    item_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    checksum: Mapped[str | None] = mapped_column(String(128), nullable=True)
    sealed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    updated_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class MustHaveRequirement(Base):
    """M1 support registry for AC-001 coverage calculation."""

    __tablename__ = "tr_must_have_requirements"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "requirement_id",
            name="uq_tr_must_have_requirements_org_req",
        ),
        Index("ix_tr_must_have_requirements_org_project", "organization_id", "project_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    requirement_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    requirement_code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class EvidenceManifestItem(Base):
    """M1 support items for evidence manifests (AC-003)."""

    __tablename__ = "tr_evidence_manifest_items"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "manifest_id",
            "item_type",
            "item_id",
            name="uq_tr_evidence_manifest_items_org_manifest_item",
        ),
        Index("ix_tr_evidence_manifest_items_manifest", "organization_id", "manifest_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    manifest_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    item_type: Mapped[str] = mapped_column(String(32), nullable=False)
    item_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class EvidenceExport(Base):
    """M1 support evidence export jobs (AC-003)."""

    __tablename__ = "tr_evidence_exports"
    __table_args__ = (
        Index("ix_tr_evidence_exports_org_status", "organization_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    manifest_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    export_format: Mapped[str] = mapped_column(String(16), nullable=False, default="json")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    payload_preview: Mapped[str | None] = mapped_column(Text, nullable=True)
    reconciliation_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    requested_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ActionAudit(Base):
    """M1 support module-local audit mirror for AC-002 coverage."""

    __tablename__ = "tr_action_audits"
    __table_args__ = (
        Index("ix_tr_action_audits_org_action", "organization_id", "action"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(96), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    payload_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
