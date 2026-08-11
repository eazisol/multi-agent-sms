"""HTTP routes for MOD-220 conversations and messages."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.comms.schemas import (
    AttachmentLinkCreate,
    AttachmentLinkRead,
    ConversationCreate,
    ConversationRead,
    DeliveryReceiptCreate,
    DeliveryReceiptRead,
    MessageCreate,
    MessageRead,
    MessageRevisionRead,
    MessageUpdateBody,
    RecipientCreate,
    RecipientRead,
)
from masms_api.modules.comms.service import CommsService

router = APIRouter(prefix="/comms", tags=["comms"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> CommsService:
    return CommsService(db, ctx)


@router.post("/conversations", response_model=ConversationRead, status_code=201)
def create_conversation(
    body: ConversationCreate, service: CommsService = Depends(_service)
) -> ConversationRead:
    return ConversationRead.model_validate(service.create_conversation(body))


@router.post("/messages", response_model=MessageRead, status_code=201)
def create_message(
    body: MessageCreate, service: CommsService = Depends(_service)
) -> MessageRead:
    return MessageRead.model_validate(service.create_message(body))


@router.patch("/messages/{message_id}", response_model=MessageRead)
def update_message(
    message_id: UUID,
    body: MessageUpdateBody,
    service: CommsService = Depends(_service),
) -> MessageRead:
    return MessageRead.model_validate(service.update_draft_body(message_id, body))


@router.post("/messages/{message_id}/approve", response_model=MessageRead)
def approve_message(
    message_id: UUID, service: CommsService = Depends(_service)
) -> MessageRead:
    return MessageRead.model_validate(service.approve_message(message_id))


@router.post("/messages/{message_id}/send", response_model=MessageRead)
def send_message(
    message_id: UUID, service: CommsService = Depends(_service)
) -> MessageRead:
    return MessageRead.model_validate(service.send_message(message_id))


@router.get("/messages/{message_id}/revisions", response_model=list[MessageRevisionRead])
def list_revisions(
    message_id: UUID, service: CommsService = Depends(_service)
) -> list[MessageRevisionRead]:
    return [MessageRevisionRead.model_validate(r) for r in service.list_revisions(message_id)]


@router.get("/conversations/{conversation_id}/messages", response_model=list[MessageRead])
def list_messages(
    conversation_id: UUID, service: CommsService = Depends(_service)
) -> list[MessageRead]:
    return [MessageRead.model_validate(m) for m in service.list_messages(conversation_id)]


@router.post("/recipients", response_model=RecipientRead, status_code=201)
def add_recipient(
    body: RecipientCreate, service: CommsService = Depends(_service)
) -> RecipientRead:
    return RecipientRead.model_validate(service.add_recipient(body))


@router.post("/attachments", response_model=AttachmentLinkRead, status_code=201)
def add_attachment(
    body: AttachmentLinkCreate, service: CommsService = Depends(_service)
) -> AttachmentLinkRead:
    return AttachmentLinkRead.model_validate(service.add_attachment(body))


@router.post("/delivery-receipts", response_model=DeliveryReceiptRead, status_code=201)
def record_delivery(
    body: DeliveryReceiptCreate, service: CommsService = Depends(_service)
) -> DeliveryReceiptRead:
    return DeliveryReceiptRead.model_validate(service.record_delivery(body))
