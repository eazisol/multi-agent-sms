"""API/integration tests for MOD-130 capacity."""

from __future__ import annotations

from collections.abc import Generator
from datetime import UTC, date, datetime, timedelta
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from masms_api.db import Base, get_db
from masms_api.kernel import outbox as _outbox  # noqa: F401
from masms_api.main import create_app
from masms_api.modules.access import models as _access  # noqa: F401
from masms_api.modules.auth import models as _auth  # noqa: F401
from masms_api.modules.capacity import models as _capacity  # noqa: F401
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


def _headers() -> dict[str, str]:
    return {
        "X-Organization-Id": "00000000-0000-4000-8000-000000000001",
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": "human",
        "X-Correlation-Id": str(uuid4()),
    }


def test_capacity_assignment_and_sla(client: TestClient) -> None:
    headers = _headers()
    actor_id = headers["X-Actor-Id"]

    skill = client.post(
        "/api/v1/capacity/skills",
        headers=headers,
        json={"code": "python", "title": "Python", "category": "engineering"},
    )
    assert skill.status_code == 201, skill.text
    skill_id = skill.json()["id"]

    link = client.post(
        "/api/v1/capacity/actor-skills",
        headers=headers,
        json={"actor_id": actor_id, "skill_id": skill_id, "proficiency": 4},
    )
    assert link.status_code == 201

    avail = client.post(
        "/api/v1/capacity/availability",
        headers=headers,
        json={
            "actor_id": actor_id,
            "weekday": 0,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "timezone": "Asia/Karachi",
        },
    )
    assert avail.status_code == 201, avail.text

    alloc = client.post(
        "/api/v1/capacity/allocations",
        headers=headers,
        json={
            "actor_id": actor_id,
            "allocation_pct": "40.00",
            "effective_from": date(2026, 8, 1).isoformat(),
        },
    )
    assert alloc.status_code == 201

    calendar = client.post(
        "/api/v1/capacity/calendars",
        headers=headers,
        json={"code": "pk_std", "title": "Pakistan Standard", "timezone": "Asia/Karachi"},
    )
    assert calendar.status_code == 201
    calendar_id = calendar.json()["id"]

    holiday = client.post(
        "/api/v1/capacity/holidays",
        headers=headers,
        json={
            "calendar_id": calendar_id,
            "holiday_date": "2026-08-14",
            "title": "Company day",
        },
    )
    assert holiday.status_code == 201

    leave = client.post(
        "/api/v1/capacity/leave",
        headers=headers,
        json={
            "actor_id": actor_id,
            "starts_on": "2026-09-01",
            "ends_on": "2026-09-05",
            "leave_type": "annual",
        },
    )
    assert leave.status_code == 201

    oncall = client.post(
        "/api/v1/capacity/oncall",
        headers=headers,
        json={
            "actor_id": actor_id,
            "rotation_name": "primary",
            "starts_at": datetime.now(UTC).isoformat(),
            "ends_at": (datetime.now(UTC) + timedelta(days=7)).isoformat(),
        },
    )
    assert oncall.status_code == 201

    ok = client.post(
        "/api/v1/capacity/evaluate-assignment",
        headers=headers,
        json={
            "actor_id": actor_id,
            "skill_code": "python",
            "min_proficiency": 3,
            "as_of": "2026-08-10",
            "calendar_id": calendar_id,
            "deadline": "2026-08-13",
        },
    )
    assert ok.status_code == 200, ok.text
    assert ok.json()["eligible"] is True
    assert float(ok.json()["remaining_capacity_pct"]) == 60.0

    sla = client.post(
        "/api/v1/capacity/sla/business-days",
        headers=headers,
        json={
            "calendar_id": calendar_id,
            "start_date": "2026-08-13",
            "business_days": 1,
        },
    )
    assert sla.status_code == 200
    # Thursday + 1 with Friday holiday → Monday 17
    assert sla.json()["due_date"] == "2026-08-17"
    assert sla.json()["calendar_timezone"] == "Asia/Karachi"
