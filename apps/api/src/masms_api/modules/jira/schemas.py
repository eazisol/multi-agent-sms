"""API schemas for MOD-520 Jira integration."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class JiraIssuePushCreate(BaseModel):
    internal_ticket_id: UUID
    summary: str = Field(min_length=1, max_length=512)
    approval_status: str = Field(min_length=1, max_length=32)
    simulated_jira_key: str | None = Field(default=None, max_length=64)


class JiraIssuePushRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    internal_ticket_id: UUID
    jira_issue_key: str
    summary: str
    approval_status: str
    push_status: str
    version: int
    created_by_actor_id: UUID
    updated_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class JiraStatusWebhookIn(BaseModel):
    issue_push_id: UUID
    external_status: str = Field(min_length=1, max_length=64)
    attempted_internal_status: str | None = Field(default=None, max_length=64)


class JiraStatusConflictRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    issue_push_id: UUID
    external_status: str
    attempted_internal_status: str | None
    conflict_reason: str
    created_by_actor_id: UUID
    created_at: datetime


class JiraCommentSyncCreate(BaseModel):
    issue_push_id: UUID
    comment_text: str = Field(min_length=1)
    force_fail: bool = False


class JiraCommentSyncRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    issue_push_id: UUID
    comment_text: str
    sync_status: str
    retry_count: int
    failure_reason: str | None
    last_attempt_at: datetime | None
    created_by_actor_id: UUID
    updated_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime
