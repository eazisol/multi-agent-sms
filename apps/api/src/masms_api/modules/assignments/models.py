"""Assignment entities (MOD-310)."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON, Uuid

from masms_api.db import Base


class Assignment(Base):
    """Current active assignment of an actor to a ticket."""

    __tablename__ = "asg_assignments"
    __table_args__ = (
        Index("ix_asg_assignments_ticket", "organization_id", "ticket_id"),
        Index("ix_asg_assignments_actor", "organization_id", "assignee_actor_id"),
        Index("ix_asg_assignments_status", "organization_id", "ticket_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("prj_projects.id"), nullable=False
    )
    ticket_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tkt_tickets.id"), nullable=False
    )
    assignee_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    role_code: Mapped[str] = mapped_column(String(64), nullable=False, default="developer")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending_ack")
    # pending_ack | acknowledged | closed
    required_skill_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    min_proficiency: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    override_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_override: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    recommendation_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    assigned_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class AssignmentRecommendation(Base):
    __tablename__ = "asg_assignment_recommendations"
    __table_args__ = (
        Index("ix_asg_recommendations_ticket", "organization_id", "ticket_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("prj_projects.id"), nullable=False
    )
    ticket_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tkt_tickets.id"), nullable=False
    )
    candidate_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    score: Mapped[Decimal] = mapped_column(Numeric(8, 4), nullable=False, default=Decimal("0"))
    rank: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    eligible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    reasons_json: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    remaining_capacity_pct: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="proposed")
    # proposed | accepted | rejected | superseded
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class AllocationHistory(Base):
    """Append-only allocation snapshot (AC-003)."""

    __tablename__ = "asg_allocation_history"
    __table_args__ = (Index("ix_asg_alloc_hist_actor", "organization_id", "actor_id"),)

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("prj_projects.id"), nullable=False
    )
    ticket_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tkt_tickets.id"), nullable=False
    )
    assignment_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("asg_assignments.id"), nullable=False
    )
    actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    allocation_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    event_type: Mapped[str] = mapped_column(String(32), nullable=False)
    # allocated | released | overridden
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    recorded_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class AssignmentAcknowledgment(Base):
    __tablename__ = "asg_acknowledgments"
    __table_args__ = (
        Index("ix_asg_ack_assignment", "organization_id", "assignment_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("prj_projects.id"), nullable=False
    )
    assignment_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("asg_assignments.id"), nullable=False
    )
    actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="acknowledged")
    # acknowledged | declined
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    acknowledged_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ReassignmentHistory(Base):
    """Append-only reassignment ledger (AC-003)."""

    __tablename__ = "asg_reassignment_history"
    __table_args__ = (
        Index("ix_asg_reassign_ticket", "organization_id", "ticket_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("prj_projects.id"), nullable=False
    )
    ticket_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("tkt_tickets.id"), nullable=False
    )
    from_assignment_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    to_assignment_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    from_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    to_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    is_override: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    recorded_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
