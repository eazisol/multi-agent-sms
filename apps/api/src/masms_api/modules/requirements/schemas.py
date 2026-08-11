"""Requirement gathering API schemas (MOD-230)."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class QuestionItem(BaseModel):
    key: str = Field(min_length=1, max_length=128)
    text: str = Field(min_length=1, max_length=512)
    mandatory: bool = True
    answer_type: str = Field(default="text", max_length=32)


class QuestionnaireCreate(BaseModel):
    code: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    title: str = Field(min_length=2, max_length=255)


class QuestionnaireRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    status: str
    created_at: datetime


class QuestionnaireVersionCreate(BaseModel):
    questionnaire_id: UUID
    questions: list[QuestionItem] = Field(min_length=1)


class QuestionnaireVersionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    questionnaire_id: UUID
    version_number: int
    status: str
    questions_json: list[dict[str, Any]]
    published_at: datetime | None
    created_at: datetime


class AnswerUpsert(BaseModel):
    questionnaire_version_id: UUID
    related_entity_type: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    related_entity_id: UUID
    question_key: str = Field(min_length=1, max_length=128)
    answer_text: str | None = None
    explicitly_unavailable: bool = False
    client_id: UUID | None = None
    project_id: UUID | None = None


class AnswerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    questionnaire_version_id: UUID
    related_entity_type: str
    related_entity_id: UUID
    question_key: str
    answer_text: str | None
    explicitly_unavailable: bool
    client_id: UUID | None
    project_id: UUID | None
    created_at: datetime
    updated_at: datetime


class CompletenessCompute(BaseModel):
    questionnaire_version_id: UUID
    related_entity_type: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    related_entity_id: UUID


class CompletenessScoreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    questionnaire_version_id: UUID
    related_entity_type: str
    related_entity_id: UUID
    mandatory_total: int
    covered_count: int
    percentage: Decimal
    meets_threshold: bool
    gap_question_keys: list[str]
    computed_at: datetime


class ClarificationCreate(BaseModel):
    questionnaire_version_id: UUID
    related_entity_type: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    related_entity_id: UUID
    question_key: str = Field(min_length=1, max_length=128)
    question_text: str = Field(min_length=1, max_length=512)
    owner_actor_id: UUID
    due_at: datetime | None = None


class ClarificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    questionnaire_version_id: UUID
    related_entity_type: str
    related_entity_id: UUID
    question_key: str
    question_text: str
    owner_actor_id: UUID
    status: str
    due_at: datetime | None
    response_text: str | None
    created_at: datetime


class BriefCreate(BaseModel):
    related_entity_type: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_]+$")
    related_entity_id: UUID
    title: str = Field(min_length=2, max_length=255)
    summary: str = Field(min_length=1)
    questionnaire_version_id: UUID | None = None
    completeness_score_id: UUID | None = None
    client_id: UUID | None = None
    project_id: UUID | None = None


class BriefRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    related_entity_type: str
    related_entity_id: UUID
    version_number: int
    title: str
    summary: str
    status: str
    questionnaire_version_id: UUID | None
    completeness_score_id: UUID | None
    approved_by_actor_id: UUID | None
    approved_at: datetime | None
    client_id: UUID | None
    project_id: UUID | None
    created_at: datetime
