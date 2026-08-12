"""API/integration tests for MOD-440 notifications."""

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
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.knowledge import models as _kn  # noqa: F401
from masms_api.modules.insights import models as _rp  # noqa: F401
from masms_api.modules.integrations import models as _ig  # noqa: F401
from masms_api.modules.notifications import models as _ntf  # noqa: F401
from masms_api.modules.orchestrator import models as _orf  # noqa: F401
from masms_api.modules.projects import models as _projects  # noqa: F401
from masms_api.modules.queries import models as _queries  # noqa: F401
from masms_api.modules.releases import models as _rl  # noqa: F401
from masms_api.modules.requirements import models as _reqs  # noqa: F401
from masms_api.modules.roadmap import models as _roadmap  # noqa: F401
from masms_api.modules.statusengine import models as _wfe  # noqa: F401
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


def _headers() -> dict[str, str]:
    return {
        "X-Organization-Id": "00000000-0000-4000-8000-000000000001",
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": "human",
        "X-Correlation-Id": str(uuid4()),
    }


def test_notification_idempotency_preferences_and_dlq_replay(client: TestClient) -> None:
    headers = _headers()
    recipient = "00000000-0000-4000-8000-000000000201"
    key = f"idem-{uuid4()}"

    # AC-001: create with idempotency_key → 201; duplicate → 409
    created = client.post(
        "/api/v1/notifications",
        headers=headers,
        json={
            "title": "Ticket assigned",
            "body": "You were assigned TKT-1",
            "recipient_actor_id": recipient,
            "notification_type": "assignment",
            "channel": "in_app",
            "priority": "normal",
            "idempotency_key": key,
        },
    )
    assert created.status_code == 201, created.text
    assert created.json()["status"] == "pending"

    dup = client.post(
        "/api/v1/notifications",
        headers=headers,
        json={
            "title": "Ticket assigned again",
            "body": "duplicate",
            "recipient_actor_id": recipient,
            "notification_type": "assignment",
            "channel": "in_app",
            "priority": "normal",
            "idempotency_key": key,
        },
    )
    assert dup.status_code == 409, dup.text

    # AC-002: cannot mute system_alert
    muted = client.put(
        "/api/v1/notifications/preferences",
        headers=headers,
        json={
            "actor_id": recipient,
            "channel": "in_app",
            "notification_type": "system_alert",
            "enabled": False,
        },
    )
    assert muted.status_code == 422, muted.text

    ok_pref = client.put(
        "/api/v1/notifications/preferences",
        headers=headers,
        json={
            "actor_id": recipient,
            "channel": "email",
            "notification_type": "reminder",
            "enabled": False,
        },
    )
    assert ok_pref.status_code == 200, ok_pref.text

    # AC-003: fail → retries → DLQ → list → replay
    delivery_target = client.post(
        "/api/v1/notifications",
        headers=headers,
        json={
            "title": "Delivery target",
            "body": "Will fail thrice",
            "recipient_actor_id": recipient,
            "notification_type": "reminder",
            "channel": "in_app",
            "priority": "normal",
        },
    )
    assert delivery_target.status_code == 201, delivery_target.text
    ntf_id = delivery_target.json()["id"]

    for i in range(3):
        failed = client.post(
            f"/api/v1/notifications/{ntf_id}/deliver",
            headers=headers,
            json={"succeed": False, "error_message": f"sim fail {i + 1}"},
        )
        assert failed.status_code == 200, failed.text
        body = failed.json()
        if i < 2:
            assert body["status"] == "failed"
            assert body["retry_count"] == i + 1
        else:
            assert body["status"] == "dead_lettered"
            assert body["retry_count"] >= 3

    listed_dlq = client.get("/api/v1/notifications/dead-letters?status=open", headers=headers)
    assert listed_dlq.status_code == 200, listed_dlq.text
    items = listed_dlq.json()["items"]
    assert len(items) >= 1
    dl_id = next(i["id"] for i in items if i["notification_id"] == ntf_id)

    replayed = client.post(
        f"/api/v1/notifications/dead-letters/{dl_id}/replay",
        headers=headers,
    )
    assert replayed.status_code == 200, replayed.text
    assert replayed.json()["status"] == "replayed"

    recovered = client.get(f"/api/v1/notifications/{ntf_id}", headers=headers)
    assert recovered.status_code == 200
    assert recovered.json()["status"] == "pending"
    assert recovered.json()["retry_count"] == 0

    page = client.get("/api/v1/notifications?limit=10&offset=0", headers=headers)
    assert page.status_code == 200
    assert "items" in page.json() and "page" in page.json()
