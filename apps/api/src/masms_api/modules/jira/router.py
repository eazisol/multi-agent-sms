"""HTTP routes for MOD-520 Jira integration."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.jira.schemas import (
    JiraCommentSyncCreate,
    JiraCommentSyncRead,
    JiraIssuePushCreate,
    JiraIssuePushRead,
    JiraStatusConflictRead,
    JiraStatusWebhookIn,
)
from masms_api.modules.jira.service import JiraService

router = APIRouter(prefix="/jira", tags=["jira"])


class JiraIssuePushPage(BaseModel):
    items: list[JiraIssuePushRead]
    page: PageMeta = Field(description="Pagination metadata")


class JiraCommentSyncPage(BaseModel):
    items: list[JiraCommentSyncRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> JiraService:
    return JiraService(db, ctx)


@router.post("/issues/push", response_model=JiraIssuePushRead, status_code=201)
def push_issue(
    body: JiraIssuePushCreate, service: JiraService = Depends(_service)
) -> JiraIssuePushRead:
    return JiraIssuePushRead.model_validate(service.push_issue(body))


@router.get("/issues/pushes", response_model=JiraIssuePushPage)
def list_issue_pushes(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: JiraService = Depends(_service),
) -> JiraIssuePushPage:
    items, page = service.list_issue_pushes(limit=limit, offset=offset)
    return JiraIssuePushPage(
        items=[JiraIssuePushRead.model_validate(item) for item in items], page=page
    )


@router.post("/webhooks/status", response_model=JiraStatusConflictRead)
def receive_status_webhook(
    body: JiraStatusWebhookIn,
    response: Response,
    service: JiraService = Depends(_service),
) -> JiraStatusConflictRead:
    conflict = service.receive_status_webhook(body)
    response.status_code = status.HTTP_409_CONFLICT
    return JiraStatusConflictRead.model_validate(conflict)


@router.post("/comments/sync", response_model=JiraCommentSyncRead, status_code=201)
def create_comment_sync(
    body: JiraCommentSyncCreate, service: JiraService = Depends(_service)
) -> JiraCommentSyncRead:
    return JiraCommentSyncRead.model_validate(service.create_comment_sync(body))


@router.get("/comments/sync", response_model=JiraCommentSyncPage)
def list_comment_syncs(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: JiraService = Depends(_service),
) -> JiraCommentSyncPage:
    items, page = service.list_comment_syncs(limit=limit, offset=offset)
    return JiraCommentSyncPage(
        items=[JiraCommentSyncRead.model_validate(item) for item in items], page=page
    )


@router.post("/comments/sync/{sync_id}/retry", response_model=JiraCommentSyncRead)
def retry_comment_sync(
    sync_id: UUID, service: JiraService = Depends(_service)
) -> JiraCommentSyncRead:
    return JiraCommentSyncRead.model_validate(service.retry_comment_sync(sync_id))
