"""Configuration administration models (MOD-140)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
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


class ConfigurationVersion(Base):
    """Versioned config bundle. Only status=effective controls live execution."""

    __tablename__ = "cfg_configuration_versions"
    __table_args__ = (
        UniqueConstraint("organization_id", "version_number", name="uq_cfg_versions_org_num"),
        Index("ix_cfg_versions_status", "organization_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    # draft | approved | effective | superseded | rolled_back
    based_on_version_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    change_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    approved_by_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    effective_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    superseded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rolled_back_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class WorkflowDefinition(Base):
    __tablename__ = "cfg_workflow_definitions"
    __table_args__ = (
        UniqueConstraint(
            "configuration_version_id", "code", name="uq_cfg_workflows_version_code"
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    configuration_version_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("cfg_configuration_versions.id"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class StatusDefinition(Base):
    __tablename__ = "cfg_status_definitions"
    __table_args__ = (
        UniqueConstraint(
            "workflow_definition_id", "code", name="uq_cfg_statuses_workflow_code"
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    configuration_version_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("cfg_configuration_versions.id"), nullable=False
    )
    workflow_definition_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("cfg_workflow_definitions.id"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    is_terminal: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class TransitionRule(Base):
    __tablename__ = "cfg_transition_rules"
    __table_args__ = (
        UniqueConstraint(
            "workflow_definition_id",
            "from_status_code",
            "to_status_code",
            name="uq_cfg_transitions_edge",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    configuration_version_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("cfg_configuration_versions.id"), nullable=False
    )
    workflow_definition_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("cfg_workflow_definitions.id"), nullable=False
    )
    from_status_code: Mapped[str] = mapped_column(String(64), nullable=False)
    to_status_code: Mapped[str] = mapped_column(String(64), nullable=False)
    requires_reason: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class FollowUpRule(Base):
    __tablename__ = "cfg_followup_rules"
    __table_args__ = (
        Index("ix_cfg_followup_version", "configuration_version_id", "workflow_code"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    configuration_version_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("cfg_configuration_versions.id"), nullable=False
    )
    workflow_code: Mapped[str] = mapped_column(String(64), nullable=False)
    trigger_status_code: Mapped[str] = mapped_column(String(64), nullable=False)
    due_offset_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=24)
    required_response: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ReminderRule(Base):
    __tablename__ = "cfg_reminder_rules"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    configuration_version_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("cfg_configuration_versions.id"), nullable=False
    )
    workflow_code: Mapped[str] = mapped_column(String(64), nullable=False)
    offset_hours_before_due: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    channel: Mapped[str] = mapped_column(String(32), nullable=False, default="in_app")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class EscalationRule(Base):
    __tablename__ = "cfg_escalation_rules"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    configuration_version_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("cfg_configuration_versions.id"), nullable=False
    )
    workflow_code: Mapped[str] = mapped_column(String(64), nullable=False)
    after_hours_overdue: Mapped[int] = mapped_column(Integer, nullable=False, default=24)
    escalate_to_role_code: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ApprovalWorkflowConfig(Base):
    __tablename__ = "cfg_approval_workflows"
    __table_args__ = (
        UniqueConstraint(
            "configuration_version_id", "code", name="uq_cfg_approval_wf_version_code"
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    configuration_version_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("cfg_configuration_versions.id"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    action_code: Mapped[str] = mapped_column(String(128), nullable=False)
    steps_json: Mapped[list[dict[str, Any]]] = mapped_column("steps", JSON, default=list)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
