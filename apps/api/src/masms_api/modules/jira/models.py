"""Persistence models for MOD-520 Jira integration."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from masms_api.db import Base


class JiraIssuePush(Base):
    __tablename__ = "jr_issue_pushes"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "internal_ticket_id",
            name="uq_jr_issue_pushes_org_ticket",
        ),
        Index("ix_jr_issue_pushes_org_status", "organization_id", "push_status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    internal_ticket_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    jira_issue_key: Mapped[str] = mapped_column(String(64), nullable=False)
    summary: Mapped[str] = mapped_column(String(512), nullable=False)
    approval_status: Mapped[str] = mapped_column(String(32), nullable=False)
    push_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pushed")
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


class JiraStatusConflict(Base):
    __tablename__ = "jr_status_conflicts"
    __table_args__ = (
        Index("ix_jr_status_conflicts_org_created", "organization_id", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    issue_push_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    external_status: Mapped[str] = mapped_column(String(64), nullable=False)
    attempted_internal_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    conflict_reason: Mapped[str] = mapped_column(String(255), nullable=False)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class JiraCommentSync(Base):
    __tablename__ = "jr_comment_syncs"
    __table_args__ = (
        Index("ix_jr_comment_syncs_org_status", "organization_id", "sync_status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    issue_push_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    sync_status: Mapped[str] = mapped_column(String(32), nullable=False, default="synced")
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_attempt_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
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
