"""API/integration tests for MOD-240 projects and SRS."""

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
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.projects import models as _projects  # noqa: F401
from masms_api.modules.queries import models as _queries  # noqa: F401
from masms_api.modules.requirements import models as _requirements  # noqa: F401
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


def test_project_requirement_ac_and_srs_approval(client: TestClient) -> None:
    headers = _headers()

    project = client.post(
        "/api/v1/projects",
        headers=headers,
        json={"code": "ACME-PORTAL", "title": "Acme Customer Portal"},
    )
    assert project.status_code == 201, project.text
    project_id = project.json()["id"]

    requirement = client.post(
        "/api/v1/projects/requirements",
        headers=headers,
        json={
            "project_id": project_id,
            "requirement_code": "REQ-001",
            "title": "User login",
        },
    )
    assert requirement.status_code == 201, requirement.text
    requirement_id = requirement.json()["id"]
    assert requirement.json()["requirement_code"] == "REQ-001"

    version = client.post(
        "/api/v1/projects/requirement-versions",
        headers=headers,
        json={
            "requirement_id": requirement_id,
            "statement": "Users must authenticate with MFA.",
            "priority": "must_have",
        },
    )
    assert version.status_code == 201, version.text
    version_id = version.json()["id"]

    blocked = client.post(
        f"/api/v1/projects/requirement-versions/{version_id}/approve",
        headers=headers,
    )
    assert blocked.status_code == 422

    ac = client.post(
        "/api/v1/projects/acceptance-criteria",
        headers=headers,
        json={
            "requirement_version_id": version_id,
            "criterion_code": "AC-1",
            "text": "Given valid credentials, MFA challenge succeeds",
        },
    )
    assert ac.status_code == 201, ac.text

    rule = client.post(
        "/api/v1/projects/business-rules",
        headers=headers,
        json={
            "requirement_version_id": version_id,
            "rule_code": "BR-1",
            "text": "Passwords must rotate every 90 days",
        },
    )
    assert rule.status_code == 201

    assumption = client.post(
        "/api/v1/projects/assumptions",
        headers=headers,
        json={
            "project_id": project_id,
            "assumption_code": "ASM-1",
            "text": "Auth0 tenant already provisioned",
            "requirement_version_id": version_id,
        },
    )
    assert assumption.status_code == 201

    constraint = client.post(
        "/api/v1/projects/constraints",
        headers=headers,
        json={
            "project_id": project_id,
            "constraint_code": "CON-1",
            "text": "Must remain SOC2 compliant",
        },
    )
    assert constraint.status_code == 201

    approved_req = client.post(
        f"/api/v1/projects/requirement-versions/{version_id}/approve",
        headers=headers,
    )
    assert approved_req.status_code == 200, approved_req.text
    assert approved_req.json()["status"] == "approved"
    assert approved_req.json()["approved_by_actor_id"] is not None

    immutable = client.post(
        "/api/v1/projects/acceptance-criteria",
        headers=headers,
        json={
            "requirement_version_id": version_id,
            "criterion_code": "AC-2",
            "text": "Should not work after approve",
        },
    )
    assert immutable.status_code == 403

    v2 = client.post(
        "/api/v1/projects/requirement-versions",
        headers=headers,
        json={
            "requirement_id": requirement_id,
            "statement": "Users must authenticate with MFA and device trust.",
            "priority": "must_have",
            "change_reason": "CR-12 add device trust",
        },
    )
    assert v2.status_code == 201
    assert v2.json()["version_number"] == 2

    srs = client.post(
        "/api/v1/projects/srs-baselines",
        headers=headers,
        json={
            "project_id": project_id,
            "title": "SRS v1",
            "summary": "Initial baseline",
            "requirement_version_ids": [version_id],
        },
    )
    assert srs.status_code == 201, srs.text
    assert srs.json()["status"] == "draft"
    srs_id = srs.json()["id"]

    approved_srs = client.post(
        f"/api/v1/projects/srs-baselines/{srs_id}/approve",
        headers=headers,
    )
    assert approved_srs.status_code == 200, approved_srs.text
    assert approved_srs.json()["status"] == "approved"
    assert approved_srs.json()["approved_by_actor_id"] is not None

    listed = client.get(f"/api/v1/projects/{project_id}/requirements", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert listed.json()[0]["status"] == "approved"

    projects = client.get("/api/v1/projects", headers=headers)
    assert projects.status_code == 200, projects.text
    assert any(row["id"] == project_id for row in projects.json()["items"])

    filtered = client.get("/api/v1/projects", headers=headers, params={"status": "active"})
    assert filtered.status_code == 200
    assert all(row["status"] == "active" for row in filtered.json()["items"])
    assert any(row["id"] == project_id for row in filtered.json()["items"])

    searched = client.get("/api/v1/projects", headers=headers, params={"q": "ACME"})
    assert searched.status_code == 200
    assert any(row["id"] == project_id for row in searched.json()["items"])

    got = client.get(f"/api/v1/projects/{project_id}", headers=headers)
    assert got.status_code == 200
    assert got.json()["id"] == project_id
    assert got.json()["code"] == "ACME-PORTAL"
