"""HTTP routes for MOD-460 traceability."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.traceability.schemas import (
    AuditCoverageReport,
    CoverageReport,
    ExportCreate,
    ExportRead,
    ManifestCreate,
    ManifestItemCreate,
    ManifestItemRead,
    ManifestRead,
    ManifestSeal,
    MustHaveCreate,
    MustHaveRead,
    RequirementDocumentLinkCreate,
    RequirementDocumentLinkRead,
    RequirementReleaseLinkCreate,
    RequirementReleaseLinkRead,
    RequirementTestLinkCreate,
    RequirementTestLinkRead,
    RequirementTicketLinkCreate,
    RequirementTicketLinkRead,
    TicketTestLinkCreate,
    TicketTestLinkRead,
)
from masms_api.modules.traceability.service import TraceabilityService

router = APIRouter(prefix="/traceability", tags=["traceability"])


class MustHavePage(BaseModel):
    items: list[MustHaveRead]
    page: PageMeta = Field(description="Pagination metadata")


class RequirementTicketLinkPage(BaseModel):
    items: list[RequirementTicketLinkRead]
    page: PageMeta = Field(description="Pagination metadata")


class RequirementTestLinkPage(BaseModel):
    items: list[RequirementTestLinkRead]
    page: PageMeta = Field(description="Pagination metadata")


class RequirementReleaseLinkPage(BaseModel):
    items: list[RequirementReleaseLinkRead]
    page: PageMeta = Field(description="Pagination metadata")


class RequirementDocumentLinkPage(BaseModel):
    items: list[RequirementDocumentLinkRead]
    page: PageMeta = Field(description="Pagination metadata")


class TicketTestLinkPage(BaseModel):
    items: list[TicketTestLinkRead]
    page: PageMeta = Field(description="Pagination metadata")


class ManifestPage(BaseModel):
    items: list[ManifestRead]
    page: PageMeta = Field(description="Pagination metadata")


class ExportPage(BaseModel):
    items: list[ExportRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> TraceabilityService:
    return TraceabilityService(db, ctx)


@router.post("/must-haves", response_model=MustHaveRead, status_code=201)
def register_must_have(
    body: MustHaveCreate, service: TraceabilityService = Depends(_service)
) -> MustHaveRead:
    return MustHaveRead.model_validate(service.register_must_have(body))


@router.get("/must-haves", response_model=MustHavePage)
def list_must_haves(
    project_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: TraceabilityService = Depends(_service),
) -> MustHavePage:
    items, page = service.list_must_haves(
        project_id=project_id, limit=limit, offset=offset
    )
    return MustHavePage(items=[MustHaveRead.model_validate(r) for r in items], page=page)


@router.post(
    "/links/requirement-tickets",
    response_model=RequirementTicketLinkRead,
    status_code=201,
)
def create_requirement_ticket_link(
    body: RequirementTicketLinkCreate, service: TraceabilityService = Depends(_service)
) -> RequirementTicketLinkRead:
    return RequirementTicketLinkRead.model_validate(
        service.create_requirement_ticket_link(body)
    )


@router.get("/links/requirement-tickets", response_model=RequirementTicketLinkPage)
def list_requirement_ticket_links(
    requirement_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: TraceabilityService = Depends(_service),
) -> RequirementTicketLinkPage:
    items, page = service.list_requirement_ticket_links(
        requirement_id=requirement_id, limit=limit, offset=offset
    )
    return RequirementTicketLinkPage(
        items=[RequirementTicketLinkRead.model_validate(r) for r in items], page=page
    )


@router.post(
    "/links/requirement-tests",
    response_model=RequirementTestLinkRead,
    status_code=201,
)
def create_requirement_test_link(
    body: RequirementTestLinkCreate, service: TraceabilityService = Depends(_service)
) -> RequirementTestLinkRead:
    return RequirementTestLinkRead.model_validate(
        service.create_requirement_test_link(body)
    )


@router.get("/links/requirement-tests", response_model=RequirementTestLinkPage)
def list_requirement_test_links(
    requirement_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: TraceabilityService = Depends(_service),
) -> RequirementTestLinkPage:
    items, page = service.list_requirement_test_links(
        requirement_id=requirement_id, limit=limit, offset=offset
    )
    return RequirementTestLinkPage(
        items=[RequirementTestLinkRead.model_validate(r) for r in items], page=page
    )


@router.post(
    "/links/requirement-releases",
    response_model=RequirementReleaseLinkRead,
    status_code=201,
)
def create_requirement_release_link(
    body: RequirementReleaseLinkCreate, service: TraceabilityService = Depends(_service)
) -> RequirementReleaseLinkRead:
    return RequirementReleaseLinkRead.model_validate(
        service.create_requirement_release_link(body)
    )


@router.get("/links/requirement-releases", response_model=RequirementReleaseLinkPage)
def list_requirement_release_links(
    requirement_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: TraceabilityService = Depends(_service),
) -> RequirementReleaseLinkPage:
    items, page = service.list_requirement_release_links(
        requirement_id=requirement_id, limit=limit, offset=offset
    )
    return RequirementReleaseLinkPage(
        items=[RequirementReleaseLinkRead.model_validate(r) for r in items], page=page
    )


@router.post(
    "/links/requirement-documents",
    response_model=RequirementDocumentLinkRead,
    status_code=201,
)
def create_requirement_document_link(
    body: RequirementDocumentLinkCreate, service: TraceabilityService = Depends(_service)
) -> RequirementDocumentLinkRead:
    return RequirementDocumentLinkRead.model_validate(
        service.create_requirement_document_link(body)
    )


@router.get("/links/requirement-documents", response_model=RequirementDocumentLinkPage)
def list_requirement_document_links(
    requirement_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: TraceabilityService = Depends(_service),
) -> RequirementDocumentLinkPage:
    items, page = service.list_requirement_document_links(
        requirement_id=requirement_id, limit=limit, offset=offset
    )
    return RequirementDocumentLinkPage(
        items=[RequirementDocumentLinkRead.model_validate(r) for r in items], page=page
    )


@router.post("/links/ticket-tests", response_model=TicketTestLinkRead, status_code=201)
def create_ticket_test_link(
    body: TicketTestLinkCreate, service: TraceabilityService = Depends(_service)
) -> TicketTestLinkRead:
    return TicketTestLinkRead.model_validate(service.create_ticket_test_link(body))


@router.get("/links/ticket-tests", response_model=TicketTestLinkPage)
def list_ticket_test_links(
    ticket_id: UUID | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: TraceabilityService = Depends(_service),
) -> TicketTestLinkPage:
    items, page = service.list_ticket_test_links(
        ticket_id=ticket_id, limit=limit, offset=offset
    )
    return TicketTestLinkPage(
        items=[TicketTestLinkRead.model_validate(r) for r in items], page=page
    )


@router.get("/coverage", response_model=CoverageReport)
def coverage_report(
    project_id: UUID | None = Query(default=None),
    service: TraceabilityService = Depends(_service),
) -> CoverageReport:
    return service.coverage_report(project_id=project_id)


@router.get("/audit-coverage", response_model=AuditCoverageReport)
def audit_coverage(
    service: TraceabilityService = Depends(_service),
) -> AuditCoverageReport:
    return service.audit_coverage()


@router.post("/manifests", response_model=ManifestRead, status_code=201)
def create_manifest(
    body: ManifestCreate, service: TraceabilityService = Depends(_service)
) -> ManifestRead:
    return ManifestRead.model_validate(service.create_manifest(body))


@router.get("/manifests", response_model=ManifestPage)
def list_manifests(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: TraceabilityService = Depends(_service),
) -> ManifestPage:
    items, page = service.list_manifests(limit=limit, offset=offset)
    return ManifestPage(items=[ManifestRead.model_validate(r) for r in items], page=page)


@router.get("/manifests/{manifest_id}", response_model=ManifestRead)
def get_manifest(
    manifest_id: UUID, service: TraceabilityService = Depends(_service)
) -> ManifestRead:
    return ManifestRead.model_validate(service.get_manifest(manifest_id))


@router.post(
    "/manifests/{manifest_id}/items",
    response_model=ManifestItemRead,
    status_code=201,
)
def add_manifest_item(
    manifest_id: UUID,
    body: ManifestItemCreate,
    service: TraceabilityService = Depends(_service),
) -> ManifestItemRead:
    return ManifestItemRead.model_validate(service.add_manifest_item(manifest_id, body))


@router.post("/manifests/{manifest_id}/seal", response_model=ManifestRead)
def seal_manifest(
    manifest_id: UUID,
    body: ManifestSeal | None = None,
    service: TraceabilityService = Depends(_service),
) -> ManifestRead:
    return ManifestRead.model_validate(service.seal_manifest(manifest_id, body))


@router.post("/exports", response_model=ExportRead, status_code=201)
def create_export(
    body: ExportCreate, service: TraceabilityService = Depends(_service)
) -> ExportRead:
    return ExportRead.model_validate(service.create_export(body))


@router.get("/exports", response_model=ExportPage)
def list_exports(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: TraceabilityService = Depends(_service),
) -> ExportPage:
    items, page = service.list_exports(limit=limit, offset=offset)
    return ExportPage(items=[ExportRead.model_validate(r) for r in items], page=page)


@router.get("/exports/{export_id}", response_model=ExportRead)
def get_export(
    export_id: UUID, service: TraceabilityService = Depends(_service)
) -> ExportRead:
    return ExportRead.model_validate(service.get_export(export_id))
