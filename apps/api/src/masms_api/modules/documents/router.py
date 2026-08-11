"""HTTP routes for MOD-250 documents and secure storage metadata."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.documents.schemas import (
    AccessCheckRead,
    AccessCheckRequest,
    AttachmentCreate,
    AttachmentRead,
    DocumentCreate,
    DocumentRead,
    DocumentVersionCreate,
    DocumentVersionRead,
    MarkAvailableRequest,
    PermissionCreate,
    PermissionRead,
    ScanResultCreate,
    ScanResultRead,
    TemplateCreate,
    TemplateRead,
    TemplateVersionCreate,
    TemplateVersionRead,
)
from masms_api.modules.documents.service import DocumentsService

router = APIRouter(prefix="/documents", tags=["documents"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> DocumentsService:
    return DocumentsService(db, ctx)


@router.post("/templates", response_model=TemplateRead, status_code=201)
def create_template(
    body: TemplateCreate, service: DocumentsService = Depends(_service)
) -> TemplateRead:
    return TemplateRead.model_validate(service.create_template(body))


@router.post("/template-versions", response_model=TemplateVersionRead, status_code=201)
def create_template_version(
    body: TemplateVersionCreate, service: DocumentsService = Depends(_service)
) -> TemplateVersionRead:
    return TemplateVersionRead.model_validate(service.create_template_version(body))


@router.post(
    "/template-versions/{version_id}/publish",
    response_model=TemplateVersionRead,
)
def publish_template_version(
    version_id: UUID, service: DocumentsService = Depends(_service)
) -> TemplateVersionRead:
    return TemplateVersionRead.model_validate(service.publish_template_version(version_id))


@router.post("", response_model=DocumentRead, status_code=201)
def create_document(
    body: DocumentCreate, service: DocumentsService = Depends(_service)
) -> DocumentRead:
    return DocumentRead.model_validate(service.create_document(body))


@router.post("/versions", response_model=DocumentVersionRead, status_code=201)
def create_document_version(
    body: DocumentVersionCreate, service: DocumentsService = Depends(_service)
) -> DocumentVersionRead:
    return DocumentVersionRead.model_validate(service.create_document_version(body))


@router.post(
    "/versions/{version_id}/available",
    response_model=DocumentVersionRead,
)
def mark_available(
    version_id: UUID,
    body: MarkAvailableRequest,
    service: DocumentsService = Depends(_service),
) -> DocumentVersionRead:
    return DocumentVersionRead.model_validate(service.mark_available(version_id, body))


@router.post("/attachments", response_model=AttachmentRead, status_code=201)
def add_attachment(
    body: AttachmentCreate, service: DocumentsService = Depends(_service)
) -> AttachmentRead:
    return AttachmentRead.model_validate(service.add_attachment(body))


@router.post("/permissions", response_model=PermissionRead, status_code=201)
def grant_permission(
    body: PermissionCreate, service: DocumentsService = Depends(_service)
) -> PermissionRead:
    return PermissionRead.model_validate(service.grant_permission(body))


@router.post("/scan-results", response_model=ScanResultRead, status_code=201)
def record_scan(
    body: ScanResultCreate, service: DocumentsService = Depends(_service)
) -> ScanResultRead:
    return ScanResultRead.model_validate(service.record_scan(body))


@router.post("/access-check", response_model=AccessCheckRead)
def check_access(
    body: AccessCheckRequest, service: DocumentsService = Depends(_service)
) -> AccessCheckRead:
    return AccessCheckRead.model_validate(service.check_access(body))
