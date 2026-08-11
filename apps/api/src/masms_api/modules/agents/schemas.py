"""Agent runtime API schemas (MOD-360)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DefinitionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    description: str | None
    status: str
    department_code: str
    authority_level: str
    supervisor_actor_id: UUID | None
    created_at: datetime


class PromptVersionCreate(BaseModel):
    prompt_text: str = Field(min_length=1)
    model_name: str = Field(default="stub-model", max_length=128)
    temperature: float = Field(default=0.0, ge=0.0, le=2.0)


class PromptVersionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    definition_id: UUID
    version_number: int
    status: str
    prompt_text: str
    model_name: str
    temperature: float
    created_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class ToolPolicyCreate(BaseModel):
    policy_key: str = Field(default="default", min_length=1, max_length=64)
    allowed_tools: list[Any] = Field(default_factory=list)
    denied_tools: list[Any] = Field(default_factory=list)


class ToolPolicyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    definition_id: UUID
    policy_key: str
    status: str
    allowed_tools: list[Any]
    denied_tools: list[Any]
    created_by_actor_id: UUID
    created_at: datetime


class ContextProfileCreate(BaseModel):
    code: str = Field(default="default", min_length=1, max_length=64)
    min_sources: int = Field(default=0, ge=0)
    max_tokens: int = Field(default=2048, ge=1)
    include_rules: dict[str, Any] = Field(default_factory=dict)


class ContextProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    definition_id: UUID
    code: str
    min_sources: int
    max_tokens: int
    include_rules: dict[str, Any]
    status: str
    created_by_actor_id: UUID
    created_at: datetime


class RunCreate(BaseModel):
    agent_code: str = Field(min_length=1, max_length=64)
    related_entity_type: str = Field(min_length=1, max_length=64)
    related_entity_id: UUID
    project_id: UUID | None = None
    owner_actor_id: UUID | None = None
    input_json: dict[str, Any] = Field(default_factory=dict)
    prompt_version_id: UUID | None = None
    tool_policy_id: UUID | None = None
    context_profile_id: UUID | None = None
    idempotency_key: str | None = Field(default=None, max_length=128)


class RunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    definition_id: UUID
    agent_code: str
    prompt_version_id: UUID
    tool_policy_id: UUID | None
    context_profile_id: UUID | None
    related_entity_type: str
    related_entity_id: UUID
    status: str
    langgraph_run_id: str | None
    model_name: str
    prompt_version_number: int
    input_json: dict[str, Any]
    output_json: dict[str, Any]
    sources_json: list[Any]
    tools_used_json: list[Any]
    confidence: float | None
    cost_units: float | None
    review_required: bool
    owner_actor_id: UUID
    correlation_id: UUID
    version: int
    created_at: datetime
    updated_at: datetime
    closed_at: datetime | None


class FailRun(BaseModel):
    reason: str = Field(min_length=1)
    expected_version: int | None = None


class ReviewCreate(BaseModel):
    decision: str = Field(min_length=1, max_length=32)
    decision_reason: str | None = None
    outcome_json: dict[str, Any] = Field(default_factory=dict)
    expected_version: int | None = None


class ReviewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    run_id: UUID
    status: str
    reviewer_actor_id: UUID
    decision_reason: str | None
    outcome_json: dict[str, Any]
    created_at: datetime


class EvaluationCreate(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    rubric_code: str = Field(default="default", max_length=64)
    notes: str | None = None
    metrics_json: dict[str, Any] = Field(default_factory=dict)


class EvaluationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    run_id: UUID
    score: float
    rubric_code: str
    notes: str | None
    evaluator_actor_id: UUID
    metrics_json: dict[str, Any]
    created_at: datetime
