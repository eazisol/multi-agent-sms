"""API/integration tests for MOD-320 status engine."""

from __future__ import annotations

from collections.abc import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from masms_api.db import Base, get_db
from masms_api.kernel import outbox as _outbox  # noqa: F401
from masms_api.main import create_app
from masms_api.modules.access import models as _access  # noqa: F401
from masms_api.modules.assignments import models as _asg  # noqa: F401
from masms_api.modules.auth import models as _auth  # noqa: F401
from masms_api.modules.capacity import models as _capacity  # noqa: F401
from masms_api.modules.clients import models as _clients  # noqa: F401
from masms_api.modules.comms import models as _comms  # noqa: F401
from masms_api.modules.configadmin import models as _cfg  # noqa: F401
from masms_api.modules.documents import models as _docs  # noqa: F401
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


def _headers(*, actor_kind: str = "human") -> dict[str, str]:
    return {
        "X-Organization-Id": "00000000-0000-4000-8000-000000000001",
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": actor_kind,
        "X-Correlation-Id": str(uuid4()),
    }


def _bootstrap_effective_ticket_workflow(client: TestClient, headers: dict[str, str]) -> None:
    version = client.post(
        "/api/v1/config/versions",
        headers=headers,
        json={"title": "Ticket WF", "change_reason": "mod320"},
    )
    assert version.status_code == 201, version.text
    version_id = version.json()["id"]

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

    for edge in (
        ("open", "in_progress", False, False),
        ("in_progress", "done", True, True),
    ):
        tr = client.post(
            "/api/v1/config/transitions",
            headers=headers,
            json={
                "configuration_version_id": version_id,
                "workflow_definition_id": workflow_id,
                "from_status_code": edge[0],
                "to_status_code": edge[1],
                "requires_reason": edge[2],
                "requires_approval": edge[3],
            },
        )
        assert tr.status_code == 201, tr.text

    approved = client.post(f"/api/v1/config/versions/{version_id}/approve", headers=headers)
    assert approved.status_code == 200, approved.text
    activated = client.post(f"/api/v1/config/versions/{version_id}/activate", headers=headers)
    assert activated.status_code == 200, activated.text


def test_transition_history_hold_reopen_and_agent_approval_gate(client: TestClient) -> None:
    headers = _headers()
    _bootstrap_effective_ticket_workflow(client, headers)

    binding = client.post(
        "/api/v1/status-engine/bindings",
        headers=headers,
        json={"entity_type": "ticket", "workflow_code": "ticket", "priority": 10},
    )
    assert binding.status_code == 201, binding.text

    entity_id = str(uuid4())
    init = client.post(
        "/api/v1/status-engine/states",
        headers=headers,
        json={
            "entity_type": "ticket",
            "entity_id": entity_id,
            "initial_status_code": "open",
        },
    )
    assert init.status_code == 201, init.text
    assert init.json()["status_code"] == "open"
    assert isinstance(init.json()["status_code"], str)

    resolve = client.get(
        "/api/v1/status-engine/resolve",
        headers=headers,
        params={"entity_type": "ticket"},
    )
    assert resolve.status_code == 200
    assert resolve.json()["workflow_code"] == "ticket"

    actions = client.get(
        f"/api/v1/status-engine/states/ticket/{entity_id}/actions",
        headers=headers,
    )
    assert actions.status_code == 200, actions.text
    assert actions.json()["actions"][0]["to_status_code"] == "in_progress"

    moved = client.post(
        "/api/v1/status-engine/transitions",
        headers=headers,
        json={
            "entity_type": "ticket",
            "entity_id": entity_id,
            "to_status_code": "in_progress",
        },
    )
    assert moved.status_code == 200, moved.text
    assert moved.json()["status_code"] == "in_progress"

    history = client.get(
        f"/api/v1/status-engine/states/ticket/{entity_id}/history",
        headers=headers,
    )
    assert history.status_code == 200
    assert len(history.json()) >= 2

    agent_headers = _headers(actor_kind="agent")
    agent_blocked = client.post(
        "/api/v1/status-engine/transitions",
        headers=agent_headers,
        json={
            "entity_type": "ticket",
            "entity_id": entity_id,
            "to_status_code": "done",
            "reason": "closing",
            "approval_id": str(uuid4()),
        },
    )
    assert agent_blocked.status_code == 403, agent_blocked.text

    human_needs_approval = client.post(
        "/api/v1/status-engine/transitions",
        headers=headers,
        json={
            "entity_type": "ticket",
            "entity_id": entity_id,
            "to_status_code": "done",
            "reason": "closing",
        },
    )
    assert human_needs_approval.status_code == 409, human_needs_approval.text

    done = client.post(
        "/api/v1/status-engine/transitions",
        headers=headers,
        json={
            "entity_type": "ticket",
            "entity_id": entity_id,
            "to_status_code": "done",
            "reason": "closing",
            "approval_id": str(uuid4()),
        },
    )
    assert done.status_code == 200, done.text
    assert done.json()["status_code"] == "done"

    hold = client.post(
        "/api/v1/status-engine/holds",
        headers=headers,
        json={
            "entity_type": "ticket",
            "entity_id": entity_id,
            "reason": "Waiting on client",
        },
    )
    # On terminal state, hold still allowed; transition blocked while held
    assert hold.status_code == 201, hold.text

    release = client.post(
        f"/api/v1/status-engine/holds/ticket/{entity_id}/release",
        headers=headers,
        json={"note": "Client replied"},
    )
    assert release.status_code == 200, release.text

    reopen = client.post(
        "/api/v1/status-engine/reopen",
        headers=headers,
        json={
            "entity_type": "ticket",
            "entity_id": entity_id,
            "to_status_code": "open",
            "reason": "Incomplete acceptance",
        },
    )
    assert reopen.status_code == 200, reopen.text
    assert reopen.json()["to_status_code"] == "open"

    state = client.get(
        f"/api/v1/status-engine/states/ticket/{entity_id}",
        headers=headers,
    )
    assert state.status_code == 200
    assert state.json()["status_code"] == "open"

    final_history = client.get(
        f"/api/v1/status-engine/states/ticket/{entity_id}/history",
        headers=headers,
    )
    assert final_history.status_code == 200
    assert any(h["to_status_code"] == "done" for h in final_history.json())
    assert any(h["from_status_code"] == "done" for h in final_history.json())


def test_invalid_transition_rejected(client: TestClient) -> None:
    headers = _headers()
    _bootstrap_effective_ticket_workflow(client, headers)
    client.post(
        "/api/v1/status-engine/bindings",
        headers=headers,
        json={"entity_type": "ticket", "workflow_code": "ticket"},
    )
    entity_id = str(uuid4())
    client.post(
        "/api/v1/status-engine/states",
        headers=headers,
        json={
            "entity_type": "ticket",
            "entity_id": entity_id,
            "initial_status_code": "open",
        },
    )
    bad = client.post(
        "/api/v1/status-engine/transitions",
        headers=headers,
        json={
            "entity_type": "ticket",
            "entity_id": entity_id,
            "to_status_code": "done",
        },
    )
    assert bad.status_code == 409, bad.text
