"""HTTP routes for MOD-430 releases."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.releases.schemas import (
    ApproveRelease,
    BackupCreate,
    BackupRead,
    CompletionReportCreate,
    CompletionReportRead,
    DeploymentCheckCreate,
    DeploymentCheckRead,
    DeploymentCreate,
    DeploymentRead,
    MigrationPlanCreate,
    MigrationPlanRead,
    ReleaseCreate,
    ReleaseItemCreate,
    ReleaseItemRead,
    ReleaseRead,
    RollbackCreate,
    RollbackRead,
    SubmitApproval,
    TraceabilitySummary,
)
from masms_api.modules.releases.service import ReleaseService

router = APIRouter(prefix="/releases", tags=["releases"])


class ReleasePage(BaseModel):
    items: list[ReleaseRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> ReleaseService:
    return ReleaseService(db, ctx)


@router.post("", response_model=ReleaseRead, status_code=201)
def create_release(
    body: ReleaseCreate, service: ReleaseService = Depends(_service)
) -> ReleaseRead:
    return ReleaseRead.model_validate(service.create_release(body))


@router.get("", response_model=ReleasePage)
def list_releases(
    status: str | None = Query(default=None),
    project_id: UUID | None = Query(default=None),
    q: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ReleaseService = Depends(_service),
) -> ReleasePage:
    items, page = service.list_releases(
        status=status, project_id=project_id, q=q, limit=limit, offset=offset
    )
    return ReleasePage(items=[ReleaseRead.model_validate(r) for r in items], page=page)


@router.post(
    "/deployments/{deployment_id}/checks",
    response_model=DeploymentCheckRead,
    status_code=201,
)
def add_check(
    deployment_id: UUID,
    body: DeploymentCheckCreate,
    service: ReleaseService = Depends(_service),
) -> DeploymentCheckRead:
    return DeploymentCheckRead.model_validate(service.add_check(deployment_id, body))


@router.get("/deployments/{deployment_id}/checks", response_model=list[DeploymentCheckRead])
def list_checks(
    deployment_id: UUID, service: ReleaseService = Depends(_service)
) -> list[DeploymentCheckRead]:
    return [DeploymentCheckRead.model_validate(r) for r in service.list_checks(deployment_id)]


@router.get("/{release_id}", response_model=ReleaseRead)
def get_release(
    release_id: UUID, service: ReleaseService = Depends(_service)
) -> ReleaseRead:
    return ReleaseRead.model_validate(service.get_release(release_id))


@router.get("/{release_id}/traceability", response_model=TraceabilitySummary)
def traceability(
    release_id: UUID, service: ReleaseService = Depends(_service)
) -> TraceabilitySummary:
    return service.traceability(release_id)


@router.post("/{release_id}/items", response_model=ReleaseItemRead, status_code=201)
def add_item(
    release_id: UUID,
    body: ReleaseItemCreate,
    service: ReleaseService = Depends(_service),
) -> ReleaseItemRead:
    return ReleaseItemRead.model_validate(service.add_item(release_id, body))


@router.get("/{release_id}/items", response_model=list[ReleaseItemRead])
def list_items(
    release_id: UUID, service: ReleaseService = Depends(_service)
) -> list[ReleaseItemRead]:
    return [ReleaseItemRead.model_validate(r) for r in service.list_items(release_id)]


@router.post("/{release_id}/submit", response_model=ReleaseRead)
def submit(
    release_id: UUID,
    body: SubmitApproval | None = None,
    service: ReleaseService = Depends(_service),
) -> ReleaseRead:
    return ReleaseRead.model_validate(
        service.submit_for_approval(release_id, body or SubmitApproval())
    )


@router.post("/{release_id}/approve", response_model=ReleaseRead)
def approve(
    release_id: UUID,
    body: ApproveRelease,
    service: ReleaseService = Depends(_service),
) -> ReleaseRead:
    return ReleaseRead.model_validate(service.approve(release_id, body))


@router.post("/{release_id}/backups", response_model=BackupRead, status_code=201)
def add_backup(
    release_id: UUID,
    body: BackupCreate,
    service: ReleaseService = Depends(_service),
) -> BackupRead:
    return BackupRead.model_validate(service.add_backup(release_id, body))


@router.get("/{release_id}/backups", response_model=list[BackupRead])
def list_backups(
    release_id: UUID, service: ReleaseService = Depends(_service)
) -> list[BackupRead]:
    return [BackupRead.model_validate(r) for r in service.list_backups(release_id)]


@router.post(
    "/{release_id}/migration-plans",
    response_model=MigrationPlanRead,
    status_code=201,
)
def add_migration(
    release_id: UUID,
    body: MigrationPlanCreate,
    service: ReleaseService = Depends(_service),
) -> MigrationPlanRead:
    return MigrationPlanRead.model_validate(service.add_migration_plan(release_id, body))


@router.get("/{release_id}/migration-plans", response_model=list[MigrationPlanRead])
def list_migrations(
    release_id: UUID, service: ReleaseService = Depends(_service)
) -> list[MigrationPlanRead]:
    return [
        MigrationPlanRead.model_validate(r) for r in service.list_migration_plans(release_id)
    ]


@router.post("/{release_id}/deployments", response_model=DeploymentRead, status_code=201)
def start_deployment(
    release_id: UUID,
    body: DeploymentCreate,
    service: ReleaseService = Depends(_service),
) -> DeploymentRead:
    return DeploymentRead.model_validate(service.start_deployment(release_id, body))


@router.get("/{release_id}/deployments", response_model=list[DeploymentRead])
def list_deployments(
    release_id: UUID, service: ReleaseService = Depends(_service)
) -> list[DeploymentRead]:
    return [DeploymentRead.model_validate(r) for r in service.list_deployments(release_id)]


@router.post("/{release_id}/rollbacks", response_model=RollbackRead, status_code=201)
def rollback(
    release_id: UUID,
    body: RollbackCreate,
    service: ReleaseService = Depends(_service),
) -> RollbackRead:
    return RollbackRead.model_validate(service.rollback(release_id, body))


@router.get("/{release_id}/rollbacks", response_model=list[RollbackRead])
def list_rollbacks(
    release_id: UUID, service: ReleaseService = Depends(_service)
) -> list[RollbackRead]:
    return [RollbackRead.model_validate(r) for r in service.list_rollbacks(release_id)]


@router.put("/{release_id}/completion", response_model=CompletionReportRead)
def upsert_completion(
    release_id: UUID,
    body: CompletionReportCreate,
    service: ReleaseService = Depends(_service),
) -> CompletionReportRead:
    return CompletionReportRead.model_validate(service.upsert_completion(release_id, body))


@router.get("/{release_id}/completion", response_model=CompletionReportRead | None)
def get_completion(
    release_id: UUID, service: ReleaseService = Depends(_service)
) -> CompletionReportRead | None:
    row = service.get_completion(release_id)
    return CompletionReportRead.model_validate(row) if row else None
