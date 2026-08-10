"""Identity provider and token validation contracts (MOD-110)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from uuid import UUID

from masms_api.errors import ForbiddenError
from masms_api.kernel.actor import ActorKind


@dataclass(frozen=True, slots=True)
class ValidatedIdentity:
    organization_id: UUID
    actor_id: UUID
    actor_kind: ActorKind
    display_name: str
    idp_subject: str | None
    assurance_level: int
    session_id: UUID | None = None


class IdentityProvider(ABC):
    @abstractmethod
    def validate_access_token(self, token: str) -> ValidatedIdentity:
        """Validate an inbound bearer token and return authenticated identity."""


class Auth0IdentityProvider(IdentityProvider):
    """Auth0 JWT validation placeholder.

    Real JWKS verification is deferred until Auth0 tenant + audience are approved.
    """

    def __init__(self, *, domain: str | None, audience: str | None) -> None:
        self.domain = domain
        self.audience = audience

    def validate_access_token(self, token: str) -> ValidatedIdentity:
        _ = token
        if not self.domain or not self.audience:
            raise ForbiddenError(
                "Auth0 provider is not configured (MASMS_AUTH0_DOMAIN / MASMS_AUTH0_AUDIENCE)"
            )
        raise ForbiddenError(
            "Auth0 JWKS token validation is not enabled in this scaffold; "
            f"configure domain '{self.domain}' before accepting production tokens"
        )


class LocalSessionIdentityProvider(IdentityProvider):
    """Resolve opaque local session bearer tokens via AuthSession rows."""

    def __init__(self, resolver: Callable[[str], ValidatedIdentity]) -> None:
        self._resolver = resolver

    def validate_access_token(self, token: str) -> ValidatedIdentity:
        return self._resolver(token)
