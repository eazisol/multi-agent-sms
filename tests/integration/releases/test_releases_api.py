"""API/integration tests for MOD-430 releases."""

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
from masms_api.modules.notifications import models as _ntf  # noqa: F401
from masms_api.modules.orchestrator import models as _orf  # noqa: F401
from masms_api.modules.projects import models as _projects  # noqa: F401
from masms_api.modules.queries import models as _queries  # noqa: F401
from masms_api.modules.releases import models as _rl  # noqa: F401
from masms_api.modules.requirements import models as _reqs  # noqa: F401
from masms_api.modules.roadmap import models as _roadmap  # noqa: F401
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


def _headers() -> dict[str, str]:
    return {
        "X-Organization-Id": "00000000-0000-4000-8000-000000000001",
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": "human",
        "X-Correlation-Id": str(uuid4()),
    }


def test_release_production_gate_traceability_and_closure(client: TestClient) -> None:
    headers = _headers()
    ids = {k: str(uuid4()) for k in (
        "requirement", "ticket", "test_case", "bug", "change_request", "document"
    )}

    created = client.post(
        "/api/v1/releases",
        headers=headers,
        json={
            "code": "REL-1.0.0",
            "title": "First production package",
            "version_label": "1.0.0",
            "items": [
                {"link_type": t, "linked_entity_id": eid} for t, eid in ids.items()
            ],
        },
    )
    assert created.status_code == 201, created.text
    release_id = created.json()["id"]
    version = created.json()["version"]

    # AC-001: production blocked without approval
    blocked = client.post(
        f"/api/v1/releases/{release_id}/deployments",
        headers=headers,
        json={"environment_code": "production", "build_ref": "sha-1", "expected_version": version},
    )
    assert blocked.status_code == 409, blocked.text

    trace = client.get(f"/api/v1/releases/{release_id}/traceability", headers=headers)
    assert trace.status_code == 200
    assert trace.json()["item_count"] == 6
    assert trace.json()["missing_link_types"] == []

    submitted = client.post(
        f"/api/v1/releases/{release_id}/submit",
        headers=headers,
        json={"expected_version": version},
    )
    assert submitted.status_code == 200, submitted.text
    version = submitted.json()["version"]

    approved = client.post(
        f"/api/v1/releases/{release_id}/approve",
        headers=headers,
        json={"evidence": "CAB signed minutes", "expected_version": version},
    )
    assert approved.status_code == 200, approved.text
    version = approved.json()["version"]

    # still need backup for production
    no_backup = client.post(
        f"/api/v1/releases/{release_id}/deployments",
        headers=headers,
        json={"environment_code": "production", "build_ref": "sha-1", "expected_version": version},
    )
    assert no_backup.status_code == 422, no_backup.text

    assert (
        client.post(
            f"/api/v1/releases/{release_id}/backups",
            headers=headers,
            json={"backup_ref": "s3://backups/rel-1", "confirmed": True},
        ).status_code
        == 201
    )
    assert (
        client.post(
            f"/api/v1/releases/{release_id}/migration-plans",
            headers=headers,
            json={"plan_text": "alembic upgrade head", "alembic_revision": "20260811_0027"},
        ).status_code
        == 201
    )

    deploy = client.post(
        f"/api/v1/releases/{release_id}/deployments",
        headers=headers,
        json={"environment_code": "production", "build_ref": "sha-1", "expected_version": version},
    )
    assert deploy.status_code == 201, deploy.text
    deploy_id = deploy.json()["id"]

    check = client.post(
        f"/api/v1/releases/deployments/{deploy_id}/checks",
        headers=headers,
        json={"check_name": "smoke", "result": "passed", "evidence": "health 200"},
    )
    assert check.status_code == 201, check.text
    assert client.get(f"/api/v1/releases/{release_id}", headers=headers).json()["status"] == "deployed"
    version = client.get(f"/api/v1/releases/{release_id}", headers=headers).json()["version"]

    # AC-003: partial acceptance does not close
    partial = client.put(
        f"/api/v1/releases/{release_id}/completion",
        headers=headers,
        json={
            "summary": "Delivered",
            "client_accepted": True,
            "internal_accepted": False,
            "expected_version": version,
        },
    )
    assert partial.status_code == 200
    assert client.get(f"/api/v1/releases/{release_id}", headers=headers).json()["status"] == "deployed"

    closed = client.put(
        f"/api/v1/releases/{release_id}/completion",
        headers=headers,
        json={
            "summary": "Delivered",
            "client_accepted": True,
            "internal_accepted": True,
            "client_acceptance_notes": "UAT signed",
            "internal_acceptance_notes": "Ops signed",
            "expected_version": version,
        },
    )
    assert closed.status_code == 200, closed.text
    assert client.get(f"/api/v1/releases/{release_id}", headers=headers).json()["status"] == "closed"

    listed = client.get("/api/v1/releases?limit=10&offset=0", headers=headers)
    assert listed.status_code == 200
    assert "items" in listed.json() and "page" in listed.json()
