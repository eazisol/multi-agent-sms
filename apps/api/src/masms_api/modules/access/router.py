"""HTTP routes for MOD-120 access control."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.errors import ForbiddenError
from masms_api.modules.access.schemas import (
    AccessReviewComplete,
    AccessReviewCreate,
    AccessReviewRead,
    ApprovalAuthorityCreate,
    ApprovalAuthorityRead,
    DocumentAccessCreate,
    DocumentAccessRead,
    ModuleAccessCreate,
    ModuleAccessRead,
    PermissionCheckRequest,
    PermissionCheckResponse,
    PermissionCreate,
    PermissionRead,
    ProjectMemberCreate,
    ProjectMemberRead,
    RolePermissionCreate,
    RolePermissionRead,
)
from masms_api.modules.access.service import AccessService

router = APIRouter(prefix="/access", tags=["access"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> AccessService:
    return AccessService(db, ctx)


@router.post("/permissions", response_model=PermissionRead, status_code=201)
def create_permission(
    body: PermissionCreate,
    service: AccessService = Depends(_service),
) -> PermissionRead:
    return PermissionRead.model_validate(service.create_permission(body))


@router.get("/permissions", response_model=list[PermissionRead])
def list_permissions(service: AccessService = Depends(_service)) -> list[PermissionRead]:
    return [PermissionRead.model_validate(r) for r in service.list_permissions()]


@router.post("/role-permissions", response_model=RolePermissionRead, status_code=201)
def grant_role_permission(
    body: RolePermissionCreate,
    service: AccessService = Depends(_service),
) -> RolePermissionRead:
    return RolePermissionRead.model_validate(service.grant_role_permission(body))


@router.post("/project-members", response_model=ProjectMemberRead, status_code=201)
def add_project_member(
    body: ProjectMemberCreate,
    service: AccessService = Depends(_service),
) -> ProjectMemberRead:
    return ProjectMemberRead.model_validate(service.add_project_member(body))


@router.post("/module-access", response_model=ModuleAccessRead, status_code=201)
def grant_module_access(
    body: ModuleAccessCreate,
    service: AccessService = Depends(_service),
) -> ModuleAccessRead:
    return ModuleAccessRead.model_validate(service.grant_module_access(body))


@router.post("/document-access", response_model=DocumentAccessRead, status_code=201)
def grant_document_access(
    body: DocumentAccessCreate,
    service: AccessService = Depends(_service),
) -> DocumentAccessRead:
    return DocumentAccessRead.model_validate(service.grant_document_access(body))


@router.post("/approval-authorities", response_model=ApprovalAuthorityRead, status_code=201)
def create_approval_authority(
    body: ApprovalAuthorityCreate,
    service: AccessService = Depends(_service),
) -> ApprovalAuthorityRead:
    return ApprovalAuthorityRead.model_validate(service.create_approval_authority(body))


@router.post("/reviews", response_model=AccessReviewRead, status_code=201)
def create_access_review(
    body: AccessReviewCreate,
    service: AccessService = Depends(_service),
) -> AccessReviewRead:
    return AccessReviewRead.model_validate(service.create_access_review(body))


@router.post("/reviews/{review_id}/complete", response_model=AccessReviewRead)
def complete_access_review(
    review_id: UUID,
    body: AccessReviewComplete,
    service: AccessService = Depends(_service),
) -> AccessReviewRead:
    return AccessReviewRead.model_validate(service.complete_access_review(review_id, body))


@router.post("/checks/permission", response_model=PermissionCheckResponse)
def check_permission(
    body: PermissionCheckRequest,
    service: AccessService = Depends(_service),
) -> PermissionCheckResponse:
    if body.role_id is None:
        return PermissionCheckResponse(
            allowed=False,
            permission_code=body.permission_code,
            reason="role_id is required for role-permission checks in M1",
        )
    try:
        if body.project_id is not None:
            service.require_project_access(project_id=body.project_id)
        service.require_permission(role_id=body.role_id, permission_code=body.permission_code)
    except ForbiddenError as exc:
        return PermissionCheckResponse(
            allowed=False,
            permission_code=body.permission_code,
            reason=exc.message,
        )
    return PermissionCheckResponse(
        allowed=True,
        permission_code=body.permission_code,
        reason="granted",
    )
