"""Tenant / organization scope for multi-tenant authorization."""

from __future__ import annotations

from dataclasses import dataclass

from masms_api.kernel.ids import ClientId, OrganizationId, ProjectId


@dataclass(frozen=True, slots=True)
class TenantContext:
    """Organization ownership with optional client and project scope.

    ``project_id`` may be null for valid pre-project records (queries, opportunities).
    """

    organization_id: OrganizationId
    client_id: ClientId | None = None
    project_id: ProjectId | None = None

    def same_organization(self, organization_id: OrganizationId) -> bool:
        return self.organization_id == organization_id

    def requires_project(self) -> bool:
        return self.project_id is not None
