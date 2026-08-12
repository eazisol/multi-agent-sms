"""API schemas for MOD-600 security hardening."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ThreatModelCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    scope_summary: str = Field(min_length=1)
    status: str = Field(default="draft", min_length=1, max_length=32)
    owner_actor_id: UUID | None = None


class ThreatModelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    scope_summary: str
    status: str
    version: int
    owner_actor_id: UUID
    created_by_actor_id: UUID
    updated_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class PiiInventoryCreate(BaseModel):
    data_category: str = Field(min_length=1, max_length=128)
    field_path: str = Field(min_length=1, max_length=255)
    classification: str = Field(min_length=1, max_length=32)
    purpose: str = Field(min_length=1)
    retention_days: int | None = Field(default=None, ge=0)


class PiiInventoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    data_category: str
    field_path: str
    classification: str
    purpose: str
    retention_days: int | None
    created_at: datetime


class RetentionPolicyCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    entity_type: str = Field(min_length=1, max_length=64)
    retain_days: int = Field(ge=0)
    action: str = Field(min_length=1, max_length=32)
    status: str = Field(default="draft", min_length=1, max_length=32)


class RetentionPolicyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    entity_type: str
    retain_days: int
    action: str
    status: str
    version: int
    created_by_actor_id: UUID
    updated_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class LegalHoldCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    reason: str = Field(min_length=1)
    scope_json: dict[str, Any] = Field(default_factory=dict)
    held_entity_type: str | None = Field(default=None, max_length=64)
    held_entity_id: UUID | None = None


class LegalHoldRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    reason: str
    scope_json: dict[str, Any]
    status: str
    held_entity_type: str | None
    held_entity_id: UUID | None
    created_by_actor_id: UUID
    released_by_actor_id: UUID | None
    created_at: datetime
    released_at: datetime | None


class DeletionJobCreate(BaseModel):
    target_entity_type: str = Field(min_length=1, max_length=64)
    retention_policy_id: UUID | None = None
    target_entity_id: UUID | None = None
    simulated_rows: int = Field(default=1, ge=0)


class DeletionJobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    retention_policy_id: UUID | None
    target_entity_type: str
    status: str
    blocked_reason: str | None
    rows_affected: int
    created_by_actor_id: UUID
    created_at: datetime
    completed_at: datetime | None


class BackupRecordCreate(BaseModel):
    backup_ref: str = Field(min_length=1, max_length=255)
    environment: str = Field(min_length=1, max_length=32)
    rpo_minutes: int = Field(ge=0)
    rto_minutes: int = Field(ge=0)
    status: str = Field(default="recorded", min_length=1, max_length=32)


class BackupRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    backup_ref: str
    environment: str
    rpo_minutes: int
    rto_minutes: int
    status: str
    created_by_actor_id: UUID
    created_at: datetime


class RestoreTestCreate(BaseModel):
    backup_record_id: UUID
    measured_rpo_minutes: int = Field(ge=0)
    measured_rto_minutes: int = Field(ge=0)
    notes: str | None = None


class RestoreTestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    backup_record_id: UUID
    measured_rpo_minutes: int
    measured_rto_minutes: int
    result: str
    notes: str | None
    tested_by_actor_id: UUID
    created_at: datetime


class SecurityIncidentCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=255)
    severity: str = Field(min_length=1, max_length=32)
    summary: str = Field(min_length=1)
    status: str = Field(default="open", min_length=1, max_length=32)


class SecurityIncidentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    severity: str
    status: str
    summary: str
    version: int
    created_by_actor_id: UUID
    updated_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class SecurityIncidentClose(BaseModel):
    expected_version: int | None = None
    summary: str | None = None


class TrainingPolicyUpdate(BaseModel):
    allow_model_training: bool
    human_approval_evidence: str | None = None


class TrainingPolicyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    allow_model_training: bool
    approval_evidence: str | None
    updated_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class SecurityGateRead(BaseModel):
    critical_open_count: int
    gate_passed: bool


class RecoveryValidationRead(BaseModel):
    backup_record_id: UUID | None
    restore_test_id: UUID | None
    target_rpo_minutes: int | None
    target_rto_minutes: int | None
    measured_rpo_minutes: int | None
    measured_rto_minutes: int | None
    rpo_met: bool
    rto_met: bool
    validated: bool
