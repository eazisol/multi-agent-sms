"""API/integration tests for MOD-140 configuration."""

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
from masms_api.modules.configadmin import models as _cfg  # noqa: F401
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
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


def test_draft_cannot_control_live_until_effective(client: TestClient) -> None:
    headers = _headers()

    version = client.post(
        "/api/v1/config/versions",
        headers=headers,
        json={"title": "Ticket workflow v1", "change_reason": "initial"},
    )
    assert version.status_code == 201, version.text
    version_id = version.json()["id"]
    assert version.json()["status"] == "draft"
    assert version.json()["version_number"] == 1

    workflow = client.post(
        "/api/v1/config/workflows",
        headers=headers,
        json={
            "configuration_version_id": version_id,
            "code": "ticket",
            "title": "Ticket",
            "entity_type": "ticket",
        },
    )
    assert workflow.status_code == 201, workflow.text
    workflow_id = workflow.json()["id"]

    for code, title, terminal in (
        ("open", "Open", False),
        ("in_progress", "In Progress", False),
        ("done", "Done", True),
    ):
        st = client.post(
            "/api/v1/config/statuses",
            headers=headers,
            json={
                "configuration_version_id": version_id,
                "workflow_definition_id": workflow_id,
                "code": code,
                "title": title,
                "is_terminal": terminal,
            },
        )
        assert st.status_code == 201, st.text

    transition = client.post(
        "/api/v1/config/transitions",
        headers=headers,
        json={
            "configuration_version_id": version_id,
            "workflow_definition_id": workflow_id,
            "from_status_code": "open",
            "to_status_code": "in_progress",
        },
    )
    assert transition.status_code == 201, transition.text

    follow = client.post(
        "/api/v1/config/followup-rules",
        headers=headers,
        json={
            "configuration_version_id": version_id,
            "workflow_code": "ticket",
            "trigger_status_code": "open",
            "due_offset_hours": 24,
            "required_response": "Acknowledge",
        },
    )
    assert follow.status_code == 201

    reminder = client.post(
        "/api/v1/config/reminder-rules",
        headers=headers,
        json={
            "configuration_version_id": version_id,
            "workflow_code": "ticket",
            "offset_hours_before_due": 4,
        },
    )
    assert reminder.status_code == 201

    escalation = client.post(
        "/api/v1/config/escalation-rules",
        headers=headers,
        json={
            "configuration_version_id": version_id,
            "workflow_code": "ticket",
            "after_hours_overdue": 48,
            "escalate_to_role_code": "PM",
        },
    )
    assert escalation.status_code == 201

    approval = client.post(
        "/api/v1/config/approval-workflows",
        headers=headers,
        json={
            "configuration_version_id": version_id,
            "code": "ticket_close",
            "title": "Close ticket",
            "action_code": "tickets.close",
            "steps": [{"role": "PM", "order": 1}],
        },
    )
    assert approval.status_code == 201, approval.text

    # Draft must not control live transitions (AC-003)
    draft_live = client.post(
        "/api/v1/config/live/transitions/check",
        headers=headers,
        json={
            "workflow_code": "ticket",
            "from_status_code": "open",
            "to_status_code": "in_progress",
        },
    )
    assert draft_live.status_code == 200
    assert draft_live.json()["allowed"] is False

    # Cannot edit after approve/activate path: first approve+activate
    approved = client.post(f"/api/v1/config/versions/{version_id}/approve", headers=headers)
    assert approved.status_code == 200
    assert approved.json()["status"] == "approved"

    edit_blocked = client.post(
        "/api/v1/config/workflows",
        headers=headers,
        json={
            "configuration_version_id": version_id,
            "code": "other",
            "title": "Other",
            "entity_type": "ticket",
        },
    )
    assert edit_blocked.status_code == 403

    activated = client.post(f"/api/v1/config/versions/{version_id}/activate", headers=headers)
    assert activated.status_code == 200
    assert activated.json()["status"] == "effective"

    live_ok = client.post(
        "/api/v1/config/live/transitions/check",
        headers=headers,
        json={
            "workflow_code": "ticket",
            "from_status_code": "open",
            "to_status_code": "in_progress",
        },
    )
    assert live_ok.json()["allowed"] is True
    assert live_ok.json()["configuration_status"] == "effective"

    live_bad = client.post(
        "/api/v1/config/live/transitions/check",
        headers=headers,
        json={
            "workflow_code": "ticket",
            "from_status_code": "open",
            "to_status_code": "done",
        },
    )
    assert live_bad.json()["allowed"] is False

    # New draft + activate supersedes prior; rollback restores prior
    v2 = client.post(
        "/api/v1/config/versions",
        headers=headers,
        json={"title": "Ticket workflow v2", "based_on_version_id": version_id},
    )
    assert v2.status_code == 201
    v2_id = v2.json()["id"]
    assert v2.json()["version_number"] == 2

    client.post(f"/api/v1/config/versions/{v2_id}/approve", headers=headers)
    client.post(f"/api/v1/config/versions/{v2_id}/activate", headers=headers)

    rolled = client.post(
        "/api/v1/config/versions/rollback",
        headers=headers,
        params={"restore_version_id": version_id},
    )
    assert rolled.status_code == 200, rolled.text
    assert rolled.json()["id"] == version_id
    assert rolled.json()["status"] == "effective"
