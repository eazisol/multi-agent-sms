"""HTTP routes for MOD-350 orchestrator registry."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.orchestrator.schemas import (
    DefinitionRead,
    FailureCreate,
    FailureRead,
    InstanceCreate,
    InstanceRead,
    InterventionCreate,
    InterventionRead,
    InterventionResolve,
    SignalCreate,
    SignalRead,
    VersionCreate,
    VersionRead,
)
from masms_api.modules.orchestrator.service import OrchestratorService

router = APIRouter(prefix="/orchestrator", tags=["orchestrator"])


class InstancePage(BaseModel):
    items: list[InstanceRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> OrchestratorService:
    return OrchestratorService(db, ctx)


@router.get("/definitions", response_model=list[DefinitionRead])
def list_definitions(
    service: OrchestratorService = Depends(_service),
) -> list[DefinitionRead]:
    return [DefinitionRead.model_validate(r) for r in service.list_definitions()]


@router.post(
    "/definitions/{code}/versions",
    response_model=VersionRead,
    status_code=201,
)
def create_version(
    code: str,
    body: VersionCreate,
    service: OrchestratorService = Depends(_service),
) -> VersionRead:
    return VersionRead.model_validate(service.create_version(code, body))


@router.get("/versions", response_model=list[VersionRead])
def list_versions(
    definition_id: UUID | None = Query(default=None),
    service: OrchestratorService = Depends(_service),
) -> list[VersionRead]:
    return [
        VersionRead.model_validate(r) for r in service.list_versions(definition_id)
    ]


@router.post("/versions/{version_id}/activate", response_model=VersionRead)
def activate_version(
    version_id: UUID,
    service: OrchestratorService = Depends(_service),
) -> VersionRead:
    return VersionRead.model_validate(service.activate_version(version_id))


@router.post("/instances", response_model=InstanceRead, status_code=201)
def start_instance(
    body: InstanceCreate,
    service: OrchestratorService = Depends(_service),
) -> InstanceRead:
    return InstanceRead.model_validate(service.start_instance(body))


@router.get("/instances", response_model=InstancePage)
def list_instances(
    status: str | None = Query(default=None),
    q: str | None = Query(default=None),
    workflow_code: str | None = Query(default=None),
    project_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: OrchestratorService = Depends(_service),
) -> InstancePage:
    items, page = service.list_instances(
        status=status,
        q=q,
        workflow_code=workflow_code,
        project_id=project_id,
        limit=limit,
        offset=offset,
    )
    return InstancePage(
        items=[InstanceRead.model_validate(r) for r in items],
        page=page,
    )


@router.get("/instances/{instance_id}", response_model=InstanceRead)
def get_instance(
    instance_id: UUID,
    service: OrchestratorService = Depends(_service),
) -> InstanceRead:
    return InstanceRead.model_validate(service.get_instance(instance_id))


@router.post(
    "/instances/{instance_id}/signals",
    response_model=SignalRead,
    status_code=201,
)
def signal_instance(
    instance_id: UUID,
    body: SignalCreate,
    service: OrchestratorService = Depends(_service),
) -> SignalRead:
    row, was_duplicate = service.signal_instance(instance_id, body)
    read = SignalRead.model_validate(row)
    if was_duplicate:
        return read.model_copy(update={"status": "duplicate"})
    return read


@router.get("/instances/{instance_id}/signals", response_model=list[SignalRead])
def list_signals(
    instance_id: UUID,
    service: OrchestratorService = Depends(_service),
) -> list[SignalRead]:
    return [SignalRead.model_validate(r) for r in service.list_signals(instance_id)]


@router.post(
    "/instances/{instance_id}/failures",
    response_model=FailureRead,
    status_code=201,
)
def record_failure(
    instance_id: UUID,
    body: FailureCreate,
    service: OrchestratorService = Depends(_service),
) -> FailureRead:
    return FailureRead.model_validate(service.record_failure(instance_id, body))


@router.get("/instances/{instance_id}/failures", response_model=list[FailureRead])
def list_failures(
    instance_id: UUID,
    service: OrchestratorService = Depends(_service),
) -> list[FailureRead]:
    return [FailureRead.model_validate(r) for r in service.list_failures(instance_id)]


@router.post(
    "/instances/{instance_id}/interventions",
    response_model=InterventionRead,
    status_code=201,
)
def create_intervention(
    instance_id: UUID,
    body: InterventionCreate,
    service: OrchestratorService = Depends(_service),
) -> InterventionRead:
    return InterventionRead.model_validate(service.create_intervention(instance_id, body))


@router.get(
    "/instances/{instance_id}/interventions",
    response_model=list[InterventionRead],
)
def list_interventions(
    instance_id: UUID,
    service: OrchestratorService = Depends(_service),
) -> list[InterventionRead]:
    return [
        InterventionRead.model_validate(r) for r in service.list_interventions(instance_id)
    ]


@router.post(
    "/interventions/{intervention_id}/resolve",
    response_model=InterventionRead,
)
def resolve_intervention(
    intervention_id: UUID,
    body: InterventionResolve | None = None,
    service: OrchestratorService = Depends(_service),
) -> InterventionRead:
    return InterventionRead.model_validate(
        service.resolve_intervention(intervention_id, body)
    )
