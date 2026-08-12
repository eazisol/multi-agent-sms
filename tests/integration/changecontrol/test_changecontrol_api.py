"""API/integration tests for MOD-420 change control."""

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
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.knowledge import models as _kn  # noqa: F401
from masms_api.modules.insights import models as _rp  # noqa: F401
from masms_api.modules.gmail import models as _gm  # noqa: F401
from masms_api.modules.integrations import models as _ig  # noqa: F401
from masms_api.modules.notifications import models as _ntf  # noqa: F401
from masms_api.modules.orchestrator import models as _orf  # noqa: F401
from masms_api.modules.projects import models as _projects  # noqa: F401
from masms_api.modules.queries import models as _queries  # noqa: F401
from masms_api.modules.releases import models as _rl  # noqa: F401
from masms_api.modules.requirements import models as _reqs  # noqa: F401
from masms_api.modules.roadmap import models as _roadmap  # noqa: F401
from masms_api.modules.reliability import models as _rlb  # noqa: F401
from masms_api.modules.securityhardening import models as _sh  # noqa: F401
from masms_api.modules.statusengine import models as _wfe  # noqa: F401
from masms_api.modules.uateval import models as _ua  # noqa: F401
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


def test_change_control_gate_approve_reject_and_baseline(client: TestClient) -> None:
    headers = _headers()
    artifact_id = str(uuid4())
    ticket_id = str(uuid4())

    risk = client.post(
        "/api/v1/change-control/risks",
        headers=headers,
        json={
            "code": "RISK-001",
            "title": "Scope creep without CR",
            "risk_level": "high",
        },
    )
    assert risk.status_code == 201, risk.text
    review = client.post(
        f"/api/v1/change-control/risks/{risk.json()['id']}/reviews",
        headers=headers,
        json={"outcome": "mitigating", "notes": "Require CR approval", "expected_version": 1},
    )
    assert review.status_code == 201, review.text

    cr = client.post(
        "/api/v1/change-control/change-requests",
        headers=headers,
        json={
            "code": "CR-001",
            "title": "Add reporting dashboard",
            "change_type": "scope",
            "rationale": "Client asked for extra widgets",
        },
    )
    assert cr.status_code == 201, cr.text
    cr_id = cr.json()["id"]
    version = cr.json()["version"]

    # AC-001: draft cannot update baseline / enter development
    blocked = client.post(
        f"/api/v1/change-control/change-requests/{cr_id}/baseline-updates",
        headers=headers,
        json={
            "artifact_type": "requirement",
            "artifact_id": artifact_id,
            "from_version": 1,
            "to_version": 2,
            "ticket_id": ticket_id,
        },
    )
    assert blocked.status_code == 409, blocked.text
    gate = client.get(
        f"/api/v1/change-control/change-requests/{cr_id}/development-gate",
        headers=headers,
    )
    assert gate.status_code == 200
    assert gate.json()["allowed"] is False

    impact = client.post(
        f"/api/v1/change-control/change-requests/{cr_id}/impacts",
        headers=headers,
        json={
            "summary": "Touches requirements + tickets",
            "affected_areas": ["requirements", "tickets"],
            "estimated_effort_hours": 40,
            "expected_version": version,
        },
    )
    assert impact.status_code == 201, impact.text
    version = client.get(
        f"/api/v1/change-control/change-requests/{cr_id}", headers=headers
    ).json()["version"]

    submitted = client.post(
        f"/api/v1/change-control/change-requests/{cr_id}/submit",
        headers=headers,
        json={"expected_version": version},
    )
    assert submitted.status_code == 200, submitted.text
    assert submitted.json()["status"] == "pending_approval"
    version = submitted.json()["version"]

    approved = client.post(
        f"/api/v1/change-control/change-requests/{cr_id}/approvals",
        headers=headers,
        json={
            "decision": "approved",
            "rationale": "Within capacity",
            "evidence": "CAB minutes 2026-08-11",
            "expected_version": version,
        },
    )
    assert approved.status_code == 201, approved.text
    assert (
        client.get(f"/api/v1/change-control/change-requests/{cr_id}", headers=headers).json()[
            "status"
        ]
        == "approved"
    )
    assert (
        client.get(
            f"/api/v1/change-control/change-requests/{cr_id}/development-gate",
            headers=headers,
        ).json()["allowed"]
        is True
    )

    # AC-002: approved CR updates artifact version + ticket link
    baseline = client.post(
        f"/api/v1/change-control/change-requests/{cr_id}/baseline-updates",
        headers=headers,
        json={
            "artifact_type": "requirement",
            "artifact_id": artifact_id,
            "from_version": 1,
            "to_version": 2,
            "ticket_id": ticket_id,
            "notes": "SRS v2 after CR-001",
        },
    )
    assert baseline.status_code == 201, baseline.text
    assert baseline.json()["to_version"] == 2
    assert baseline.json()["ticket_id"] == ticket_id

    # AC-003: rejected CR preserves rationale + evidence
    cr2 = client.post(
        "/api/v1/change-control/change-requests",
        headers=headers,
        json={"code": "CR-002", "title": "Rewrite platform", "change_type": "architecture"},
    )
    assert cr2.status_code == 201
    cr2_id = cr2.json()["id"]
    v2 = cr2.json()["version"]
    assert (
        client.post(
            f"/api/v1/change-control/change-requests/{cr2_id}/impacts",
            headers=headers,
            json={"summary": "Too large", "affected_areas": ["all"], "expected_version": v2},
        ).status_code
        == 201
    )
    v2 = client.get(
        f"/api/v1/change-control/change-requests/{cr2_id}", headers=headers
    ).json()["version"]
    assert (
        client.post(
            f"/api/v1/change-control/change-requests/{cr2_id}/submit",
            headers=headers,
            json={"expected_version": v2},
        ).status_code
        == 200
    )
    v2 = client.get(
        f"/api/v1/change-control/change-requests/{cr2_id}", headers=headers
    ).json()["version"]
    rejected = client.post(
        f"/api/v1/change-control/change-requests/{cr2_id}/approvals",
        headers=headers,
        json={
            "decision": "rejected",
            "rationale": "Out of budget",
            "evidence": "Finance note FN-9",
            "expected_version": v2,
        },
    )
    assert rejected.status_code == 201, rejected.text
    body = client.get(
        f"/api/v1/change-control/change-requests/{cr2_id}", headers=headers
    ).json()
    assert body["status"] == "rejected"
    assert body["rationale"] == "Out of budget"
    assert body["decision_evidence"] == "Finance note FN-9"
    approvals = client.get(
        f"/api/v1/change-control/change-requests/{cr2_id}/approvals", headers=headers
    )
    assert approvals.status_code == 200
    assert approvals.json()[0]["evidence"] == "Finance note FN-9"

    listed = client.get("/api/v1/change-control/change-requests?limit=10&offset=0", headers=headers)
    assert listed.status_code == 200
    assert "items" in listed.json() and "page" in listed.json()
