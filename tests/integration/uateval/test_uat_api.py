"""API/integration tests for MOD-620 UAT evaluation."""

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
from masms_api.modules.gmail import models as _gm  # noqa: F401
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.insights import models as _rp  # noqa: F401
from masms_api.modules.integrations import models as _ig  # noqa: F401
from masms_api.modules.jira import models as _jira  # noqa: F401
from masms_api.modules.knowledge import models as _kn  # noqa: F401
from masms_api.modules.notifications import models as _ntf  # noqa: F401
from masms_api.modules.orchestrator import models as _orf  # noqa: F401
from masms_api.modules.projects import models as _projects  # noqa: F401
from masms_api.modules.queries import models as _queries  # noqa: F401
from masms_api.modules.releases import models as _rl  # noqa: F401
from masms_api.modules.reliability import models as _rlb  # noqa: F401
from masms_api.modules.requirements import models as _reqs  # noqa: F401
from masms_api.modules.roadmap import models as _roadmap  # noqa: F401
from masms_api.modules.securityhardening import models as _sh  # noqa: F401
from masms_api.modules.statusengine import models as _wfe  # noqa: F401
from masms_api.modules.testcases import models as _tc  # noqa: F401
from masms_api.modules.tickets import models as _tickets  # noqa: F401
from masms_api.modules.traceability import models as _tr  # noqa: F401
from masms_api.modules.uateval import models as _ua  # noqa: F401
from masms_api.modules.pilot import models as _pl  # noqa: F401
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
    testing_session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session, None, None]:
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


def _headers(org_suffix: str = "1", actor_kind: str = "human") -> dict[str, str]:
    return {
        "X-Organization-Id": f"00000000-0000-4000-8000-00000000000{org_suffix}",
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": actor_kind,
        "X-Correlation-Id": str(uuid4()),
    }


def test_ac001_sample_gate_requires_three_passed_workflows(client: TestClient) -> None:
    headers = _headers("1")

    seeded = client.post("/api/v1/uat/sample-projects/seed", headers=headers)
    assert seeded.status_code == 200, seeded.text
    codes = sorted(item["code"] for item in seeded.json())
    assert codes == ["SAMPLE-A", "SAMPLE-B", "SAMPLE-C"]
    assert all(item["workflow_status"] == "pending" for item in seeded.json())

    again = client.post("/api/v1/uat/sample-projects/seed", headers=headers)
    assert again.status_code == 200, again.text
    assert len(again.json()) == 3

    listed = client.get("/api/v1/uat/sample-projects", headers=headers)
    assert listed.status_code == 200, listed.text
    assert listed.json()["page"]["total"] == 3

    for code in ("SAMPLE-A", "SAMPLE-B"):
        passed = client.post(f"/api/v1/uat/sample-projects/{code}/pass", headers=headers)
        assert passed.status_code == 200, passed.text
        assert passed.json()["workflow_status"] == "passed"

    gate_partial = client.get("/api/v1/uat/sample-gate", headers=headers)
    assert gate_partial.status_code == 200, gate_partial.text
    body_partial = gate_partial.json()
    assert body_partial["passed_count"] == 2
    assert body_partial["required_count"] == 3
    assert body_partial["gate_passed"] is False

    third = client.post("/api/v1/uat/sample-projects/SAMPLE-C/pass", headers=headers)
    assert third.status_code == 200, third.text
    assert third.json()["workflow_status"] == "passed"

    gate_ok = client.get("/api/v1/uat/sample-gate", headers=headers)
    assert gate_ok.status_code == 200, gate_ok.text
    body_ok = gate_ok.json()
    assert body_ok["passed_count"] == 3
    assert body_ok["required_count"] == 3
    assert body_ok["gate_passed"] is True


def test_ac002_agent_quality_meets_target(client: TestClient) -> None:
    headers = _headers("1")

    high = client.post(
        "/api/v1/uat/agent-evaluations",
        headers=headers,
        json={
            "code": "EVAL-85",
            "agent_code": "intake-agent",
            "accuracy_pct": 85,
            "sample_count": 20,
        },
    )
    assert high.status_code == 201, high.text
    assert high.json()["accuracy_pct"] == 85

    quality_ok = client.get("/api/v1/uat/agent-quality", headers=headers)
    assert quality_ok.status_code == 200, quality_ok.text
    body_ok = quality_ok.json()
    assert body_ok["target_pct"] == 80
    assert body_ok["latest_score"] == 85
    assert body_ok["meets_target"] is True

    low = client.post(
        "/api/v1/uat/agent-evaluations",
        headers=headers,
        json={
            "code": "EVAL-70",
            "agent_code": "intake-agent",
            "accuracy_pct": 70,
            "sample_count": 20,
        },
    )
    assert low.status_code == 201, low.text
    assert low.json()["accuracy_pct"] == 70

    quality_bad = client.get("/api/v1/uat/agent-quality", headers=headers)
    assert quality_bad.status_code == 200, quality_bad.text
    body_bad = quality_bad.json()
    assert body_bad["latest_score"] == 70
    assert body_bad["meets_target"] is False


def test_ac003_agent_cannot_accept_evidence_and_org_isolation(client: TestClient) -> None:
    headers = _headers("1")
    other = _headers("2")
    agent = _headers("1", actor_kind="agent")

    seeded = client.post("/api/v1/uat/sample-projects/seed", headers=headers)
    assert seeded.status_code == 200, seeded.text

    other_list = client.get("/api/v1/uat/sample-projects", headers=other)
    assert other_list.status_code == 200, other_list.text
    assert other_list.json()["items"] == []

    cross_project = client.get("/api/v1/uat/sample-projects/SAMPLE-A", headers=other)
    assert cross_project.status_code == 404, cross_project.text

    seed = client.post(
        "/api/v1/uat/seed-scripts",
        headers=headers,
        json={
            "code": "SEED-A",
            "title": "Sample A seed registry",
            "sample_project_code": "SAMPLE-A",
        },
    )
    assert seed.status_code == 201, seed.text
    seed_id = seed.json()["id"]

    cross_seed = client.get(f"/api/v1/uat/seed-scripts/{seed_id}", headers=other)
    assert cross_seed.status_code == 404, cross_seed.text

    evidence = client.post(
        "/api/v1/uat/acceptance-evidence",
        headers=headers,
        json={
            "code": "EV-001",
            "title": "UAT pack",
            "evidence_ref": "docs/uat/ev-001",
            "status": "submitted",
        },
    )
    assert evidence.status_code == 201, evidence.text
    evidence_id = evidence.json()["id"]

    agent_accept = client.post(
        f"/api/v1/uat/acceptance-evidence/{evidence_id}/accept",
        headers=agent,
        json={"expected_version": evidence.json()["version"]},
    )
    assert agent_accept.status_code == 409, agent_accept.text

    human_accept = client.post(
        f"/api/v1/uat/acceptance-evidence/{evidence_id}/accept",
        headers=headers,
        json={"expected_version": evidence.json()["version"]},
    )
    assert human_accept.status_code == 200, human_accept.text
    assert human_accept.json()["status"] == "accepted"
