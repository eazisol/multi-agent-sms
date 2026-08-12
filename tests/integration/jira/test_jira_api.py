"""API/integration tests for MOD-520 Jira."""

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
from masms_api.modules.gmail import models as _gm  # noqa: F401
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.insights import models as _rp  # noqa: F401
from masms_api.modules.integrations import models as _ig  # noqa: F401
from masms_api.modules.jira import models as _jira  # noqa: F401
from masms_api.modules.knowledge import models as _kn  # noqa: F401
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
    testing_session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session, None, None]:
        db = testing_session_local()
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


def _push_approved_issue(client: TestClient, headers: dict[str, str]) -> dict[str, str]:
    response = client.post(
        "/api/v1/jira/issues/push",
        headers=headers,
        json={
            "internal_ticket_id": str(uuid4()),
            "summary": "Approved ticket for Jira",
            "approval_status": "approved",
            "simulated_jira_key": "SIM-520",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_ac001_approved_only_issue_push_and_key_retained(client: TestClient) -> None:
    headers = _headers("1")

    approved = _push_approved_issue(client, headers)
    assert approved["jira_issue_key"] == "SIM-520"
    assert approved["approval_status"] == "approved"
    assert approved["push_status"] == "pushed"

    unapproved = client.post(
        "/api/v1/jira/issues/push",
        headers=headers,
        json={
            "internal_ticket_id": str(uuid4()),
            "summary": "Unapproved ticket must fail",
            "approval_status": "pending",
            "simulated_jira_key": "SIM-521",
        },
    )
    assert unapproved.status_code == 422, unapproved.text
    assert "Only approved internal tickets can be pushed to Jira" in unapproved.text


def test_ac002_inbound_status_webhook_creates_conflict_without_mutation(
    client: TestClient,
) -> None:
    headers = _headers("1")
    pushed = _push_approved_issue(client, headers)

    webhook = client.post(
        "/api/v1/jira/webhooks/status",
        headers=headers,
        json={
            "issue_push_id": pushed["id"],
            "external_status": "Done",
            "attempted_internal_status": "closed",
        },
    )
    assert webhook.status_code == 409, webhook.text
    conflict = webhook.json()
    assert conflict["issue_push_id"] == pushed["id"]
    assert conflict["external_status"] == "Done"
    assert "cannot mutate internal workflow status" in conflict["conflict_reason"]

    listing = client.get("/api/v1/jira/issues/pushes", headers=headers)
    assert listing.status_code == 200, listing.text
    issue = listing.json()["items"][0]
    assert issue["id"] == pushed["id"]
    assert issue["push_status"] == "pushed"


def test_ac003_comment_sync_failure_visible_then_retry_success(client: TestClient) -> None:
    headers = _headers("1")
    pushed = _push_approved_issue(client, headers)

    failed_sync = client.post(
        "/api/v1/jira/comments/sync",
        headers=headers,
        json={
            "issue_push_id": pushed["id"],
            "comment_text": "First sync should fail",
            "force_fail": True,
        },
    )
    assert failed_sync.status_code == 201, failed_sync.text
    failed = failed_sync.json()
    assert failed["sync_status"] == "failed"
    assert failed["retry_count"] == 1
    assert failed["failure_reason"] is not None

    list_failed = client.get("/api/v1/jira/comments/sync", headers=headers)
    assert list_failed.status_code == 200, list_failed.text
    assert list_failed.json()["items"][0]["sync_status"] == "failed"

    retried = client.post(
        f"/api/v1/jira/comments/sync/{failed['id']}/retry",
        headers=headers,
    )
    assert retried.status_code == 200, retried.text
    retried_body = retried.json()
    assert retried_body["sync_status"] == "synced"
    assert retried_body["retry_count"] == 2
    assert retried_body["failure_reason"] is None
