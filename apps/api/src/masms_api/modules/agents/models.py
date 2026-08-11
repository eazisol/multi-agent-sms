"""Agent runtime entities (MOD-360).

PostgreSQL is the source of truth. LangGraph run ids are opaque stubs in M1.
Agents mutate only agr_* + outbox/audit — never other business tables.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
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


class AgentDefinition(Base):
    __tablename__ = "agr_agent_definitions"
    __table_args__ = (
        UniqueConstraint("organization_id", "code", name="uq_agr_definitions_org_code"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    department_code: Mapped[str] = mapped_column(String(64), nullable=False, default="general")
    authority_level: Mapped[str] = mapped_column(String(32), nullable=False, default="assist")
    supervisor_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
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


class PromptVersion(Base):
    __tablename__ = "agr_prompt_versions"
    __table_args__ = (
        UniqueConstraint(
            "definition_id", "version_number", name="uq_agr_prompt_definition_number"
        ),
        Index("ix_agr_prompt_definition", "organization_id", "definition_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    definition_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    prompt_text: Mapped[str] = mapped_column(Text, nullable=False)
    model_name: Mapped[str] = mapped_column(String(128), nullable=False, default="stub-model")
    temperature: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
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


class ToolPolicy(Base):
    __tablename__ = "agr_tool_policies"
    __table_args__ = (
        UniqueConstraint(
            "definition_id", "policy_key", name="uq_agr_tool_policy_definition_key"
        ),
        Index("ix_agr_tool_policy_definition", "organization_id", "definition_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    definition_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    policy_key: Mapped[str] = mapped_column(String(64), nullable=False, default="default")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    allowed_tools: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    denied_tools: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
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


class ContextProfile(Base):
    __tablename__ = "agr_context_profiles"
    __table_args__ = (
        UniqueConstraint(
            "definition_id", "code", name="uq_agr_context_definition_code"
        ),
        Index("ix_agr_context_definition", "organization_id", "definition_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    definition_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False, default="default")
    min_sources: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=2048)
    include_rules: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
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


class AgentRun(Base):
    __tablename__ = "agr_agent_runs"
    __table_args__ = (
        Index("ix_agr_runs_status", "organization_id", "status"),
        Index("ix_agr_runs_definition", "organization_id", "definition_id"),
        Index(
            "ix_agr_runs_related",
            "organization_id",
            "related_entity_type",
            "related_entity_id",
        ),
        UniqueConstraint(
            "organization_id",
            "idempotency_key",
            name="uq_agr_runs_org_idempotency",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    definition_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    agent_code: Mapped[str] = mapped_column(String(64), nullable=False)
    prompt_version_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    tool_policy_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    context_profile_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    related_entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    related_entity_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    langgraph_run_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    model_name: Mapped[str] = mapped_column(String(128), nullable=False, default="stub-model")
    prompt_version_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    input_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    output_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    sources_json: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    tools_used_json: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    cost_units: Mapped[float | None] = mapped_column(Float, nullable=True)
    review_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    correlation_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    idempotency_key: Mapped[str | None] = mapped_column(String(128), nullable=True)
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


class AgentReview(Base):
    __tablename__ = "agr_agent_reviews"
    __table_args__ = (
        Index("ix_agr_reviews_run", "organization_id", "run_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    run_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    reviewer_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    decision_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    outcome_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class AgentEvaluation(Base):
    __tablename__ = "agr_agent_evaluations"
    __table_args__ = (
        Index("ix_agr_evaluations_run", "organization_id", "run_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    run_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    rubric_code: Mapped[str] = mapped_column(String(64), nullable=False, default="default")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    evaluator_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    metrics_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
