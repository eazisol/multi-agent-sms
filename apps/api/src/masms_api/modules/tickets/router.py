"""HTTP routes for MOD-300 tickets."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.tickets.schemas import (
    CheckCreate,
    CheckRead,
    CheckSatisfy,
    EvidenceCreate,
    EvidenceRead,
    ReopenRequest,
    RequirementLinkCreate,
    RequirementLinkRead,
    SubtaskCreate,
    SubtaskRead,
    TicketCreate,
    TicketDependencyCreate,
    TicketDependencyRead,
    TicketRead,
    TicketUpdate,
    TransitionRequest,
)
from masms_api.modules.tickets.service import TicketService

router = APIRouter(prefix="/tickets", tags=["tickets"])


class TicketPage(BaseModel):
    items: list[TicketRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> TicketService:
    return TicketService(db, ctx)


@router.post("", response_model=TicketRead, status_code=201)
def create_ticket(
    body: TicketCreate, service: TicketService = Depends(_service)
) -> TicketRead:
    return TicketRead.model_validate(service.create_ticket(body))


@router.get("/projects/{project_id}", response_model=TicketPage)
def list_tickets(
    project_id: UUID,
    status: str | None = Query(default=None),
    q: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: TicketService = Depends(_service),
) -> TicketPage:
    items, page = service.list_tickets(
        project_id, status=status, q=q, limit=limit, offset=offset
    )
    return TicketPage(items=[TicketRead.model_validate(t) for t in items], page=page)


@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(
    ticket_id: UUID, service: TicketService = Depends(_service)
) -> TicketRead:
    return TicketRead.model_validate(service.get_ticket(ticket_id))


@router.patch("/{ticket_id}", response_model=TicketRead)
def update_ticket(
    ticket_id: UUID,
    body: TicketUpdate,
    service: TicketService = Depends(_service),
) -> TicketRead:
    return TicketRead.model_validate(service.update_ticket(ticket_id, body))


@router.post("/{ticket_id}/transitions", response_model=TicketRead)
def transition_ticket(
    ticket_id: UUID,
    body: TransitionRequest,
    service: TicketService = Depends(_service),
) -> TicketRead:
    return TicketRead.model_validate(service.transition(ticket_id, body))


@router.post("/{ticket_id}/reopen", response_model=TicketRead)
def reopen_ticket(
    ticket_id: UUID,
    body: ReopenRequest,
    service: TicketService = Depends(_service),
) -> TicketRead:
    return TicketRead.model_validate(service.reopen(ticket_id, body))


@router.post("/subtasks", response_model=SubtaskRead, status_code=201)
def create_subtask(
    body: SubtaskCreate, service: TicketService = Depends(_service)
) -> SubtaskRead:
    return SubtaskRead.model_validate(service.create_subtask(body))


@router.post("/dependencies", response_model=TicketDependencyRead, status_code=201)
def create_dependency(
    body: TicketDependencyCreate, service: TicketService = Depends(_service)
) -> TicketDependencyRead:
    return TicketDependencyRead.model_validate(service.create_dependency(body))


@router.post("/requirement-links", response_model=RequirementLinkRead, status_code=201)
def link_requirement(
    body: RequirementLinkCreate, service: TicketService = Depends(_service)
) -> RequirementLinkRead:
    return RequirementLinkRead.model_validate(service.link_requirement(body))


@router.post("/evidence", response_model=EvidenceRead, status_code=201)
def add_evidence(
    body: EvidenceCreate, service: TicketService = Depends(_service)
) -> EvidenceRead:
    return EvidenceRead.model_validate(service.add_evidence(body))


@router.post("/readiness-checks", response_model=CheckRead, status_code=201)
def add_readiness_check(
    body: CheckCreate, service: TicketService = Depends(_service)
) -> CheckRead:
    return CheckRead.model_validate(service.add_readiness_check(body))


@router.post("/readiness-checks/{check_id}/satisfy", response_model=CheckRead)
def satisfy_readiness_check(
    check_id: UUID,
    body: CheckSatisfy,
    service: TicketService = Depends(_service),
) -> CheckRead:
    return CheckRead.model_validate(service.satisfy_readiness_check(check_id, body))


@router.get("/{ticket_id}/readiness-checks", response_model=list[CheckRead])
def list_readiness_checks(
    ticket_id: UUID, service: TicketService = Depends(_service)
) -> list[CheckRead]:
    return [
        CheckRead.model_validate(c) for c in service.list_readiness_checks(ticket_id)
    ]


@router.post("/done-checks", response_model=CheckRead, status_code=201)
def add_done_check(
    body: CheckCreate, service: TicketService = Depends(_service)
) -> CheckRead:
    return CheckRead.model_validate(service.add_done_check(body))


@router.post("/done-checks/{check_id}/satisfy", response_model=CheckRead)
def satisfy_done_check(
    check_id: UUID,
    body: CheckSatisfy,
    service: TicketService = Depends(_service),
) -> CheckRead:
    return CheckRead.model_validate(service.satisfy_done_check(check_id, body))


@router.get("/{ticket_id}/done-checks", response_model=list[CheckRead])
def list_done_checks(
    ticket_id: UUID, service: TicketService = Depends(_service)
) -> list[CheckRead]:
    return [CheckRead.model_validate(c) for c in service.list_done_checks(ticket_id)]
