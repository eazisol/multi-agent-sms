"""Combined request principal: actor + tenant + correlation."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from masms_api.kernel.actor import ActorContext, ActorKind
from masms_api.kernel.ids import ActorId, CorrelationId, OrganizationId
from masms_api.kernel.tenant import TenantContext


@dataclass(frozen=True, slots=True)
class RequestContext:
    """Authoritative request identity for FastAPI services (until Auth0 / MOD-110)."""

    tenant: TenantContext
    actor: ActorContext
    correlation_id: CorrelationId

    @property
    def organization_id(self) -> OrganizationId:
        return self.tenant.organization_id

    @property
    def actor_id(self) -> ActorId:
        return self.actor.actor_id

    @property
    def actor_kind(self) -> ActorKind:
        return self.actor.actor_kind

    @property
    def display_name(self) -> str:
        return self.actor.display_name

    @classmethod
    def from_parts(
        cls,
        *,
        organization_id: UUID,
        actor_id: UUID,
        actor_kind: ActorKind,
        correlation_id: UUID,
        display_name: str,
        client_id: UUID | None = None,
        project_id: UUID | None = None,
    ) -> RequestContext:
        from masms_api.kernel.ids import (
            as_actor_id,
            as_client_id,
            as_correlation_id,
            as_organization_id,
            as_project_id,
        )

        return cls(
            tenant=TenantContext(
                organization_id=as_organization_id(organization_id),
                client_id=as_client_id(client_id) if client_id is not None else None,
                project_id=as_project_id(project_id) if project_id is not None else None,
            ),
            actor=ActorContext(
                actor_id=as_actor_id(actor_id),
                actor_kind=actor_kind,
                display_name=display_name,
            ),
            correlation_id=as_correlation_id(correlation_id),
        )
