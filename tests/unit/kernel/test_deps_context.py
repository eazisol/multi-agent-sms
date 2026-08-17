"""API wiring tests for RequestContext headers (MOD-020)."""

from __future__ import annotations

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from masms_api.config import get_settings
from masms_api.deps import get_request_context
from masms_api.kernel.actor import ActorKind
from masms_api.main import create_app


def test_meta_lists_mod_020() -> None:
    client = TestClient(create_app())
    resp = client.get("/api/v1/meta")
    assert resp.status_code == 200
    body = resp.json()
    assert "MOD-020" in body["modules"]
    assert "MOD-030" in body["modules"]
    assert "MOD-040" in body["modules"]
    assert "MOD-100" in body["modules"]
    assert "MOD-110" in body["modules"]
    assert "MOD-120" in body["modules"]
    assert "MOD-130" in body["modules"]
    assert "MOD-140" in body["modules"]
    assert "MOD-200" in body["modules"]
    assert "MOD-210" in body["modules"]
    assert "environment" in body
    assert "auth_provider" in body


def test_get_request_context_parses_optional_project() -> None:
    ctx = get_request_context(
        x_organization_id="00000000-0000-4000-8000-000000000001",
        x_actor_id="00000000-0000-4000-8000-000000000101",
        x_actor_kind="agent",
        x_correlation_id="00000000-0000-4000-8000-000000000999",
        x_actor_name="ci-bot",
        x_client_id="00000000-0000-4000-8000-000000000201",
        x_project_id="00000000-0000-4000-8000-000000000301",
    )
    assert ctx.actor_kind is ActorKind.AGENT
    assert ctx.tenant.client_id is not None
    assert ctx.tenant.project_id is not None
    assert str(ctx.tenant.project_id).endswith("0301")


def test_auth0_mode_rejects_header_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MASMS_AUTH_PROVIDER", "auth0")
    get_settings.cache_clear()
    try:
        with pytest.raises(HTTPException) as exc_info:
            get_request_context(
                x_organization_id="00000000-0000-4000-8000-000000000001",
                x_actor_id="00000000-0000-4000-8000-000000000101",
            )
        assert exc_info.value.status_code == 401
    finally:
        get_settings.cache_clear()
