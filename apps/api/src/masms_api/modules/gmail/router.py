"""HTTP routes for MOD-510 Gmail integration."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.gmail.schemas import (
    ApprovedSendRead,
    AttachmentImportCreate,
    AttachmentImportRead,
    ConnectionCreate,
    ConnectionRead,
    ConnectionTransition,
    DraftCreate,
    DraftRead,
    DraftReject,
    DraftTransition,
    HistoryCursorRead,
    HistoryCursorUpsert,
    InboundProcess,
    InboundProcessResult,
    MessageMappingRead,
    PushReceive,
    PushReceiveResult,
    SendApprovedResult,
    ThreadMappingRead,
)
from masms_api.modules.gmail.service import GmailService

router = APIRouter(prefix="/gmail", tags=["gmail"])


class ConnectionPage(BaseModel):
    items: list[ConnectionRead]
    page: PageMeta = Field(description="Pagination metadata")


class ThreadPage(BaseModel):
    items: list[ThreadMappingRead]
    page: PageMeta = Field(description="Pagination metadata")


class MessagePage(BaseModel):
    items: list[MessageMappingRead]
    page: PageMeta = Field(description="Pagination metadata")


class DraftPage(BaseModel):
    items: list[DraftRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> GmailService:
    return GmailService(db, ctx)


@router.post("/connections", response_model=ConnectionRead, status_code=201)
def create_connection(
    body: ConnectionCreate, service: GmailService = Depends(_service)
) -> ConnectionRead:
    return ConnectionRead.model_validate(service.create_connection(body))


@router.get("/connections", response_model=ConnectionPage)
def list_connections(
    status: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: GmailService = Depends(_service),
) -> ConnectionPage:
    items, page = service.list_connections(status=status, limit=limit, offset=offset)
    return ConnectionPage(
        items=[ConnectionRead.model_validate(r) for r in items], page=page
    )


@router.get("/connections/{connection_id}", response_model=ConnectionRead)
def get_connection(
    connection_id: UUID, service: GmailService = Depends(_service)
) -> ConnectionRead:
    return ConnectionRead.model_validate(service.get_connection(connection_id))


@router.post("/connections/{connection_id}/sync")
def sync_connection(
    connection_id: UUID,
    limit: int = Query(default=20, ge=1, le=100),
    service: GmailService = Depends(_service),
) -> dict[str, object]:
    return service.sync_inbound(connection_id, limit=limit)


@router.post("/connections/{connection_id}/activate", response_model=ConnectionRead)
def activate_connection(
    connection_id: UUID,
    body: ConnectionTransition | None = None,
    service: GmailService = Depends(_service),
) -> ConnectionRead:
    expected = body.expected_version if body else None
    return ConnectionRead.model_validate(
        service.activate_connection(connection_id, expected_version=expected)
    )


@router.post("/connections/{connection_id}/pause", response_model=ConnectionRead)
def pause_connection(
    connection_id: UUID,
    body: ConnectionTransition | None = None,
    service: GmailService = Depends(_service),
) -> ConnectionRead:
    expected = body.expected_version if body else None
    return ConnectionRead.model_validate(
        service.pause_connection(connection_id, expected_version=expected)
    )


@router.put("/history-cursors", response_model=HistoryCursorRead)
def upsert_history_cursor(
    body: HistoryCursorUpsert, service: GmailService = Depends(_service)
) -> HistoryCursorRead:
    return HistoryCursorRead.model_validate(service.upsert_history_cursor(body))


@router.get("/history-cursors", response_model=HistoryCursorRead)
def get_history_cursor(
    connection_id: UUID = Query(...),
    cursor_key: str = Query(default="history"),
    service: GmailService = Depends(_service),
) -> HistoryCursorRead:
    return HistoryCursorRead.model_validate(
        service.get_history_cursor(connection_id=connection_id, cursor_key=cursor_key)
    )


@router.post("/inbound/process", response_model=InboundProcessResult)
def process_inbound(
    body: InboundProcess,
    response: Response,
    service: GmailService = Depends(_service),
) -> InboundProcessResult:
    result = service.process_inbound(body)
    if result.get("idempotent"):
        response.status_code = status.HTTP_409_CONFLICT
    return InboundProcessResult.model_validate(result)


@router.post("/push/receive", response_model=PushReceiveResult, status_code=201)
def receive_push(
    body: PushReceive,
    response: Response,
    service: GmailService = Depends(_service),
) -> PushReceiveResult:
    result = service.receive_push_notification(body)
    if result.get("idempotent"):
        response.status_code = status.HTTP_200_OK
    inbound = result.get("inbound")
    inbound_result = None
    if inbound and "thread_mapping_id" in inbound:
        inbound_result = InboundProcessResult.model_validate(inbound)
    elif inbound and "message_mapping_id" in inbound:
        inbound_result = InboundProcessResult(
            thread_mapping_id=UUID(int=0),
            message_mapping_id=inbound["message_mapping_id"],
            query_id=UUID(int=0),
            internal_thread_id=UUID(int=0),
            idempotent=True,
        )
    return PushReceiveResult(
        external_event_id=result["external_event_id"],
        event_type=result["event_type"],
        status=result["status"],
        inbound=inbound_result,
        idempotent=result.get("idempotent", False),
    )


@router.get("/threads", response_model=ThreadPage)
def list_threads(
    connection_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: GmailService = Depends(_service),
) -> ThreadPage:
    items, page = service.list_thread_mappings(
        connection_id=connection_id, limit=limit, offset=offset
    )
    return ThreadPage(
        items=[ThreadMappingRead.model_validate(r) for r in items], page=page
    )


@router.get("/messages", response_model=MessagePage)
def list_messages(
    connection_id: UUID | None = Query(default=None),
    direction: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: GmailService = Depends(_service),
) -> MessagePage:
    items, page = service.list_message_mappings(
        connection_id=connection_id, direction=direction, limit=limit, offset=offset
    )
    return MessagePage(
        items=[MessageMappingRead.model_validate(r) for r in items], page=page
    )


@router.post(
    "/messages/{message_mapping_id}/attachments",
    response_model=AttachmentImportRead,
    status_code=201,
)
def import_attachment(
    message_mapping_id: UUID,
    body: AttachmentImportCreate,
    service: GmailService = Depends(_service),
) -> AttachmentImportRead:
    return AttachmentImportRead.model_validate(
        service.import_attachment(message_mapping_id, body)
    )


@router.post("/drafts", response_model=DraftRead, status_code=201)
def create_draft(
    body: DraftCreate, service: GmailService = Depends(_service)
) -> DraftRead:
    return DraftRead.model_validate(service.create_draft(body))


@router.get("/drafts", response_model=DraftPage)
def list_drafts(
    connection_id: UUID | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: GmailService = Depends(_service),
) -> DraftPage:
    items, page = service.list_drafts(
        connection_id=connection_id, status=status, limit=limit, offset=offset
    )
    return DraftPage(items=[DraftRead.model_validate(r) for r in items], page=page)


@router.post("/drafts/{draft_review_id}/submit", response_model=DraftRead)
def submit_draft(
    draft_review_id: UUID,
    body: DraftTransition | None = None,
    service: GmailService = Depends(_service),
) -> DraftRead:
    expected = body.expected_version if body else None
    return DraftRead.model_validate(
        service.submit_for_review(draft_review_id, expected_version=expected)
    )


@router.post("/drafts/{draft_review_id}/approve", response_model=DraftRead)
def approve_draft(
    draft_review_id: UUID,
    body: DraftTransition | None = None,
    service: GmailService = Depends(_service),
) -> DraftRead:
    expected = body.expected_version if body else None
    return DraftRead.model_validate(
        service.approve_draft(draft_review_id, expected_version=expected)
    )


@router.post("/drafts/{draft_review_id}/reject", response_model=DraftRead)
def reject_draft(
    draft_review_id: UUID,
    body: DraftReject,
    service: GmailService = Depends(_service),
) -> DraftRead:
    return DraftRead.model_validate(service.reject_draft(draft_review_id, body))


@router.post("/drafts/{draft_review_id}/send", response_model=SendApprovedResult)
def send_approved_draft(
    draft_review_id: UUID, service: GmailService = Depends(_service)
) -> SendApprovedResult:
    result = service.send_approved(draft_review_id)
    return SendApprovedResult(
        approved_send=ApprovedSendRead.model_validate(result["approved_send"]),
        message_mapping=MessageMappingRead.model_validate(result["message_mapping"]),
    )
