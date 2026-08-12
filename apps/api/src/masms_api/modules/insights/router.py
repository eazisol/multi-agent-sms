"""HTTP routes for MOD-450 insights."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.insights.schemas import (
    ActivityCreate,
    ActivityEventRead,
    DashboardRefresh,
    DashboardSnapshotRead,
    ExportCreate,
    ExportRead,
    ProjectHealthRead,
    ProjectHealthUpsert,
    ReportCreate,
    ReportRead,
    SavedFilterCreate,
    SavedFilterRead,
    SearchDocumentRead,
    SearchIndexCreate,
)
from masms_api.modules.insights.service import InsightsService

router = APIRouter(prefix="/insights", tags=["insights"])


class ProjectHealthPage(BaseModel):
    items: list[ProjectHealthRead]
    page: PageMeta = Field(description="Pagination metadata")


class SavedFilterPage(BaseModel):
    items: list[SavedFilterRead]
    page: PageMeta = Field(description="Pagination metadata")


class SearchPage(BaseModel):
    items: list[SearchDocumentRead]
    page: PageMeta = Field(description="Pagination metadata")


class ActivityPage(BaseModel):
    items: list[ActivityEventRead]
    page: PageMeta = Field(description="Pagination metadata")


class ReportPage(BaseModel):
    items: list[ReportRead]
    page: PageMeta = Field(description="Pagination metadata")


class ExportPage(BaseModel):
    items: list[ExportRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> InsightsService:
    return InsightsService(db, ctx)


@router.get("/dashboard", response_model=DashboardSnapshotRead)
def get_dashboard(
    project_id: UUID | None = Query(default=None),
    service: InsightsService = Depends(_service),
) -> DashboardSnapshotRead:
    return service.get_dashboard(project_id=project_id)


@router.post("/dashboard", response_model=DashboardSnapshotRead)
@router.post("/dashboard/refresh", response_model=DashboardSnapshotRead)
def refresh_dashboard(
    body: DashboardRefresh | None = None,
    service: InsightsService = Depends(_service),
) -> DashboardSnapshotRead:
    return service.refresh_dashboard(body)


@router.get("/project-health", response_model=ProjectHealthPage)
def list_project_health(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: InsightsService = Depends(_service),
) -> ProjectHealthPage:
    items, page = service.list_project_health(limit=limit, offset=offset)
    return ProjectHealthPage(
        items=[ProjectHealthRead.model_validate(r) for r in items], page=page
    )


@router.post("/project-health", response_model=ProjectHealthRead, status_code=201)
def upsert_project_health(
    body: ProjectHealthUpsert, service: InsightsService = Depends(_service)
) -> ProjectHealthRead:
    return ProjectHealthRead.model_validate(service.upsert_project_health(body))


@router.get("/saved-filters", response_model=SavedFilterPage)
def list_saved_filters(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: InsightsService = Depends(_service),
) -> SavedFilterPage:
    items, page = service.list_saved_filters(limit=limit, offset=offset)
    return SavedFilterPage(
        items=[SavedFilterRead.model_validate(r) for r in items], page=page
    )


@router.post("/saved-filters", response_model=SavedFilterRead, status_code=201)
def create_saved_filter(
    body: SavedFilterCreate, service: InsightsService = Depends(_service)
) -> SavedFilterRead:
    return SavedFilterRead.model_validate(service.create_saved_filter(body))


@router.delete("/saved-filters/{filter_id}", status_code=204)
def delete_saved_filter(
    filter_id: UUID, service: InsightsService = Depends(_service)
) -> Response:
    service.delete_saved_filter(filter_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/search/index", response_model=SearchDocumentRead, status_code=201)
def index_search_document(
    body: SearchIndexCreate, service: InsightsService = Depends(_service)
) -> SearchDocumentRead:
    return SearchDocumentRead.model_validate(service.index_search_document(body))


@router.get("/search", response_model=SearchPage)
def global_search(
    q: str = Query(min_length=1),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: InsightsService = Depends(_service),
) -> SearchPage:
    items, page = service.global_search(q=q, limit=limit, offset=offset)
    return SearchPage(
        items=[SearchDocumentRead.model_validate(r) for r in items], page=page
    )


@router.get("/activity", response_model=ActivityPage)
def list_activity(
    project_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: InsightsService = Depends(_service),
) -> ActivityPage:
    items, page = service.list_activity(
        project_id=project_id, limit=limit, offset=offset
    )
    return ActivityPage(
        items=[ActivityEventRead.model_validate(r) for r in items], page=page
    )


@router.post("/activity", response_model=ActivityEventRead, status_code=201)
def record_activity(
    body: ActivityCreate, service: InsightsService = Depends(_service)
) -> ActivityEventRead:
    return ActivityEventRead.model_validate(service.record_activity(body))


@router.get("/reports", response_model=ReportPage)
def list_reports(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: InsightsService = Depends(_service),
) -> ReportPage:
    items, page = service.list_reports(limit=limit, offset=offset)
    return ReportPage(items=[ReportRead.model_validate(r) for r in items], page=page)


@router.post("/reports", response_model=ReportRead, status_code=201)
def create_report(
    body: ReportCreate, service: InsightsService = Depends(_service)
) -> ReportRead:
    return ReportRead.model_validate(service.create_report(body))


@router.get("/exports", response_model=ExportPage)
def list_exports(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: InsightsService = Depends(_service),
) -> ExportPage:
    items, page = service.list_exports(limit=limit, offset=offset)
    return ExportPage(items=[ExportRead.model_validate(r) for r in items], page=page)


@router.post("/exports", response_model=ExportRead, status_code=201)
def create_export(
    body: ExportCreate, service: InsightsService = Depends(_service)
) -> ExportRead:
    return ExportRead.model_validate(service.create_export(body))
