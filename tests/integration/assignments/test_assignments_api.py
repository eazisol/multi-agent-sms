"""API/integration tests for MOD-310 assignments."""

from __future__ import annotations

from collections.abc import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from masms_api.db import Base, get_db
from masms_api.kernel import outbox as _outbox  # noqa: F401
from masms_api.main import create_app
from masms_api.modules.access import models as _access  # noqa: F401
from masms_api.modules.assignments import models as _assignments  # noqa: F401
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

ORG = "00000000-0000-4000-8000-000000000001"
ACTOR = "00000000-0000-4000-8000-000000000101"
OTHER = "00000000-0000-4000-8000-000000000202"


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


def _headers(actor: str = ACTOR) -> dict[str, str]:
    return {
        "X-Organization-Id": ORG,
        "X-Actor-Id": actor,
        "X-Actor-Kind": "human",
        "X-Correlation-Id": str(uuid4()),
    }


def _seed_ticket(client: TestClient, headers: dict[str, str]) -> tuple[str, str]:
    project = client.post(
        "/api/v1/projects",
        headers=headers,
        json={"code": "PORTAL", "title": "Portal"},
    )
    assert project.status_code == 201, project.text
    project_id = project.json()["id"]
    ticket = client.post(
        "/api/v1/tickets",
        headers=headers,
        json={"project_id": project_id, "code": "T-10", "title": "Auth work"},
    )
    assert ticket.status_code == 201, ticket.text
    return project_id, ticket.json()["id"]


def _add_member(
    client: TestClient, headers: dict[str, str], project_id: str, actor_id: str
) -> None:
    member = client.post(
        "/api/v1/access/project-members",
        headers=headers,
        json={"project_id": project_id, "actor_id": actor_id, "role_code": "developer"},
    )
    assert member.status_code == 201, member.text


def test_unauthorized_blocked_and_assign_ack_reassign(client: TestClient) -> None:
    headers = _headers()
    project_id, ticket_id = _seed_ticket(client, headers)

    blocked = client.post(
        "/api/v1/assignments",
        headers=headers,
        json={"ticket_id": ticket_id, "assignee_actor_id": ACTOR},
    )
    assert blocked.status_code == 403, blocked.text

    _add_member(client, headers, project_id, ACTOR)
    _add_member(client, headers, project_id, OTHER)

    assigned = client.post(
        "/api/v1/assignments",
        headers=headers,
        json={"ticket_id": ticket_id, "assignee_actor_id": ACTOR, "allocation_pct": "20"},
    )
    assert assigned.status_code == 201, assigned.text
    assignment_id = assigned.json()["id"]
    assert assigned.json()["status"] == "pending_ack"

    recs = client.post(
        "/api/v1/assignments/recommendations",
        headers=headers,
        json={
            "ticket_id": ticket_id,
            "candidate_actor_ids": [ACTOR, OTHER],
        },
    )
    assert recs.status_code == 201, recs.text
    assert len(recs.json()) == 2
    assert all(r["eligible"] for r in recs.json())

    ack = client.post(
        f"/api/v1/assignments/{assignment_id}/acknowledge",
        headers=headers,
        json={"note": "Starting now"},
    )
    assert ack.status_code == 200, ack.text
    assert ack.json()["status"] == "acknowledged"

    version = client.get(f"/api/v1/assignments/tickets/{ticket_id}", headers=headers)
    assert version.status_code == 200
    active = next(a for a in version.json() if a["id"] == assignment_id)
    assert active["status"] == "acknowledged"

    reassigned = client.post(
        f"/api/v1/assignments/{assignment_id}/reassign",
        headers=headers,
        json={
            "new_assignee_actor_id": OTHER,
            "reason": "Load balance across team",
            "expected_version": active["version"],
            "allocation_pct": "15",
        },
    )
    assert reassigned.status_code == 200, reassigned.text
    assert reassigned.json()["assignee_actor_id"] == OTHER

    history = client.get(
        f"/api/v1/assignments/tickets/{ticket_id}/reassignment-history",
        headers=headers,
    )
    assert history.status_code == 200
    assert len(history.json()) == 1
    assert history.json()[0]["reason"] == "Load balance across team"

    alloc = client.get(
        f"/api/v1/assignments/tickets/{ticket_id}/allocation-history",
        headers=headers,
    )
    assert alloc.status_code == 200
    assert len(alloc.json()) >= 2


def test_override_requires_reason(client: TestClient) -> None:
    headers = _headers()
    project_id, ticket_id = _seed_ticket(client, headers)
    # No membership — even override must be authorized first
    missing_member = client.post(
        "/api/v1/assignments",
        headers=headers,
        json={
            "ticket_id": ticket_id,
            "assignee_actor_id": ACTOR,
            "allow_override": True,
            "override_reason": "Emergency",
        },
    )
    assert missing_member.status_code == 403

    _add_member(client, headers, project_id, ACTOR)
    # Put actor on leave so eligibility fails
    leave = client.post(
        "/api/v1/capacity/leave",
        headers=headers,
        json={
            "actor_id": ACTOR,
            "starts_on": "2000-01-01",
            "ends_on": "2100-01-01",
            "leave_type": "annual",
        },
    )
    assert leave.status_code == 201, leave.text

    no_reason = client.post(
        "/api/v1/assignments",
        headers=headers,
        json={
            "ticket_id": ticket_id,
            "assignee_actor_id": ACTOR,
            "allow_override": True,
        },
    )
    assert no_reason.status_code == 422, no_reason.text

    ok = client.post(
        "/api/v1/assignments",
        headers=headers,
        json={
            "ticket_id": ticket_id,
            "assignee_actor_id": ACTOR,
            "allow_override": True,
            "override_reason": "Critical production incident",
        },
    )
    assert ok.status_code == 201, ok.text
    assert ok.json()["is_override"] is True
