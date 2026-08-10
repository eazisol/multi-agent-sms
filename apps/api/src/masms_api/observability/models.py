"""Shared observability ORM models (MOD-040). Append-only operational tables."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON, Uuid

from masms_api.db import Base


class AuditLog(Base):
    __tablename__ = "ops_audit_logs"
    __table_args__ = (
        Index("ix_ops_audit_logs_org_created", "organization_id", "created_at"),
        Index("ix_ops_audit_logs_entity", "organization_id", "entity_type", "entity_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    actor_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    entity_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(String(64), nullable=False, default="api")
    correlation_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    payload_redacted: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ActivityEvent(Base):
    __tablename__ = "ops_activity_events"
    __table_args__ = (
        Index("ix_ops_activity_org_created", "organization_id", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    actor_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    activity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    summary: Mapped[str] = mapped_column(String(512), nullable=False)
    entity_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    entity_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    correlation_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    payload_redacted: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class StatusHistory(Base):
    __tablename__ = "ops_status_history"
    __table_args__ = (
        Index(
            "ix_ops_status_history_entity",
            "organization_id",
            "entity_type",
            "entity_id",
            "created_at",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    previous_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    next_status: Mapped[str] = mapped_column(String(64), nullable=False)
    actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    actor_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    rule: Mapped[str | None] = mapped_column(String(128), nullable=True)
    correlation_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class AgentRun(Base):
    __tablename__ = "ops_agent_runs"
    __table_args__ = (
        Index("ix_ops_agent_runs_org_started", "organization_id", "started_at"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    agent_name: Mapped[str] = mapped_column(String(128), nullable=False)
    actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="started")
    correlation_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    input_summary_redacted: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default=dict
    )
    output_summary_redacted: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default=dict
    )
    error_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class IntegrationEvent(Base):
    __tablename__ = "ops_integration_events"
    __table_args__ = (
        Index("ix_ops_integration_org_created", "organization_id", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    direction: Mapped[str] = mapped_column(String(16), nullable=False)  # inbound|outbound
    event_type: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="received")
    correlation_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    payload_redacted: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    error_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
