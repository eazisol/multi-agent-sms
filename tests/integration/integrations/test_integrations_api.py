"""API/integration tests for MOD-500 integrations."""

from __future__ import annotations

import json
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
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.insights import models as _rp  # noqa: F401
from masms_api.modules.gmail import models as _gm  # noqa: F401
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


def _create_connection(client: TestClient, headers: dict[str, str], code: str = "gh-main") -> str:
    resp = client.post(
        "/api/v1/integrations/connections",
        headers=headers,
        json={"code": code, "provider": "github", "auth_type": "oauth2"},
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["credential_ref"].startswith("secrets/")
    assert "client_secret" not in body
    assert "access_token" not in body
    activated = client.post(
        f"/api/v1/integrations/connections/{body['id']}/activate",
        headers=headers,
        json={},
    )
    assert activated.status_code == 200, activated.text
    return body["id"]


def test_ac001_inbox_failure_does_not_corrupt_mappings(client: TestClient) -> None:
    headers = _headers("1")
    conn_id = _create_connection(client, headers)
    internal_id = str(uuid4())

    inbox = client.post(
        "/api/v1/integrations/inbox",
        headers=headers,
        json={
            "connection_id": conn_id,
            "external_event_id": "ext-fail-1",
            "event_type": "issue.created",
            "payload": {
                "internal_entity_type": "ticket",
                "internal_entity_id": internal_id,
                "external_entity_type": "issue",
                "external_entity_id": "GH-99",
            },
        },
    )
    assert inbox.status_code == 201, inbox.text
    inbox_id = inbox.json()["id"]

    before = client.get(
        f"/api/v1/integrations/mappings?connection_id={conn_id}",
        headers=headers,
    )
    assert before.status_code == 200, before.text
    count_before = before.json()["page"]["total"]

    failed = client.post(
        f"/api/v1/integrations/inbox/{inbox_id}/process",
        headers=headers,
        json={"force_fail": True},
    )
    assert failed.status_code == 200, failed.text
    assert failed.json()["status"] == "failed"

    after_fail = client.get(
        f"/api/v1/integrations/mappings?connection_id={conn_id}",
        headers=headers,
    )
    assert after_fail.json()["page"]["total"] == count_before

    conn_after = client.get(
        f"/api/v1/integrations/connections/{conn_id}",
        headers=headers,
    )
    assert conn_after.status_code == 200

    inbox_ok = client.post(
        "/api/v1/integrations/inbox",
        headers=headers,
        json={
            "connection_id": conn_id,
            "external_event_id": "ext-ok-1",
            "event_type": "issue.created",
            "payload": {
                "internal_entity_type": "ticket",
                "internal_entity_id": internal_id,
                "external_entity_type": "issue",
                "external_entity_id": "GH-100",
            },
        },
    )
    assert inbox_ok.status_code == 201, inbox_ok.text
    processed = client.post(
        f"/api/v1/integrations/inbox/{inbox_ok.json()['id']}/process",
        headers=headers,
        json={"force_fail": False},
    )
    assert processed.status_code == 200, processed.text
    assert processed.json()["status"] == "processed"

    after_ok = client.get(
        f"/api/v1/integrations/mappings?connection_id={conn_id}",
        headers=headers,
    )
    assert after_ok.json()["page"]["total"] == count_before + 1


def test_ac002_tenant_scoped_mappings_and_audit(client: TestClient) -> None:
    headers_a = _headers("1")
    headers_b = _headers("2")
    conn_a = _create_connection(client, headers_a, code="org-a-gh")

    webhook = client.post(
        "/api/v1/integrations/webhooks/receive",
        headers=headers_a,
        json={
            "connection_id": conn_a,
            "external_event_id": "wh-1",
            "event_type": "push",
            "payload": {"repo": "masms"},
        },
    )
    assert webhook.status_code == 201, webhook.text

    mapping = client.post(
        "/api/v1/integrations/mappings",
        headers=headers_a,
        json={
            "connection_id": conn_a,
            "internal_entity_type": "ticket",
            "internal_entity_id": str(uuid4()),
            "external_entity_type": "issue",
            "external_entity_id": "JIRA-1",
        },
    )
    assert mapping.status_code == 201, mapping.text

    cross_conn = client.get(
        f"/api/v1/integrations/connections/{conn_a}",
        headers=headers_b,
    )
    assert cross_conn.status_code == 404

    cross_map = client.get(
        f"/api/v1/integrations/mappings?connection_id={conn_a}",
        headers=headers_b,
    )
    assert cross_map.status_code == 200
    assert cross_map.json()["page"]["total"] == 0
    assert cross_map.json()["items"] == []

    audits = client.get("/api/v1/observability/audit-logs", headers=headers_a)
    assert audits.status_code == 200, audits.text
    actions = {item["action"] for item in audits.json()["items"]}
    assert "ig_connection_create" in actions
    assert "ig_mapping_create" in actions
    assert "ig_webhook_receive" in actions

    outbox = client.post(
        "/api/v1/observability/outbox/relay",
        headers=headers_a,
        json={"limit": 50},
    )
    assert outbox.status_code == 200, outbox.text
    event_types = {item["event_type"] for item in outbox.json()["items"]}
    assert "integrations.connection.created" in event_types
    assert "integrations.mapping.created" in event_types


def test_ac003_credentials_never_in_responses_or_audit(client: TestClient) -> None:
    headers = _headers("1")
    raw_secret = "super-secret-client-secret-value-12345"

    rejected = client.post(
        "/api/v1/integrations/connections",
        headers=headers,
        json={
            "code": "bad-secret",
            "provider": "github",
            "auth_type": "oauth2",
            "client_secret": raw_secret,
        },
    )
    assert rejected.status_code == 422, rejected.text

    rejected_token = client.post(
        "/api/v1/integrations/connections",
        headers=headers,
        json={
            "code": "bad-token",
            "provider": "jira",
            "auth_type": "oauth2",
            "access_token": "ya29.super-long-oauth-access-token-value",
        },
    )
    assert rejected_token.status_code == 422, rejected_token.text

    created = client.post(
        "/api/v1/integrations/connections",
        headers=headers,
        json={
            "code": "safe-conn",
            "provider": "slack",
            "auth_type": "oauth2",
            "metadata_json": json.dumps({"note": "no secrets here"}),
        },
    )
    assert created.status_code == 201, created.text
    body = created.json()
    response_text = json.dumps(body)
    assert raw_secret not in response_text
    assert "client_secret" not in body
    assert body["credential_ref"].startswith("secrets/")

    audits = client.get("/api/v1/observability/audit-logs", headers=headers)
    assert audits.status_code == 200, audits.text
    for item in audits.json()["items"]:
        if item["action"] == "ig_connection_create" and item["entity_id"] == body["id"]:
            audit_payload = json.dumps(item.get("payload_redacted") or {})
            assert raw_secret not in audit_payload
            assert "super-secret" not in audit_payload
            break
    else:
        pytest.fail("Expected ig_connection_create audit log")
