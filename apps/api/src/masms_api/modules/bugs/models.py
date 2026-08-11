"""Bug entities (MOD-410)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from masms_api.db import Base


class Bug(Base):
    __tablename__ = "bg_bugs"
    __table_args__ = (
        UniqueConstraint("organization_id", "code", name="uq_bg_bugs_org_code"),
        Index("ix_bg_bugs_status", "organization_id", "status"),
        Index("ix_bg_bugs_project", "organization_id", "project_id"),
        Index("ix_bg_bugs_severity", "organization_id", "severity"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    severity: Mapped[str] = mapped_column(String(16), nullable=False, default="medium")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    blocks_release: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    rejection_evidence: Mapped[str | None] = mapped_column(Text, nullable=True)
    reopen_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    assignee_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
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


class BugLink(Base):
    __tablename__ = "bg_links"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "bug_id",
            "link_type",
            "linked_entity_id",
            name="uq_bg_links_bug_type_entity",
        ),
        Index("ix_bg_links_bug", "organization_id", "bug_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    bug_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    link_type: Mapped[str] = mapped_column(String(32), nullable=False)
    linked_entity_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class BugAssignment(Base):
    __tablename__ = "bg_assignments"
    __table_args__ = (
        Index("ix_bg_assignments_bug", "organization_id", "bug_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    bug_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    assignee_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    assigned_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    effective_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class BugFixSubmission(Base):
    __tablename__ = "bg_fix_submissions"
    __table_args__ = (
        Index("ix_bg_fixes_bug", "organization_id", "bug_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    bug_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    build_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="submitted")
    submitted_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class BugRetest(Base):
    __tablename__ = "bg_retests"
    __table_args__ = (
        Index("ix_bg_retests_bug", "organization_id", "bug_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    bug_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    fix_submission_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    result: Mapped[str] = mapped_column(String(16), nullable=False)
    evidence_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    environment_code: Mapped[str] = mapped_column(String(64), nullable=False, default="local")
    build_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    tested_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class BugKnownIssueApproval(Base):
    __tablename__ = "bg_known_issue_approvals"
    __table_args__ = (
        Index("ix_bg_known_issue_bug", "organization_id", "bug_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    bug_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    release_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    approved_by_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class BugSeveritySla(Base):
    __tablename__ = "bg_severity_slas"
    __table_args__ = (
        UniqueConstraint("organization_id", "severity", name="uq_bg_severity_slas_org_sev"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    response_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    resolve_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    blocks_release: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
