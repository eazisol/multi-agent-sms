"""Shared authorization primitives for tenant/project scope (MOD-020-SEC-001).

Full RBAC, classification, environment, and effective-date evaluation lives in
MOD-120 (`masms_api.modules.access`). This module provides deny-by-default
scope assertions used by application services before mutation.
"""

from __future__ import annotations

from uuid import UUID

from masms_api.kernel.errors import ForbiddenError, TenantMismatchError
from masms_api.kernel.ids import OrganizationId, ProjectId


def assert_same_organization(
    *,
    active_organization_id: OrganizationId | UUID,
    resource_organization_id: OrganizationId | UUID,
    correlation_id: UUID | None = None,
) -> None:
    """Deny access when the resource belongs to another organization."""
    if active_organization_id != resource_organization_id:
        raise TenantMismatchError(
            "Resource is outside the active organization scope",
            correlation_id=correlation_id,
        )


def assert_project_scope(
    *,
    active_project_id: ProjectId | UUID | None,
    resource_project_id: ProjectId | UUID | None,
    require_active_project: bool = False,
    correlation_id: UUID | None = None,
) -> None:
    """Deny when an active project context does not match the resource project.

    Pre-project records may have ``resource_project_id is None``. When
    ``require_active_project`` is True, a missing active project is forbidden.
    """
    if require_active_project and active_project_id is None:
        raise ForbiddenError(
            "Active project context is required for this operation",
            correlation_id=correlation_id,
        )
    if active_project_id is None or resource_project_id is None:
        return
    if active_project_id != resource_project_id:
        raise ForbiddenError(
            "Resource is outside the active project scope",
            correlation_id=correlation_id,
        )
