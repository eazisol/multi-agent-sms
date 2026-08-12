"""API schemas for MOD-620 UAT evaluation."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SampleProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    workflow_status: str
    created_by_actor_id: UUID
    created_at: datetime


class SampleGateRead(BaseModel):
    passed_count: int
    required_count: int
    gate_passed: bool


class AgentQualityRead(BaseModel):
    evaluation_id: UUID | None
    target_pct: int
    latest_score: int | None
    meets_target: bool


class SeedScriptCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    sample_project_code: str = Field(min_length=1, max_length=64)
    status: str = Field(default="registered", min_length=1, max_length=32)
    checksum: str | None = Field(default=None, max_length=128)


class SeedScriptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    sample_project_code: str
    status: str
    checksum: str | None
    version: int
    created_by_actor_id: UUID
    updated_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class ExpectedDecisionCreate(BaseModel):
    decision_key: str = Field(min_length=1, max_length=128)
    expected_outcome: str = Field(min_length=1)
    seed_script_id: UUID | None = None
    status: str = Field(default="pending", min_length=1, max_length=32)


class ExpectedDecisionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    seed_script_id: UUID | None
    decision_key: str
    expected_outcome: str
    status: str
    created_by_actor_id: UUID
    created_at: datetime


class AgentEvaluationCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    agent_code: str = Field(min_length=1, max_length=64)
    accuracy_pct: int = Field(ge=0, le=100)
    sample_count: int = Field(default=0, ge=0)
    status: str | None = Field(default=None, max_length=32)
    notes: str | None = None


class AgentEvaluationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    agent_code: str
    accuracy_pct: int
    sample_count: int
    status: str
    notes: str | None
    created_by_actor_id: UUID
    created_at: datetime


class E2eTestCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    suite_name: str = Field(min_length=1, max_length=255)
    result: str = Field(min_length=1, max_length=32)
    evidence: str | None = None


class E2eTestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    suite_name: str
    result: str
    evidence: str | None
    created_by_actor_id: UUID
    created_at: datetime


class RoleUatCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    role_code: str = Field(min_length=1, max_length=64)
    scenario: str = Field(min_length=1, max_length=255)
    result: str = Field(min_length=1, max_length=32)
    tester_actor_id: UUID


class RoleUatRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    role_code: str
    scenario: str
    result: str
    tester_actor_id: UUID
    created_by_actor_id: UUID
    created_at: datetime


class AcceptanceEvidenceCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    evidence_ref: str = Field(min_length=1, max_length=512)
    status: str = Field(default="draft", min_length=1, max_length=32)


class AcceptanceEvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    evidence_ref: str
    status: str
    submitted_by_actor_id: UUID
    accepted_by_actor_id: UUID | None
    version: int
    created_at: datetime
    updated_at: datetime


class AcceptanceEvidenceAccept(BaseModel):
    expected_version: int | None = None
