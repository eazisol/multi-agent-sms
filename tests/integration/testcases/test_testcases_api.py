"""API/integration tests for MOD-400 test cases."""

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
from masms_api.modules.capacity import models as _capacity  # noqa: F401
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


def test_testcase_lifecycle_coverage_and_evidence(client: TestClient) -> None:
    headers = _headers()
    req_id = str(uuid4())

    case = client.post(
        "/api/v1/test-cases/cases",
        headers=headers,
        json={
            "code": "TC-AUTH-001",
            "title": "Deny cross-tenant case read",
            "case_type": "permission",
            "priority": "P0",
            "expected_result": "403 or not-found for foreign org",
            "steps": [
                {
                    "step_number": 1,
                    "action_text": "Call get with foreign org header",
                    "expected_text": "Access denied",
                }
            ],
        },
    )
    assert case.status_code == 201, case.text
    case_id = case.json()["id"]
    assert case.json()["status"] == "draft"

    steps = client.get(f"/api/v1/test-cases/cases/{case_id}/steps", headers=headers)
    assert steps.status_code == 200
    assert len(steps.json()) == 1

    # Draft cannot run
    blocked = client.post(
        "/api/v1/test-cases/runs",
        headers=headers,
        json={"case_id": case_id, "environment_code": "local", "build_ref": "sha-draft"},
    )
    assert blocked.status_code == 422, blocked.text

    approved = client.post(
        f"/api/v1/test-cases/cases/{case_id}/approve",
        headers=headers,
        json={"expected_version": 1},
    )
    assert approved.status_code == 200, approved.text
    assert approved.json()["status"] == "approved"

    coverage = client.post(
        f"/api/v1/test-cases/cases/{case_id}/coverage",
        headers=headers,
        json={
            "requirement_id": req_id,
            "requirement_priority": "Must-Have",
            "coverage_notes": "AC-001 / AC-002 signal",
        },
    )
    assert coverage.status_code == 201, coverage.text

    suite = client.post(
        "/api/v1/test-cases/suites",
        headers=headers,
        json={"code": "SUITE-AUTH", "title": "Auth negatives", "case_ids": [case_id]},
    )
    assert suite.status_code == 201, suite.text

    plan = client.post(
        "/api/v1/test-cases/plans",
        headers=headers,
        json={
            "code": "PLAN-LOCAL",
            "title": "Local M1 plan",
            "environment_code": "local",
            "build_ref": "sha-abc123",
            "suite_ids": [suite.json()["id"]],
        },
    )
    assert plan.status_code == 201, plan.text
    assert plan.json()["environment_code"] == "local"
    assert plan.json()["build_ref"] == "sha-abc123"

    run = client.post(
        "/api/v1/test-cases/runs",
        headers=headers,
        json={
            "case_id": case_id,
            "plan_id": plan.json()["id"],
            "environment_code": "staging",
            "build_ref": "sha-abc123",
        },
    )
    assert run.status_code == 201, run.text
    run_id = run.json()["id"]
    assert run.json()["status"] == "running"
    assert run.json()["environment_code"] == "staging"
    assert run.json()["build_ref"] == "sha-abc123"

    done = client.post(
        f"/api/v1/test-cases/runs/{run_id}/complete",
        headers=headers,
        json={
            "status": "passed",
            "result_summary": "Cross-tenant denied",
            "expected_version": 1,
            "evidence_title": "Response snapshot",
            "evidence_body": "HTTP 404 problem+json",
        },
    )
    assert done.status_code == 200, done.text
    assert done.json()["status"] == "passed"

    evidence = client.get(f"/api/v1/test-cases/runs/{run_id}/evidence", headers=headers)
    assert evidence.status_code == 200
    assert len(evidence.json()) == 1
    assert evidence.json()[0]["environment_code"] == "staging"
    assert evidence.json()[0]["build_ref"] == "sha-abc123"

    summary = client.post(
        "/api/v1/test-cases/coverage/summary",
        headers=headers,
        json={"must_have_requirement_ids": [req_id]},
    )
    assert summary.status_code == 200, summary.text
    body = summary.json()
    assert body["must_have_total"] == 1
    assert body["must_have_covered"] == 1
    assert body["permission_negative_cases"] >= 1
    assert body["uncovered_must_have_requirement_ids"] == []

    listed = client.get("/api/v1/test-cases/cases?limit=10&offset=0", headers=headers)
    assert listed.status_code == 200
    assert "items" in listed.json() and "page" in listed.json()

    # Concurrency conflict on re-complete
    conflict = client.post(
        f"/api/v1/test-cases/runs/{run_id}/complete",
        headers=headers,
        json={"status": "failed", "expected_version": 1},
    )
    assert conflict.status_code in {409, 422}
