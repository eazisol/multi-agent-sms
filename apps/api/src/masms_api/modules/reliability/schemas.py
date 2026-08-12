"""API schemas for MOD-610 reliability."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PerformanceTestCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    suite_name: str = Field(min_length=1, max_length=255)
    p95_ms: int | None = Field(default=None, ge=0)
    sample_count: int | None = Field(default=None, ge=0)
    samples: list[int] | None = None
    status: str | None = Field(default=None, max_length=32)
    notes: str | None = None


class PerformanceTestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    suite_name: str
    p95_ms: int
    sample_count: int
    samples_json: list[int] | None = None
    status: str
    notes: str | None
    version: int
    created_by_actor_id: UUID
    created_at: datetime


class ResilienceTestCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    scenario: str = Field(min_length=1, max_length=255)
    result: str = Field(min_length=1, max_length=32)
    evidence: str | None = None


class ResilienceTestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    scenario: str
    result: str
    evidence: str | None
    created_by_actor_id: UUID
    created_at: datetime


class IndexReviewCreate(BaseModel):
    table_name: str = Field(min_length=1, max_length=128)
    index_name: str = Field(min_length=1, max_length=128)
    recommendation: str = Field(min_length=1, max_length=32)
    status: str = Field(default="open", min_length=1, max_length=32)
    notes: str | None = None


class IndexReviewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    table_name: str
    index_name: str
    recommendation: str
    status: str
    notes: str | None
    created_by_actor_id: UUID
    created_at: datetime


class SloDashboardUpsert(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    dashboard_p95_ms: int | None = Field(default=None, ge=0)
    api_p95_ms: int | None = Field(default=None, ge=0)
    samples: list[int] | None = None
    status: str = Field(default="active", min_length=1, max_length=32)


class SloDashboardRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    name: str
    dashboard_p95_ms: int
    api_p95_ms: int | None
    samples_json: list[int] | None = None
    status: str
    version: int
    created_by_actor_id: UUID
    updated_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class WorkflowReplayCreate(BaseModel):
    workflow_name: str = Field(min_length=1, max_length=128)
    idempotency_key: str = Field(min_length=1, max_length=128)


class WorkflowReplayRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    workflow_name: str
    idempotency_key: str
    status: str
    attempt_count: int
    last_error: str | None
    version: int
    created_by_actor_id: UUID
    updated_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class WorkflowReplayFail(BaseModel):
    last_error: str | None = None
    expected_version: int | None = None


class WorkflowReplayAction(BaseModel):
    expected_version: int | None = None


class IntegrationFailureTestCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    provider: str = Field(min_length=1, max_length=64)
    result: str = Field(min_length=1, max_length=32)
    failure_mode: str = Field(min_length=1, max_length=128)
    recovered: bool = False


class IntegrationFailureTestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    provider: str
    result: str
    failure_mode: str
    recovered: bool
    created_by_actor_id: UUID
    created_at: datetime


class DrRunbookCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    rto_minutes: int = Field(ge=0)
    rpo_minutes: int = Field(ge=0)
    status: str = Field(default="draft", min_length=1, max_length=32)
    body_preview: str | None = None


class DrRunbookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    rto_minutes: int
    rpo_minutes: int
    status: str
    body_preview: str | None
    version: int
    created_by_actor_id: UUID
    updated_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class DrRunbookApprove(BaseModel):
    expected_version: int | None = None


class ApiSloRead(BaseModel):
    performance_test_id: UUID | None
    p95_ms: int | None
    sample_count: int
    budget_ms: int
    slo_met: bool


class DashboardSloRead(BaseModel):
    slo_dashboard_id: UUID | None
    dashboard_p95_ms: int | None
    sample_count: int
    budget_ms: int
    slo_met: bool
