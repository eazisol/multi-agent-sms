"""API/integration tests for MOD-300 tickets."""

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
from masms_api.modules.documents import models as _documents  # noqa: F401
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.projects import models as _projects  # noqa: F401
from masms_api.modules.queries import models as _queries  # noqa: F401
from masms_api.modules.requirements import models as _requirements  # noqa: F401
from masms_api.modules.roadmap import models as _roadmap  # noqa: F401
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


def _seed_project_phase_requirement(
    client: TestClient, headers: dict[str, str]
) -> tuple[str, str, str]:
    project = client.post(
        "/api/v1/projects",
        headers=headers,
        json={"code": "PORTAL", "title": "Portal"},
    )
    assert project.status_code == 201, project.text
    project_id = project.json()["id"]

    phase = client.post(
        "/api/v1/roadmap/phases",
        headers=headers,
        json={
            "project_id": project_id,
            "code": "BUILD",
            "title": "Build",
            "sequence": 1,
        },
    )
    assert phase.status_code == 201, phase.text

    req = client.post(
        "/api/v1/projects/requirements",
        headers=headers,
        json={
            "project_id": project_id,
            "requirement_code": "REQ-100",
            "title": "Auth",
        },
    )
    assert req.status_code == 201
    return project_id, phase.json()["id"], req.json()["id"]


def _satisfy_all_checks(
    client: TestClient, headers: dict[str, str], ticket_id: str, kind: str
) -> None:
    listed = client.get(f"/api/v1/tickets/{ticket_id}/{kind}-checks", headers=headers)
    assert listed.status_code == 200, listed.text
    for check in listed.json():
        ok = client.post(
            f"/api/v1/tickets/{kind}-checks/{check['id']}/satisfy",
            headers=headers,
            json={"notes": "ok"},
        )
        assert ok.status_code == 200, ok.text


def test_ready_gate_links_and_reopen(client: TestClient) -> None:
    headers = _headers()
    owner = "00000000-0000-4000-8000-000000000101"
    project_id, phase_id, requirement_id = _seed_project_phase_requirement(
        client, headers
    )

    create = client.post(
        "/api/v1/tickets",
        headers=headers,
        json={
            "project_id": project_id,
            "code": "T-1",
            "title": "Login story",
            "ticket_type": "story",
        },
    )
    assert create.status_code == 201, create.text
    ticket_id = create.json()["id"]
    version = create.json()["version"]

    # AC-001: Ready blocked without required info
    not_ready = client.post(
        f"/api/v1/tickets/{ticket_id}/transitions",
        headers=headers,
        json={"next_status": "ready", "expected_version": version},
    )
    assert not_ready.status_code == 422, not_ready.text

    update = client.patch(
        f"/api/v1/tickets/{ticket_id}",
        headers=headers,
        json={
            "description": "Implement login",
            "acceptance_criteria": "User authenticates",
            "definition_of_done": "Unit + API tests pass",
            "estimate_points": "5",
            "priority": "high",
            "phase_id": phase_id,
            "owner_actor_id": owner,
            "expected_version": version,
        },
    )
    assert update.status_code == 200, update.text
    version = update.json()["version"]

    link = client.post(
        "/api/v1/tickets/requirement-links",
        headers=headers,
        json={"ticket_id": ticket_id, "requirement_id": requirement_id},
    )
    assert link.status_code == 201, link.text

    sub = client.post(
        "/api/v1/tickets/subtasks",
        headers=headers,
        json={"ticket_id": ticket_id, "code": "S-1", "title": "Form UI"},
    )
    assert sub.status_code == 201, sub.text

    _satisfy_all_checks(client, headers, ticket_id, "readiness")
    ready = client.post(
        f"/api/v1/tickets/{ticket_id}/transitions",
        headers=headers,
        json={"next_status": "ready", "expected_version": version},
    )
    assert ready.status_code == 200, ready.text
    assert ready.json()["status"] == "ready"
    version = ready.json()["version"]

    # Walk to passed_qa then done
    for nxt in (
        "assigned",
        "in_progress",
        "code_review",
        "ready_for_qa",
        "qa_in_progress",
        "passed_qa",
    ):
        step = client.post(
            f"/api/v1/tickets/{ticket_id}/transitions",
            headers=headers,
            json={"next_status": nxt, "expected_version": version},
        )
        assert step.status_code == 200, step.text
        version = step.json()["version"]

    blocked_done = client.post(
        f"/api/v1/tickets/{ticket_id}/transitions",
        headers=headers,
        json={"next_status": "done", "expected_version": version},
    )
    assert blocked_done.status_code == 422, blocked_done.text

    _satisfy_all_checks(client, headers, ticket_id, "done")
    done = client.post(
        f"/api/v1/tickets/{ticket_id}/transitions",
        headers=headers,
        json={"next_status": "done", "expected_version": version},
    )
    assert done.status_code == 200, done.text
    assert done.json()["status"] == "done"
    version = done.json()["version"]

    evidence = client.post(
        "/api/v1/tickets/evidence",
        headers=headers,
        json={
            "ticket_id": ticket_id,
            "evidence_type": "reopen_justification",
            "title": "Regression found",
            "summary": "Login fails for SSO users",
        },
    )
    assert evidence.status_code == 201, evidence.text

    # AC-003: reopen needs reason + evidence
    reopen = client.post(
        f"/api/v1/tickets/{ticket_id}/reopen",
        headers=headers,
        json={
            "reason": "Confirmed defect against AC",
            "evidence_id": evidence.json()["id"],
            "next_status": "in_progress",
            "expected_version": version,
        },
    )
    assert reopen.status_code == 200, reopen.text
    assert reopen.json()["status"] == "in_progress"
    assert reopen.json()["reopen_reason"] is not None

    listed = client.get(f"/api/v1/tickets/projects/{project_id}", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_dependency_and_self_link_rejected(client: TestClient) -> None:
    headers = _headers()
    project_id, _phase_id, _req = _seed_project_phase_requirement(client, headers)
    a = client.post(
        "/api/v1/tickets",
        headers=headers,
        json={"project_id": project_id, "code": "A", "title": "Ticket A"},
    )
    b = client.post(
        "/api/v1/tickets",
        headers=headers,
        json={"project_id": project_id, "code": "B", "title": "Ticket B"},
    )
    assert a.status_code == 201 and b.status_code == 201
    dep = client.post(
        "/api/v1/tickets/dependencies",
        headers=headers,
        json={
            "project_id": project_id,
            "predecessor_ticket_id": a.json()["id"],
            "successor_ticket_id": b.json()["id"],
        },
    )
    assert dep.status_code == 201, dep.text
    self_dep = client.post(
        "/api/v1/tickets/dependencies",
        headers=headers,
        json={
            "project_id": project_id,
            "predecessor_ticket_id": a.json()["id"],
            "successor_ticket_id": a.json()["id"],
        },
    )
    assert self_dep.status_code == 422
