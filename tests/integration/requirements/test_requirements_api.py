"""API/integration tests for MOD-230 requirement gathering."""

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


def test_questionnaire_completeness_clarification_and_brief_approval(
    client: TestClient,
) -> None:
    headers = _headers()
    entity_id = str(uuid4())
    owner = "00000000-0000-4000-8000-000000000201"

    questionnaire = client.post(
        "/api/v1/requirements/questionnaires",
        headers=headers,
        json={"code": "intake_v1", "title": "Discovery intake"},
    )
    assert questionnaire.status_code == 201, questionnaire.text
    questionnaire_id = questionnaire.json()["id"]

    questions = [
        {
            "key": f"q{i}",
            "text": f"Question {i}",
            "mandatory": True,
            "answer_type": "text",
        }
        for i in range(1, 21)
    ]
    version = client.post(
        "/api/v1/requirements/questionnaire-versions",
        headers=headers,
        json={"questionnaire_id": questionnaire_id, "questions": questions},
    )
    assert version.status_code == 201, version.text
    version_id = version.json()["id"]
    assert version.json()["status"] == "draft"

    published = client.post(
        f"/api/v1/requirements/questionnaire-versions/{version_id}/publish",
        headers=headers,
    )
    assert published.status_code == 200
    assert published.json()["status"] == "published"

    for i in range(1, 20):
        answer = client.post(
            "/api/v1/requirements/answers",
            headers=headers,
            json={
                "questionnaire_version_id": version_id,
                "related_entity_type": "crm_query",
                "related_entity_id": entity_id,
                "question_key": f"q{i}",
                "answer_text": f"Answer {i}",
            },
        )
        assert answer.status_code == 201, answer.text

    score = client.post(
        "/api/v1/requirements/completeness-scores",
        headers=headers,
        json={
            "questionnaire_version_id": version_id,
            "related_entity_type": "crm_query",
            "related_entity_id": entity_id,
        },
    )
    assert score.status_code == 201, score.text
    assert float(score.json()["percentage"]) == 0.95
    assert score.json()["meets_threshold"] is True
    assert score.json()["gap_question_keys"] == ["q20"]
    score_id = score.json()["id"]

    blocked = client.post(
        "/api/v1/requirements/briefs",
        headers=headers,
        json={
            "related_entity_type": "crm_query",
            "related_entity_id": entity_id,
            "title": "Query brief",
            "summary": "Initial brief draft",
            "questionnaire_version_id": version_id,
            "completeness_score_id": score_id,
        },
    )
    assert blocked.status_code == 201
    brief_id = blocked.json()["id"]
    assert blocked.json()["version_number"] == 1
    assert blocked.json()["status"] == "draft"

    approve_without_owner = client.post(
        f"/api/v1/requirements/briefs/{brief_id}/approve", headers=headers
    )
    assert approve_without_owner.status_code == 422

    clarification = client.post(
        "/api/v1/requirements/clarifications",
        headers=headers,
        json={
            "questionnaire_version_id": version_id,
            "related_entity_type": "crm_query",
            "related_entity_id": entity_id,
            "question_key": "q20",
            "question_text": "Question 20",
            "owner_actor_id": owner,
        },
    )
    assert clarification.status_code == 201, clarification.text
    assert clarification.json()["owner_actor_id"] == owner

    approved = client.post(
        f"/api/v1/requirements/briefs/{brief_id}/approve", headers=headers
    )
    assert approved.status_code == 200, approved.text
    assert approved.json()["status"] == "approved"
    assert approved.json()["approved_by_actor_id"] is not None

    listed = client.get(
        "/api/v1/requirements/briefs",
        headers=headers,
        params={"related_entity_type": "crm_query", "related_entity_id": entity_id},
    )
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert listed.json()[0]["status"] == "approved"

    questionnaires = client.get("/api/v1/requirements/questionnaires", headers=headers)
    assert questionnaires.status_code == 200, questionnaires.text
    assert any(row["id"] == questionnaire_id for row in questionnaires.json())

    searched = client.get(
        "/api/v1/requirements/questionnaires", headers=headers, params={"q": "intake"}
    )
    assert searched.status_code == 200
    assert any(row["id"] == questionnaire_id for row in searched.json())

    versions = client.get(
        f"/api/v1/requirements/questionnaires/{questionnaire_id}/versions",
        headers=headers,
    )
    assert versions.status_code == 200
    assert any(row["id"] == version_id for row in versions.json())

    published_get = client.get(
        f"/api/v1/requirements/questionnaires/{questionnaire_id}/published-version",
        headers=headers,
    )
    assert published_get.status_code == 200
    assert published_get.json()["id"] == version_id
    assert published_get.json()["status"] == "published"

    answers = client.get(
        "/api/v1/requirements/answers",
        headers=headers,
        params={
            "questionnaire_version_id": version_id,
            "related_entity_type": "crm_query",
            "related_entity_id": entity_id,
        },
    )
    assert answers.status_code == 200
    assert len(answers.json()) == 19

    org_briefs = client.get("/api/v1/requirements/briefs", headers=headers)
    assert org_briefs.status_code == 200
    assert any(row["id"] == brief_id for row in org_briefs.json())

    got_brief = client.get(f"/api/v1/requirements/briefs/{brief_id}", headers=headers)
    assert got_brief.status_code == 200
    assert got_brief.json()["id"] == brief_id

