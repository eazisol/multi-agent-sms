"""API/integration tests for MOD-210 queries."""

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
from masms_api.modules.queries import models as _queries  # noqa: F401
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


def test_query_lifecycle_qualification_convert_and_sla(client: TestClient) -> None:
    headers = _headers()

    source = client.post(
        "/api/v1/queries/sources",
        headers=headers,
        json={"code": "web_form", "title": "Website form", "channel": "web"},
    )
    assert source.status_code == 201, source.text

    created = client.post(
        "/api/v1/queries",
        headers=headers,
        json={
            "subject": "Need a portal",
            "summary": "Client wants a customer portal",
            "original_message": "Hi, we need a portal ASAP.",
            "source_id": source.json()["id"],
            "sla_hours": 24,
        },
    )
    assert created.status_code == 201, created.text
    query_id = created.json()["id"]
    assert created.json()["status"] == "received"
    assert created.json()["sla_status"] == "pending"
    assert created.json()["project_id"] is None

    classify = client.post(
        f"/api/v1/queries/{query_id}/transitions",
        headers=headers,
        json={"next_status": "classified", "classification": "new_build"},
    )
    assert classify.status_code == 200

    qualify = client.post(
        f"/api/v1/queries/{query_id}/transitions",
        headers=headers,
        json={"next_status": "qualifying"},
    )
    assert qualify.status_code == 200

    answer = client.post(
        "/api/v1/queries/qualification-answers",
        headers=headers,
        json={
            "query_id": query_id,
            "question_key": "budget",
            "question_text": "Do you have an approved budget?",
            "answer_text": "Yes, approximately 50k",
            "rationale": "Confirmed by commercial contact",
        },
    )
    assert answer.status_code == 201, answer.text

    response = client.post(
        f"/api/v1/queries/{query_id}/first-response",
        headers=headers,
        json={"note": "Acknowledged via email"},
    )
    assert response.status_code == 200
    assert response.json()["sla_status"] == "met"

    qualified = client.post(
        f"/api/v1/queries/{query_id}/transitions",
        headers=headers,
        json={"next_status": "qualified", "reason": "Budget and fit confirmed"},
    )
    assert qualified.status_code == 200

    opportunity = client.post(
        f"/api/v1/queries/{query_id}/convert",
        headers=headers,
        json={
            "title": "Acme Portal Opportunity",
            "estimated_value": "50000.00",
            "conversion_notes": "Preserve original inquiry thread",
        },
    )
    assert opportunity.status_code == 201, opportunity.text
    assert opportunity.json()["query_id"] == query_id

    listed_opps = client.get("/api/v1/queries/opportunities", headers=headers)
    assert listed_opps.status_code == 200, listed_opps.text
    assert any(row["id"] == opportunity.json()["id"] for row in listed_opps.json()["items"])

    history = client.get(f"/api/v1/queries/{query_id}/history", headers=headers)
    assert history.status_code == 200
    statuses = [h["next_status"] for h in history.json()]
    assert statuses[0] == "received"
    assert "converted" in statuses
    convert_row = [h for h in history.json() if h["next_status"] == "converted"][0]
    assert convert_row["evidence_json"]["original_message_preserved"] is True
    assert len(convert_row["evidence_json"]["qualification_answer_ids"]) == 1

    answers = client.get(
        f"/api/v1/queries/{query_id}/qualification-answers", headers=headers
    )
    assert len(answers.json()) == 1
    assert answers.json()[0]["rationale"]

    listed = client.get("/api/v1/queries", headers=headers)
    assert listed.status_code == 200, listed.text
    assert any(row["id"] == query_id for row in listed.json()["items"])

    filtered = client.get("/api/v1/queries", headers=headers, params={"status": "converted"})
    assert filtered.status_code == 200
    assert all(row["status"] == "converted" for row in filtered.json()["items"])
    assert any(row["id"] == query_id for row in filtered.json()["items"])

    searched = client.get("/api/v1/queries", headers=headers, params={"q": "portal"})
    assert searched.status_code == 200
    assert any(row["id"] == query_id for row in searched.json()["items"])

    got = client.get(f"/api/v1/queries/{query_id}", headers=headers)
    assert got.status_code == 200
    assert got.json()["id"] == query_id
