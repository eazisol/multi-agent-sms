"""Follow-up runtime entities (MOD-340)."""

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


class FollowUp(Base):
    __tablename__ = "flu_followups"
    __table_args__ = (
        Index("ix_flu_followups_status", "organization_id", "status"),
        Index("ix_flu_followups_due", "organization_id", "due_at"),
        Index(
            "ix_flu_followups_source",
            "organization_id",
            "source_entity_type",
            "source_entity_id",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    direction: Mapped[str] = mapped_column(String(32), nullable=False, default="outbound")
    # outbound = we ask them; inbound = they ask us / return path
    source_entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    source_entity_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    source_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    recipient_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    required_response: Mapped[str] = mapped_column(String(255), nullable=False)
    closure_condition: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    rule_version_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    reminder_rule_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    escalation_rule_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reminder_offset_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    escalation_after_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=24)
    escalate_to_role_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    parent_followup_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    return_to_followup_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    sla_paused: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
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
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class FollowUpLink(Base):
    """Explicit parent-child link with return routing (AC-003)."""

    __tablename__ = "flu_parent_child_links"
    __table_args__ = (
        UniqueConstraint("parent_followup_id", "child_followup_id", name="uq_flu_parent_child"),
        Index("ix_flu_links_parent", "organization_id", "parent_followup_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    parent_followup_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    child_followup_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    link_type: Mapped[str] = mapped_column(String(32), nullable=False, default="child")
    mandatory: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    return_route: Mapped[str] = mapped_column(String(64), nullable=False, default="parent")
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ReminderEvent(Base):
    __tablename__ = "flu_reminders"
    __table_args__ = (
        Index("ix_flu_reminders_followup", "organization_id", "followup_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    followup_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    scheduled_for: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="scheduled")
    channel: Mapped[str] = mapped_column(String(32), nullable=False, default="in_app")
    triggered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class EscalationEvent(Base):
    __tablename__ = "flu_escalations"
    __table_args__ = (
        Index("ix_flu_escalations_followup", "organization_id", "followup_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    followup_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    escalate_to_role_code: Mapped[str] = mapped_column(String(64), nullable=False)
    escalate_to_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    triggered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)


class SlaPause(Base):
    __tablename__ = "flu_sla_pauses"
    __table_args__ = (
        Index("ix_flu_sla_pauses_followup", "organization_id", "followup_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    followup_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    responsible_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    next_action: Mapped[str] = mapped_column(String(255), nullable=False)
    review_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    paused_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    resumed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resumed_by_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)


class BusinessDeadline(Base):
    """Computed business-time deadline snapshot for a follow-up."""

    __tablename__ = "flu_business_deadlines"
    __table_args__ = (
        UniqueConstraint("followup_id", name="uq_flu_business_deadlines_followup"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    followup_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    calendar_code: Mapped[str] = mapped_column(String(64), nullable=False, default="default")
    due_offset_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    wall_clock_due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    business_due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ClosureEvidence(Base):
    __tablename__ = "flu_closure_evidence"
    __table_args__ = (
        Index("ix_flu_closure_followup", "organization_id", "followup_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    followup_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    evidence_ref: Mapped[str] = mapped_column(String(512), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(64), nullable=False, default="response")
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
