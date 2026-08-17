"""Jira sandbox client contract tests without external traffic."""

from __future__ import annotations

import hashlib
import hmac
import json
from uuid import uuid4

import httpx
import pytest
from masms_api.modules.jira.client import LiveJiraClient
from masms_api.platform.secrets import LocalEnvSecretBackend


def _client() -> LiveJiraClient:
    return LiveJiraClient(
        base_url="https://sandbox.atlassian.net",
        project_key="SAN",
        credential_ref="secrets/jira_sandbox",
        secrets=LocalEnvSecretBackend(
            {
                "secrets/jira_sandbox": json.dumps(
                    {
                        "email": "jira@example.test",
                        "api_token": "test-token",
                        "webhook_secret": "webhook-test",
                    }
                )
            }
        ),
    )


def test_live_jira_create_returns_external_key(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_request(method: str, url: str, **kwargs: object) -> httpx.Response:
        _ = kwargs
        return httpx.Response(
            201,
            json={"id": "10001", "key": "SAN-1"},
            request=httpx.Request(method, url),
        )

    monkeypatch.setattr(httpx, "request", fake_request)

    key = _client().create_issue(internal_ticket_id=uuid4(), summary="Sandbox issue")

    assert key == "SAN-1"


def test_live_jira_webhook_requires_valid_signature() -> None:
    body = b'{"issue":"SAN-1"}'
    signature = hmac.new(b"webhook-test", body, hashlib.sha256).hexdigest()

    _client().verify_webhook(body=body, signature=f"sha256={signature}")

    with pytest.raises(PermissionError, match="Invalid"):
        _client().verify_webhook(body=body, signature="sha256=bad")
