"""API/integration tests for MOD-510 Gmail."""

from __future__ import annotations

from collections.abc import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from masms_api.db import Base, get_db
from masms_api.kernel import outbox as _outbox  # noqa: F401
from masms_api.main import create_app
from masms_api.modules.access import models as _access  # noqa: F401
from masms_api.modules.agents import models as _agr  # noqa: F401
from masms_api.modules.approvalgates import models as _apr  # noqa: F401
from masms_api.modules.assignments import models as _asg  # noqa: F401
from masms_api.modules.auth import models as _auth  # noqa: F401
from masms_api.modules.bugs import models as _bugs  # noqa: F401
from masms_api.modules.capacity import models as _capacity  # noqa: F401
from masms_api.modules.changecontrol import models as _cc  # noqa: F401
from masms_api.modules.clients import models as _clients  # noqa: F401
from masms_api.modules.comms import models as _comms  # noqa: F401
from masms_api.modules.configadmin import models as _cfg  # noqa: F401
from masms_api.modules.documents import models as _docs  # noqa: F401
from masms_api.modules.followups import models as _flu  # noqa: F401
from masms_api.modules.gmail import models as _gm  # noqa: F401
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.insights import models as _rp  # noqa: F401
from masms_api.modules.integrations import models as _ig  # noqa: F401
from masms_api.modules.knowledge import models as _kn  # noqa: F401
from masms_api.modules.notifications import models as _ntf  # noqa: F401
from masms_api.modules.orchestrator import models as _orf  # noqa: F401
from masms_api.modules.projects import models as _projects  # noqa: F401
from masms_api.modules.queries import models as _queries  # noqa: F401
from masms_api.modules.releases import models as _rl  # noqa: F401
from masms_api.modules.requirements import models as _reqs  # noqa: F401
from masms_api.modules.roadmap import models as _roadmap  # noqa: F401
from masms_api.modules.reliability import models as _rlb  # noqa: F401
from masms_api.modules.securityhardening import models as _sh  # noqa: F401
from masms_api.modules.statusengine import models as _wfe  # noqa: F401
from masms_api.modules.uateval import models as _ua  # noqa: F401
from masms_api.modules.pilot import models as _pl  # noqa: F401
from masms_api.modules.testcases import models as _tc  # noqa: F401
from masms_api.modules.tickets import models as _tickets  # noqa: F401
from masms_api.modules.traceability import models as _tr  # noqa: F401
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


def _headers(org_suffix: str = "1") -> dict[str, str]:
    return {
        "X-Organization-Id": f"00000000-0000-4000-8000-00000000000{org_suffix}",
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": "human",
        "X-Correlation-Id": str(uuid4()),
    }


def _create_connection(client: TestClient, headers: dict[str, str], code: str = "gmail-main") -> str:
    resp = client.post(
        "/api/v1/gmail/connections",
        headers=headers,
        json={
            "code": code,
            "email_address": f"{code}@example.com",
        },
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["credential_ref"].startswith("secrets/")
    activated = client.post(
        f"/api/v1/gmail/connections/{body['id']}/activate",
        headers=headers,
        json={},
    )
    assert activated.status_code == 200, activated.text
    return body["id"]


def test_ac001_inbound_idempotent_by_gmail_message_id(client: TestClient) -> None:
    headers = _headers("1")
    conn_id = _create_connection(client, headers)
    gmail_message_id = "msg-inbound-001"
    gmail_thread_id = "thread-001"
    payload = {
        "connection_id": conn_id,
        "gmail_message_id": gmail_message_id,
        "gmail_thread_id": gmail_thread_id,
        "subject": "New inquiry",
        "from_email": "client@example.com",
        "snippet": "Hello, I need a quote",
    }

    first = client.post("/api/v1/gmail/inbound/process", headers=headers, json=payload)
    assert first.status_code == 200, first.text
    first_body = first.json()
    assert first_body["idempotent"] is False

    second = client.post("/api/v1/gmail/inbound/process", headers=headers, json=payload)
    assert second.status_code == 409, second.text
    second_body = second.json()
    assert second_body["idempotent"] is True
    assert second_body["message_mapping_id"] == first_body["message_mapping_id"]
    assert second_body["thread_mapping_id"] == first_body["thread_mapping_id"]

    threads = client.get(f"/api/v1/gmail/threads?connection_id={conn_id}", headers=headers)
    assert threads.status_code == 200, threads.text
    assert threads.json()["page"]["total"] == 1

    messages = client.get(f"/api/v1/gmail/messages?connection_id={conn_id}", headers=headers)
    assert messages.status_code == 200, messages.text
    assert messages.json()["page"]["total"] == 1


def test_ac002_draft_review_approve_send(client: TestClient) -> None:
    headers = _headers("1")
    conn_id = _create_connection(client, headers, code="gmail-send")

    draft_resp = client.post(
        "/api/v1/gmail/drafts",
        headers=headers,
        json={
            "connection_id": conn_id,
            "to_addresses": "client@example.com",
            "subject": "Re: Your inquiry",
            "body_preview": "Thank you for reaching out.",
        },
    )
    assert draft_resp.status_code == 201, draft_resp.text
    draft_id = draft_resp.json()["id"]

    submit = client.post(f"/api/v1/gmail/drafts/{draft_id}/submit", headers=headers, json={})
    assert submit.status_code == 200, submit.text
    assert submit.json()["status"] == "pending_review"

    approve = client.post(f"/api/v1/gmail/drafts/{draft_id}/approve", headers=headers, json={})
    assert approve.status_code == 200, approve.text
    assert approve.json()["status"] == "approved"

    send = client.post(f"/api/v1/gmail/drafts/{draft_id}/send", headers=headers)
    assert send.status_code == 200, send.text
    send_body = send.json()
    assert send_body["approved_send"]["status"] == "sent"
    assert send_body["approved_send"]["external_send_id"].startswith("local-gmail-sim-")
    assert send_body["message_mapping"]["direction"] == "outbound"
    assert send_body["message_mapping"]["status"] == "sent"

    outbound = client.get(
        f"/api/v1/gmail/messages?connection_id={conn_id}&direction=outbound",
        headers=headers,
    )
    assert outbound.status_code == 200, outbound.text
    assert outbound.json()["page"]["total"] == 1


def test_ac003_push_duplicate_external_event_id(client: TestClient) -> None:
    headers = _headers("1")
    conn_id = _create_connection(client, headers, code="gmail-push")
    external_event_id = "push-event-001"
    body = {
        "connection_id": conn_id,
        "external_event_id": external_event_id,
        "event_type": "message_received",
        "payload": {
            "gmail_message_id": "msg-push-001",
            "gmail_thread_id": "thread-push-001",
            "from_email": "notify@example.com",
            "subject": "Push notification test",
        },
    }

    first = client.post("/api/v1/gmail/push/receive", headers=headers, json=body)
    assert first.status_code == 201, first.text
    assert first.json()["idempotent"] is False

    second = client.post("/api/v1/gmail/push/receive", headers=headers, json=body)
    assert second.status_code == 200, second.text
    assert second.json()["idempotent"] is True

    threads = client.get(f"/api/v1/gmail/threads?connection_id={conn_id}", headers=headers)
    assert threads.json()["page"]["total"] == 1

    messages = client.get(f"/api/v1/gmail/messages?connection_id={conn_id}", headers=headers)
    assert messages.json()["page"]["total"] == 1
