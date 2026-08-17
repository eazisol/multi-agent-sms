"""API/integration tests for MOD-360 agent runtime registry."""

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
from masms_api.modules.agents.domain import AGENT_DEPARTMENTS, AGENT_TITLES, ALLOWED_CODES
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


AGENT_ENTITY_TYPES: dict[str, str] = {
    "query_intake_agent": "crm_query",
    "requirements_clarifier": "req_requirement",
    "roadmap_planner": "rmp_roadmap_item",
    "ticket_triage_agent": "wfe_ticket",
    "qa_review_assistant": "qa_review",
    "status_report_drafter": "prj_project",
}


def test_agent_runtime_happy_path_review_and_unknown_code(client: TestClient) -> None:
    headers = _headers()

    defs = client.get("/api/v1/agent-runtime/definitions", headers=headers)
    assert defs.status_code == 200, defs.text
    assert len(defs.json()) == 6
    codes = {row["code"] for row in defs.json()}
    assert "query_intake_agent" in codes
    assert "status_report_drafter" in codes

    entity_id = str(uuid4())
    high = client.post(
        "/api/v1/agent-runtime/runs",
        headers=headers,
        json={
            "agent_code": "query_intake_agent",
            "related_entity_type": "crm_query",
            "related_entity_id": entity_id,
            "input_json": {"note": "high confidence"},
        },
    )
    assert high.status_code == 201, high.text
    high_body = high.json()
    assert high_body["status"] == "completed"
    assert high_body["langgraph_run_id"].startswith("stub-lg-")
    assert high_body["model_name"]
    assert high_body["prompt_version_number"] >= 1
    assert high_body["sources_json"]
    assert high_body["confidence"] is not None and high_body["confidence"] >= 0.6

    low = client.post(
        "/api/v1/agent-runtime/runs",
        headers=headers,
        json={
            "agent_code": "ticket_triage_agent",
            "related_entity_type": "wfe_ticket",
            "related_entity_id": str(uuid4()),
            "input_json": {"force_low_confidence": True},
        },
    )
    assert low.status_code == 201, low.text
    low_body = low.json()
    assert low_body["status"] == "review_required"
    assert low_body["review_required"] is True

    review = client.post(
        f"/api/v1/agent-runtime/runs/{low_body['id']}/reviews",
        headers=headers,
        json={
            "decision": "approved",
            "decision_reason": "Looks good",
            "expected_version": low_body["version"],
        },
    )
    assert review.status_code == 201, review.text
    assert review.json()["status"] == "approved"

    done = client.get(f"/api/v1/agent-runtime/runs/{low_body['id']}", headers=headers)
    assert done.status_code == 200
    assert done.json()["status"] == "completed"

    evaluation = client.post(
        f"/api/v1/agent-runtime/runs/{high_body['id']}/evaluations",
        headers=headers,
        json={"score": 0.9, "rubric_code": "m1_stub", "notes": "ok"},
    )
    assert evaluation.status_code == 201, evaluation.text
    assert evaluation.json()["score"] == 0.9

    listed = client.get("/api/v1/agent-runtime/runs?limit=10&offset=0", headers=headers)
    assert listed.status_code == 200, listed.text
    page = listed.json()
    assert "items" in page and "page" in page
    assert page["page"]["total"] >= 2

    bad = client.post(
        "/api/v1/agent-runtime/runs",
        headers=headers,
        json={
            "agent_code": "not_a_real_agent",
            "related_entity_type": "crm_query",
            "related_entity_id": str(uuid4()),
        },
    )
    assert bad.status_code == 422, bad.text


@pytest.mark.parametrize("agent_code", sorted(ALLOWED_CODES))
def test_every_catalog_agent_starts_and_completes_stub_run(
    client: TestClient, agent_code: str
) -> None:
    headers = _headers()
    entity_type = AGENT_ENTITY_TYPES[agent_code]
    created = client.post(
        "/api/v1/agent-runtime/runs",
        headers=headers,
        json={
            "agent_code": agent_code,
            "related_entity_type": entity_type,
            "related_entity_id": str(uuid4()),
            "input_json": {"note": f"catalog check for {agent_code}"},
        },
    )
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["agent_code"] == agent_code
    assert body["status"] == "completed"
    assert body["review_required"] is False
    assert body["langgraph_run_id"].startswith("stub-lg-")
    assert body["model_name"]
    assert body["prompt_version_number"] >= 1
    assert body["sources_json"]
    assert body["output_json"]["stub"] is True
    assert agent_code in str(body["output_json"]["summary"])
    assert body["confidence"] is not None and body["confidence"] >= 0.6

    fetched = client.get(f"/api/v1/agent-runtime/runs/{body['id']}", headers=headers)
    assert fetched.status_code == 200, fetched.text
    assert fetched.json()["status"] == "completed"

    listed = client.get(
        f"/api/v1/agent-runtime/runs?agent_code={agent_code}&limit=10&offset=0",
        headers=headers,
    )
    assert listed.status_code == 200, listed.text
    codes = {item["agent_code"] for item in listed.json()["items"]}
    assert agent_code in codes


def test_definitions_seed_all_catalog_codes_with_expected_departments(
    client: TestClient,
) -> None:
    headers = _headers()
    defs = client.get("/api/v1/agent-runtime/definitions", headers=headers)
    assert defs.status_code == 200, defs.text
    rows = defs.json()
    assert {row["code"] for row in rows} == set(ALLOWED_CODES)
    assert all(row["status"] == "active" for row in rows)
    by_code = {row["code"]: row for row in rows}

    for code in ALLOWED_CODES:
        assert by_code[code]["title"] == AGENT_TITLES[code]
        assert by_code[code]["department_code"] == AGENT_DEPARTMENTS[code]
