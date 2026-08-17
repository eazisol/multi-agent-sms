"""API/integration tests for MOD-610 reliability."""

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
from masms_api.modules.pilot import models as _pl  # noqa: F401
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


def _headers(org_suffix: str = "1") -> dict[str, str]:
    return {
        "X-Organization-Id": f"00000000-0000-4000-8000-00000000000{org_suffix}",
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": "human",
        "X-Correlation-Id": str(uuid4()),
    }


def test_ac001_api_slo_from_recorded_p95(client: TestClient) -> None:
    headers = _headers("1")

    passed = client.post(
        "/api/v1/reliability/performance-tests",
        headers=headers,
        json={
            "code": "PERF-1800",
            "suite_name": "api-normal",
            "p95_ms": 1800,
            "sample_count": 100,
        },
    )
    assert passed.status_code == 201, passed.text
    assert passed.json()["p95_ms"] == 1800

    slo_ok = client.get("/api/v1/reliability/api-slo", headers=headers)
    assert slo_ok.status_code == 200, slo_ok.text
    body_ok = slo_ok.json()
    assert body_ok["p95_ms"] == 1800
    assert body_ok["budget_ms"] == 2000
    assert body_ok["slo_met"] is True

    failed = client.post(
        "/api/v1/reliability/performance-tests",
        headers=headers,
        json={
            "code": "PERF-2500",
            "suite_name": "api-normal",
            "p95_ms": 2500,
            "sample_count": 100,
        },
    )
    assert failed.status_code == 201, failed.text
    assert failed.json()["p95_ms"] == 2500

    slo_bad = client.get("/api/v1/reliability/api-slo", headers=headers)
    assert slo_bad.status_code == 200, slo_bad.text
    body_bad = slo_bad.json()
    assert body_bad["p95_ms"] == 2500
    assert body_bad["slo_met"] is False


def test_ac002_dashboard_slo_from_recorded_p95(client: TestClient) -> None:
    headers = _headers("1")

    ok = client.post(
        "/api/v1/reliability/slo-dashboards",
        headers=headers,
        json={
            "name": "pilot-desk",
            "dashboard_p95_ms": 2500,
            "status": "active",
        },
    )
    assert ok.status_code == 201, ok.text
    assert ok.json()["dashboard_p95_ms"] == 2500

    slo_ok = client.get("/api/v1/reliability/dashboard-slo", headers=headers)
    assert slo_ok.status_code == 200, slo_ok.text
    body_ok = slo_ok.json()
    assert body_ok["dashboard_p95_ms"] == 2500
    assert body_ok["budget_ms"] == 3000
    assert body_ok["slo_met"] is True

    bad = client.post(
        "/api/v1/reliability/slo-dashboards",
        headers=headers,
        json={
            "name": "pilot-desk",
            "dashboard_p95_ms": 4000,
            "status": "active",
        },
    )
    assert bad.status_code == 201, bad.text
    assert bad.json()["dashboard_p95_ms"] == 4000

    slo_bad = client.get("/api/v1/reliability/dashboard-slo", headers=headers)
    assert slo_bad.status_code == 200, slo_bad.text
    body_bad = slo_bad.json()
    assert body_bad["dashboard_p95_ms"] == 4000
    assert body_bad["slo_met"] is False


def test_ac003_workflow_replay_resume_idempotency_and_org_isolation(
    client: TestClient,
) -> None:
    headers = _headers("1")
    other = _headers("2")
    key = "replay-key-610"

    created = client.post(
        "/api/v1/reliability/replays",
        headers=headers,
        json={"workflow_name": "query_intake", "idempotency_key": key},
    )
    assert created.status_code == 201, created.text
    replay = created.json()
    assert replay["status"] == "pending"
    replay_id = replay["id"]

    failed = client.post(
        f"/api/v1/reliability/replays/{replay_id}/fail",
        headers=headers,
        json={"last_error": "worker crash", "expected_version": replay["version"]},
    )
    assert failed.status_code == 200, failed.text
    assert failed.json()["status"] == "failed"

    resumed = client.post(
        f"/api/v1/reliability/replays/{replay_id}/resume",
        headers=headers,
        json={"expected_version": failed.json()["version"]},
    )
    assert resumed.status_code == 200, resumed.text
    assert resumed.json()["status"] == "resumed"

    completed = client.post(
        f"/api/v1/reliability/replays/{replay_id}/complete",
        headers=headers,
        json={"expected_version": resumed.json()["version"]},
    )
    assert completed.status_code == 200, completed.text
    assert completed.json()["status"] == "completed"

    duplicate_create = client.post(
        "/api/v1/reliability/replays",
        headers=headers,
        json={"workflow_name": "query_intake", "idempotency_key": key},
    )
    assert duplicate_create.status_code == 409, duplicate_create.text

    duplicate_resume = client.post(
        f"/api/v1/reliability/replays/{replay_id}/resume",
        headers=headers,
        json={},
    )
    assert duplicate_resume.status_code == 409, duplicate_resume.text

    listed = client.get("/api/v1/reliability/replays", headers=headers)
    assert listed.status_code == 200, listed.text
    assert len(listed.json()["items"]) == 1

    other_list = client.get("/api/v1/reliability/replays", headers=other)
    assert other_list.status_code == 200, other_list.text
    assert other_list.json()["items"] == []

    cross = client.post(
        f"/api/v1/reliability/replays/{replay_id}/resume",
        headers=other,
        json={},
    )
    assert cross.status_code == 404, cross.text
