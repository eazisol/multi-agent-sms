"""API/integration tests for MOD-110 auth."""

from __future__ import annotations

from collections.abc import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from masms_api.db import Base, get_db
from masms_api.kernel import outbox as _outbox  # noqa: F401
from masms_api.main import create_app
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


def _headers(*, assurance: int = 1) -> dict[str, str]:
    return {
        "X-Organization-Id": "00000000-0000-4000-8000-000000000001",
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": "human",
        "X-Correlation-Id": str(uuid4()),
        "X-Assurance-Level": str(assurance),
    }


def test_provider_meta_and_session_mfa_flow(client: TestClient) -> None:
    provider = client.get("/api/v1/auth/provider")
    assert provider.status_code == 200
    assert provider.json()["provider"] == "local"
    assert provider.json()["jwks_enabled"] is False

    org_id = "00000000-0000-4000-8000-000000000001"
    actor_id = "00000000-0000-4000-8000-000000000101"
    created = client.post(
        "/api/v1/auth/sessions",
        headers=_headers(),
        json={
            "organization_id": org_id,
            "actor_id": actor_id,
            "display_name": "Alice",
            "assurance_level": 1,
            "ttl_minutes": 60,
        },
    )
    assert created.status_code == 201, created.text
    body = created.json()
    token = body["access_token"]
    session_id = body["session"]["id"]
    assert token.startswith("sess_")

    me = client.get(
        "/api/v1/auth/sessions/me",
        headers={**_headers(), "Authorization": f"Bearer {token}"},
    )
    assert me.status_code == 200
    assert me.json()["id"] == session_id

    denied = client.post(
        f"/api/v1/auth/sessions/{session_id}/revoke",
        headers=_headers(assurance=1),
    )
    assert denied.status_code == 403

    challenge = client.post(
        "/api/v1/auth/mfa/challenges",
        headers=_headers(),
        json={"session_id": session_id, "purpose": "login"},
    )
    assert challenge.status_code == 201, challenge.text
    code = challenge.json()["debug_code"]
    assert code and len(code) == 6

    verified = client.post(
        "/api/v1/auth/mfa/verify",
        headers=_headers(),
        json={"challenge_id": challenge.json()["challenge"]["id"], "code": code},
    )
    assert verified.status_code == 200
    assert verified.json()["assurance_level"] == 2

    # Bearer principal now carries MFA assurance from the session row.
    revoked = client.post(
        f"/api/v1/auth/sessions/{session_id}/revoke",
        headers={**_headers(), "Authorization": f"Bearer {token}"},
    )
    assert revoked.status_code == 200
    assert revoked.json()["status"] == "revoked"

    dead = client.get(
        "/api/v1/auth/sessions/me",
        headers={**_headers(), "Authorization": f"Bearer {token}"},
    )
    assert dead.status_code == 403


def test_step_up_invite_and_service_identity(client: TestClient) -> None:
    org_id = "00000000-0000-4000-8000-000000000001"
    actor_id = "00000000-0000-4000-8000-000000000101"
    created = client.post(
        "/api/v1/auth/sessions",
        headers=_headers(),
        json={
            "organization_id": org_id,
            "actor_id": actor_id,
            "display_name": "Bob",
            "assurance_level": 2,
        },
    )
    session_id = created.json()["session"]["id"]

    low = client.post(
        "/api/v1/auth/step-up/assert",
        headers=_headers(),
        json={
            "session_id": session_id,
            "action": "production_deploy",
            "required_assurance_level": 3,
        },
    )
    assert low.status_code == 403

    step = client.post(
        "/api/v1/auth/mfa/challenges",
        headers=_headers(),
        json={"session_id": session_id, "purpose": "step_up"},
    )
    verified = client.post(
        "/api/v1/auth/mfa/verify",
        headers=_headers(),
        json={
            "challenge_id": step.json()["challenge"]["id"],
            "code": step.json()["debug_code"],
        },
    )
    assert verified.json()["assurance_level"] == 3

    ok = client.post(
        "/api/v1/auth/step-up/assert",
        headers=_headers(),
        json={
            "session_id": session_id,
            "action": "production_deploy",
            "required_assurance_level": 3,
        },
    )
    assert ok.status_code == 200

    invite = client.post(
        "/api/v1/auth/invitations",
        headers=_headers(),
        json={"email": "client@example.com", "invited_role_code": "client"},
    )
    assert invite.status_code == 201, invite.text
    assert invite.json()["invite_token"].startswith("invite_")

    dup = client.post(
        "/api/v1/auth/invitations",
        headers=_headers(),
        json={"email": "client@example.com"},
    )
    assert dup.status_code == 422

    svc = client.post(
        "/api/v1/auth/service-identities",
        headers=_headers(),
        json={"service_key": "ci_runner", "display_name": "CI Runner"},
    )
    assert svc.status_code == 201, svc.text
    assert svc.json()["client_secret"].startswith("svcsec_")
    assert svc.json()["identity"]["client_id"].startswith("svc_ci_runner_")
