"""API/integration tests for MOD-100 identity."""

from __future__ import annotations

from collections.abc import Generator
from datetime import UTC, datetime
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from masms_api.db import Base, get_db
from masms_api.kernel import outbox as _outbox  # noqa: F401
from masms_api.main import create_app
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


def _headers(org: str | None = None) -> dict[str, str]:
    return {
        "X-Organization-Id": org or "00000000-0000-4000-8000-000000000001",
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": "human",
        "X-Correlation-Id": str(uuid4()),
    }


def test_identity_bootstrap_and_agent_supervisor_rule(client: TestClient) -> None:
    org = client.post(
        "/api/v1/identity/organizations",
        headers=_headers(),
        json={"name": "Eazisols", "slug": "eazisols"},
    )
    assert org.status_code == 201, org.text
    org_id = org.json()["id"]
    headers = _headers(org_id)

    human = client.post(
        "/api/v1/identity/humans",
        headers=headers,
        json={
            "email": "alice@example.com",
            "full_name": "Alice Supervisor",
            "primary_role_code": "PM",
        },
    )
    assert human.status_code == 201, human.text
    human_id = human.json()["id"]
    human_actor_id = human.json()["actor_id"]

    agent = client.post(
        "/api/v1/identity/agents",
        headers=headers,
        json={
            "agent_key": "bd_agent",
            "display_name": "BD Agent",
            "supervisor_human_user_id": human_id,
        },
    )
    assert agent.status_code == 201, agent.text
    assert agent.json()["actor_id"] != human_actor_id
    assert agent.json()["supervisor_human_user_id"] == human_id

    role = client.post(
        "/api/v1/identity/roles",
        headers=headers,
        json={"code": "PM", "title": "Project Manager"},
    )
    assert role.status_code == 201

    dept = client.post(
        "/api/v1/identity/departments",
        headers=headers,
        json={"code": "DELIVERY", "name": "Delivery"},
    )
    assert dept.status_code == 201
    team = client.post(
        "/api/v1/identity/teams",
        headers=headers,
        json={
            "code": "ALPHA",
            "name": "Alpha",
            "department_id": dept.json()["id"],
        },
    )
    assert team.status_code == 201
    member = client.post(
        "/api/v1/identity/team-members",
        headers=headers,
        json={
            "team_id": team.json()["id"],
            "actor_id": human_actor_id,
            "membership_role": "lead",
        },
    )
    assert member.status_code == 201

    reporting = client.post(
        "/api/v1/identity/reporting-lines",
        headers=headers,
        json={
            "subordinate_actor_id": agent.json()["actor_id"],
            "manager_actor_id": human_actor_id,
            "effective_from": datetime.now(UTC).isoformat(),
        },
    )
    assert reporting.status_code == 201

    actors = client.get("/api/v1/identity/actors", headers=headers)
    assert actors.status_code == 200
    assert actors.json()["page"]["total"] >= 2
