"""API/integration tests for MOD-250 documents."""

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
from masms_api.modules.documents import models as _documents  # noqa: F401
from masms_api.modules.governance import models as _gov  # noqa: F401
from masms_api.modules.identity import models as _identity  # noqa: F401
from masms_api.modules.projects import models as _projects  # noqa: F401
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


def test_document_scan_gate_permissions_and_authoritative_version(
    client: TestClient,
) -> None:
    headers = _headers()
    grantee = "00000000-0000-4000-8000-000000000201"

    template = client.post(
        "/api/v1/documents/templates",
        headers=headers,
        json={"code": "srs_template", "title": "SRS Template"},
    )
    assert template.status_code == 201, template.text
    template_id = template.json()["id"]

    tv = client.post(
        "/api/v1/documents/template-versions",
        headers=headers,
        json={"template_id": template_id, "body_markdown": "# SRS\n..."},
    )
    assert tv.status_code == 201
    published = client.post(
        f"/api/v1/documents/template-versions/{tv.json()['id']}/publish",
        headers=headers,
    )
    assert published.status_code == 200
    assert published.json()["status"] == "published"

    document = client.post(
        "/api/v1/documents",
        headers=headers,
        json={
            "title": "Acme SRS",
            "classification": "confidential",
            "template_id": template_id,
        },
    )
    assert document.status_code == 201, document.text
    document_id = document.json()["id"]
    assert document.json()["owner_actor_id"]

    version = client.post(
        "/api/v1/documents/versions",
        headers=headers,
        json={
            "document_id": document_id,
            "storage_key": "s3://bucket/org/acme-srs-v1.pdf",
            "filename": "acme-srs-v1.pdf",
            "content_type": "application/pdf",
            "size_bytes": 2048,
            "checksum_sha256": "a" * 64,
        },
    )
    assert version.status_code == 201, version.text
    version_id = version.json()["id"]

    attachment = client.post(
        "/api/v1/documents/attachments",
        headers=headers,
        json={
            "document_version_id": version_id,
            "storage_key": "s3://bucket/org/acme-srs-v1.pdf",
            "filename": "acme-srs-v1.pdf",
            "content_type": "application/pdf",
            "size_bytes": 2048,
        },
    )
    assert attachment.status_code == 201

    no_scan = client.post(
        f"/api/v1/documents/versions/{version_id}/available",
        headers=headers,
        json={"effective_at": "2026-08-11T00:00:00Z"},
    )
    assert no_scan.status_code == 422

    infected = client.post(
        "/api/v1/documents/scan-results",
        headers=headers,
        json={
            "document_version_id": version_id,
            "verdict": "infected",
            "detail": "EICAR",
        },
    )
    assert infected.status_code == 201
    blocked = client.post(
        f"/api/v1/documents/versions/{version_id}/available",
        headers=headers,
        json={"effective_at": "2026-08-11T00:00:00Z"},
    )
    assert blocked.status_code == 403

    clean_doc = client.post(
        "/api/v1/documents",
        headers=headers,
        json={"title": "Safe Spec", "classification": "internal"},
    )
    clean_version = client.post(
        "/api/v1/documents/versions",
        headers=headers,
        json={
            "document_id": clean_doc.json()["id"],
            "storage_key": "s3://bucket/org/safe.pdf",
            "filename": "safe.pdf",
            "content_type": "application/pdf",
            "size_bytes": 100,
        },
    )
    clean_version_id = clean_version.json()["id"]
    clean_doc_id = clean_doc.json()["id"]

    scan = client.post(
        "/api/v1/documents/scan-results",
        headers=headers,
        json={"document_version_id": clean_version_id, "verdict": "clean"},
    )
    assert scan.status_code == 201

    available = client.post(
        f"/api/v1/documents/versions/{clean_version_id}/available",
        headers=headers,
        json={"effective_at": "2026-08-11T12:00:00Z"},
    )
    assert available.status_code == 200, available.text
    assert available.json()["status"] == "available"
    assert available.json()["effective_at"] is not None
    assert available.json()["indexing_allowed"] is True
    assert available.json()["owner_actor_id"]
    assert available.json()["version_number"] == 1

    client.post(
        "/api/v1/documents/permissions",
        headers=headers,
        json={
            "document_id": clean_doc_id,
            "grantee_actor_id": grantee,
            "can_download": True,
            "can_preview": True,
            "can_extract_text": False,
            "can_use_embeddings": False,
        },
    )

    ok_preview = client.post(
        "/api/v1/documents/access-check",
        headers=headers,
        json={
            "document_version_id": clean_version_id,
            "actor_id": grantee,
            "action": "preview",
        },
    )
    assert ok_preview.status_code == 200
    assert ok_preview.json()["allowed"] is True

    deny_embed = client.post(
        "/api/v1/documents/access-check",
        headers=headers,
        json={
            "document_version_id": clean_version_id,
            "actor_id": grantee,
            "action": "embeddings",
        },
    )
    assert deny_embed.status_code == 403
