"""API smoke tests for MOD-040 observability."""

from __future__ import annotations

from collections.abc import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from masms_api.db import Base, get_db
from masms_api.kernel import outbox as _outbox  # noqa: F401
from masms_api.main import create_app
from masms_api.modules.governance import models as _gov  # noqa: F401
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


ORG = "00000000-0000-4000-8000-000000000001"


def _headers() -> dict[str, str]:
    return {
        "X-Organization-Id": ORG,
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": "human",
        "X-Correlation-Id": str(uuid4()),
    }


def test_ready_and_live(client: TestClient) -> None:
    assert client.get("/health/live").status_code == 200
    ready = client.get("/health/ready")
    assert ready.status_code == 200
    assert ready.json()["status"] == "ready"
    assert ready.json()["checks"]["database"]["status"] == "up"


def test_agent_run_writes_audit_and_blocks_delete(client: TestClient) -> None:
    create = client.post(
        "/api/v1/observability/agent-runs",
        headers=_headers(),
        json={"agent_name": "bd-classifier", "input_summary": {"api_token": "secret"}},
    )
    assert create.status_code == 201, create.text
    run_id = create.json()["id"]

    finish = client.post(
        f"/api/v1/observability/agent-runs/{run_id}/finish",
        headers=_headers(),
        json={"status": "succeeded", "output_summary": {"label": "qualified"}},
    )
    assert finish.status_code == 200
    assert finish.json()["status"] == "succeeded"

    audits = client.get("/api/v1/observability/audit-logs", headers=_headers())
    assert audits.status_code == 200
    items = audits.json()["items"]
    assert items
    assert items[0]["payload_redacted"]["api_token"] == "[REDACTED]"

    audit_id = items[0]["id"]
    blocked = client.delete(
        f"/api/v1/observability/audit-logs/{audit_id}",
        headers=_headers(),
    )
    assert blocked.status_code == 403
    assert blocked.json()["code"] == "forbidden"
