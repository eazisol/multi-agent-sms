"""Gmail sandbox client contract tests without external traffic."""

from __future__ import annotations

import json
from uuid import uuid4

import httpx
import pytest
from masms_api.modules.gmail.client import LiveGmailClient
from masms_api.modules.gmail.models import GmailConnection, GmailDraftReview
from masms_api.platform.secrets import LocalEnvSecretBackend


def test_live_gmail_send_uses_opaque_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_post(url: str, **kwargs: object) -> httpx.Response:
        captured["url"] = url
        captured["headers"] = kwargs.get("headers")
        return httpx.Response(
            200,
            json={"id": "gmail-message-1", "threadId": "gmail-thread-1"},
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(httpx, "post", fake_post)
    actor_id = uuid4()
    connection = GmailConnection(
        id=uuid4(),
        organization_id=uuid4(),
        code="gmail-sandbox",
        email_address="sender@example.test",
        credential_ref="secrets/gmail_sandbox",
        status="active",
        owner_actor_id=actor_id,
        created_by_actor_id=actor_id,
        updated_by_actor_id=actor_id,
    )
    draft = GmailDraftReview(
        id=uuid4(),
        organization_id=connection.organization_id,
        connection_id=connection.id,
        draft_id=uuid4(),
        to_addresses="recipient@example.test",
        subject="Sandbox message",
        body_preview="Test body",
        status="approved",
        created_by_actor_id=actor_id,
        updated_by_actor_id=actor_id,
    )
    client = LiveGmailClient(
        secrets=LocalEnvSecretBackend(
            {"secrets/gmail_sandbox": json.dumps({"access_token": "test-token"})}
        )
    )

    result = client.send_message(connection=connection, draft=draft, thread_id=None)

    assert result.message_id == "gmail-message-1"
    assert captured["url"] == "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"
    assert captured["headers"] == {"Authorization": "Bearer test-token"}
