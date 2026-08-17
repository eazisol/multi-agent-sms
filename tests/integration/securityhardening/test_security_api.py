"""API/integration tests for MOD-600 security hardening."""

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


def test_ac001_critical_gate_and_org_isolation(client: TestClient) -> None:
    headers = _headers("1")
    other = _headers("2")

    gate_ok = client.get("/api/v1/security/gate", headers=headers)
    assert gate_ok.status_code == 200, gate_ok.text
    assert gate_ok.json()["critical_open_count"] == 0
    assert gate_ok.json()["gate_passed"] is True

    created = client.post(
        "/api/v1/security/incidents",
        headers=headers,
        json={
            "code": "INC-CRIT-1",
            "title": "Critical isolation defect",
            "severity": "critical",
            "summary": "Open critical incident for gate",
        },
    )
    assert created.status_code == 201, created.text
    incident = created.json()
    assert incident["severity"] == "critical"
    assert incident["status"] == "open"

    gate_fail = client.get("/api/v1/security/gate", headers=headers)
    assert gate_fail.status_code == 200, gate_fail.text
    assert gate_fail.json()["critical_open_count"] == 1
    assert gate_fail.json()["gate_passed"] is False

    closed = client.post(
        f"/api/v1/security/incidents/{incident['id']}/close",
        headers=headers,
        json={"expected_version": incident["version"]},
    )
    assert closed.status_code == 200, closed.text
    assert closed.json()["status"] == "closed"

    gate_after = client.get("/api/v1/security/gate", headers=headers)
    assert gate_after.status_code == 200, gate_after.text
    assert gate_after.json()["critical_open_count"] == 0
    assert gate_after.json()["gate_passed"] is True

    other_list = client.get("/api/v1/security/incidents", headers=other)
    assert other_list.status_code == 200, other_list.text
    assert other_list.json()["items"] == []

    cross = client.post(
        f"/api/v1/security/incidents/{incident['id']}/close",
        headers=other,
        json={},
    )
    assert cross.status_code == 404, cross.text


def test_ac002_rpo_rto_recovery_validation(client: TestClient) -> None:
    headers = _headers("1")

    backup = client.post(
        "/api/v1/security/backups",
        headers=headers,
        json={
            "backup_ref": "bk-local-001",
            "environment": "local",
            "rpo_minutes": 60,
            "rto_minutes": 120,
        },
    )
    assert backup.status_code == 201, backup.text
    backup_id = backup.json()["id"]

    passed = client.post(
        "/api/v1/security/restore-tests",
        headers=headers,
        json={
            "backup_record_id": backup_id,
            "measured_rpo_minutes": 30,
            "measured_rto_minutes": 90,
            "notes": "Within targets",
        },
    )
    assert passed.status_code == 201, passed.text
    assert passed.json()["result"] == "passed"

    validation_ok = client.get("/api/v1/security/recovery-validation", headers=headers)
    assert validation_ok.status_code == 200, validation_ok.text
    body_ok = validation_ok.json()
    assert body_ok["rpo_met"] is True
    assert body_ok["rto_met"] is True
    assert body_ok["validated"] is True

    failed = client.post(
        "/api/v1/security/restore-tests",
        headers=headers,
        json={
            "backup_record_id": backup_id,
            "measured_rpo_minutes": 90,
            "measured_rto_minutes": 180,
            "notes": "Exceeds targets",
        },
    )
    assert failed.status_code == 201, failed.text
    assert failed.json()["result"] == "failed"

    validation_bad = client.get("/api/v1/security/recovery-validation", headers=headers)
    assert validation_bad.status_code == 200, validation_bad.text
    body_bad = validation_bad.json()
    assert body_bad["rpo_met"] is False
    assert body_bad["rto_met"] is False
    assert body_bad["validated"] is False


def test_ac003_training_policy_default_and_opt_in(client: TestClient) -> None:
    headers = _headers("1")

    default_policy = client.get("/api/v1/security/training-policy", headers=headers)
    assert default_policy.status_code == 200, default_policy.text
    assert default_policy.json()["allow_model_training"] is False
    assert default_policy.json()["approval_evidence"] is None

    denied = client.put(
        "/api/v1/security/training-policy",
        headers=headers,
        json={"allow_model_training": True},
    )
    assert denied.status_code in (409, 422), denied.text
    assert "human_approval_evidence" in denied.text

    allowed = client.put(
        "/api/v1/security/training-policy",
        headers=headers,
        json={
            "allow_model_training": True,
            "human_approval_evidence": "Approved by security owner 2026-08-11",
        },
    )
    assert allowed.status_code == 200, allowed.text
    assert allowed.json()["allow_model_training"] is True
    assert allowed.json()["approval_evidence"] is not None
