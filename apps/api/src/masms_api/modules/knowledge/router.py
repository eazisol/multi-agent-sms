"""HTTP routes for MOD-370 knowledge base."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.knowledge.schemas import (
    ActivateVersion,
    CitationHit,
    ChunkRead,
    ConflictCreate,
    ConflictRead,
    ConflictResolve,
    ItemCreate,
    ItemRead,
    PermissionCreate,
    PermissionRead,
    SearchRequest,
    SearchResponse,
    UsageLogRead,
    VersionCreate,
    VersionRead,
)
from masms_api.modules.knowledge.service import KnowledgeService

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


class ItemPage(BaseModel):
    items: list[ItemRead]
    page: PageMeta = Field(description="Pagination metadata")


class UsagePage(BaseModel):
    items: list[UsageLogRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> KnowledgeService:
    return KnowledgeService(db, ctx)


@router.post("/items", response_model=ItemRead, status_code=201)
def create_item(
    body: ItemCreate,
    service: KnowledgeService = Depends(_service),
) -> ItemRead:
    return ItemRead.model_validate(service.create_item(body))


@router.get("/items", response_model=ItemPage)
def list_items(
    status: str | None = Query(default=None),
    project_id: UUID | None = Query(default=None),
    q: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: KnowledgeService = Depends(_service),
) -> ItemPage:
    items, page = service.list_items(
        status=status, project_id=project_id, q=q, limit=limit, offset=offset
    )
    return ItemPage(items=[ItemRead.model_validate(r) for r in items], page=page)


@router.get("/items/{item_id}", response_model=ItemRead)
def get_item(
    item_id: UUID,
    service: KnowledgeService = Depends(_service),
) -> ItemRead:
    return ItemRead.model_validate(service.get_item(item_id))


@router.post("/items/{item_id}/versions", response_model=VersionRead, status_code=201)
def create_version(
    item_id: UUID,
    body: VersionCreate,
    service: KnowledgeService = Depends(_service),
) -> VersionRead:
    return VersionRead.model_validate(service.create_version(item_id, body))


@router.get("/versions", response_model=list[VersionRead])
def list_versions(
    item_id: UUID | None = Query(default=None),
    service: KnowledgeService = Depends(_service),
) -> list[VersionRead]:
    return [VersionRead.model_validate(r) for r in service.list_versions(item_id)]


@router.post("/versions/{version_id}/activate", response_model=VersionRead)
def activate_version(
    version_id: UUID,
    body: ActivateVersion | None = None,
    service: KnowledgeService = Depends(_service),
) -> VersionRead:
    return VersionRead.model_validate(service.activate_version(version_id, body))


@router.get("/versions/{version_id}/chunks", response_model=list[ChunkRead])
def list_chunks(
    version_id: UUID,
    service: KnowledgeService = Depends(_service),
) -> list[ChunkRead]:
    return [ChunkRead.model_validate(r) for r in service.list_chunks(version_id)]


@router.post(
    "/items/{item_id}/permissions",
    response_model=PermissionRead,
    status_code=201,
)
def add_permission(
    item_id: UUID,
    body: PermissionCreate,
    service: KnowledgeService = Depends(_service),
) -> PermissionRead:
    return PermissionRead.model_validate(service.add_permission(item_id, body))


@router.get("/items/{item_id}/permissions", response_model=list[PermissionRead])
def list_permissions(
    item_id: UUID,
    service: KnowledgeService = Depends(_service),
) -> list[PermissionRead]:
    return [PermissionRead.model_validate(r) for r in service.list_permissions(item_id)]


@router.post("/search", response_model=SearchResponse)
def search(
    body: SearchRequest,
    service: KnowledgeService = Depends(_service),
) -> SearchResponse:
    hits = service.search(body)
    return SearchResponse(
        query=body.query,
        items=[CitationHit.model_validate(h) for h in hits],
        stub=True,
    )


@router.post("/conflicts", response_model=ConflictRead, status_code=201)
def create_conflict(
    body: ConflictCreate,
    service: KnowledgeService = Depends(_service),
) -> ConflictRead:
    return ConflictRead.model_validate(service.create_conflict(body))


@router.post("/conflicts/{conflict_id}/resolve", response_model=ConflictRead)
def resolve_conflict(
    conflict_id: UUID,
    body: ConflictResolve,
    service: KnowledgeService = Depends(_service),
) -> ConflictRead:
    return ConflictRead.model_validate(service.resolve_conflict(conflict_id, body))


@router.get("/conflicts", response_model=list[ConflictRead])
def list_conflicts(
    status: str | None = Query(default=None),
    service: KnowledgeService = Depends(_service),
) -> list[ConflictRead]:
    return [ConflictRead.model_validate(r) for r in service.list_conflicts(status=status)]


@router.get("/usage-logs", response_model=UsagePage)
def list_usage_logs(
    item_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: KnowledgeService = Depends(_service),
) -> UsagePage:
    items, page = service.list_usage_logs(item_id=item_id, limit=limit, offset=offset)
    return UsagePage(items=[UsageLogRead.model_validate(r) for r in items], page=page)
