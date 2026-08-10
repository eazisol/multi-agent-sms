"""Access application service (MOD-120)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, ForbiddenError, NotFoundError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.access import domain
from masms_api.modules.access.models import (
    AccessReview,
    ApprovalAuthority,
    DocumentAccess,
    ModuleAccess,
    Permission,
    ProjectMember,
    RolePermission,
)
from masms_api.modules.access.schemas import (
    AccessReviewComplete,
    AccessReviewCreate,
    ApprovalAuthorityCreate,
    DocumentAccessCreate,
    ModuleAccessCreate,
    PermissionCreate,
    ProjectMemberCreate,
    RolePermissionCreate,
)
from masms_api.modules.identity.models import RoleDefinition
from masms_api.observability.writer import ObservabilityWriter


class AccessService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_permission(self, data: PermissionCreate) -> Permission:
        existing = self.db.scalar(
            select(Permission).where(
                Permission.organization_id == self.ctx.organization_id,
                Permission.code == data.code,
            )
        )
        if existing is not None:
            raise ConflictError(f"Permission '{data.code}' already exists")
        row = Permission(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code,
            module_key=data.module_key,
            action_key=data.action_key,
            title=data.title,
            description=data.description,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="permission_create",
            entity_type="auth_permission",
            entity_id=row.id,
            payload={"code": data.code},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_permissions(self) -> list[Permission]:
        rows = self.db.scalars(
            select(Permission).where(Permission.organization_id == self.ctx.organization_id)
        )
        return list(rows)

    def grant_role_permission(self, data: RolePermissionCreate) -> RolePermission:
        role = self.db.scalar(select(RoleDefinition).where(RoleDefinition.id == data.role_id))
        if role is None or role.organization_id != self.ctx.organization_id:
            raise NotFoundError("Role not found")
        permission = self.db.scalar(select(Permission).where(Permission.id == data.permission_id))
        if permission is None or permission.organization_id != self.ctx.organization_id:
            raise NotFoundError("Permission not found")
        existing = self.db.scalar(
            select(RolePermission).where(
                RolePermission.role_id == data.role_id,
                RolePermission.permission_id == data.permission_id,
            )
        )
        if existing is not None:
            raise ConflictError("Role already has this permission")
        row = RolePermission(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            role_id=data.role_id,
            permission_id=data.permission_id,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="role_permission_grant",
            entity_type="org_role_permission",
            entity_id=row.id,
            payload={"role_id": str(data.role_id), "permission_id": str(data.permission_id)},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def add_project_member(self, data: ProjectMemberCreate) -> ProjectMember:
        existing = self.db.scalar(
            select(ProjectMember).where(
                ProjectMember.organization_id == self.ctx.organization_id,
                ProjectMember.project_id == data.project_id,
                ProjectMember.actor_id == data.actor_id,
            )
        )
        if existing is not None:
            raise ConflictError("Actor is already a project member")
        row = ProjectMember(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            client_id=data.client_id,
            project_id=data.project_id,
            actor_id=data.actor_id,
            role_code=data.role_code,
            access_level=data.access_level,
            status="active",
            assigned_by_actor_id=self.ctx.actor_id,
            effective_from=data.effective_from or datetime.now(UTC),
            effective_to=data.effective_to,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="project_member_add",
            entity_type="org_project_member",
            entity_id=row.id,
            payload={"project_id": str(data.project_id), "actor_id": str(data.actor_id)},
            project_id=data.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def grant_module_access(self, data: ModuleAccessCreate) -> ModuleAccess:
        row = ModuleAccess(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            actor_id=data.actor_id,
            module_key=data.module_key,
            project_id=data.project_id,
            access_level=data.access_level,
            status="active",
            granted_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="module_access_grant",
            entity_type="org_module_access",
            entity_id=row.id,
            payload={"module_key": data.module_key, "actor_id": str(data.actor_id)},
            project_id=data.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def grant_document_access(self, data: DocumentAccessCreate) -> DocumentAccess:
        domain.assert_document_principal(actor_id=data.actor_id, role_code=data.role_code)
        row = DocumentAccess(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            document_ref=data.document_ref,
            classification=data.classification,
            actor_id=data.actor_id,
            role_code=data.role_code,
            access_level=data.access_level,
            status="active",
            granted_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="document_access_grant",
            entity_type="org_document_access",
            entity_id=row.id,
            payload={"document_ref": data.document_ref, "classification": data.classification},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_approval_authority(self, data: ApprovalAuthorityCreate) -> ApprovalAuthority:
        domain.assert_authority_subject(
            actor_id=data.authority_actor_id,
            role_code=data.authority_role_code,
        )
        row = ApprovalAuthority(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            action_code=data.action_code,
            authority_actor_id=data.authority_actor_id,
            authority_role_code=data.authority_role_code,
            client_id=data.client_id,
            project_id=data.project_id,
            environment=data.environment,
            amount_threshold=data.amount_threshold,
            status="active",
            effective_from=data.effective_from or datetime.now(UTC),
            effective_to=data.effective_to,
            delegated_from_authority_id=data.delegated_from_authority_id,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="approval_authority_create",
            entity_type="org_approval_authority",
            entity_id=row.id,
            payload={"action_code": data.action_code},
            project_id=data.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_access_review(self, data: AccessReviewCreate) -> AccessReview:
        row = AccessReview(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            title=data.title,
            status="open",
            due_at=data.due_at,
            owner_actor_id=data.owner_actor_id,
            summary=data.summary,
            findings_json={},
            created_by_actor_id=self.ctx.actor_id,
            version=1,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="access_review_create",
            entity_type="org_access_review",
            entity_id=row.id,
            payload={"title": data.title},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def complete_access_review(
        self, review_id: UUID, data: AccessReviewComplete
    ) -> AccessReview:
        row = self.db.scalar(select(AccessReview).where(AccessReview.id == review_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Access review not found")
        domain.assert_review_open(row.status)
        row.status = "completed"
        row.completed_at = datetime.now(UTC)
        if data.summary is not None:
            row.summary = data.summary
        row.findings_json = data.findings
        row.version += 1
        self.uow.add(row)
        self.obs.write_audit(
            action="access_review_complete",
            entity_type="org_access_review",
            entity_id=row.id,
            entity_version=row.version,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def has_role_permission(self, *, role_id: UUID, permission_code: str) -> bool:
        permission = self.db.scalar(
            select(Permission).where(
                Permission.organization_id == self.ctx.organization_id,
                Permission.code == permission_code,
                Permission.status == "active",
            )
        )
        if permission is None:
            return False
        grant = self.db.scalar(
            select(RolePermission).where(
                RolePermission.organization_id == self.ctx.organization_id,
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission.id,
                RolePermission.status == "active",
            )
        )
        return grant is not None

    def require_permission(self, *, role_id: UUID, permission_code: str) -> None:
        domain.require_permission_granted(
            granted=self.has_role_permission(role_id=role_id, permission_code=permission_code),
            permission_code=permission_code,
        )

    def require_project_access(
        self, *, project_id: UUID, actor_id: UUID | None = None
    ) -> ProjectMember:
        target = actor_id or self.ctx.actor_id
        member = self.db.scalar(
            select(ProjectMember).where(
                ProjectMember.organization_id == self.ctx.organization_id,
                ProjectMember.project_id == project_id,
                ProjectMember.actor_id == target,
                ProjectMember.status == "active",
            )
        )
        domain.require_project_membership(has_membership=member is not None, project_id=project_id)
        assert member is not None
        domain.assert_effective_window(
            effective_from=member.effective_from,
            effective_to=member.effective_to,
            entity="project membership",
        )
        return member

    def assert_client_scope(self, *, resource_client_id: UUID | None) -> None:
        """Deny cross-client access when both sides declare a client scope."""
        ctx_client = self.ctx.tenant.client_id
        if ctx_client is None or resource_client_id is None:
            return
        if resource_client_id != ctx_client:
            raise ForbiddenError("Cross-client access denied")
