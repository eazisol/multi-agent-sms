"""Project phases, milestones, dependencies, baselines, and forecasts (MOD-260)."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON, Uuid

from masms_api.db import Base


class Phase(Base):
    __tablename__ = "pm_phases"
    __table_args__ = (
        UniqueConstraint("project_id", "code", name="uq_pm_phases_code"),
        Index("ix_pm_phases_project", "organization_id", "project_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("prj_projects.id"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="planned")
    # planned | active | completed | cancelled
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    planned_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    planned_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Milestone(Base):
    __tablename__ = "pm_milestones"
    __table_args__ = (
        UniqueConstraint("phase_id", "code", name="uq_pm_milestones_code"),
        Index("ix_pm_milestones_phase", "organization_id", "phase_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("prj_projects.id"), nullable=False
    )
    phase_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("pm_phases.id"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    target_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="planned")
    # planned | in_progress | pending_approval | completed | cancelled
    requires_approval: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    approved_by_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Deliverable(Base):
    __tablename__ = "pm_deliverables"
    __table_args__ = (
        UniqueConstraint("phase_id", "code", name="uq_pm_deliverables_code"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("prj_projects.id"), nullable=False
    )
    phase_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("pm_phases.id"), nullable=False
    )
    milestone_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("pm_milestones.id"), nullable=True
    )
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="planned")
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class PhaseDependency(Base):
    __tablename__ = "pm_phase_dependencies"
    __table_args__ = (
        UniqueConstraint(
            "predecessor_phase_id",
            "successor_phase_id",
            name="uq_pm_phase_dependencies",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("prj_projects.id"), nullable=False
    )
    predecessor_phase_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("pm_phases.id"), nullable=False
    )
    successor_phase_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("pm_phases.id"), nullable=False
    )
    dependency_type: Mapped[str] = mapped_column(
        String(32), nullable=False, default="finish_to_start"
    )
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class RequirementPhaseMap(Base):
    """Maps approved requirements to phases (AC-001)."""

    __tablename__ = "pm_requirement_phase_maps"
    __table_args__ = (
        UniqueConstraint(
            "requirement_id", "phase_id", name="uq_pm_requirement_phase_maps"
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("prj_projects.id"), nullable=False
    )
    requirement_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("prj_requirements.id"), nullable=False
    )
    phase_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("pm_phases.id"), nullable=False
    )
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ProjectPlanBaseline(Base):
    __tablename__ = "pm_project_baselines"
    __table_args__ = (
        UniqueConstraint("project_id", "version_number", name="uq_pm_project_baselines"),
        Index("ix_pm_baselines_project", "organization_id", "project_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("prj_projects.id"), nullable=False
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    # draft | approved | superseded
    snapshot_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    approved_by_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Forecast(Base):
    __tablename__ = "pm_forecasts"
    __table_args__ = (Index("ix_pm_forecasts_project", "organization_id", "project_id"),)

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("prj_projects.id"), nullable=False
    )
    phase_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("pm_phases.id"), nullable=True
    )
    forecast_type: Mapped[str] = mapped_column(String(32), nullable=False, default="completion")
    # completion | effort | cost
    predicted_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    predicted_value: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    confidence: Mapped[Decimal] = mapped_column(
        Numeric(5, 4), nullable=False, default=Decimal("0.5")
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
