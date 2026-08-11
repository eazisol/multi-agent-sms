"""API/integration tests for MOD-410 bugs."""

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
from masms_api.modules.clients import models as _clients  # noqa: F401
from masms_api.modules.comms import models as _comms  # noqa: F401
from masms_api.modules.configadmin import models as _cfg  # noqa: F401
from masms_api.modules.documents import models as _docs  # noqa: F401
from masms_api.modules.followups import models as _flu  # noqa: F401
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.knowledge import models as _kn  # noqa: F401
from masms_api.modules.orchestrator import models as _orf  # noqa: F401
from masms_api.modules.projects import models as _projects  # noqa: F401
from masms_api.modules.queries import models as _queries  # noqa: F401
from masms_api.modules.requirements import models as _reqs  # noqa: F401
from masms_api.modules.roadmap import models as _roadmap  # noqa: F401
from masms_api.modules.statusengine import models as _wfe  # noqa: F401
from masms_api.modules.testcases import models as _tc  # noqa: F401
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


def test_bug_lifecycle_release_gate_and_history(client: TestClient) -> None:
    headers = _headers()
    project_id = str(uuid4())
    req_id = str(uuid4())
    ticket_id = str(uuid4())
    test_id = str(uuid4())
    assignee = "00000000-0000-4000-8000-000000000202"

    sla = client.put(
        "/api/v1/bugs/severity-slas",
        headers=headers,
        json={
            "severity": "critical",
            "response_hours": 4,
            "resolve_hours": 24,
            "blocks_release": True,
        },
    )
    assert sla.status_code == 200, sla.text

    created = client.post(
        "/api/v1/bugs",
        headers=headers,
        json={
            "code": "BUG-CRIT-001",
            "title": "Auth leak on stale session",
            "severity": "critical",
            "project_id": project_id,
            "links": [
                {"link_type": "requirement", "linked_entity_id": req_id},
                {"link_type": "ticket", "linked_entity_id": ticket_id},
                {"link_type": "test_case", "linked_entity_id": test_id},
            ],
        },
    )
    assert created.status_code == 201, created.text
    bug_id = created.json()["id"]
    assert created.json()["blocks_release"] is True
    version = created.json()["version"]

    gate = client.get(
        f"/api/v1/bugs/release-gate?project_id={project_id}",
        headers=headers,
    )
    assert gate.status_code == 200
    assert gate.json()["release_allowed"] is False
    assert "BUG-CRIT-001" in gate.json()["blocking_codes"]

    rejected = client.post(
        f"/api/v1/bugs/{bug_id}/reject",
        headers=headers,
        json={
            "reason": "QA failed smoke",
            "evidence": "screenshot-01",
            "expected_version": version,
        },
    )
    assert rejected.status_code == 200, rejected.text
    assert rejected.json()["status"] == "rejected"
    version = rejected.json()["version"]

    reopened = client.post(
        f"/api/v1/bugs/{bug_id}/reopen",
        headers=headers,
        json={"reason": "Dev restarted fix loop", "expected_version": version},
    )
    assert reopened.status_code == 200, reopened.text
    assert reopened.json()["status"] == "open"
    version = reopened.json()["version"]

    assigned = client.post(
        f"/api/v1/bugs/{bug_id}/assignments",
        headers=headers,
        json={"assignee_actor_id": assignee, "reason": "Primary fixer"},
    )
    assert assigned.status_code == 201, assigned.text

    fix = client.post(
        f"/api/v1/bugs/{bug_id}/fixes",
        headers=headers,
        json={
            "summary": "Rotate session key on logout",
            "build_ref": "sha-fix-1",
            "expected_version": version,
        },
    )
    assert fix.status_code == 201, fix.text
    bug_after_fix = client.get(f"/api/v1/bugs/{bug_id}", headers=headers)
    assert bug_after_fix.json()["status"] == "fixed"
    version = bug_after_fix.json()["version"]

    retest = client.post(
        f"/api/v1/bugs/{bug_id}/retests",
        headers=headers,
        json={
            "result": "passed",
            "evidence_text": "Session cleared",
            "environment_code": "staging",
            "build_ref": "sha-fix-1",
            "fix_submission_id": fix.json()["id"],
            "expected_version": version,
        },
    )
    assert retest.status_code == 201, retest.text
    assert client.get(f"/api/v1/bugs/{bug_id}", headers=headers).json()["status"] == "verified"

    gate2 = client.get(
        f"/api/v1/bugs/release-gate?project_id={project_id}",
        headers=headers,
    )
    assert gate2.json()["release_allowed"] is True

    # Second critical open bug + known-issue exception
    other = client.post(
        "/api/v1/bugs",
        headers=headers,
        json={
            "code": "BUG-CRIT-002",
            "title": "Cosmetic but tagged critical incorrectly wait",
            "severity": "critical",
            "project_id": project_id,
        },
    )
    assert other.status_code == 201
    other_id = other.json()["id"]
    assert (
        client.get(f"/api/v1/bugs/release-gate?project_id={project_id}", headers=headers).json()[
            "release_allowed"
        ]
        is False
    )
    ki = client.post(
        f"/api/v1/bugs/{other_id}/known-issues",
        headers=headers,
        json={"reason": "Accepted for release 1.0", "release_ref": "REL-1.0"},
    )
    assert ki.status_code == 201, ki.text
    decided = client.post(
        f"/api/v1/bugs/known-issues/{ki.json()['id']}/decide",
        headers=headers,
        json={"status": "approved", "expected_bug_version": other.json()["version"]},
    )
    assert decided.status_code == 200, decided.text
    assert decided.json()["status"] == "approved"
    assert (
        client.get(f"/api/v1/bugs/release-gate?project_id={project_id}", headers=headers).json()[
            "release_allowed"
        ]
        is True
    )

    history = client.get(f"/api/v1/bugs/{bug_id}/history", headers=headers)
    assert history.status_code == 200, history.text
    body = history.json()
    link_types = {link["link_type"] for link in body["links"]}
    assert {"requirement", "ticket", "test_case", "fix", "retest"} <= link_types
    assert len(body["fixes"]) >= 1
    assert len(body["retests"]) >= 1
    assert len(body["assignments"]) >= 1

    listed = client.get("/api/v1/bugs?limit=10&offset=0", headers=headers)
    assert listed.status_code == 200
    assert "items" in listed.json() and "page" in listed.json()
