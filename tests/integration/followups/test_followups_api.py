"""API/integration tests for MOD-340 follow-ups."""

from __future__ import annotations

from collections.abc import Generator
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from masms_api.db import Base, get_db
from masms_api.kernel import outbox as _outbox  # noqa: F401
from masms_api.main import create_app
from masms_api.modules.access import models as _access  # noqa: F401
from masms_api.modules.approvalgates import models as _apr  # noqa: F401
from masms_api.modules.assignments import models as _asg  # noqa: F401
from masms_api.modules.auth import models as _auth  # noqa: F401
from masms_api.modules.capacity import models as _capacity  # noqa: F401
from masms_api.modules.clients import models as _clients  # noqa: F401
from masms_api.modules.comms import models as _comms  # noqa: F401
from masms_api.modules.configadmin import models as _cfg  # noqa: F401
from masms_api.modules.documents import models as _docs  # noqa: F401
from masms_api.modules.followups import models as _flu  # noqa: F401
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.projects import models as _projects  # noqa: F401
from masms_api.modules.queries import models as _queries  # noqa: F401
from masms_api.modules.requirements import models as _reqs  # noqa: F401
from masms_api.modules.roadmap import models as _roadmap  # noqa: F401
from masms_api.modules.statusengine import models as _wfe  # noqa: F401
from masms_api.modules.tickets import models as _tickets  # noqa: F401
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


def test_create_requires_owner_deadline_rule_closure(client: TestClient) -> None:
    headers = _headers()
    bad = client.post(
        "/api/v1/follow-ups",
        headers=headers,
        json={
            "title": "Missing rule",
            "source_entity_type": "ticket",
            "source_entity_id": str(uuid4()),
            "recipient_actor_id": "00000000-0000-4000-8000-000000000201",
            "owner_actor_id": "00000000-0000-4000-8000-000000000101",
            "required_response": "Reply",
            "closure_condition": "Answer received",
            # no rule_version_id and no effective config
        },
    )
    assert bad.status_code == 422, bad.text

    ok = client.post(
        "/api/v1/follow-ups",
        headers=headers,
        json={
            "title": "Need clarification",
            "source_entity_type": "ticket",
            "source_entity_id": str(uuid4()),
            "recipient_actor_id": "00000000-0000-4000-8000-000000000201",
            "owner_actor_id": "00000000-0000-4000-8000-000000000101",
            "required_response": "Reply with details",
            "closure_condition": "Answer received",
            "rule_version_id": str(uuid4()),
            "due_offset_hours": 8,
            "reminder_offset_hours": 2,
            "escalation_after_hours": 1,
        },
    )
    assert ok.status_code == 201, ok.text
    body = ok.json()
    assert body["owner_actor_id"]
    assert body["due_at"]
    assert body["rule_version_id"]
    assert body["closure_condition"]

    deadline = client.get(f"/api/v1/follow-ups/{body['id']}/deadline", headers=headers)
    assert deadline.status_code == 200
    assert deadline.json()["business_due_at"]


def test_parent_child_return_routing_and_overdue(client: TestClient) -> None:
    headers = _headers()
    rule = str(uuid4())
    parent = client.post(
        "/api/v1/follow-ups",
        headers=headers,
        json={
            "title": "Parent clarification",
            "source_entity_type": "query",
            "source_entity_id": str(uuid4()),
            "recipient_actor_id": "00000000-0000-4000-8000-000000000201",
            "owner_actor_id": "00000000-0000-4000-8000-000000000101",
            "required_response": "Confirm",
            "closure_condition": "Confirmed",
            "rule_version_id": rule,
        },
    )
    assert parent.status_code == 201, parent.text
    parent_id = parent.json()["id"]

    child = client.post(
        "/api/v1/follow-ups",
        headers=headers,
        json={
            "title": "Child detail request",
            "source_entity_type": "query",
            "source_entity_id": str(uuid4()),
            "recipient_actor_id": "00000000-0000-4000-8000-000000000202",
            "owner_actor_id": "00000000-0000-4000-8000-000000000101",
            "required_response": "Provide attachment",
            "closure_condition": "Attachment received",
            "rule_version_id": rule,
            "parent_followup_id": parent_id,
            "due_at": (datetime.now(UTC) - timedelta(hours=5)).isoformat(),
            "reminder_offset_hours": 1,
            "escalation_after_hours": 0,
        },
    )
    assert child.status_code == 201, child.text
    child_id = child.json()["id"]
    assert child.json()["return_to_followup_id"] == parent_id

    links = client.get(f"/api/v1/follow-ups/{parent_id}/children", headers=headers)
    assert links.status_code == 200
    assert len(links.json()) == 1
    assert links.json()[0]["return_route"] == "parent"

    # Parent cannot close while child open
    parent_close = client.post(f"/api/v1/follow-ups/{parent_id}/close", headers=headers)
    assert parent_close.status_code in {403, 422}

    overdue = client.post(f"/api/v1/follow-ups/{child_id}/process-overdue", headers=headers)
    assert overdue.status_code == 200, overdue.text
    assert overdue.json()["reminders_created"] >= 1
    assert overdue.json()["escalations_created"] >= 1

    reminders = client.get(f"/api/v1/follow-ups/{child_id}/reminders", headers=headers)
    assert any(r["status"] == "sent" for r in reminders.json())
    escalations = client.get(f"/api/v1/follow-ups/{child_id}/escalations", headers=headers)
    assert len(escalations.json()) >= 1

    pause = client.post(
        f"/api/v1/follow-ups/{child_id}/sla-pauses",
        headers=headers,
        json={
            "reason": "Waiting on vendor",
            "next_action": "Call vendor",
            "review_at": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        },
    )
    assert pause.status_code == 201, pause.text

    evidence = client.post(
        f"/api/v1/follow-ups/{child_id}/closure-evidence",
        headers=headers,
        json={"evidence_ref": "msg://reply-1"},
    )
    assert evidence.status_code == 201

    # Resume then close child
    resume = client.post(f"/api/v1/follow-ups/{child_id}/sla-pauses/resume", headers=headers)
    assert resume.status_code == 200

    closed_child = client.post(f"/api/v1/follow-ups/{child_id}/close", headers=headers)
    assert closed_child.status_code == 200
    assert closed_child.json()["status"] == "closed"
    assert closed_child.json()["return_to_followup_id"] == parent_id

    parent_evidence = client.post(
        f"/api/v1/follow-ups/{parent_id}/closure-evidence",
        headers=headers,
        json={"evidence_ref": "msg://parent-done"},
    )
    assert parent_evidence.status_code == 201
    closed_parent = client.post(f"/api/v1/follow-ups/{parent_id}/close", headers=headers)
    assert closed_parent.status_code == 200, closed_parent.text
