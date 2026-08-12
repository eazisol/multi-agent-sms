"""API/integration tests for MOD-450 insights."""

from __future__ import annotations

import json
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
from masms_api.modules.insights import models as _rp  # noqa: F401
from masms_api.modules.gmail import models as _gm  # noqa: F401
from masms_api.modules.integrations import models as _ig  # noqa: F401
from masms_api.modules.knowledge import models as _kn  # noqa: F401
from masms_api.modules.notifications import models as _ntf  # noqa: F401
from masms_api.modules.orchestrator import models as _orf  # noqa: F401
from masms_api.modules.projects import models as _projects  # noqa: F401
from masms_api.modules.queries import models as _queries  # noqa: F401
from masms_api.modules.releases import models as _rl  # noqa: F401
from masms_api.modules.requirements import models as _reqs  # noqa: F401
from masms_api.modules.roadmap import models as _roadmap  # noqa: F401
from masms_api.modules.securityhardening import models as _sh  # noqa: F401
from masms_api.modules.statusengine import models as _wfe  # noqa: F401
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


def _headers(org_suffix: str = "1") -> dict[str, str]:
    return {
        "X-Organization-Id": f"00000000-0000-4000-8000-00000000000{org_suffix}",
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": "human",
        "X-Correlation-Id": str(uuid4()),
    }


def test_dashboard_reconcile_freshness_and_tenant_isolation(client: TestClient) -> None:
    headers_a = _headers("1")
    headers_b = _headers("2")

    # AC-001: create org-scoped projects then refresh; snapshot counts match
    for code in ("INS-A1", "INS-A2"):
        created = client.post(
            "/api/v1/projects",
            headers=headers_a,
            json={"code": code, "title": f"Insights {code}"},
        )
        assert created.status_code == 201, created.text

    other = client.post(
        "/api/v1/projects",
        headers=headers_b,
        json={"code": "INS-B1", "title": "Other org project"},
    )
    assert other.status_code == 201, other.text

    refreshed = client.post(
        "/api/v1/insights/dashboard/refresh",
        headers=headers_a,
        json={},
    )
    assert refreshed.status_code == 200, refreshed.text
    body = refreshed.json()
    assert body["metrics"]["projects_total"] == 2
    assert body["metrics"]["reconciled"] is True
    assert body["is_fresh"] is True
    assert body["scope_key"] == "org"

    # AC-002: GET latest after refresh is fresh with current timestamps
    got = client.get("/api/v1/insights/dashboard", headers=headers_a)
    assert got.status_code == 200, got.text
    snap = got.json()
    assert snap["is_fresh"] is True
    assert snap["computed_at"]
    assert snap["refreshed_at"]
    assert snap["metrics"]["projects_total"] == 2

    # Org B refresh must not see Org A's projects
    refresh_b = client.post(
        "/api/v1/insights/dashboard/refresh",
        headers=headers_b,
        json={},
    )
    assert refresh_b.status_code == 200, refresh_b.text
    assert refresh_b.json()["metrics"]["projects_total"] == 1

    # AC-003: search and exports are org-scoped
    entity_id = str(uuid4())
    indexed = client.post(
        "/api/v1/insights/search/index",
        headers=headers_a,
        json={
            "entity_type": "project",
            "entity_id": entity_id,
            "title": "SecretOrgAWidget",
            "body_preview": "confidential org A indexed document",
            "classification": "internal",
        },
    )
    assert indexed.status_code == 201, indexed.text

    search_a = client.get(
        "/api/v1/insights/search",
        headers=headers_a,
        params={"q": "SecretOrgAWidget"},
    )
    assert search_a.status_code == 200, search_a.text
    assert search_a.json()["page"]["total"] >= 1
    assert any(i["title"] == "SecretOrgAWidget" for i in search_a.json()["items"])

    search_b = client.get(
        "/api/v1/insights/search",
        headers=headers_b,
        params={"q": "SecretOrgAWidget"},
    )
    assert search_b.status_code == 200, search_b.text
    assert search_b.json()["page"]["total"] == 0
    assert search_b.json()["items"] == []

    export_a = client.post(
        "/api/v1/insights/exports",
        headers=headers_a,
        json={"export_format": "json", "include_dashboard_metrics": True},
    )
    assert export_a.status_code == 201, export_a.text
    assert export_a.json()["status"] == "ready"
    preview_a = json.loads(export_a.json()["payload_preview"])
    assert preview_a["organization_id"] == headers_a["X-Organization-Id"]
    assert preview_a["metrics"]["projects_total"] == 2

    export_b = client.post(
        "/api/v1/insights/exports",
        headers=headers_b,
        json={"export_format": "json", "include_dashboard_metrics": True},
    )
    assert export_b.status_code == 201, export_b.text
    preview_b = json.loads(export_b.json()["payload_preview"])
    assert preview_b["organization_id"] == headers_b["X-Organization-Id"]
    assert preview_b["metrics"]["projects_total"] == 1

    # Cross-tenant: org B cannot list org A's export by id (get via list only own)
    list_b = client.get("/api/v1/insights/exports", headers=headers_b)
    assert list_b.status_code == 200
    assert all(
        item["organization_id"] == headers_b["X-Organization-Id"]
        for item in list_b.json()["items"]
    )
    assert all(item["id"] != export_a.json()["id"] for item in list_b.json()["items"])


def test_saved_filters_activity_health_and_reports(client: TestClient) -> None:
    headers = _headers("1")
    project = client.post(
        "/api/v1/projects",
        headers=headers,
        json={"code": "HLTH-1", "title": "Health project"},
    )
    assert project.status_code == 201, project.text
    project_id = project.json()["id"]

    health = client.post(
        "/api/v1/insights/project-health",
        headers=headers,
        json={
            "project_id": project_id,
            "health_status": "watch",
            "score": 72,
            "open_tickets": 3,
            "open_bugs": 1,
        },
    )
    assert health.status_code == 201, health.text
    assert health.json()["health_status"] == "watch"

    listed_health = client.get("/api/v1/insights/project-health", headers=headers)
    assert listed_health.status_code == 200
    assert listed_health.json()["page"]["total"] >= 1

    filt = client.post(
        "/api/v1/insights/saved-filters",
        headers=headers,
        json={
            "name": "Open tickets",
            "module_key": "tickets",
            "filter_json": '{"status":"open"}',
            "is_shared": False,
        },
    )
    assert filt.status_code == 201, filt.text
    filter_id = filt.json()["id"]

    listed_filt = client.get("/api/v1/insights/saved-filters", headers=headers)
    assert listed_filt.status_code == 200
    assert any(i["id"] == filter_id for i in listed_filt.json()["items"])

    deleted = client.delete(f"/api/v1/insights/saved-filters/{filter_id}", headers=headers)
    assert deleted.status_code == 204, deleted.text

    activity = client.post(
        "/api/v1/insights/activity",
        headers=headers,
        json={
            "event_type": "note",
            "entity_type": "project",
            "entity_id": project_id,
            "project_id": project_id,
            "summary": "Health reviewed",
        },
    )
    assert activity.status_code == 201, activity.text

    listed_act = client.get(
        "/api/v1/insights/activity",
        headers=headers,
        params={"project_id": project_id},
    )
    assert listed_act.status_code == 200
    assert listed_act.json()["page"]["total"] >= 1

    report = client.post(
        "/api/v1/insights/reports",
        headers=headers,
        json={
            "code": "ORG-SUMMARY",
            "title": "Org summary",
            "report_type": "dashboard",
            "definition_json": "{}",
            "status": "ready",
        },
    )
    assert report.status_code == 201, report.text

    listed_reports = client.get("/api/v1/insights/reports", headers=headers)
    assert listed_reports.status_code == 200
    assert listed_reports.json()["page"]["total"] >= 1
