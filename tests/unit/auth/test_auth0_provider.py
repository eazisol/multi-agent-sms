"""Auth0 JWT validation and MASMS identity mapping tests."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from masms_api.errors import ForbiddenError
from masms_api.modules.auth import provider as provider_module
from masms_api.modules.auth.provider import Auth0IdentityProvider
from masms_api.modules.identity.models import Actor, HumanUser
from sqlalchemy.orm import Session

DOMAIN = "tenant.example.auth0.com"
AUDIENCE = "https://api.masms.local"


@pytest.fixture()
def private_key() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def _token(
    private_key: rsa.RSAPrivateKey,
    *,
    audience: str = AUDIENCE,
    subject: str = "auth0|user-1",
    amr: list[str] | None = None,
) -> str:
    now = datetime.now(UTC)
    return jwt.encode(
        {
            "sub": subject,
            "iss": f"https://{DOMAIN}/",
            "aud": audience,
            "iat": now,
            "exp": now + timedelta(minutes=5),
            "amr": amr or [],
        },
        private_key,
        algorithm="RS256",
        headers={"kid": "test-key"},
    )


def _provider(
    monkeypatch: pytest.MonkeyPatch,
    private_key: rsa.RSAPrivateKey,
    *,
    linked: bool = True,
) -> Auth0IdentityProvider:
    jwks = Mock()
    jwks.get_signing_key_from_jwt.return_value = SimpleNamespace(
        key=private_key.public_key()
    )
    monkeypatch.setattr(provider_module, "_jwks_client", lambda _url: jwks)

    organization_id = uuid4()
    actor_id = uuid4()
    user = HumanUser(
        id=uuid4(),
        organization_id=organization_id,
        actor_id=actor_id,
        email="alice@example.test",
        full_name="Alice Tester",
        idp_subject="auth0|user-1",
        status="active",
        created_by_actor_id=actor_id,
        updated_by_actor_id=actor_id,
    )
    actor = Actor(
        id=actor_id,
        organization_id=organization_id,
        actor_kind="human",
        display_name="Alice Tester",
        status="active",
        created_by_actor_id=actor_id,
        updated_by_actor_id=actor_id,
    )
    db = Mock(spec=Session)
    db.scalar.return_value = user if linked else None
    db.get.return_value = actor
    return Auth0IdentityProvider(domain=DOMAIN, audience=AUDIENCE, db=db)


def test_valid_token_maps_to_linked_actor_with_mfa(
    monkeypatch: pytest.MonkeyPatch,
    private_key: rsa.RSAPrivateKey,
) -> None:
    provider = _provider(monkeypatch, private_key)

    identity = provider.validate_access_token(_token(private_key, amr=["pwd", "mfa"]))

    assert identity.display_name == "Alice Tester"
    assert identity.idp_subject == "auth0|user-1"
    assert identity.assurance_level == 2


def test_wrong_audience_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
    private_key: rsa.RSAPrivateKey,
) -> None:
    provider = _provider(monkeypatch, private_key)

    with pytest.raises(ForbiddenError, match="Invalid Auth0 access token"):
        provider.validate_access_token(_token(private_key, audience="wrong-audience"))


def test_unlinked_subject_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
    private_key: rsa.RSAPrivateKey,
) -> None:
    provider = _provider(monkeypatch, private_key, linked=False)

    with pytest.raises(ForbiddenError, match="not linked"):
        provider.validate_access_token(_token(private_key))
