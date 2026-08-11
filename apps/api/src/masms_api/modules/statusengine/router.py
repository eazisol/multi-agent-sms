"""HTTP routes for MOD-320 status / transition engine."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.statusengine.schemas import (
    AvailableActionsRead,
    EntityStateInit,
    EntityStateRead,
    HoldCreate,
    HoldRead,
    HoldRelease,
    ReopenApply,
    ReopenRead,
    ResolveWorkflowRead,
    StatusHistoryRead,
    TransitionApply,
    WorkflowBindingCreate,
    WorkflowBindingRead,
)
from masms_api.modules.statusengine.service import StatusEngineService

router = APIRouter(prefix="/status-engine", tags=["status-engine"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> StatusEngineService:
    return StatusEngineService(db, ctx)


@router.post("/bindings", response_model=WorkflowBindingRead, status_code=201)
def create_binding(
    body: WorkflowBindingCreate, service: StatusEngineService = Depends(_service)
) -> WorkflowBindingRead:
    return WorkflowBindingRead.model_validate(service.create_binding(body))


@router.get("/bindings", response_model=list[WorkflowBindingRead])
def list_bindings(
    entity_type: str | None = Query(default=None),
    service: StatusEngineService = Depends(_service),
) -> list[WorkflowBindingRead]:
    rows = service.list_bindings(entity_type=entity_type)
    return [WorkflowBindingRead.model_validate(r) for r in rows]


@router.get("/resolve", response_model=ResolveWorkflowRead)
def resolve_workflow(
    entity_type: str = Query(...),
    project_id: UUID | None = Query(default=None),
    service: StatusEngineService = Depends(_service),
) -> ResolveWorkflowRead:
    return service.resolve_workflow(entity_type=entity_type, project_id=project_id)


@router.post("/states", response_model=EntityStateRead, status_code=201)
def initialize_state(
    body: EntityStateInit, service: StatusEngineService = Depends(_service)
) -> EntityStateRead:
    return EntityStateRead.model_validate(service.initialize_state(body))


@router.get(
    "/states/{entity_type}/{entity_id}",
    response_model=EntityStateRead,
)
def get_state(
    entity_type: str,
    entity_id: UUID,
    service: StatusEngineService = Depends(_service),
) -> EntityStateRead:
    return EntityStateRead.model_validate(service.get_state(entity_type, entity_id))


@router.get(
    "/states/{entity_type}/{entity_id}/history",
    response_model=list[StatusHistoryRead],
)
def list_history(
    entity_type: str,
    entity_id: UUID,
    service: StatusEngineService = Depends(_service),
) -> list[StatusHistoryRead]:
    return [
        StatusHistoryRead.model_validate(r)
        for r in service.list_history(entity_type, entity_id)
    ]


@router.get(
    "/states/{entity_type}/{entity_id}/actions",
    response_model=AvailableActionsRead,
)
def available_actions(
    entity_type: str,
    entity_id: UUID,
    service: StatusEngineService = Depends(_service),
) -> AvailableActionsRead:
    return service.available_actions(entity_type, entity_id)


@router.post("/transitions", response_model=EntityStateRead)
def apply_transition(
    body: TransitionApply, service: StatusEngineService = Depends(_service)
) -> EntityStateRead:
    return EntityStateRead.model_validate(service.apply_transition(body))


@router.post("/holds", response_model=HoldRead, status_code=201)
def place_hold(
    body: HoldCreate, service: StatusEngineService = Depends(_service)
) -> HoldRead:
    return HoldRead.model_validate(service.place_hold(body))


@router.post(
    "/holds/{entity_type}/{entity_id}/release",
    response_model=HoldRead,
)
def release_hold(
    entity_type: str,
    entity_id: UUID,
    body: HoldRelease,
    service: StatusEngineService = Depends(_service),
) -> HoldRead:
    return HoldRead.model_validate(service.release_hold(entity_type, entity_id, body))


@router.post("/reopen", response_model=ReopenRead)
def reopen(
    body: ReopenApply, service: StatusEngineService = Depends(_service)
) -> ReopenRead:
    _state, reopen_row = service.reopen(body)
    return ReopenRead.model_validate(reopen_row)
