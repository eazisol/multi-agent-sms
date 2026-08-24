"""API/integration tests for MOD-350 orchestrator registry."""

from __future__ import annotations

from collections.abc import Generator
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
from masms_api.modules.followups import models as _flu  # noqa: F401
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.orchestrator import models as _orf  # noqa: F401
from masms_api.modules.orchestrator.temporal_adapter import TemporalAdapter
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


def _headers() -> dict[str, str]:
    return {
        "X-Organization-Id": "00000000-0000-4000-8000-000000000001",
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": "human",
        "X-Correlation-Id": str(uuid4()),
    }


class CompletingTemporalAdapter(TemporalAdapter):
    def wait_for_workflow_result(
        self,
        *,
        workflow_id: str,
        run_id: str | None = None,
        timeout_seconds: float = 5.0,
    ) -> dict[str, object]:
        _ = workflow_id, run_id, timeout_seconds
        return {"status": "completed"}


class EventuallyCompletingTemporalAdapter(TemporalAdapter):
    def __init__(self) -> None:
        self.result_checks = 0

    def wait_for_workflow_result(
        self,
        *,
        workflow_id: str,
        run_id: str | None = None,
        timeout_seconds: float = 5.0,
    ) -> dict[str, object] | None:
        _ = workflow_id, run_id, timeout_seconds
        self.result_checks += 1
        if self.result_checks == 1:
            return None
        return {"status": "completed"}


def test_orchestrator_happy_path_and_unknown_code(client: TestClient) -> None:
    headers = _headers()

    defs = client.get("/api/v1/orchestrator/definitions", headers=headers)
    assert defs.status_code == 200, defs.text
    assert len(defs.json()) == 12
    codes = {row["code"] for row in defs.json()}
    assert "query_intake" in codes
    assert "followup_escalation" in codes

    version = client.post(
        "/api/v1/orchestrator/definitions/query_intake/versions",
        headers=headers,
        json={
            "definition_json": {"steps": ["intake", "classify"]},
            "temporal_workflow_type": "masms.query_intake",
        },
    )
    assert version.status_code == 201, version.text
    version_id = version.json()["id"]
    assert version.json()["status"] == "draft"
    assert version.json()["version_number"] == 1

    activated = client.post(
        f"/api/v1/orchestrator/versions/{version_id}/activate",
        headers=headers,
    )
    assert activated.status_code == 200, activated.text
    assert activated.json()["status"] == "active"

    related_id = str(uuid4())
    started = client.post(
        "/api/v1/orchestrator/instances",
        headers=headers,
        json={
            "workflow_code": "query_intake",
            "related_entity_type": "crm_query",
            "related_entity_id": related_id,
            "input_json": {"source": "test"},
        },
    )
    assert started.status_code == 201, started.text
    instance = started.json()
    assert instance["status"] == "running"
    assert instance["temporal_run_id"]
    assert instance["temporal_run_id"].startswith("stub-")
    assert instance["temporal_workflow_id"]
    instance_id = instance["id"]

    unknown = client.post(
        "/api/v1/orchestrator/instances",
        headers=headers,
        json={
            "workflow_code": "not_a_real_workflow",
            "related_entity_type": "crm_query",
            "related_entity_id": related_id,
        },
    )
    assert unknown.status_code == 422, unknown.text

    signal_body = {
        "signal_name": "client_replied",
        "payload_json": {"ok": True},
        "idempotency_key": "sig-1",
    }
    first = client.post(
        f"/api/v1/orchestrator/instances/{instance_id}/signals",
        headers=headers,
        json=signal_body,
    )
    assert first.status_code == 201, first.text
    assert first.json()["status"] == "applied"
    signal_id = first.json()["id"]

    duplicate = client.post(
        f"/api/v1/orchestrator/instances/{instance_id}/signals",
        headers=headers,
        json=signal_body,
    )
    assert duplicate.status_code == 201, duplicate.text
    assert duplicate.json()["id"] == signal_id
    assert duplicate.json()["status"] == "duplicate"

    signals = client.get(
        f"/api/v1/orchestrator/instances/{instance_id}/signals",
        headers=headers,
    )
    assert signals.status_code == 200
    assert len(signals.json()) == 1

    failure = client.post(
        f"/api/v1/orchestrator/instances/{instance_id}/failures",
        headers=headers,
        json={
            "failure_code": "ACTIVITY_TIMEOUT",
            "message": "Classify timed out",
            "retryable": True,
            "attempt": 1,
        },
    )
    assert failure.status_code == 201, failure.text

    after_fail = client.get(
        f"/api/v1/orchestrator/instances/{instance_id}",
        headers=headers,
    )
    assert after_fail.status_code == 200
    assert after_fail.json()["status"] == "failed"
    failed_version = after_fail.json()["version"]

    intervention = client.post(
        f"/api/v1/orchestrator/instances/{instance_id}/interventions",
        headers=headers,
        json={
            "reason": "Abandon after timeout",
            "action_code": "cancel",
            "notes": "Ops cancel",
        },
    )
    assert intervention.status_code == 201, intervention.text
    intervention_id = intervention.json()["id"]

    resolved = client.post(
        f"/api/v1/orchestrator/interventions/{intervention_id}/resolve",
        headers=headers,
        json={"expected_version": failed_version},
    )
    assert resolved.status_code == 200, resolved.text
    assert resolved.json()["status"] == "resolved"

    closed = client.get(
        f"/api/v1/orchestrator/instances/{instance_id}",
        headers=headers,
    )
    assert closed.status_code == 200
    assert closed.json()["status"] == "cancelled"
    assert closed.json()["closed_at"]

    page = client.get(
        "/api/v1/orchestrator/instances?status=cancelled&limit=10&offset=0",
        headers=headers,
    )
    assert page.status_code == 200, page.text
    body = page.json()
    assert "items" in body and "page" in body
    assert body["page"]["total"] >= 1
    assert body["page"]["limit"] == 10
    assert body["page"]["offset"] == 0
    assert any(item["id"] == instance_id for item in body["items"])

    failures = client.get(
        f"/api/v1/orchestrator/instances/{instance_id}/failures",
        headers=headers,
    )
    assert len(failures.json()) == 1

    interventions = client.get(
        f"/api/v1/orchestrator/instances/{instance_id}/interventions",
        headers=headers,
    )
    assert len(interventions.json()) == 1


def test_terminal_signal_reconciles_confirmed_temporal_completion(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        "masms_api.modules.orchestrator.service.get_temporal_adapter",
        CompletingTemporalAdapter,
    )
    headers = _headers()
    version = client.post(
        "/api/v1/orchestrator/definitions/query_intake/versions",
        headers=headers,
        json={"temporal_workflow_type": "masms.query_intake"},
    )
    assert version.status_code == 201, version.text
    activated = client.post(
        f"/api/v1/orchestrator/versions/{version.json()['id']}/activate",
        headers=headers,
    )
    assert activated.status_code == 200, activated.text
    started = client.post(
        "/api/v1/orchestrator/instances",
        headers=headers,
        json={
            "workflow_code": "query_intake",
            "related_entity_type": "crm_query",
            "related_entity_id": str(uuid4()),
        },
    )
    assert started.status_code == 201, started.text

    signal = client.post(
        f"/api/v1/orchestrator/instances/{started.json()['id']}/signals",
        headers=headers,
        json={
            "signal_name": "approved",
            "idempotency_key": "terminal-signal-1",
        },
    )
    assert signal.status_code == 201, signal.text

    completed = client.get(
        f"/api/v1/orchestrator/instances/{started.json()['id']}",
        headers=headers,
    )
    assert completed.status_code == 200, completed.text
    assert completed.json()["status"] == "completed"
    assert completed.json()["closed_at"] is not None


def test_duplicate_terminal_signal_reconciles_a_later_completion(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    temporal = EventuallyCompletingTemporalAdapter()
    monkeypatch.setattr(
        "masms_api.modules.orchestrator.service.get_temporal_adapter",
        lambda: temporal,
    )
    headers = _headers()
    version = client.post(
        "/api/v1/orchestrator/definitions/query_intake/versions",
        headers=headers,
        json={"temporal_workflow_type": "masms.query_intake"},
    )
    assert version.status_code == 201, version.text
    assert (
        client.post(
            f"/api/v1/orchestrator/versions/{version.json()['id']}/activate",
            headers=headers,
        ).status_code
        == 200
    )
    started = client.post(
        "/api/v1/orchestrator/instances",
        headers=headers,
        json={
            "workflow_code": "query_intake",
            "related_entity_type": "crm_query",
            "related_entity_id": str(uuid4()),
        },
    )
    assert started.status_code == 201, started.text
    signal_url = f"/api/v1/orchestrator/instances/{started.json()['id']}/signals"
    payload = {"signal_name": "approved", "idempotency_key": "terminal-retry-1"}
    assert client.post(signal_url, headers=headers, json=payload).status_code == 201

    duplicate = client.post(signal_url, headers=headers, json=payload)
    assert duplicate.status_code == 201, duplicate.text
    assert duplicate.json()["status"] == "duplicate"
    completed = client.get(
        f"/api/v1/orchestrator/instances/{started.json()['id']}", headers=headers
    )
    assert completed.status_code == 200, completed.text
    assert completed.json()["status"] == "completed"
