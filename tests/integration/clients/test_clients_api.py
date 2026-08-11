"""API/integration tests for MOD-200 clients."""

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
from masms_api.modules.configadmin import models as _cfg  # noqa: F401
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


def test_clients_contacts_merge_and_isolation(client: TestClient) -> None:
    headers = _headers()

    a = client.post(
        "/api/v1/clients",
        headers=headers,
        json={"code": "acme", "legal_name": "Acme Corp"},
    )
    assert a.status_code == 201, a.text
    a_id = a.json()["id"]

    b = client.post(
        "/api/v1/clients",
        headers=headers,
        json={"code": "acme2", "legal_name": "Acme Corporation"},
    )
    assert b.status_code == 201
    b_id = b.json()["id"]

    contact = client.post(
        "/api/v1/clients/contacts",
        headers=headers,
        json={
            "client_id": a_id,
            "full_name": "Ada Decision",
            "email": "Ada@Acme.example",
            "authority_level": "decision_maker",
            "is_primary": True,
        },
    )
    assert contact.status_code == 201, contact.text
    assert contact.json()["email"] == "ada@acme.example"
    assert contact.json()["authority_level"] == "decision_maker"
    contact_id = contact.json()["id"]

    second = client.post(
        "/api/v1/clients/contacts",
        headers=headers,
        json={
            "client_id": a_id,
            "full_name": "Bob Tech",
            "email": "bob@acme.example",
            "authority_level": "technical",
        },
    )
    assert second.status_code == 201

    listed = client.get(f"/api/v1/clients/{a_id}/contacts", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 2

    pref = client.post(
        "/api/v1/clients/preferences",
        headers=headers,
        json={"contact_id": contact_id, "channel": "email", "opted_in": True},
    )
    assert pref.status_code == 201

    proj = client.post(
        "/api/v1/clients/project-contacts",
        headers=headers,
        json={
            "client_id": a_id,
            "project_id": str(uuid4()),
            "contact_id": contact_id,
            "role_label": "sponsor",
        },
    )
    assert proj.status_code == 201

    dup = client.post(
        "/api/v1/clients/duplicates",
        headers=headers,
        json={
            "left_client_id": a_id,
            "right_client_id": b_id,
            "score": 92.5,
            "reason": "similar legal name",
        },
    )
    assert dup.status_code == 201, dup.text
    dup_id = dup.json()["id"]

    # Cross-client isolation: header client scope cannot see other client
    denied = client.get(
        f"/api/v1/clients/{b_id}/contacts",
        headers=_headers(client_id=a_id),
    )
    assert denied.status_code == 403

    merge = client.post(
        "/api/v1/clients/merge",
        headers=headers,
        json={
            "surviving_client_id": a_id,
            "merged_client_id": b_id,
            "duplicate_suggestion_id": dup_id,
            "reason": "Confirmed duplicate legal entities",
        },
    )
    assert merge.status_code == 201, merge.text
    assert merge.json()["surviving_client_id"] == a_id
    assert merge.json()["merged_client_id"] == b_id
    assert merge.json()["merged_snapshot"]["code"] == "acme2"

    clients = client.get("/api/v1/clients", headers=headers)
    assert clients.status_code == 200
    codes = {item["code"] for item in clients.json()["items"]}
    assert "acme" in codes
    assert "acme2" not in codes
