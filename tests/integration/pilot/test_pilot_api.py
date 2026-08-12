"""API/integration tests for MOD-630 controlled pilot gates."""

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


def _headers(org_suffix: str = "1", actor_kind: str = "human") -> dict[str, str]:
    return {
        "X-Organization-Id": f"00000000-0000-4000-8000-00000000000{org_suffix}",
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": actor_kind,
        "X-Correlation-Id": str(uuid4()),
    }


def _create_plan(client: TestClient, headers: dict[str, str], code: str = "PILOT-630") -> str:
    created = client.post(
        "/api/v1/pilot/plans",
        headers=headers,
        json={"code": code, "title": "Controlled pilot"},
    )
    assert created.status_code == 201, created.text
    return created.json()["id"]


def test_ac001_acceptance_gate_blocks_failed_critical(client: TestClient) -> None:
    headers = _headers("1")
    plan_id = _create_plan(client, headers)

    recorded = client.post(
        f"/api/v1/pilot/plans/{plan_id}/acceptance-tests",
        headers=headers,
        json={
            "code": "AT-CRIT-1",
            "title": "Critical production path",
            "severity": "critical",
            "result": "failed",
        },
    )
    assert recorded.status_code == 201, recorded.text
    test_id = recorded.json()["id"]

    gate_fail = client.get(
        f"/api/v1/pilot/acceptance-gate?plan_id={plan_id}", headers=headers
    )
    assert gate_fail.status_code == 200, gate_fail.text
    body_fail = gate_fail.json()
    assert body_fail["critical_high_failed_count"] == 1
    assert body_fail["gate_passed"] is False

    passed = client.post(
        f"/api/v1/pilot/plans/{plan_id}/acceptance-tests/{test_id}/result",
        headers=headers,
        json={"result": "passed"},
    )
    assert passed.status_code == 200, passed.text
    assert passed.json()["result"] == "passed"

    gate_ok = client.get(
        f"/api/v1/pilot/acceptance-gate?plan_id={plan_id}", headers=headers
    )
    assert gate_ok.status_code == 200, gate_ok.text
    body_ok = gate_ok.json()
    assert body_ok["critical_high_failed_count"] == 0
    assert body_ok["gate_passed"] is True


def test_ac002_pilot_approval_requires_all_registered_users(client: TestClient) -> None:
    headers = _headers("1")
    plan_id = _create_plan(client, headers, code="PILOT-USERS")
    actor_a = "00000000-0000-4000-8000-000000000201"
    actor_b = "00000000-0000-4000-8000-000000000202"

    first = client.post(
        f"/api/v1/pilot/plans/{plan_id}/users",
        headers=headers,
        json={"actor_id": actor_a, "role_label": "pilot-ops"},
    )
    assert first.status_code == 201, first.text
    first_id = first.json()["id"]

    second = client.post(
        f"/api/v1/pilot/plans/{plan_id}/users",
        headers=headers,
        json={"actor_id": actor_b, "role_label": "pilot-qa"},
    )
    assert second.status_code == 201, second.text
    second_id = second.json()["id"]

    approve_first = client.post(
        f"/api/v1/pilot/plans/{plan_id}/users/{first_id}/approve", headers=headers
    )
    assert approve_first.status_code == 200, approve_first.text
    assert approve_first.json()["approved_production_use"] is True

    gate_partial = client.get(
        f"/api/v1/pilot/pilot-approval-gate?plan_id={plan_id}", headers=headers
    )
    assert gate_partial.status_code == 200, gate_partial.text
    body_partial = gate_partial.json()
    assert body_partial["approved_count"] == 1
    assert body_partial["pending_count"] == 1
    assert body_partial["gate_passed"] is False

    approve_second = client.post(
        f"/api/v1/pilot/plans/{plan_id}/users/{second_id}/approve", headers=headers
    )
    assert approve_second.status_code == 200, approve_second.text

    gate_ok = client.get(
        f"/api/v1/pilot/pilot-approval-gate?plan_id={plan_id}", headers=headers
    )
    assert gate_ok.status_code == 200, gate_ok.text
    body_ok = gate_ok.json()
    assert body_ok["approved_count"] == 2
    assert body_ok["pending_count"] == 0
    assert body_ok["gate_passed"] is True


def test_ac003_readiness_gate_and_agent_cannot_sign(client: TestClient) -> None:
    headers = _headers("1")
    agent = _headers("1", actor_kind="agent")
    plan_id = _create_plan(client, headers, code="PILOT-SIGNOFF")

    listed = client.get(f"/api/v1/pilot/signoffs?plan_id={plan_id}", headers=headers)
    assert listed.status_code == 200, listed.text
    signoffs = listed.json()["items"]
    assert {item["function_code"] for item in signoffs} == {
        "product",
        "security",
        "operations",
        "qa",
    }
    by_function = {item["function_code"]: item["id"] for item in signoffs}

    agent_sign = client.post(
        f"/api/v1/pilot/signoffs/{by_function['product']}/sign",
        headers=agent,
        json={"evidence": "agent must not sign"},
    )
    assert agent_sign.status_code == 409, agent_sign.text

    for function_code in ("product", "security", "operations"):
        signed = client.post(
            f"/api/v1/pilot/signoffs/{by_function[function_code]}/sign",
            headers=headers,
            json={"evidence": f"{function_code} human sign-off"},
        )
        assert signed.status_code == 200, signed.text
        assert signed.json()["status"] == "signed"

    gate_partial = client.get(
        f"/api/v1/pilot/readiness-gate?plan_id={plan_id}", headers=headers
    )
    assert gate_partial.status_code == 200, gate_partial.text
    assert gate_partial.json()["gate_passed"] is False

    fourth = client.post(
        f"/api/v1/pilot/signoffs/{by_function['qa']}/sign",
        headers=headers,
        json={"evidence": "qa human sign-off"},
    )
    assert fourth.status_code == 200, fourth.text
    assert fourth.json()["status"] == "signed"

    gate_ok = client.get(f"/api/v1/pilot/readiness-gate?plan_id={plan_id}", headers=headers)
    assert gate_ok.status_code == 200, gate_ok.text
    assert gate_ok.json()["gate_passed"] is True


def test_production_deploy_blocked_without_gates_or_evidence(client: TestClient) -> None:
    headers = _headers("1")
    other = _headers("2")
    plan_id = _create_plan(client, headers, code="PILOT-DEPLOY")

    blocked = client.post(
        "/api/v1/pilot/deployments",
        headers=headers,
        json={"plan_id": plan_id, "human_approval_evidence": "ticket-1"},
    )
    assert blocked.status_code == 409, blocked.text

    empty_evidence = client.post(
        "/api/v1/pilot/deployments",
        headers=headers,
        json={"plan_id": plan_id, "human_approval_evidence": "   "},
    )
    assert empty_evidence.status_code == 409, empty_evidence.text

    other_list = client.get("/api/v1/pilot/plans", headers=other)
    assert other_list.status_code == 200, other_list.text
    assert other_list.json()["items"] == []

    cross_plan = client.get(f"/api/v1/pilot/plans/{plan_id}", headers=other)
    assert cross_plan.status_code == 404, cross_plan.text

    recorded = client.post(
        f"/api/v1/pilot/plans/{plan_id}/acceptance-tests",
        headers=headers,
        json={
            "code": "AT-OK",
            "title": "Critical path",
            "severity": "critical",
            "result": "passed",
        },
    )
    assert recorded.status_code == 201, recorded.text

    actor_a = "00000000-0000-4000-8000-000000000301"
    user = client.post(
        f"/api/v1/pilot/plans/{plan_id}/users",
        headers=headers,
        json={"actor_id": actor_a, "role_label": "pilot"},
    )
    assert user.status_code == 201, user.text
    approved = client.post(
        f"/api/v1/pilot/plans/{plan_id}/users/{user.json()['id']}/approve",
        headers=headers,
    )
    assert approved.status_code == 200, approved.text

    signoffs = client.get(f"/api/v1/pilot/signoffs?plan_id={plan_id}", headers=headers)
    assert signoffs.status_code == 200, signoffs.text
    for item in signoffs.json()["items"]:
        signed = client.post(
            f"/api/v1/pilot/signoffs/{item['id']}/sign",
            headers=headers,
            json={"evidence": f"{item['function_code']} ready"},
        )
        assert signed.status_code == 200, signed.text

    still_empty = client.post(
        "/api/v1/pilot/deployments",
        headers=headers,
        json={"plan_id": plan_id, "human_approval_evidence": ""},
    )
    assert still_empty.status_code == 409, still_empty.text

    recorded_deploy = client.post(
        "/api/v1/pilot/deployments",
        headers=headers,
        json={"plan_id": plan_id, "human_approval_evidence": "CAB-630 human evidence"},
    )
    assert recorded_deploy.status_code == 201, recorded_deploy.text
    assert recorded_deploy.json()["status"] == "recorded"
    assert recorded_deploy.json()["environment"] == "production"
    deployment_id = recorded_deploy.json()["id"]

    rollback = client.post(
        f"/api/v1/pilot/deployments/{deployment_id}/rollback",
        headers=headers,
        json={"reason": "recorded rollback reason only"},
    )
    assert rollback.status_code == 200, rollback.text
    assert rollback.json()["status"] == "recorded"
