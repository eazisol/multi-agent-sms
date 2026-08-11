"""API/integration tests for MOD-260 roadmap."""

from __future__ import annotations

from collections.abc import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from masms_api.db import Base, get_db
from masms_api.kernel import outbox as _outbox  # noqa: F401
from masms_api.main import create_app
from masms_api.modules.access import models as _access  # noqa: F401
from masms_api.modules.auth import models as _auth  # noqa: F401
from masms_api.modules.capacity import models as _capacity  # noqa: F401
from masms_api.modules.clients import models as _clients  # noqa: F401
from masms_api.modules.comms import models as _comms  # noqa: F401
from masms_api.modules.configadmin import models as _cfg  # noqa: F401
from masms_api.modules.documents import models as _documents  # noqa: F401
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.projects import models as _projects  # noqa: F401
from masms_api.modules.queries import models as _queries  # noqa: F401
from masms_api.modules.requirements import models as _requirements  # noqa: F401
from masms_api.modules.roadmap import models as _roadmap  # noqa: F401
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


def _approved_requirement(client: TestClient, headers: dict[str, str], project_id: str) -> str:
    req = client.post(
        "/api/v1/projects/requirements",
        headers=headers,
        json={
            "project_id": project_id,
            "requirement_code": "REQ-100",
            "title": "Auth",
        },
    )
    assert req.status_code == 201
    version = client.post(
        "/api/v1/projects/requirement-versions",
        headers=headers,
        json={
            "requirement_id": req.json()["id"],
            "statement": "Users can log in",
            "priority": "must_have",
        },
    )
    assert version.status_code == 201
    ac = client.post(
        "/api/v1/projects/acceptance-criteria",
        headers=headers,
        json={
            "requirement_version_id": version.json()["id"],
            "criterion_code": "AC-1",
            "text": "Login succeeds",
        },
    )
    assert ac.status_code == 201
    approved = client.post(
        f"/api/v1/projects/requirement-versions/{version.json()['id']}/approve",
        headers=headers,
    )
    assert approved.status_code == 200
    return req.json()["id"]


def test_phases_milestones_mapping_independent_completion(client: TestClient) -> None:
    headers = _headers()
    owner = "00000000-0000-4000-8000-000000000101"

    project = client.post(
        "/api/v1/projects",
        headers=headers,
        json={"code": "PORTAL", "title": "Portal"},
    )
    assert project.status_code == 201
    project_id = project.json()["id"]
    requirement_id = _approved_requirement(client, headers, project_id)

    discover = client.post(
        "/api/v1/roadmap/phases",
        headers=headers,
        json={
            "project_id": project_id,
            "code": "DISCOVER",
            "title": "Discovery",
            "sequence": 1,
        },
    )
    assert discover.status_code == 201, discover.text
    discover_id = discover.json()["id"]

    build = client.post(
        "/api/v1/roadmap/phases",
        headers=headers,
        json={
            "project_id": project_id,
            "code": "BUILD",
            "title": "Build",
            "sequence": 2,
        },
    )
    assert build.status_code == 201
    build_id = build.json()["id"]

    # BUILD depends on DISCOVER, but completing DISCOVER does not need BUILD done
    dep = client.post(
        "/api/v1/roadmap/phase-dependencies",
        headers=headers,
        json={
            "project_id": project_id,
            "predecessor_phase_id": discover_id,
            "successor_phase_id": build_id,
        },
    )
    assert dep.status_code == 201

    ms = client.post(
        "/api/v1/roadmap/milestones",
        headers=headers,
        json={
            "phase_id": discover_id,
            "code": "MS-1",
            "title": "Kickoff",
            "owner_actor_id": owner,
            "target_date": "2026-09-01",
            "requires_approval": True,
        },
    )
    assert ms.status_code == 201, ms.text
    ms_id = ms.json()["id"]
    assert ms.json()["owner_actor_id"] == owner
    assert ms.json()["target_date"] == "2026-09-01"
    assert ms.json()["status"] == "planned"

    blocked_ms = client.post(
        f"/api/v1/roadmap/milestones/{ms_id}/complete", headers=headers
    )
    assert blocked_ms.status_code == 403
    approved_ms = client.post(
        f"/api/v1/roadmap/milestones/{ms_id}/approve", headers=headers
    )
    assert approved_ms.status_code == 200
    assert approved_ms.json()["approved_by_actor_id"] is not None
    done_ms = client.post(
        f"/api/v1/roadmap/milestones/{ms_id}/complete", headers=headers
    )
    assert done_ms.status_code == 200
    assert done_ms.json()["status"] == "completed"

    deliverable = client.post(
        "/api/v1/roadmap/deliverables",
        headers=headers,
        json={
            "phase_id": discover_id,
            "code": "DEL-1",
            "title": "Workshop notes",
            "milestone_id": ms_id,
        },
    )
    assert deliverable.status_code == 201

    mapping = client.post(
        "/api/v1/roadmap/requirement-maps",
        headers=headers,
        json={
            "project_id": project_id,
            "requirement_id": requirement_id,
            "phase_id": discover_id,
        },
    )
    assert mapping.status_code == 201, mapping.text

    baseline = client.post(
        "/api/v1/roadmap/baselines",
        headers=headers,
        json={"project_id": project_id, "title": "Plan v1"},
    )
    assert baseline.status_code == 201
    approved_baseline = client.post(
        f"/api/v1/roadmap/baselines/{baseline.json()['id']}/approve",
        headers=headers,
    )
    assert approved_baseline.status_code == 200
    assert approved_baseline.json()["status"] == "approved"

    forecast = client.post(
        "/api/v1/roadmap/forecasts",
        headers=headers,
        json={
            "project_id": project_id,
            "phase_id": build_id,
            "forecast_type": "completion",
            "predicted_date": "2026-12-01",
            "confidence": "0.7000",
        },
    )
    assert forecast.status_code == 201

    # Independent completion: DISCOVER completes while BUILD still planned
    blocked_build = client.post(
        f"/api/v1/roadmap/phases/{build_id}/complete", headers=headers
    )
    assert blocked_build.status_code == 403

    complete_discover = client.post(
        f"/api/v1/roadmap/phases/{discover_id}/complete", headers=headers
    )
    assert complete_discover.status_code == 200, complete_discover.text
    assert complete_discover.json()["status"] == "completed"

    complete_build = client.post(
        f"/api/v1/roadmap/phases/{build_id}/complete", headers=headers
    )
    assert complete_build.status_code == 200
    assert complete_build.json()["status"] == "completed"

    phases = client.get(
        f"/api/v1/roadmap/projects/{project_id}/phases", headers=headers
    )
    assert phases.status_code == 200
    assert len(phases.json()) == 2

    milestones = client.get(
        f"/api/v1/roadmap/projects/{project_id}/milestones", headers=headers
    )
    assert milestones.status_code == 200, milestones.text
    assert any(row["id"] == ms_id for row in milestones.json())

    by_phase = client.get(
        f"/api/v1/roadmap/projects/{project_id}/milestones",
        headers=headers,
        params={"phase_id": discover_id},
    )
    assert by_phase.status_code == 200
    assert all(row["phase_id"] == discover_id for row in by_phase.json())
    assert any(row["id"] == ms_id for row in by_phase.json())
