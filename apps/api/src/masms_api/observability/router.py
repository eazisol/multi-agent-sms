"""Observability HTTP routes."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.observability.schemas import (
    ActivityEventPage,
    ActivityEventRead,
    AgentRunCreate,
    AgentRunFinish,
    AgentRunRead,
    AuditLogPage,
    AuditLogRead,
    StatusHistoryRead,
)
from masms_api.observability.service import ObservabilityService

router = APIRouter(prefix="/observability", tags=["observability"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> ObservabilityService:
    return ObservabilityService(db, ctx)


@router.get("/audit-logs", response_model=AuditLogPage)
def list_audit_logs(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ObservabilityService = Depends(_service),
) -> AuditLogPage:
    items, page = service.list_audit_logs(limit=limit, offset=offset)
    return AuditLogPage(items=[AuditLogRead.model_validate(i) for i in items], page=page)


@router.delete("/audit-logs/{audit_id}")
def delete_audit_log(
    audit_id: UUID,
    service: ObservabilityService = Depends(_service),
) -> None:
    _ = audit_id
    service.refuse_audit_mutation()


@router.get("/activity", response_model=ActivityEventPage)
def list_activity(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ObservabilityService = Depends(_service),
) -> ActivityEventPage:
    items, page = service.list_activity(limit=limit, offset=offset)
    return ActivityEventPage(items=[ActivityEventRead.model_validate(i) for i in items], page=page)


@router.get("/status-history", response_model=dict)
def list_status_history(
    entity_type: str = Query(min_length=2, max_length=64),
    entity_id: UUID = Query(),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ObservabilityService = Depends(_service),
) -> dict[str, object]:
    items, page = service.list_status_history(
        entity_type=entity_type,
        entity_id=entity_id,
        limit=limit,
        offset=offset,
    )
    return {
        "items": [StatusHistoryRead.model_validate(i) for i in items],
        "page": page,
    }


@router.post("/agent-runs", response_model=AgentRunRead, status_code=201)
def start_agent_run(
    body: AgentRunCreate,
    service: ObservabilityService = Depends(_service),
) -> AgentRunRead:
    run = service.start_agent_run(agent_name=body.agent_name, input_summary=body.input_summary)
    return AgentRunRead.model_validate(run)


@router.post("/agent-runs/{run_id}/finish", response_model=AgentRunRead)
def finish_agent_run(
    run_id: UUID,
    body: AgentRunFinish,
    service: ObservabilityService = Depends(_service),
) -> AgentRunRead:
    run = service.finish_agent_run(
        run_id,
        status=body.status,
        output_summary=body.output_summary,
        error_summary=body.error_summary,
    )
    return AgentRunRead.model_validate(run)
