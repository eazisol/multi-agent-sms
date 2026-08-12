"""API/integration tests for MOD-460 traceability."""

from __future__ import annotations

import json
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
from masms_api.modules.insights import models as _rp  # noqa: F401
from masms_api.modules.gmail import models as _gm  # noqa: F401
from masms_api.modules.integrations import models as _ig  # noqa: F401
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


def _headers(org_suffix: str = "1") -> dict[str, str]:
    return {
        "X-Organization-Id": f"00000000-0000-4000-8000-00000000000{org_suffix}",
        "X-Actor-Id": "00000000-0000-4000-8000-000000000101",
        "X-Actor-Kind": "human",
        "X-Correlation-Id": str(uuid4()),
    }


def _fully_link_requirement(client: TestClient, headers: dict[str, str], req_id: str) -> None:
    ticket_id = str(uuid4())
    test_id = str(uuid4())
    release_id = str(uuid4())
    document_id = str(uuid4())
    for path, body in (
        (
            "/api/v1/traceability/links/requirement-tickets",
            {"requirement_id": req_id, "ticket_id": ticket_id},
        ),
        (
            "/api/v1/traceability/links/requirement-tests",
            {"requirement_id": req_id, "test_case_id": test_id},
        ),
        (
            "/api/v1/traceability/links/requirement-releases",
            {"requirement_id": req_id, "release_id": release_id},
        ),
        (
            "/api/v1/traceability/links/requirement-documents",
            {"requirement_id": req_id, "document_id": document_id},
        ),
    ):
        resp = client.post(path, headers=headers, json=body)
        assert resp.status_code == 201, resp.text


def test_ac001_coverage_95_percent_gate(client: TestClient) -> None:
    headers = _headers("1")
    req_ids: list[str] = []
    for i in range(20):
        rid = str(uuid4())
        req_ids.append(rid)
        created = client.post(
            "/api/v1/traceability/must-haves",
            headers=headers,
            json={
                "requirement_id": rid,
                "requirement_code": f"MH-{i:02d}",
                "title": f"Must-have {i}",
            },
        )
        assert created.status_code == 201, created.text

    # Fully link 19 of 20 → 95% → release_ready
    for rid in req_ids[:19]:
        _fully_link_requirement(client, headers, rid)

    cov19 = client.get("/api/v1/traceability/coverage", headers=headers)
    assert cov19.status_code == 200, cov19.text
    body19 = cov19.json()
    assert body19["total_must_haves"] == 20
    assert body19["complete_count"] == 19
    assert body19["coverage_pct"] == 95.0
    assert body19["release_ready"] is True

    # With only 18 complete → 90% → not ready
    # Unlink one by registering a fresh org scenario: delete isn't available,
    # so verify with a separate org that only links 18.
    headers_b = _headers("2")
    req_ids_b: list[str] = []
    for i in range(20):
        rid = str(uuid4())
        req_ids_b.append(rid)
        created = client.post(
            "/api/v1/traceability/must-haves",
            headers=headers_b,
            json={
                "requirement_id": rid,
                "requirement_code": f"MH-B-{i:02d}",
                "title": f"Must-have B {i}",
            },
        )
        assert created.status_code == 201, created.text

    for rid in req_ids_b[:18]:
        _fully_link_requirement(client, headers_b, rid)

    cov18 = client.get("/api/v1/traceability/coverage", headers=headers_b)
    assert cov18.status_code == 200, cov18.text
    body18 = cov18.json()
    assert body18["complete_count"] == 18
    assert body18["coverage_pct"] == 90.0
    assert body18["release_ready"] is False


def test_ac002_audit_coverage_after_mutations(client: TestClient) -> None:
    headers = _headers("1")
    req_id = str(uuid4())
    ticket_id = str(uuid4())

    mh = client.post(
        "/api/v1/traceability/must-haves",
        headers=headers,
        json={
            "requirement_id": req_id,
            "requirement_code": "AUD-01",
            "title": "Audit must-have",
        },
    )
    assert mh.status_code == 201, mh.text

    link = client.post(
        "/api/v1/traceability/links/requirement-tickets",
        headers=headers,
        json={"requirement_id": req_id, "ticket_id": ticket_id},
    )
    assert link.status_code == 201, link.text

    manifest = client.post(
        "/api/v1/traceability/manifests",
        headers=headers,
        json={"code": "MAN-AUD-1", "title": "Audit manifest"},
    )
    assert manifest.status_code == 201, manifest.text
    manifest_id = manifest.json()["id"]

    item = client.post(
        f"/api/v1/traceability/manifests/{manifest_id}/items",
        headers=headers,
        json={"item_type": "requirement", "item_id": req_id, "label": "req"},
    )
    assert item.status_code == 201, item.text

    sealed = client.post(
        f"/api/v1/traceability/manifests/{manifest_id}/seal",
        headers=headers,
        json={},
    )
    assert sealed.status_code == 200, sealed.text

    export = client.post(
        "/api/v1/traceability/exports",
        headers=headers,
        json={"manifest_id": manifest_id, "export_format": "json"},
    )
    assert export.status_code == 201, export.text

    coverage = client.get("/api/v1/traceability/audit-coverage", headers=headers)
    assert coverage.status_code == 200, coverage.text
    body = coverage.json()
    assert body["action_count"] >= 5
    assert body["audited_count"] == body["action_count"]
    assert body["coverage_pct"] == 100.0
    assert body["complete"] is True


def test_ac003_export_reconcilable_and_cross_org_404(client: TestClient) -> None:
    headers_a = _headers("1")
    headers_b = _headers("2")

    req_id = str(uuid4())
    ticket_id = str(uuid4())

    manifest = client.post(
        "/api/v1/traceability/manifests",
        headers=headers_a,
        json={"code": "MAN-EXP-1", "title": "Export manifest"},
    )
    assert manifest.status_code == 201, manifest.text
    manifest_id = manifest.json()["id"]

    for item_type, item_id in (
        ("requirement", req_id),
        ("ticket", ticket_id),
    ):
        added = client.post(
            f"/api/v1/traceability/manifests/{manifest_id}/items",
            headers=headers_a,
            json={"item_type": item_type, "item_id": item_id, "label": item_type},
        )
        assert added.status_code == 201, added.text

    sealed = client.post(
        f"/api/v1/traceability/manifests/{manifest_id}/seal",
        headers=headers_a,
        json={},
    )
    assert sealed.status_code == 200, sealed.text
    checksum = sealed.json()["checksum"]
    assert checksum
    assert sealed.json()["item_count"] == 2

    export = client.post(
        "/api/v1/traceability/exports",
        headers=headers_a,
        json={"manifest_id": manifest_id},
    )
    assert export.status_code == 201, export.text
    exp_body = export.json()
    assert exp_body["status"] == "ready"
    assert exp_body["organization_id"] == headers_a["X-Organization-Id"]
    assert exp_body["reconciliation_hash"] == checksum

    preview = json.loads(exp_body["payload_preview"])
    assert preview["organization_id"] == headers_a["X-Organization-Id"]
    assert preview["checksum"] == checksum
    assert preview["reconciliation_hash"] == checksum
    assert preview["item_count"] == 2
    assert len(preview["items"]) == 2
    item_ids = {(i["item_type"], i["item_id"]) for i in preview["items"]}
    assert ("requirement", req_id) in item_ids
    assert ("ticket", ticket_id) in item_ids

    # Cross-org GET returns 404
    cross = client.get(
        f"/api/v1/traceability/exports/{exp_body['id']}",
        headers=headers_b,
    )
    assert cross.status_code == 404, cross.text

    cross_manifest = client.get(
        f"/api/v1/traceability/manifests/{manifest_id}",
        headers=headers_b,
    )
    assert cross_manifest.status_code == 404, cross_manifest.text
