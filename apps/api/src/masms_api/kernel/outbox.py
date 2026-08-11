"""Transactional outbox model and enqueue helper (MOD-020-MP-006)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index, Integer, String, Text, func, select
from sqlalchemy.orm import Mapped, Session, mapped_column
from sqlalchemy.types import JSON, Uuid

from masms_api.db import Base
from masms_api.kernel.redact import redact_mapping


class OutboxMessage(Base):
    __tablename__ = "sys_outbox_messages"
    __table_args__ = (
        Index("ix_sys_outbox_status_available", "status", "available_at"),
        Index("ix_sys_outbox_org_created", "organization_id", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    aggregate_type: Mapped[str] = mapped_column(String(64), nullable=False)
    aggregate_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    event_type: Mapped[str] = mapped_column(String(128), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    correlation_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    causation_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    available_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)


def enqueue_outbox(
    session: Session,
    *,
    organization_id: UUID,
    aggregate_type: str,
    aggregate_id: UUID,
    event_type: str,
    payload: dict[str, Any],
    correlation_id: UUID,
    project_id: UUID | None = None,
    causation_id: UUID | None = None,
) -> OutboxMessage:
    """Insert an outbox row in the current transaction (publisher runtime is separate)."""
    message = OutboxMessage(
        organization_id=organization_id,
        project_id=project_id,
        aggregate_type=aggregate_type,
        aggregate_id=aggregate_id,
        event_type=event_type,
        payload=redact_mapping(payload),
        correlation_id=correlation_id,
        causation_id=causation_id,
        status="pending",
    )
    session.add(message)
    return message


def relay_pending_outbox(
    session: Session,
    *,
    organization_id: UUID | None = None,
    limit: int = 100,
) -> list[OutboxMessage]:
    """Mark pending outbox rows published (local relay stub).

    Idempotent: only pending rows are selected. Real SNS/SQS bridge remains MOD-500;
    this closes the M1 publisher gap for BE-003/WF-003.
    """
    stmt = (
        select(OutboxMessage)
        .where(OutboxMessage.status == "pending")
        .order_by(OutboxMessage.created_at.asc())
        .limit(max(1, min(limit, 500)))
    )
    if organization_id is not None:
        stmt = stmt.where(OutboxMessage.organization_id == organization_id)

    rows = list(session.scalars(stmt).all())
    now = datetime.now(UTC)
    for row in rows:
        row.status = "published"
        row.published_at = now
        row.attempt_count = int(row.attempt_count or 0) + 1
        row.last_error = None
        session.add(row)
    return rows
