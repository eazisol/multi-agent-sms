"""Human approval gate entities (MOD-330).

Approvals bind to exact target versions. Decisions and evidence are append-only.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
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
from sqlalchemy.types import JSON, Uuid

from masms_api.db import Base


class ApprovalRequest(Base):
    """Approval request locked to an exact target entity version (AC-002)."""

    __tablename__ = "apr_requests"
    __table_args__ = (
        Index(
            "ix_apr_requests_target",
            "organization_id",
            "target_entity_type",
            "target_entity_id",
            "target_version",
        ),
        Index("ix_apr_requests_status", "organization_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    action_code: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    target_entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    target_entity_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    target_version: Mapped[int] = mapped_column(Integer, nullable=False)
    workflow_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    current_step_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    submitted_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    submitted_by_actor_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    recommendation_source_actor_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), nullable=True
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    superseded_by_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
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
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ApprovalWorkflowInstance(Base):
    """Frozen workflow snapshot for an approval request."""

    __tablename__ = "apr_workflows"
    __table_args__ = (
        UniqueConstraint("approval_id", name="uq_apr_workflows_approval"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    approval_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    steps_json: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    configuration_version_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ApprovalStep(Base):
    __tablename__ = "apr_steps"
    __table_args__ = (
        UniqueConstraint("approval_id", "step_order", name="uq_apr_steps_order"),
        Index("ix_apr_steps_approval", "organization_id", "approval_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    approval_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)
    role_code: Mapped[str] = mapped_column(String(64), nullable=False)
    required_authority_level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    assignee_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ApprovalDecision(Base):
    """Append-only decision history."""

    __tablename__ = "apr_decisions"
    __table_args__ = (
        Index("ix_apr_decisions_approval", "organization_id", "approval_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    approval_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    step_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    decision: Mapped[str] = mapped_column(String(32), nullable=False)
    actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    actor_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    authority_mode: Mapped[str] = mapped_column(
        String(32), nullable=False, default="direct"
    )  # direct | delegated
    delegation_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    decided_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ApprovalDelegation(Base):
    __tablename__ = "apr_delegations"
    __table_args__ = (
        Index(
            "ix_apr_delegations_delegate",
            "organization_id",
            "to_actor_id",
            "status",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    from_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    to_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    action_code: Mapped[str] = mapped_column(String(128), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_by_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)


class ApprovalEvidence(Base):
    __tablename__ = "apr_evidence"
    __table_args__ = (
        Index("ix_apr_evidence_approval", "organization_id", "approval_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    approval_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(64), nullable=False, default="reference")
    evidence_ref: Mapped[str] = mapped_column(String(512), nullable=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class HumanOverride(Base):
    __tablename__ = "apr_overrides"
    __table_args__ = (
        Index(
            "ix_apr_overrides_target",
            "organization_id",
            "target_entity_type",
            "target_entity_id",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    approval_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    action_code: Mapped[str] = mapped_column(String(128), nullable=False)
    target_entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    target_entity_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    target_version: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    authority_used: Mapped[str] = mapped_column(String(128), nullable=False)
    retrospective_required: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    authorized_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
