"""Test case entities (MOD-400)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON, Uuid

from masms_api.db import Base


class TestCase(Base):
    __tablename__ = "tc_cases"
    __table_args__ = (
        UniqueConstraint("organization_id", "code", name="uq_tc_cases_org_code"),
        Index("ix_tc_cases_status", "organization_id", "status"),
        Index("ix_tc_cases_project", "organization_id", "project_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    case_type: Mapped[str] = mapped_column(String(32), nullable=False, default="functional")
    priority: Mapped[str] = mapped_column(String(8), nullable=False, default="P2")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    preconditions: Mapped[str | None] = mapped_column(Text, nullable=True)
    expected_result: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
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


class TestStep(Base):
    __tablename__ = "tc_steps"
    __table_args__ = (
        UniqueConstraint("case_id", "step_number", name="uq_tc_steps_case_number"),
        Index("ix_tc_steps_case", "organization_id", "case_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    case_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    step_number: Mapped[int] = mapped_column(Integer, nullable=False)
    action_text: Mapped[str] = mapped_column(Text, nullable=False)
    expected_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class TestSuite(Base):
    __tablename__ = "tc_suites"
    __table_args__ = (
        UniqueConstraint("organization_id", "code", name="uq_tc_suites_org_code"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    case_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
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


class TestPlan(Base):
    __tablename__ = "tc_plans"
    __table_args__ = (
        UniqueConstraint("organization_id", "code", name="uq_tc_plans_org_code"),
        Index("ix_tc_plans_status", "organization_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    environment_code: Mapped[str] = mapped_column(String(64), nullable=False, default="local")
    build_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    suite_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
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


class TestRun(Base):
    __tablename__ = "tc_runs"
    __table_args__ = (
        Index("ix_tc_runs_status", "organization_id", "status"),
        Index("ix_tc_runs_case", "organization_id", "case_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    case_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    plan_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    environment_code: Mapped[str] = mapped_column(String(64), nullable=False, default="local")
    build_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    result_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    executed_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class TestEvidence(Base):
    __tablename__ = "tc_evidence"
    __table_args__ = (
        Index("ix_tc_evidence_run", "organization_id", "run_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    run_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(32), nullable=False, default="note")
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    uri: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    environment_code: Mapped[str] = mapped_column(String(64), nullable=False, default="local")
    build_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class TestCoverageLink(Base):
    __tablename__ = "tc_coverage_links"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "case_id",
            "requirement_id",
            name="uq_tc_coverage_case_requirement",
        ),
        Index("ix_tc_coverage_case", "organization_id", "case_id"),
        Index("ix_tc_coverage_requirement", "organization_id", "requirement_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    case_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    requirement_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    requirement_priority: Mapped[str] = mapped_column(
        String(32), nullable=False, default="Must-Have"
    )
    coverage_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
