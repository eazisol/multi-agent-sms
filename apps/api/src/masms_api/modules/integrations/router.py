"""HTTP routes for MOD-500 integration framework."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.integrations.schemas import (
    ConnectionCreate,
    ConnectionHealthRead,
    ConnectionHealthRecord,
    ConnectionRead,
    ConnectionTransition,
    ExternalMappingCreate,
    ExternalMappingRead,
    InboxEventRead,
    InboxProcessRequest,
    InboxReceive,
    IntegrationOutboxCreate,
    IntegrationOutboxRead,
    OutboxRelayRequest,
    SyncCursorRead,
    SyncCursorUpsert,
    WebhookEventRead,
    WebhookReceive,
)
from masms_api.modules.integrations.service import IntegrationsService

router = APIRouter(prefix="/integrations", tags=["integrations"])


class ConnectionPage(BaseModel):
    items: list[ConnectionRead]
    page: PageMeta = Field(description="Pagination metadata")


class MappingPage(BaseModel):
    items: list[ExternalMappingRead]
    page: PageMeta = Field(description="Pagination metadata")


class OutboxPage(BaseModel):
    items: list[IntegrationOutboxRead]
    page: PageMeta = Field(description="Pagination metadata")


class InboxPage(BaseModel):
    items: list[InboxEventRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> IntegrationsService:
    return IntegrationsService(db, ctx)


@router.post("/connections", response_model=ConnectionRead, status_code=201)
def create_connection(
    body: ConnectionCreate, service: IntegrationsService = Depends(_service)
) -> ConnectionRead:
    return ConnectionRead.model_validate(service.create_connection(body))


@router.get("/connections", response_model=ConnectionPage)
def list_connections(
    status: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: IntegrationsService = Depends(_service),
) -> ConnectionPage:
    items, page = service.list_connections(status=status, limit=limit, offset=offset)
    return ConnectionPage(
        items=[ConnectionRead.model_validate(r) for r in items], page=page
    )


@router.get("/connections/{connection_id}", response_model=ConnectionRead)
def get_connection(
    connection_id: UUID, service: IntegrationsService = Depends(_service)
) -> ConnectionRead:
    return ConnectionRead.model_validate(service.get_connection(connection_id))


@router.post("/connections/{connection_id}/activate", response_model=ConnectionRead)
def activate_connection(
    connection_id: UUID,
    body: ConnectionTransition | None = None,
    service: IntegrationsService = Depends(_service),
) -> ConnectionRead:
    expected = body.expected_version if body else None
    return ConnectionRead.model_validate(
        service.activate_connection(connection_id, expected_version=expected)
    )


@router.post("/connections/{connection_id}/pause", response_model=ConnectionRead)
def pause_connection(
    connection_id: UUID,
    body: ConnectionTransition | None = None,
    service: IntegrationsService = Depends(_service),
) -> ConnectionRead:
    expected = body.expected_version if body else None
    return ConnectionRead.model_validate(
        service.pause_connection(connection_id, expected_version=expected)
    )


@router.post("/webhooks/receive", response_model=WebhookEventRead, status_code=201)
def receive_webhook(
    body: WebhookReceive, service: IntegrationsService = Depends(_service)
) -> WebhookEventRead:
    return WebhookEventRead.model_validate(service.receive_webhook(body))


@router.put("/sync-cursors", response_model=SyncCursorRead)
def upsert_sync_cursor(
    body: SyncCursorUpsert, service: IntegrationsService = Depends(_service)
) -> SyncCursorRead:
    return SyncCursorRead.model_validate(service.upsert_sync_cursor(body))


@router.get("/sync-cursors", response_model=SyncCursorRead)
def get_sync_cursor(
    connection_id: UUID = Query(...),
    stream_key: str = Query(..., min_length=1),
    service: IntegrationsService = Depends(_service),
) -> SyncCursorRead:
    return SyncCursorRead.model_validate(
        service.get_sync_cursor(connection_id=connection_id, stream_key=stream_key)
    )


@router.post("/mappings", response_model=ExternalMappingRead, status_code=201)
def create_mapping(
    body: ExternalMappingCreate, service: IntegrationsService = Depends(_service)
) -> ExternalMappingRead:
    return ExternalMappingRead.model_validate(service.create_mapping(body))


@router.get("/mappings", response_model=MappingPage)
def list_mappings(
    connection_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: IntegrationsService = Depends(_service),
) -> MappingPage:
    items, page = service.list_mappings(
        connection_id=connection_id, limit=limit, offset=offset
    )
    return MappingPage(
        items=[ExternalMappingRead.model_validate(r) for r in items], page=page
    )


@router.post("/outbox", response_model=IntegrationOutboxRead, status_code=201)
def enqueue_outbox_event(
    body: IntegrationOutboxCreate, service: IntegrationsService = Depends(_service)
) -> IntegrationOutboxRead:
    return IntegrationOutboxRead.model_validate(service.enqueue_ig_outbox(body))


@router.get("/outbox", response_model=OutboxPage)
def list_outbox_events(
    connection_id: UUID | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: IntegrationsService = Depends(_service),
) -> OutboxPage:
    items, page = service.list_ig_outbox(
        connection_id=connection_id, status=status, limit=limit, offset=offset
    )
    return OutboxPage(
        items=[IntegrationOutboxRead.model_validate(r) for r in items], page=page
    )


@router.post("/outbox/{outbox_id}/relay", response_model=IntegrationOutboxRead)
def relay_outbox_event(
    outbox_id: UUID,
    body: OutboxRelayRequest | None = None,
    service: IntegrationsService = Depends(_service),
) -> IntegrationOutboxRead:
    force_fail = body.force_fail if body else False
    return IntegrationOutboxRead.model_validate(
        service.relay_ig_outbox(outbox_id, force_fail=force_fail)
    )


@router.post("/inbox", response_model=InboxEventRead, status_code=201)
def receive_inbox_event(
    body: InboxReceive, service: IntegrationsService = Depends(_service)
) -> InboxEventRead:
    return InboxEventRead.model_validate(service.receive_inbox(body))


@router.get("/inbox", response_model=InboxPage)
def list_inbox_events(
    connection_id: UUID | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: IntegrationsService = Depends(_service),
) -> InboxPage:
    items, page = service.list_inbox(
        connection_id=connection_id, status=status, limit=limit, offset=offset
    )
    return InboxPage(items=[InboxEventRead.model_validate(r) for r in items], page=page)


@router.post("/inbox/{inbox_id}/process", response_model=InboxEventRead)
def process_inbox_event(
    inbox_id: UUID,
    body: InboxProcessRequest | None = None,
    service: IntegrationsService = Depends(_service),
) -> InboxEventRead:
    force_fail = body.force_fail if body else False
    return InboxEventRead.model_validate(
        service.process_inbox(inbox_id, force_fail=force_fail)
    )


@router.get("/health/{connection_id}", response_model=ConnectionHealthRead)
def get_connection_health(
    connection_id: UUID, service: IntegrationsService = Depends(_service)
) -> ConnectionHealthRead:
    return ConnectionHealthRead.model_validate(service.get_health(connection_id))


@router.post("/health/{connection_id}", response_model=ConnectionHealthRead)
def record_connection_health(
    connection_id: UUID,
    body: ConnectionHealthRecord,
    service: IntegrationsService = Depends(_service),
) -> ConnectionHealthRead:
    return ConnectionHealthRead.model_validate(
        service.record_health(connection_id, body)
    )


@router.post("/health/{connection_id}/check", response_model=ConnectionHealthRead)
def check_connection_health(
    connection_id: UUID, service: IntegrationsService = Depends(_service)
) -> ConnectionHealthRead:
    return ConnectionHealthRead.model_validate(service.check_health(connection_id))
