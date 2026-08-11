"""Client query / opportunity models (MOD-210)."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
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


class QuerySource(Base):
    __tablename__ = "crm_query_sources"
    __table_args__ = (
        UniqueConstraint("organization_id", "code", name="uq_crm_query_sources_code"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    channel: Mapped[str] = mapped_column(String(64), nullable=False, default="email")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ClientQuery(Base):
    """Inbound inquiry. project_id may be null until conversion (pre-project)."""

    __tablename__ = "crm_queries"
    __table_args__ = (
        Index("ix_crm_queries_status", "organization_id", "status"),
        Index("ix_crm_queries_client", "organization_id", "client_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    client_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    contact_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    source_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("crm_query_sources.id"), nullable=True
    )
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    original_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="received")
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    classification: Mapped[str | None] = mapped_column(String(64), nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    # First-response SLA
    sla_due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    first_responded_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    sla_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    # pending | met | breached
    opportunity_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    updated_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class Opportunity(Base):
    __tablename__ = "crm_opportunities"
    __table_args__ = (Index("ix_crm_opportunities_query", "organization_id", "query_id"),)

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    query_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("crm_queries.id"), nullable=False
    )
    client_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    estimated_value: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    conversion_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class QualificationAnswer(Base):
    __tablename__ = "crm_qualification_answers"
    __table_args__ = (
        UniqueConstraint(
            "query_id", "question_key", name="uq_crm_qualification_query_question"
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    query_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("crm_queries.id"), nullable=False
    )
    question_key: Mapped[str] = mapped_column(String(128), nullable=False)
    question_text: Mapped[str] = mapped_column(String(512), nullable=False)
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    answered_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class QueryStatusHistory(Base):
    __tablename__ = "crm_query_status_history"
    __table_args__ = (Index("ix_crm_query_history_query", "organization_id", "query_id"),)

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    query_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("crm_queries.id"), nullable=False
    )
    previous_status: Mapped[str] = mapped_column(String(32), nullable=False)
    next_status: Mapped[str] = mapped_column(String(32), nullable=False)
    actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    rule_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    evidence_json: Mapped[dict[str, Any]] = mapped_column("evidence", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
