"""API/integration tests for MOD-330 approval gates."""

from __future__ import annotations

from collections.abc import Generator
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from masms_api.db import Base, get_db
from masms_api.kernel import outbox as _outbox  # noqa: F401
from masms_api.main import create_app
from masms_api.modules.access import models as _access  # noqa: F401
from masms_api.modules.approvalgates import models as _apr  # noqa: F401
from masms_api.modules.assignments import models as _asg  # noqa: F401
from masms_api.modules.auth import models as _auth  # noqa: F401
from masms_api.modules.capacity import models as _capacity  # noqa: F401
from masms_api.modules.clients import models as _clients  # noqa: F401
from masms_api.modules.comms import models as _comms  # noqa: F401
from masms_api.modules.configadmin import models as _cfg  # noqa: F401
from masms_api.modules.documents import models as _docs  # noqa: F401
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.projects import models as _projects  # noqa: F401
from masms_api.modules.queries import models as _queries  # noqa: F401
from masms_api.modules.requirements import models as _reqs  # noqa: F401
from masms_api.modules.roadmap import models as _roadmap  # noqa: F401
from masms_api.modules.statusengine import models as _wfe  # noqa: F401
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


def _headers(*, actor_id: str | None = None, actor_kind: str = "human") -> dict[str, str]:
    return {
        "X-Organization-Id": "00000000-0000-4000-8000-000000000001",
        "X-Actor-Id": actor_id or "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": actor_kind,
        "X-Correlation-Id": str(uuid4()),
    }


def test_exact_version_gate_and_agent_blocked(client: TestClient) -> None:
    headers = _headers()
    entity_id = str(uuid4())
    agent_id = "00000000-0000-4000-8000-000000000201"

    blocked = client.post(
        "/api/v1/approvals/gate-check",
        headers=headers,
        json={
            "action_code": "srs.baseline",
            "target_entity_type": "srs_baseline",
            "target_entity_id": entity_id,
            "target_version": 1,
        },
    )
    assert blocked.status_code == 200
    assert blocked.json()["allowed"] is False

    created = client.post(
        "/api/v1/approvals",
        headers=_headers(actor_kind="agent", actor_id=agent_id),
        json={
            "action_code": "srs.baseline",
            "title": "Approve SRS v1",
            "target_entity_type": "srs_baseline",
            "target_entity_id": entity_id,
            "target_version": 1,
            "recommendation_source_actor_id": agent_id,
            "steps": [{"role_code": "PM", "order": 1}],
        },
    )
    assert created.status_code == 201, created.text
    approval_id = created.json()["id"]
    assert created.json()["target_version"] == 1

    agent_decide = client.post(
        f"/api/v1/approvals/{approval_id}/decisions",
        headers=_headers(actor_kind="agent", actor_id=agent_id),
        json={"decision": "approve"},
    )
    assert agent_decide.status_code == 403, agent_decide.text

    # Human who is the recommendation source (same agent id reused as human id edge) —
    # use the agent recommendation source with a human actor equal to it.
    self_approve = client.post(
        f"/api/v1/approvals/{approval_id}/decisions",
        headers=_headers(actor_id=agent_id, actor_kind="human"),
        json={"decision": "approve"},
    )
    assert self_approve.status_code == 403, self_approve.text

    evidence = client.post(
        f"/api/v1/approvals/{approval_id}/evidence",
        headers=headers,
        json={"evidence_ref": "doc://srs-v1-review", "evidence_type": "document"},
    )
    assert evidence.status_code == 201, evidence.text

    approved = client.post(
        f"/api/v1/approvals/{approval_id}/decisions",
        headers=headers,
        json={"decision": "approve"},
    )
    assert approved.status_code == 200, approved.text

    state = client.get(f"/api/v1/approvals/{approval_id}", headers=headers)
    assert state.status_code == 200
    assert state.json()["status"] == "approved"

    ok = client.post(
        "/api/v1/approvals/gate-check",
        headers=headers,
        json={
            "action_code": "srs.baseline",
            "target_entity_type": "srs_baseline",
            "target_entity_id": entity_id,
            "target_version": 1,
        },
    )
    assert ok.status_code == 200
    assert ok.json()["allowed"] is True

    wrong_version = client.post(
        "/api/v1/approvals/gate-check",
        headers=headers,
        json={
            "action_code": "srs.baseline",
            "target_entity_type": "srs_baseline",
            "target_entity_id": entity_id,
            "target_version": 2,
        },
    )
    assert wrong_version.status_code == 200
    assert wrong_version.json()["allowed"] is False

    asserted = client.post(
        "/api/v1/approvals/gate-assert",
        headers=headers,
        json={
            "action_code": "srs.baseline",
            "target_entity_type": "srs_baseline",
            "target_entity_id": entity_id,
            "target_version": 2,
        },
    )
    assert asserted.status_code == 409, asserted.text


def test_reject_reason_delegation_override_supersede(client: TestClient) -> None:
    headers = _headers()
    entity_id = str(uuid4())
    created = client.post(
        "/api/v1/approvals",
        headers=headers,
        json={
            "action_code": "tickets.close",
            "title": "Close ticket",
            "target_entity_type": "ticket",
            "target_entity_id": entity_id,
            "target_version": 3,
            "steps": [{"role_code": "PM"}],
        },
    )
    assert created.status_code == 201, created.text
    approval_id = created.json()["id"]

    no_reason = client.post(
        f"/api/v1/approvals/{approval_id}/decisions",
        headers=headers,
        json={"decision": "reject"},
    )
    assert no_reason.status_code == 422, no_reason.text

    rejected = client.post(
        f"/api/v1/approvals/{approval_id}/decisions",
        headers=headers,
        json={"decision": "reject", "reason": "Incomplete evidence"},
    )
    assert rejected.status_code == 200, rejected.text

    now = datetime.now(UTC)
    delegatee = "00000000-0000-4000-8000-000000000301"
    delegation = client.post(
        "/api/v1/approvals/delegations",
        headers=headers,
        json={
            "to_actor_id": delegatee,
            "action_code": "tickets.close",
            "reason": "On leave coverage",
            "starts_at": now.isoformat(),
            "ends_at": (now + timedelta(days=3)).isoformat(),
        },
    )
    assert delegation.status_code == 201, delegation.text

    override = client.post(
        "/api/v1/approvals/overrides",
        headers=headers,
        json={
            "action_code": "tickets.close",
            "target_entity_type": "ticket",
            "target_entity_id": entity_id,
            "target_version": 3,
            "reason": "Emergency client commitment",
            "authority_used": "incident-commander",
            "approval_id": approval_id,
        },
    )
    assert override.status_code == 201, override.text

    gate = client.post(
        "/api/v1/approvals/gate-check",
        headers=headers,
        json={
            "action_code": "tickets.close",
            "target_entity_type": "ticket",
            "target_entity_id": entity_id,
            "target_version": 3,
        },
    )
    assert gate.status_code == 200
    assert gate.json()["allowed"] is True
    assert gate.json()["approval_status"] == "override"

    # New request then supersede on material version change path
    created2 = client.post(
        "/api/v1/approvals",
        headers=headers,
        json={
            "action_code": "tickets.close",
            "title": "Close ticket v4 pending",
            "target_entity_type": "ticket",
            "target_entity_id": entity_id,
            "target_version": 4,
            "steps": [{"role_code": "PM"}],
        },
    )
    assert created2.status_code == 201
    superseded = client.post(
        f"/api/v1/approvals/{created2.json()['id']}/supersede",
        headers=headers,
        params={"reason": "Target edited after submit"},
    )
    assert superseded.status_code == 200
    assert superseded.json()["status"] == "superseded"
