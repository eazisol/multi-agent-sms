"""API/integration tests for MOD-120 access control."""

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
from masms_api.modules.auth import models as _auth  # noqa: F401
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
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


def _headers(*, client_id: str | None = None) -> dict[str, str]:
    headers = {
        "X-Organization-Id": "00000000-0000-4000-8000-000000000001",
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": "human",
        "X-Correlation-Id": str(uuid4()),
    }
    if client_id:
        headers["X-Client-Id"] = client_id
    return headers


def test_permission_role_membership_and_checks(client: TestClient) -> None:
    org = client.post(
        "/api/v1/identity/organizations",
        headers=_headers(),
        json={"name": "Access Co", "slug": "access-co"},
    )
    assert org.status_code == 201, org.text
    org_id = org.json()["id"]
    headers = _headers()
    headers["X-Organization-Id"] = org_id

    role = client.post(
        "/api/v1/identity/roles",
        headers=headers,
        json={"code": "PM", "title": "Project Manager"},
    )
    assert role.status_code == 201, role.text
    role_id = role.json()["id"]

    perm = client.post(
        "/api/v1/access/permissions",
        headers=headers,
        json={
            "code": "clients.read",
            "module_key": "clients",
            "action_key": "read",
            "title": "Read clients",
        },
    )
    assert perm.status_code == 201, perm.text
    permission_id = perm.json()["id"]

    denied = client.post(
        "/api/v1/access/checks/permission",
        headers=headers,
        json={"permission_code": "clients.read", "role_id": role_id},
    )
    assert denied.status_code == 200
    assert denied.json()["allowed"] is False

    grant = client.post(
        "/api/v1/access/role-permissions",
        headers=headers,
        json={"role_id": role_id, "permission_id": permission_id},
    )
    assert grant.status_code == 201, grant.text

    allowed = client.post(
        "/api/v1/access/checks/permission",
        headers=headers,
        json={"permission_code": "clients.read", "role_id": role_id},
    )
    assert allowed.json()["allowed"] is True

    project_id = str(uuid4())
    actor_id = headers["X-Actor-Id"]
    member = client.post(
        "/api/v1/access/project-members",
        headers=headers,
        json={"project_id": project_id, "actor_id": actor_id, "role_code": "PM"},
    )
    assert member.status_code == 201, member.text

    other_project = str(uuid4())
    no_member = client.post(
        "/api/v1/access/checks/permission",
        headers=headers,
        json={
            "permission_code": "clients.read",
            "role_id": role_id,
            "project_id": other_project,
        },
    )
    assert no_member.json()["allowed"] is False
    assert "membership" in no_member.json()["reason"].lower()

    with_member = client.post(
        "/api/v1/access/checks/permission",
        headers=headers,
        json={
            "permission_code": "clients.read",
            "role_id": role_id,
            "project_id": project_id,
        },
    )
    assert with_member.json()["allowed"] is True


def test_module_document_authority_review_and_client_scope(client: TestClient) -> None:
    headers = _headers(client_id="00000000-0000-4000-8000-000000000201")
    actor_id = headers["X-Actor-Id"]

    module = client.post(
        "/api/v1/access/module-access",
        headers=headers,
        json={"actor_id": actor_id, "module_key": "requirements", "access_level": "write"},
    )
    assert module.status_code == 201, module.text

    doc = client.post(
        "/api/v1/access/document-access",
        headers=headers,
        json={
            "document_ref": "srs:v1",
            "classification": "confidential",
            "role_code": "PM",
        },
    )
    assert doc.status_code == 201, doc.text

    auth = client.post(
        "/api/v1/access/approval-authorities",
        headers=headers,
        json={
            "action_code": "requirements.approve",
            "authority_role_code": "PM",
            "environment": "staging",
            "amount_threshold": "10000.00",
        },
    )
    assert auth.status_code == 201, auth.text

    review = client.post(
        "/api/v1/access/reviews",
        headers=headers,
        json={
            "title": "Q3 access review",
            "due_at": (datetime.now(UTC) + timedelta(days=30)).isoformat(),
            "owner_actor_id": actor_id,
        },
    )
    assert review.status_code == 201, review.text
    review_id = review.json()["id"]

    done = client.post(
        f"/api/v1/access/reviews/{review_id}/complete",
        headers=headers,
        json={"summary": "No anomalies", "findings": {"orphans": 0}},
    )
    assert done.status_code == 200
    assert done.json()["status"] == "completed"
    assert done.json()["findings_json"]["orphans"] == 0
