"""Request identity and temporary auth stub (pre MOD-110)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

from fastapi import Header, HTTPException

from masms_api.config import get_settings


class ActorKind(StrEnum):
    HUMAN = "human"
    AGENT = "agent"
    SYSTEM = "system"
    INTEGRATION = "integration"


@dataclass(frozen=True)
class RequestContext:
    """Provisional request principal until Auth0 / MOD-110 lands."""

    organization_id: UUID
    actor_id: UUID
    actor_kind: ActorKind
    correlation_id: UUID
    display_name: str


def get_request_context(
    x_organization_id: str | None = Header(default=None, alias="X-Organization-Id"),
    x_actor_id: str | None = Header(default=None, alias="X-Actor-Id"),
    x_actor_kind: str | None = Header(default="human", alias="X-Actor-Kind"),
    x_correlation_id: str | None = Header(default=None, alias="X-Correlation-Id"),
    x_actor_name: str | None = Header(default="local-dev", alias="X-Actor-Name"),
) -> RequestContext:
    settings = get_settings()
    try:
        organization_id = UUID(x_organization_id or settings.default_organization_id)
        actor_id = UUID(x_actor_id or "00000000-0000-4000-8000-000000000101")
        correlation_id = UUID(x_correlation_id or "00000000-0000-4000-8000-000000000999")
        actor_kind = ActorKind(x_actor_kind or ActorKind.HUMAN)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid request identity headers") from exc

    return RequestContext(
        organization_id=organization_id,
        actor_id=actor_id,
        actor_kind=actor_kind,
        correlation_id=correlation_id,
        display_name=x_actor_name or "local-dev",
    )
