"""HTTP routes for MOD-440 notifications."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.notifications.schemas import (
    DeadLetterRead,
    DigestCreate,
    DigestRead,
    MarkRead,
    NotificationCreate,
    NotificationRead,
    PreferenceRead,
    PreferenceUpsert,
    ProcessDigest,
    SimulateDeliver,
    TemplateCreate,
    TemplateRead,
)
from masms_api.modules.notifications.service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])


class NotificationPage(BaseModel):
    items: list[NotificationRead]
    page: PageMeta = Field(description="Pagination metadata")


class DeadLetterPage(BaseModel):
    items: list[DeadLetterRead]
    page: PageMeta = Field(description="Pagination metadata")


class DigestPage(BaseModel):
    items: list[DigestRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> NotificationService:
    return NotificationService(db, ctx)


@router.post("", response_model=NotificationRead, status_code=201)
def create_notification(
    body: NotificationCreate, service: NotificationService = Depends(_service)
) -> NotificationRead:
    return NotificationRead.model_validate(service.create_notification(body))


@router.get("", response_model=NotificationPage)
def list_notifications(
    status: str | None = Query(default=None),
    channel: str | None = Query(default=None),
    recipient_actor_id: UUID | None = Query(default=None),
    q: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: NotificationService = Depends(_service),
) -> NotificationPage:
    items, page = service.list_notifications(
        status=status,
        channel=channel,
        recipient_actor_id=recipient_actor_id,
        q=q,
        limit=limit,
        offset=offset,
    )
    return NotificationPage(
        items=[NotificationRead.model_validate(r) for r in items], page=page
    )


@router.get("/templates", response_model=list[TemplateRead])
def list_templates(
    service: NotificationService = Depends(_service),
) -> list[TemplateRead]:
    return [TemplateRead.model_validate(r) for r in service.list_templates()]


@router.post("/templates", response_model=TemplateRead, status_code=201)
def create_template(
    body: TemplateCreate, service: NotificationService = Depends(_service)
) -> TemplateRead:
    return TemplateRead.model_validate(service.create_template(body))


@router.get("/preferences", response_model=list[PreferenceRead])
def list_preferences(
    actor_id: UUID | None = Query(default=None),
    service: NotificationService = Depends(_service),
) -> list[PreferenceRead]:
    return [
        PreferenceRead.model_validate(r)
        for r in service.list_preferences(actor_id=actor_id)
    ]


@router.put("/preferences", response_model=PreferenceRead)
def upsert_preference(
    body: PreferenceUpsert, service: NotificationService = Depends(_service)
) -> PreferenceRead:
    return PreferenceRead.model_validate(service.upsert_preference(body))


@router.get("/dead-letters", response_model=DeadLetterPage)
def list_dead_letters(
    status: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: NotificationService = Depends(_service),
) -> DeadLetterPage:
    items, page = service.list_dead_letters(status=status, limit=limit, offset=offset)
    return DeadLetterPage(
        items=[DeadLetterRead.model_validate(r) for r in items], page=page
    )


@router.post("/dead-letters/{dead_letter_id}/replay", response_model=DeadLetterRead)
def replay_dead_letter(
    dead_letter_id: UUID, service: NotificationService = Depends(_service)
) -> DeadLetterRead:
    return DeadLetterRead.model_validate(service.replay_dead_letter(dead_letter_id))


@router.get("/digests", response_model=DigestPage)
def list_digests(
    status: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: NotificationService = Depends(_service),
) -> DigestPage:
    items, page = service.list_digests(status=status, limit=limit, offset=offset)
    return DigestPage(items=[DigestRead.model_validate(r) for r in items], page=page)


@router.post("/digests", response_model=DigestRead, status_code=201)
def create_digest(
    body: DigestCreate, service: NotificationService = Depends(_service)
) -> DigestRead:
    return DigestRead.model_validate(service.create_digest(body))


@router.post("/digests/{digest_id}/process", response_model=DigestRead)
def process_digest(
    digest_id: UUID,
    body: ProcessDigest | None = None,
    service: NotificationService = Depends(_service),
) -> DigestRead:
    return DigestRead.model_validate(
        service.process_digest(digest_id, body or ProcessDigest())
    )


@router.get("/{notification_id}", response_model=NotificationRead)
def get_notification(
    notification_id: UUID, service: NotificationService = Depends(_service)
) -> NotificationRead:
    return NotificationRead.model_validate(service.get_notification(notification_id))


@router.post("/{notification_id}/mark-read", response_model=NotificationRead)
def mark_read(
    notification_id: UUID,
    body: MarkRead | None = None,
    service: NotificationService = Depends(_service),
) -> NotificationRead:
    return NotificationRead.model_validate(
        service.mark_read(notification_id, body or MarkRead())
    )


@router.post("/{notification_id}/deliver", response_model=NotificationRead)
def deliver(
    notification_id: UUID,
    body: SimulateDeliver,
    service: NotificationService = Depends(_service),
) -> NotificationRead:
    return NotificationRead.model_validate(service.simulate_deliver(notification_id, body))


@router.post("/{notification_id}/retry", response_model=NotificationRead)
def retry(
    notification_id: UUID, service: NotificationService = Depends(_service)
) -> NotificationRead:
    return NotificationRead.model_validate(service.retry_delivery(notification_id))
