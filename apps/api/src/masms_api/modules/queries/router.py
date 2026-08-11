"""HTTP routes for MOD-210 client queries."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.queries.schemas import (
    ClientQueryCreate,
    ClientQueryRead,
    ConvertQueryRequest,
    FirstResponseRequest,
    OpportunityRead,
    QualificationAnswerCreate,
    QualificationAnswerRead,
    QuerySourceCreate,
    QuerySourceRead,
    QueryStatusHistoryRead,
    QueryTransitionRequest,
)
from masms_api.modules.queries.service import QueriesService

router = APIRouter(prefix="/queries", tags=["queries"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> QueriesService:
    return QueriesService(db, ctx)


@router.post("/sources", response_model=QuerySourceRead, status_code=201)
def create_source(
    body: QuerySourceCreate, service: QueriesService = Depends(_service)
) -> QuerySourceRead:
    return QuerySourceRead.model_validate(service.create_source(body))


@router.post("", response_model=ClientQueryRead, status_code=201)
def create_query(
    body: ClientQueryCreate, service: QueriesService = Depends(_service)
) -> ClientQueryRead:
    return ClientQueryRead.model_validate(service.create_query(body))


@router.post("/{query_id}/transitions", response_model=ClientQueryRead)
def transition_query(
    query_id: UUID,
    body: QueryTransitionRequest,
    service: QueriesService = Depends(_service),
) -> ClientQueryRead:
    return ClientQueryRead.model_validate(service.transition(query_id, body))


@router.post("/{query_id}/first-response", response_model=ClientQueryRead)
def first_response(
    query_id: UUID,
    body: FirstResponseRequest,
    service: QueriesService = Depends(_service),
) -> ClientQueryRead:
    return ClientQueryRead.model_validate(service.record_first_response(query_id, body))


@router.post("/qualification-answers", response_model=QualificationAnswerRead, status_code=201)
def add_qualification(
    body: QualificationAnswerCreate, service: QueriesService = Depends(_service)
) -> QualificationAnswerRead:
    return QualificationAnswerRead.model_validate(service.add_qualification(body))


@router.get("/{query_id}/qualification-answers", response_model=list[QualificationAnswerRead])
def list_qualification(
    query_id: UUID, service: QueriesService = Depends(_service)
) -> list[QualificationAnswerRead]:
    return [
        QualificationAnswerRead.model_validate(r)
        for r in service.list_qualification(query_id)
    ]


@router.post("/{query_id}/convert", response_model=OpportunityRead, status_code=201)
def convert_query(
    query_id: UUID,
    body: ConvertQueryRequest,
    service: QueriesService = Depends(_service),
) -> OpportunityRead:
    return OpportunityRead.model_validate(service.convert_to_opportunity(query_id, body))


@router.get("/{query_id}/history", response_model=list[QueryStatusHistoryRead])
def query_history(
    query_id: UUID, service: QueriesService = Depends(_service)
) -> list[QueryStatusHistoryRead]:
    return [QueryStatusHistoryRead.model_validate(r) for r in service.list_history(query_id)]
