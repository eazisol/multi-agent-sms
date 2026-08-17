"""Unit tests for MOD-110 auth domain and tokens."""

from __future__ import annotations

import pytest
from masms_api.errors import ForbiddenError, ValidationAppError
from masms_api.modules.auth import domain
from masms_api.modules.auth.provider import Auth0IdentityProvider
from masms_api.modules.auth.tokens import constant_time_equals, generate_opaque_token, hash_secret


def test_assurance_gate() -> None:
    domain.require_assurance(2, 2, action="ok")
    with pytest.raises(ForbiddenError):
        domain.require_assurance(1, 2, action="session_revoke")


def test_session_and_invite_status_guards() -> None:
    domain.assert_session_active("active")
    with pytest.raises(ForbiddenError):
        domain.assert_session_active("revoked")
    domain.assert_invitation_pending("pending")
    with pytest.raises(ValidationAppError):
        domain.assert_invitation_pending("accepted")


def test_token_hash_and_opaque_prefix() -> None:
    token = generate_opaque_token(prefix="sess")
    assert token.startswith("sess_")
    assert constant_time_equals(hash_secret(token), hash_secret(token))
    assert not constant_time_equals(hash_secret(token), hash_secret(token + "x"))


def test_auth0_provider_fail_closed() -> None:
    bare = Auth0IdentityProvider(domain=None, audience=None)
    with pytest.raises(ForbiddenError):
        bare.validate_access_token("anything")
    configured = Auth0IdentityProvider(domain="example.auth0.com", audience="api")
    with pytest.raises(ForbiddenError, match="Invalid Auth0 access token"):
        configured.validate_access_token("jwt.not.real")
