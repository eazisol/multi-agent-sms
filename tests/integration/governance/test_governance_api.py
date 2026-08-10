"""API/integration smoke tests for MOD-000 governance (SQLite)."""

from __future__ import annotations

from collections.abc import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from masms_api.db import Base, get_db
from masms_api.main import create_app
from masms_api.modules.governance import models as _models  # noqa: F401
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


ORG = "00000000-0000-4000-8000-000000000001"
HUMAN = "00000000-0000-4000-8000-000000000101"
AGENT = "00000000-0000-4000-8000-000000000201"


def _headers(*, actor: str = HUMAN, kind: str = "human", org: str = ORG) -> dict[str, str]:
    return {
        "X-Organization-Id": org,
        "X-Actor-Id": actor,
        "X-Actor-Kind": kind,
        "X-Correlation-Id": str(uuid4()),
    }


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_baseline_lifecycle_and_agent_blocked_approval(client: TestClient) -> None:
    create = client.post(
        "/api/v1/governance/baselines",
        headers=_headers(),
        json={
            "baseline_key": "BL-SRS-001",
            "title": "MVP SRS",
            "artifact_path": "Docs/Multi_Agent_Software_House_Management_System_MVP_SRS_v1.0.md",
            "document_version": "v1.0",
            "classification": "internal",
        },
    )
    assert create.status_code == 201, create.text
    baseline = create.json()
    baseline_id = baseline["id"]
    version = baseline["version"]

    for target in ("submitted", "under_review"):
        transition = client.post(
            f"/api/v1/governance/baselines/{baseline_id}/transitions",
            headers=_headers(),
            json={"target_status": target, "expected_version": version},
        )
        assert transition.status_code == 200, transition.text
        version = transition.json()["version"]

    agent_approve = client.post(
        f"/api/v1/governance/baselines/{baseline_id}/transitions",
        headers=_headers(actor=AGENT, kind="agent"),
        json={"target_status": "approved", "expected_version": version},
    )
    assert agent_approve.status_code == 403

    human_approve = client.post(
        f"/api/v1/governance/baselines/{baseline_id}/transitions",
        headers=_headers(),
        json={"target_status": "approved", "expected_version": version},
    )
    assert human_approve.status_code == 200
    assert human_approve.json()["approval_status"] == "approved"

    forbidden_update = client.patch(
        f"/api/v1/governance/baselines/{baseline_id}",
        headers=_headers(),
        json={"title": "Attempt illegal edit", "expected_version": human_approve.json()["version"]},
    )
    assert forbidden_update.status_code == 409


def test_requirement_mapping_and_change_request_idempotency(client: TestClient) -> None:
    mapping = client.post(
        "/api/v1/governance/requirement-mappings",
        headers=_headers(),
        json={
            "requirement_id": "MVP-NFR-010",
            "requirement_title": "Configurability",
            "module_id": "MOD-000",
            "mapping_role": "primary",
        },
    )
    assert mapping.status_code == 201
    mapping_id = mapping.json()["id"]

    payload = {
        "change_request_key": "GCR-0001",
        "title": "Clarify mapping notes",
        "summary": "Add supporting module note",
        "rationale": "Traceability clarity",
        "impact": {"scope": "documentation"},
        "target_entity_type": "requirement_mapping",
        "target_entity_id": mapping_id,
        "target_version": 1,
        "proposed_version": 2,
        "idempotency_key": "idem-gcr-0001",
    }
    first = client.post("/api/v1/governance/change-requests", headers=_headers(), json=payload)
    second = client.post("/api/v1/governance/change-requests", headers=_headers(), json=payload)
    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] == second.json()["id"]


def test_tenant_isolation_on_list(client: TestClient) -> None:
    client.post(
        "/api/v1/governance/baselines",
        headers=_headers(org=ORG),
        json={
            "baseline_key": "BL-A",
            "title": "Org A baseline",
            "artifact_path": "docs/a.md",
            "document_version": "1",
        },
    )
    other_org = "00000000-0000-4000-8000-000000000002"
    listed = client.get("/api/v1/governance/baselines", headers=_headers(org=other_org))
    assert listed.status_code == 200
    assert listed.json() == []
