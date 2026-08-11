"""Follow-up API schemas (MOD-340)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class FollowUpCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    source_entity_type: str = Field(min_length=1, max_length=64)
    source_entity_id: UUID
    recipient_actor_id: UUID
    owner_actor_id: UUID
    required_response: str = Field(min_length=1, max_length=255)
    closure_condition: str = Field(min_length=1, max_length=255)
    due_at: datetime | None = None
    due_offset_hours: int = Field(default=24, ge=1, le=24 * 90)
    project_id: UUID | None = None
    direction: str = Field(default="outbound", pattern=r"^(outbound|inbound)$")
    rule_version_id: UUID | None = None
    reminder_offset_hours: int = Field(default=4, ge=0, le=24 * 30)
    escalation_after_hours: int = Field(default=24, ge=0, le=24 * 90)
    escalate_to_role_code: str | None = Field(default=None, max_length=64)
    parent_followup_id: UUID | None = None
    return_to_followup_id: UUID | None = None
    calendar_code: str = Field(default="default", max_length=64)


class FollowUpRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    project_id: UUID | None
    title: str
    direction: str
    source_entity_type: str
    source_entity_id: UUID
    source_actor_id: UUID
    recipient_actor_id: UUID
    owner_actor_id: UUID
    required_response: str
    closure_condition: str
    status: str
    due_at: datetime
    rule_version_id: UUID | None
    reminder_rule_code: str | None
    escalation_rule_code: str | None
    reminder_offset_hours: int
    escalation_after_hours: int
    escalate_to_role_code: str | None
    parent_followup_id: UUID | None
    return_to_followup_id: UUID | None
    sla_paused: bool
    version: int
    created_at: datetime
    updated_at: datetime
    closed_at: datetime | None


class ChildLinkCreate(BaseModel):
    child_followup_id: UUID
    mandatory: bool = True
    return_route: str = Field(default="parent", max_length=64)
    link_type: str = Field(default="child", max_length=32)


class LinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    parent_followup_id: UUID
    child_followup_id: UUID
    link_type: str
    mandatory: bool
    return_route: str
    created_at: datetime


class ReminderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    followup_id: UUID
    scheduled_for: datetime
    status: str
    channel: str
    triggered_at: datetime | None
    created_at: datetime


class EscalationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    followup_id: UUID
    escalate_to_role_code: str
    escalate_to_actor_id: UUID | None
    reason: str
    status: str
    triggered_at: datetime


class SlaPauseCreate(BaseModel):
    reason: str = Field(min_length=1)
    next_action: str = Field(min_length=1, max_length=255)
    review_at: datetime
    responsible_actor_id: UUID | None = None


class SlaPauseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    followup_id: UUID
    reason: str
    responsible_actor_id: UUID
    next_action: str
    review_at: datetime
    status: str
    paused_at: datetime
    resumed_at: datetime | None


class BusinessDeadlineRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    followup_id: UUID
    calendar_code: str
    due_offset_hours: int
    wall_clock_due_at: datetime
    business_due_at: datetime
    computed_at: datetime


class ClosureEvidenceCreate(BaseModel):
    evidence_ref: str = Field(min_length=1, max_length=512)
    evidence_type: str = Field(default="response", max_length=64)
    note: str | None = None


class ClosureEvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    followup_id: UUID
    evidence_ref: str
    evidence_type: str
    note: str | None
    created_by_actor_id: UUID
    created_at: datetime


class ProcessOverdueResult(BaseModel):
    followup_id: UUID
    reminders_created: int
    escalations_created: int
