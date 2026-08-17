"""Testcases API schemas (MOD-400)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CaseCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    project_id: UUID | None = None
    case_type: str = Field(default="functional", max_length=32)
    priority: str = Field(default="P2", max_length=8)
    preconditions: str | None = None
    expected_result: str | None = None
    owner_actor_id: UUID | None = None
    steps: list[StepCreate] = Field(default_factory=list)


class CaseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    code: str
    title: str
    description: str | None
    case_type: str
    priority: str
    status: str
    preconditions: str | None
    expected_result: str | None
    owner_actor_id: UUID
    version: int
    created_at: datetime
    updated_at: datetime


class StepCreate(BaseModel):
    step_number: int = Field(ge=1)
    action_text: str = Field(min_length=1)
    expected_text: str | None = None


class StepRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    case_id: UUID
    step_number: int
    action_text: str
    expected_text: str | None
    created_at: datetime


class SuiteCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    project_id: UUID | None = None
    case_ids: list[UUID] = Field(default_factory=list)


class SuiteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    code: str
    title: str
    status: str
    case_ids: list[Any]
    owner_actor_id: UUID
    created_at: datetime


class PlanCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    project_id: UUID | None = None
    environment_code: str = Field(default="local", max_length=64)
    build_ref: str | None = None
    suite_ids: list[UUID] = Field(default_factory=list)


class PlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    code: str
    title: str
    status: str
    environment_code: str
    build_ref: str | None
    suite_ids: list[Any]
    owner_actor_id: UUID
    created_at: datetime


class RunCreate(BaseModel):
    case_id: UUID
    plan_id: UUID | None = None
    project_id: UUID | None = None
    environment_code: str = Field(default="local", max_length=64)
    build_ref: str | None = None


class RunComplete(BaseModel):
    status: str = Field(min_length=1, max_length=32)
    result_summary: str | None = None
    expected_version: int | None = None
    evidence_title: str | None = None
    evidence_body: str | None = None


class RunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    case_id: UUID
    plan_id: UUID | None
    status: str
    environment_code: str
    build_ref: str | None
    result_summary: str | None
    executed_by_actor_id: UUID
    version: int
    started_at: datetime | None
    finished_at: datetime | None
    created_at: datetime
    updated_at: datetime


class EvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    run_id: UUID
    evidence_type: str
    title: str
    body_text: str | None
    uri: str | None
    environment_code: str
    build_ref: str | None
    created_at: datetime


class CoverageCreate(BaseModel):
    requirement_id: UUID
    requirement_priority: str = Field(default="Must-Have", max_length=32)
    coverage_notes: str | None = None


class CoverageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    case_id: UUID
    requirement_id: UUID
    requirement_priority: str
    coverage_notes: str | None
    created_at: datetime


class CoverageSummary(BaseModel):
    must_have_total: int
    must_have_covered: int
    permission_negative_cases: int
    uncovered_must_have_requirement_ids: list[UUID]


CaseCreate.model_rebuild()
