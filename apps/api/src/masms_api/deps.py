"""Request identity FastAPI dependencies (provisional until Auth0 / MOD-110)."""

from __future__ import annotations

from uuid import UUID

from fastapi import Header, HTTPException

from masms_api.config import get_settings
from masms_api.kernel.actor import ActorKind
from masms_api.kernel.context import RequestContext

__all__ = ["ActorKind", "RequestContext", "get_request_context"]


def get_request_context(
    x_organization_id: str | None = Header(default=None, alias="X-Organization-Id"),
    x_actor_id: str | None = Header(default=None, alias="X-Actor-Id"),
    x_actor_kind: str | None = Header(default="human", alias="X-Actor-Kind"),
    x_correlation_id: str | None = Header(default=None, alias="X-Correlation-Id"),
    x_actor_name: str | None = Header(default="local-dev", alias="X-Actor-Name"),
    x_client_id: str | None = Header(default=None, alias="X-Client-Id"),
    x_project_id: str | None = Header(default=None, alias="X-Project-Id"),
) -> RequestContext:
    settings = get_settings()
    try:
        organization_id = UUID(x_organization_id or settings.default_organization_id)
        actor_id = UUID(x_actor_id or "00000000-0000-4000-8000-000000000101")
        correlation_id = UUID(x_correlation_id or "00000000-0000-4000-8000-000000000999")
        actor_kind = ActorKind(x_actor_kind or ActorKind.HUMAN)
        client_id = UUID(x_client_id) if x_client_id else None
        project_id = UUID(x_project_id) if x_project_id else None
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid request identity headers") from exc

    return RequestContext.from_parts(
        organization_id=organization_id,
        actor_id=actor_id,
        actor_kind=actor_kind,
        correlation_id=correlation_id,
        display_name=x_actor_name or "local-dev",
        client_id=client_id,
        project_id=project_id,
    )
