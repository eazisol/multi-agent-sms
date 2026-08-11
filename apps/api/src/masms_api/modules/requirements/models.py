"""Requirement gathering models (MOD-230)."""

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
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON, Uuid

from masms_api.db import Base


class Questionnaire(Base):
    __tablename__ = "req_questionnaires"
    __table_args__ = (
        UniqueConstraint("organization_id", "code", name="uq_req_questionnaires_code"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    # draft | active | retired
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class QuestionnaireVersion(Base):
    """Published versions are immutable; edits require a new version."""

    __tablename__ = "req_questionnaire_versions"
    __table_args__ = (
        UniqueConstraint(
            "questionnaire_id", "version_number", name="uq_req_questionnaire_versions"
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    questionnaire_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("req_questionnaires.id"), nullable=False
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    # draft | published | superseded
    questions_json: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    # [{key, text, mandatory, answer_type}]
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class RequirementAnswer(Base):
    __tablename__ = "req_answers"
    __table_args__ = (
        UniqueConstraint(
            "questionnaire_version_id",
            "related_entity_type",
            "related_entity_id",
            "question_key",
            name="uq_req_answers_entity_question",
        ),
        Index(
            "ix_req_answers_entity",
            "organization_id",
            "related_entity_type",
            "related_entity_id",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    questionnaire_version_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("req_questionnaire_versions.id"), nullable=False
    )
    related_entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    related_entity_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    client_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    question_key: Mapped[str] = mapped_column(String(128), nullable=False)
    answer_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    explicitly_unavailable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    answered_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class ClarificationRequest(Base):
    __tablename__ = "req_clarification_requests"
    __table_args__ = (
        Index(
            "ix_req_clarifications_entity",
            "organization_id",
            "related_entity_type",
            "related_entity_id",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    questionnaire_version_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("req_questionnaire_versions.id"), nullable=False
    )
    related_entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    related_entity_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    question_key: Mapped[str] = mapped_column(String(128), nullable=False)
    question_text: Mapped[str] = mapped_column(String(512), nullable=False)
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    # open | answered | closed
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    response_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class CompletenessScore(Base):
    __tablename__ = "req_completeness_scores"
    __table_args__ = (
        Index(
            "ix_req_completeness_entity",
            "organization_id",
            "related_entity_type",
            "related_entity_id",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    questionnaire_version_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("req_questionnaire_versions.id"), nullable=False
    )
    related_entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    related_entity_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    mandatory_total: Mapped[int] = mapped_column(Integer, nullable=False)
    covered_count: Mapped[int] = mapped_column(Integer, nullable=False)
    percentage: Mapped[Decimal] = mapped_column(Numeric(5, 4), nullable=False)
    meets_threshold: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    gap_question_keys: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    computed_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class RequirementBrief(Base):
    """Approved briefs are immutable; changes require a new version."""

    __tablename__ = "req_requirement_briefs"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "related_entity_type",
            "related_entity_id",
            "version_number",
            name="uq_req_briefs_entity_version",
        ),
        Index(
            "ix_req_briefs_entity",
            "organization_id",
            "related_entity_type",
            "related_entity_id",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    related_entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    related_entity_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    client_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    questionnaire_version_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("req_questionnaire_versions.id"), nullable=True
    )
    completeness_score_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("req_completeness_scores.id"), nullable=True
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    # draft | pending_approval | approved | superseded
    approved_by_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
