"""Identity provider and token validation contracts (MOD-110)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from functools import lru_cache
from uuid import UUID

import jwt
from jwt import PyJWKClient
from jwt.exceptions import PyJWKClientError, PyJWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from masms_api.errors import ForbiddenError
from masms_api.kernel.actor import ActorKind
from masms_api.modules.identity.models import Actor, HumanUser


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
    """Validate Auth0 access tokens and map subjects to active MASMS actors."""

    def __init__(
        self,
        *,
        domain: str | None,
        audience: str | None,
        db: Session | None = None,
    ) -> None:
        self.domain = domain
        self.audience = audience
        self.db = db

    def validate_access_token(self, token: str) -> ValidatedIdentity:
        if not self.domain or not self.audience:
            raise ForbiddenError(
                "Auth0 provider is not configured (MASMS_AUTH0_DOMAIN / MASMS_AUTH0_AUDIENCE)"
            )
        issuer = _issuer(self.domain)
        try:
            signing_key = _jwks_client(f"{issuer}.well-known/jwks.json").get_signing_key_from_jwt(
                token
            )
            claims = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=issuer,
                options={"require": ["exp", "sub"]},
            )
        except (PyJWTError, PyJWKClientError) as exc:
            raise ForbiddenError("Invalid Auth0 access token") from exc

        subject = claims.get("sub")
        if not isinstance(subject, str) or not subject.strip():
            raise ForbiddenError("Auth0 access token is missing a valid subject")
        if self.db is None:
            raise ForbiddenError("Auth0 identity mapping database is not configured")

        user = self.db.scalar(
            select(HumanUser).where(
                HumanUser.idp_subject == subject,
                HumanUser.status == "active",
                HumanUser.deleted_at.is_(None),
            )
        )
        if user is None:
            raise ForbiddenError("Authenticated identity is not linked to an active MASMS user")
        actor = self.db.get(Actor, user.actor_id)
        if actor is None or actor.status != "active" or actor.deleted_at is not None:
            raise ForbiddenError("Authenticated MASMS actor is not active")

        amr = claims.get("amr")
        assurance_level = 2 if isinstance(amr, list) and "mfa" in amr else 1
        return ValidatedIdentity(
            organization_id=user.organization_id,
            actor_id=actor.id,
            actor_kind=ActorKind.HUMAN,
            display_name=user.full_name,
            idp_subject=subject,
            assurance_level=assurance_level,
        )


def _issuer(domain: str) -> str:
    normalized = domain.strip().removeprefix("https://").rstrip("/")
    return f"https://{normalized}/"


@lru_cache(maxsize=8)
def _jwks_client(jwks_url: str) -> PyJWKClient:
    return PyJWKClient(jwks_url, cache_keys=True)


class LocalSessionIdentityProvider(IdentityProvider):
    """Resolve opaque local session bearer tokens via AuthSession rows."""

    def __init__(self, resolver: Callable[[str], ValidatedIdentity]) -> None:
        self._resolver = resolver

    def validate_access_token(self, token: str) -> ValidatedIdentity:
        return self._resolver(token)
