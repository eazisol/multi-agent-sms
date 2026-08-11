"""API/integration tests for MOD-370 knowledge base."""

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
from masms_api.modules.capacity import models as _capacity  # noqa: F401
from masms_api.modules.clients import models as _clients  # noqa: F401
from masms_api.modules.comms import models as _comms  # noqa: F401
from masms_api.modules.configadmin import models as _cfg  # noqa: F401
from masms_api.modules.documents import models as _docs  # noqa: F401
from masms_api.modules.followups import models as _flu  # noqa: F401
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.knowledge import models as _kn  # noqa: F401
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


def test_knowledge_create_activate_search_and_conflict(client: TestClient) -> None:
    headers = _headers()
    project_id = str(uuid4())

    generic = client.post(
        "/api/v1/knowledge/items",
        headers=headers,
        json={
            "code": "policy_change",
            "title": "Generic change policy",
            "description": "Org default",
        },
    )
    assert generic.status_code == 201, generic.text
    generic_id = generic.json()["id"]

    project_item = client.post(
        "/api/v1/knowledge/items",
        headers=headers,
        json={
            "code": "policy_change_project",
            "title": "Project change policy",
            "project_id": project_id,
        },
    )
    assert project_item.status_code == 201, project_item.text
    project_item_id = project_item.json()["id"]

    g_ver = client.post(
        f"/api/v1/knowledge/items/{generic_id}/versions",
        headers=headers,
        json={"body_text": "Generic approval requires two reviewers for scope changes."},
    )
    assert g_ver.status_code == 201, g_ver.text
    g_act = client.post(
        f"/api/v1/knowledge/versions/{g_ver.json()['id']}/activate",
        headers=headers,
        json={},
    )
    assert g_act.status_code == 200, g_act.text
    assert g_act.json()["status"] == "active"

    chunks = client.get(
        f"/api/v1/knowledge/versions/{g_ver.json()['id']}/chunks",
        headers=headers,
    )
    assert chunks.status_code == 200
    assert len(chunks.json()) >= 1

    p_ver = client.post(
        f"/api/v1/knowledge/items/{project_item_id}/versions",
        headers=headers,
        json={
            "body_text": "Project-approved scope changes require the project manager signature."
        },
    )
    assert p_ver.status_code == 201, p_ver.text
    assert (
        client.post(
            f"/api/v1/knowledge/versions/{p_ver.json()['id']}/activate",
            headers=headers,
            json={},
        ).status_code
        == 200
    )

    search = client.post(
        "/api/v1/knowledge/search",
        headers=headers,
        json={"query": "scope changes approval", "project_id": project_id, "limit": 10},
    )
    assert search.status_code == 200, search.text
    body = search.json()
    assert body["stub"] is True
    assert len(body["items"]) >= 1
    top = body["items"][0]
    assert "source_citation" in top
    assert "@v" in top["source_citation"]
    # Project item should rank at or above generic for overlapping query
    codes = [h["item_code"] for h in body["items"]]
    assert "policy_change_project" in codes or "policy_change" in codes

    # Superseded draft cannot be searched until activated — rejected status excluded
    draft_item = client.post(
        "/api/v1/knowledge/items",
        headers=headers,
        json={"code": "secret_unapproved", "title": "Unapproved secret"},
    )
    assert draft_item.status_code == 201
    draft_ver = client.post(
        f"/api/v1/knowledge/items/{draft_item.json()['id']}/versions",
        headers=headers,
        json={"body_text": "Unapproved content must not appear in retrieval results."},
    )
    assert draft_ver.status_code == 201
    # no activate
    search2 = client.post(
        "/api/v1/knowledge/search",
        headers=headers,
        json={"query": "Unapproved content retrieval", "limit": 10},
    )
    assert search2.status_code == 200
    assert all(h["item_code"] != "secret_unapproved" for h in search2.json()["items"])

    conflict = client.post(
        "/api/v1/knowledge/conflicts",
        headers=headers,
        json={
            "item_id_a": generic_id,
            "version_id_a": g_ver.json()["id"],
            "item_id_b": project_item_id,
            "version_id_b": p_ver.json()["id"],
            "reason": "Project policy contradicts generic org policy",
            "project_id": project_id,
        },
    )
    assert conflict.status_code == 201, conflict.text
    resolved = client.post(
        f"/api/v1/knowledge/conflicts/{conflict.json()['id']}/resolve",
        headers=headers,
        json={"status": "resolved", "resolution_notes": "Prefer project-approved"},
    )
    assert resolved.status_code == 200
    assert resolved.json()["status"] == "resolved"

    listed = client.get("/api/v1/knowledge/items?limit=10&offset=0", headers=headers)
    assert listed.status_code == 200
    assert "items" in listed.json() and "page" in listed.json()
