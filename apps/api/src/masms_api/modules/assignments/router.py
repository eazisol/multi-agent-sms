"""HTTP routes for MOD-310 assignments."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.assignments.schemas import (
    AcknowledgeRequest,
    AcknowledgmentRead,
    AllocationHistoryRead,
    AssignmentCreate,
    AssignmentRead,
    ReassignmentHistoryRead,
    ReassignRequest,
    RecommendationRead,
    RecommendRequest,
)
from masms_api.modules.assignments.service import AssignmentService

router = APIRouter(prefix="/assignments", tags=["assignments"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> AssignmentService:
    return AssignmentService(db, ctx)


@router.post("", response_model=AssignmentRead, status_code=201)
def create_assignment(
    body: AssignmentCreate, service: AssignmentService = Depends(_service)
) -> AssignmentRead:
    return AssignmentRead.model_validate(service.create_assignment(body))


@router.post("/recommendations", response_model=list[RecommendationRead], status_code=201)
def recommend(
    body: RecommendRequest, service: AssignmentService = Depends(_service)
) -> list[RecommendationRead]:
    return [RecommendationRead.model_validate(r) for r in service.recommend(body)]


@router.get("/tickets/{ticket_id}", response_model=list[AssignmentRead])
def list_assignments(
    ticket_id: UUID, service: AssignmentService = Depends(_service)
) -> list[AssignmentRead]:
    return [AssignmentRead.model_validate(a) for a in service.list_for_ticket(ticket_id)]


@router.get(
    "/tickets/{ticket_id}/recommendations",
    response_model=list[RecommendationRead],
)
def list_recommendations(
    ticket_id: UUID, service: AssignmentService = Depends(_service)
) -> list[RecommendationRead]:
    return [
        RecommendationRead.model_validate(r) for r in service.list_recommendations(ticket_id)
    ]


@router.get(
    "/tickets/{ticket_id}/allocation-history",
    response_model=list[AllocationHistoryRead],
)
def list_allocation_history(
    ticket_id: UUID, service: AssignmentService = Depends(_service)
) -> list[AllocationHistoryRead]:
    return [
        AllocationHistoryRead.model_validate(r)
        for r in service.list_allocation_history(ticket_id)
    ]


@router.get(
    "/tickets/{ticket_id}/reassignment-history",
    response_model=list[ReassignmentHistoryRead],
)
def list_reassignment_history(
    ticket_id: UUID, service: AssignmentService = Depends(_service)
) -> list[ReassignmentHistoryRead]:
    return [
        ReassignmentHistoryRead.model_validate(r)
        for r in service.list_reassignment_history(ticket_id)
    ]


@router.post("/{assignment_id}/acknowledge", response_model=AcknowledgmentRead)
def acknowledge(
    assignment_id: UUID,
    body: AcknowledgeRequest,
    service: AssignmentService = Depends(_service),
) -> AcknowledgmentRead:
    return AcknowledgmentRead.model_validate(service.acknowledge(assignment_id, body))


@router.post("/{assignment_id}/reassign", response_model=AssignmentRead)
def reassign(
    assignment_id: UUID,
    body: ReassignRequest,
    service: AssignmentService = Depends(_service),
) -> AssignmentRead:
    return AssignmentRead.model_validate(service.reassign(assignment_id, body))
