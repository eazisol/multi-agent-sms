"""API/integration tests for MOD-220 communications."""

from __future__ import annotations

from collections.abc import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from masms_api.db import Base, get_db
from masms_api.kernel import outbox as _outbox  # noqa: F401
from masms_api.main import create_app
from masms_api.modules.access import models as _access  # noqa: F401
from masms_api.modules.auth import models as _auth  # noqa: F401
from masms_api.modules.capacity import models as _capacity  # noqa: F401
from masms_api.modules.clients import models as _clients  # noqa: F401
from masms_api.modules.comms import models as _comms  # noqa: F401
from masms_api.modules.configadmin import models as _cfg  # noqa: F401
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.queries import models as _queries  # noqa: F401
from masms_api.observability import models as _ops  # noqa: F401
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


def _headers() -> dict[str, str]:
    return {
        "X-Organization-Id": "00000000-0000-4000-8000-000000000001",
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": "human",
        "X-Correlation-Id": str(uuid4()),
    }


def test_conversation_message_send_and_immutable_history(client: TestClient) -> None:
    headers = _headers()
    entity_id = str(uuid4())

    conversation = client.post(
        "/api/v1/comms/conversations",
        headers=headers,
        json={
            "subject": "Query follow-up",
            "related_entity_type": "crm_query",
            "related_entity_id": entity_id,
            "channel": "email",
            "classification": "internal",
        },
    )
    assert conversation.status_code == 201, conversation.text
    conversation_id = conversation.json()["id"]
    assert conversation.json()["related_entity_id"] == entity_id

    message = client.post(
        "/api/v1/comms/messages",
        headers=headers,
        json={"conversation_id": conversation_id, "body": "Draft reply v1"},
    )
    assert message.status_code == 201, message.text
    message_id = message.json()["id"]
    assert message.json()["status"] == "draft"
    assert message.json()["requires_approval"] is False

    updated = client.patch(
        f"/api/v1/comms/messages/{message_id}",
        headers=headers,
        json={"body": "Draft reply v2"},
    )
    assert updated.status_code == 200
    assert updated.json()["body"] == "Draft reply v2"
    assert updated.json()["revision_number"] == 2

    revisions = client.get(f"/api/v1/comms/messages/{message_id}/revisions", headers=headers)
    assert revisions.status_code == 200
    assert len(revisions.json()) == 2

    recipient = client.post(
        "/api/v1/comms/recipients",
        headers=headers,
        json={"message_id": message_id, "address": "client@example.com", "role": "to"},
    )
    assert recipient.status_code == 201, recipient.text
    recipient_id = recipient.json()["id"]

    attachment = client.post(
        "/api/v1/comms/attachments",
        headers=headers,
        json={
            "message_id": message_id,
            "file_ref": "files/pending/quote.pdf",
            "filename": "quote.pdf",
            "content_type": "application/pdf",
            "size_bytes": 1024,
        },
    )
    assert attachment.status_code == 201, attachment.text

    sent = client.post(f"/api/v1/comms/messages/{message_id}/send", headers=headers)
    assert sent.status_code == 200, sent.text
    assert sent.json()["status"] == "sent"
    assert sent.json()["sent_at"] is not None

    immutable = client.patch(
        f"/api/v1/comms/messages/{message_id}",
        headers=headers,
        json={"body": "tamper after send"},
    )
    assert immutable.status_code == 403

    add_recipient_after = client.post(
        "/api/v1/comms/recipients",
        headers=headers,
        json={"message_id": message_id, "address": "other@example.com", "role": "cc"},
    )
    assert add_recipient_after.status_code == 403

    receipt = client.post(
        "/api/v1/comms/delivery-receipts",
        headers=headers,
        json={
            "message_id": message_id,
            "recipient_id": recipient_id,
            "status": "delivered",
            "provider_ref": "prov-1",
        },
    )
    assert receipt.status_code == 201, receipt.text

    listed = client.get(
        f"/api/v1/comms/conversations/{conversation_id}/messages", headers=headers
    )
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert listed.json()[0]["status"] == "sent"

    conversations = client.get("/api/v1/comms/conversations", headers=headers)
    assert conversations.status_code == 200, conversations.text
    assert any(row["id"] == conversation_id for row in conversations.json()["items"])

    filtered = client.get(
        "/api/v1/comms/conversations", headers=headers, params={"status": "open"}
    )
    assert filtered.status_code == 200
    assert all(row["status"] == "open" for row in filtered.json()["items"])
    assert any(row["id"] == conversation_id for row in filtered.json()["items"])

    searched = client.get(
        "/api/v1/comms/conversations", headers=headers, params={"q": "follow-up"}
    )
    assert searched.status_code == 200
    assert any(row["id"] == conversation_id for row in searched.json()["items"])


def test_sensitive_message_requires_approval(client: TestClient) -> None:
    headers = _headers()
    conversation = client.post(
        "/api/v1/comms/conversations",
        headers=headers,
        json={
            "subject": "Restricted commercial terms",
            "related_entity_type": "crm_opportunity",
            "related_entity_id": str(uuid4()),
            "classification": "restricted",
        },
    )
    assert conversation.status_code == 201
    conversation_id = conversation.json()["id"]

    message = client.post(
        "/api/v1/comms/messages",
        headers=headers,
        json={
            "conversation_id": conversation_id,
            "body": "Confidential pricing",
            "classification": "restricted",
        },
    )
    assert message.status_code == 201
    message_id = message.json()["id"]
    assert message.json()["requires_approval"] is True
    assert message.json()["status"] == "pending_approval"

    client.post(
        "/api/v1/comms/recipients",
        headers=headers,
        json={"message_id": message_id, "address": "cfo@client.com", "role": "to"},
    )

    blocked = client.post(f"/api/v1/comms/messages/{message_id}/send", headers=headers)
    assert blocked.status_code == 403

    approved = client.post(f"/api/v1/comms/messages/{message_id}/approve", headers=headers)
    assert approved.status_code == 200
    assert approved.json()["approved_by_actor_id"] is not None

    sent = client.post(f"/api/v1/comms/messages/{message_id}/send", headers=headers)
    assert sent.status_code == 200
    assert sent.json()["status"] == "sent"
