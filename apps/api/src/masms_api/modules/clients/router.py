"""HTTP routes for MOD-200 clients and contacts."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.clients.schemas import (
    ClientCreate,
    ClientRead,
    CommunicationPreferenceCreate,
    CommunicationPreferenceRead,
    ContactCreate,
    ContactRead,
    DuplicateSuggestionCreate,
    DuplicateSuggestionRead,
    MergeClientsRequest,
    MergeHistoryRead,
    ProjectContactCreate,
    ProjectContactRead,
)
from masms_api.modules.clients.service import ClientsService

router = APIRouter(prefix="/clients", tags=["clients"])


class ClientPage(BaseModel):
    items: list[ClientRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> ClientsService:
    return ClientsService(db, ctx)


@router.post("", response_model=ClientRead, status_code=201)
def create_client(
    body: ClientCreate, service: ClientsService = Depends(_service)
) -> ClientRead:
    return ClientRead.model_validate(service.create_client(body))


@router.get("", response_model=ClientPage)
def list_clients(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ClientsService = Depends(_service),
) -> ClientPage:
    items, page = service.list_clients(limit=limit, offset=offset)
    return ClientPage(items=[ClientRead.model_validate(i) for i in items], page=page)


@router.post("/contacts", response_model=ContactRead, status_code=201)
def create_contact(
    body: ContactCreate, service: ClientsService = Depends(_service)
) -> ContactRead:
    return ContactRead.model_validate(service.create_contact(body))


@router.get("/{client_id}/contacts", response_model=list[ContactRead])
def list_contacts(
    client_id: UUID, service: ClientsService = Depends(_service)
) -> list[ContactRead]:
    return [ContactRead.model_validate(c) for c in service.list_contacts(client_id=client_id)]


@router.post("/project-contacts", response_model=ProjectContactRead, status_code=201)
def create_project_contact(
    body: ProjectContactCreate, service: ClientsService = Depends(_service)
) -> ProjectContactRead:
    return ProjectContactRead.model_validate(service.create_project_contact(body))


@router.post("/preferences", response_model=CommunicationPreferenceRead, status_code=201)
def create_preference(
    body: CommunicationPreferenceCreate, service: ClientsService = Depends(_service)
) -> CommunicationPreferenceRead:
    return CommunicationPreferenceRead.model_validate(service.create_preference(body))


@router.post("/duplicates", response_model=DuplicateSuggestionRead, status_code=201)
def create_duplicate(
    body: DuplicateSuggestionCreate, service: ClientsService = Depends(_service)
) -> DuplicateSuggestionRead:
    return DuplicateSuggestionRead.model_validate(service.create_duplicate(body))


@router.post("/merge", response_model=MergeHistoryRead, status_code=201)
def merge_clients(
    body: MergeClientsRequest, service: ClientsService = Depends(_service)
) -> MergeHistoryRead:
    return MergeHistoryRead.model_validate(service.merge_clients(body))
