"""Request identity FastAPI dependencies (header stub + local bearer sessions)."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from masms_api.config import get_settings
from masms_api.db import get_db
from masms_api.errors import AppError
from masms_api.kernel.actor import ActorKind
from masms_api.kernel.context import RequestContext
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.modules.auth.provider import Auth0IdentityProvider

__all__ = ["ActorKind", "RequestContext", "get_request_context"]


def get_request_context(
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
    x_organization_id: Annotated[str | None, Header(alias="X-Organization-Id")] = None,
    x_actor_id: Annotated[str | None, Header(alias="X-Actor-Id")] = None,
    x_actor_kind: Annotated[str | None, Header(alias="X-Actor-Kind")] = "human",
    x_correlation_id: Annotated[str | None, Header(alias="X-Correlation-Id")] = None,
    x_actor_name: Annotated[str | None, Header(alias="X-Actor-Name")] = "local-dev",
    x_client_id: Annotated[str | None, Header(alias="X-Client-Id")] = None,
    x_project_id: Annotated[str | None, Header(alias="X-Project-Id")] = None,
    x_assurance_level: Annotated[str | None, Header(alias="X-Assurance-Level")] = None,
    db: Annotated[Session | None, Depends(get_db)] = None,
) -> RequestContext:
    settings = get_settings()

    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
        if not token:
            raise HTTPException(status_code=401, detail="Empty bearer token")
        if db is None:
            raise HTTPException(
                status_code=500,
                detail="Database session unavailable for bearer auth",
            )
        try:
            if settings.auth_provider == "auth0":
                identity = Auth0IdentityProvider(
                    domain=settings.auth0_domain,
                    audience=settings.auth0_audience,
                ).validate_access_token(token)
            else:
                from masms_api.modules.auth.service import resolve_session_token

                identity = resolve_session_token(db, token)
        except AppError as exc:
            raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
        try:
            correlation_id = UUID(x_correlation_id or "00000000-0000-4000-8000-000000000999")
            client_id = UUID(x_client_id) if x_client_id else None
            project_id = UUID(x_project_id) if x_project_id else None
        except (ValueError, TypeError) as exc:
            raise HTTPException(status_code=400, detail="Invalid request identity headers") from exc
        ctx = RequestContext.from_parts(
            organization_id=identity.organization_id,
            actor_id=identity.actor_id,
            actor_kind=identity.actor_kind,
            correlation_id=correlation_id,
            display_name=identity.display_name,
            client_id=client_id,
            project_id=project_id,
            session_id=identity.session_id,
            assurance_level=identity.assurance_level,
        )
        if db is not None:
            apply_tenant_rls(db, ctx.organization_id)
        return ctx

    try:
        organization_id = UUID(x_organization_id or settings.default_organization_id)
        actor_id = UUID(x_actor_id or "00000000-0000-4000-8000-000000000101")
        correlation_id = UUID(x_correlation_id or "00000000-0000-4000-8000-000000000999")
        actor_kind = ActorKind(x_actor_kind or ActorKind.HUMAN)
        client_id = UUID(x_client_id) if x_client_id else None
        project_id = UUID(x_project_id) if x_project_id else None
        assurance_level = int(x_assurance_level) if x_assurance_level else 1
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid request identity headers") from exc

    if assurance_level < 1 or assurance_level > 3:
        raise HTTPException(status_code=400, detail="X-Assurance-Level must be 1..3")

    ctx = RequestContext.from_parts(
        organization_id=organization_id,
        actor_id=actor_id,
        actor_kind=actor_kind,
        correlation_id=correlation_id,
        display_name=x_actor_name or "local-dev",
        client_id=client_id,
        project_id=project_id,
        assurance_level=assurance_level,
    )
    if db is not None:
        apply_tenant_rls(db, ctx.organization_id)
    return ctx
