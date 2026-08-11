#!/usr/bin/env python3
"""Idempotent synthetic E2E seed for deep UI/API flow testing (MOD-620 style).

Creates ~15 linked records per major module via the running MASMS API.
Uses stable SEED-* codes so re-runs skip existing rows.

Usage (API must be up, Postgres migrated):

  .\\.venv\\Scripts\\python.exe scripts/seed_e2e_dummy_data.py
  .\\.venv\\Scripts\\python.exe scripts/seed_e2e_dummy_data.py --base-url http://127.0.0.1:8000 --count 15

Synthetic data only — no real PII or production credentials.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import uuid
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any
from uuid import UUID

import httpx

ORG_ID = "00000000-0000-4000-8000-000000000001"
ACTOR_ID = "00000000-0000-4000-8000-000000000101"
ACTOR_B = "00000000-0000-4000-8000-000000000102"
ACTOR_C = "00000000-0000-4000-8000-000000000103"

CLIENT_NAMES = [
    ("seed-cli-01", "Northwind Analytics LLC"),
    ("seed-cli-02", "Contoso Retail Group"),
    ("seed-cli-03", "Fabrikam Health Systems"),
    ("seed-cli-04", "Adventure Works Motors"),
    ("seed-cli-05", "Wide World Importers"),
    ("seed-cli-06", "Litware Cloud Services"),
    ("seed-cli-07", "Tailspin Toys Digital"),
    ("seed-cli-08", "Blue Yonder Airlines"),
    ("seed-cli-09", "Humongous Insurance Co"),
    ("seed-cli-10", "Southridge Video Media"),
    ("seed-cli-11", "Proseware Education"),
    ("seed-cli-12", "Coho Vineyard Logistics"),
    ("seed-cli-13", "Trey Research Labs"),
    ("seed-cli-14", "Wingtip Toys Commerce"),
    ("seed-cli-15", "Alpine Ski House Ops"),
]

PROJECT_TITLES = [
    "Customer Portal Redesign",
    "Claims Automation Suite",
    "Inventory Sync Platform",
    "Member Self-Service App",
    "Fleet Telemetry Hub",
    "Billing Consolidation",
    "Partner API Gateway",
    "Field Ops Mobile",
    "Knowledge Desk Copilot",
    "Release Governance Console",
    "QA Evidence Vault",
    "Support Escalation Board",
    "Sales Intake Workspace",
    "Roadmap Forecast Engine",
    "Change Control Desk",
]

SEVERITIES = ["critical", "high", "medium", "low", "medium", "high", "low", "medium", "high", "medium", "low", "critical", "medium", "high", "low"]
PRIORITIES = ["must_have", "should_have", "could_have", "must_have", "should_have"]
CASE_TYPES = ["functional", "permission", "regression", "integration", "functional"]
CHANGE_TYPES = ["scope", "architecture", "timeline", "budget", "scope", "architecture"]
AGENT_CODES = [
    "query_intake_agent",
    "requirements_clarifier",
    "roadmap_planner",
    "ticket_triage_agent",
    "qa_review_assistant",
    "status_report_drafter",
]
WORKFLOW_CODES = [
    "query_intake",
    "requirement_clarification",
    "project_handover",
    "assignment_ack",
    "blocker_resolution",
    "qa_rejection_loop",
    "client_status_report",
    "change_request_flow",
    "deployment_approval",
    "project_closure",
    "approval_gate_wait",
    "followup_escalation",
]


@dataclass
class Stats:
    created: dict[str, int] = field(default_factory=dict)
    skipped: dict[str, int] = field(default_factory=dict)
    failed: dict[str, list[str]] = field(default_factory=dict)

    def ok(self, kind: str) -> None:
        self.created[kind] = self.created.get(kind, 0) + 1

    def skip(self, kind: str) -> None:
        self.skipped[kind] = self.skipped.get(kind, 0) + 1

    def fail(self, kind: str, detail: str) -> None:
        self.failed.setdefault(kind, []).append(detail[:240])


class Seeder:
    def __init__(self, base_url: str, count: int) -> None:
        self.base_url = base_url.rstrip("/")
        self.count = max(10, min(count, 20))
        self.stats = Stats()
        self.client = httpx.Client(base_url=self.base_url, timeout=60.0)
        self.clients: list[dict[str, Any]] = []
        self.queries: list[dict[str, Any]] = []
        self.projects: list[dict[str, Any]] = []
        self.requirements: list[dict[str, Any]] = []
        self.requirement_versions: list[dict[str, Any]] = []
        self.phases: list[dict[str, Any]] = []
        self.tickets: list[dict[str, Any]] = []
        self.documents: list[dict[str, Any]] = []
        self.test_cases: list[dict[str, Any]] = []
        self.bugs: list[dict[str, Any]] = []
        self.crs: list[dict[str, Any]] = []
        self.source_id: str | None = None

    def close(self) -> None:
        self.client.close()

    def headers(self, actor_id: str = ACTOR_ID) -> dict[str, str]:
        return {
            "X-Organization-Id": ORG_ID,
            "X-Actor-Id": actor_id,
            "X-Actor-Kind": "human",
            "X-Correlation-Id": str(uuid.uuid4()),
            "Content-Type": "application/json",
        }

    def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        actor_id: str = ACTOR_ID,
        retries: int = 3,
    ) -> httpx.Response:
        last_exc: Exception | None = None
        for attempt in range(retries):
            try:
                return self.client.request(
                    method,
                    path,
                    headers=self.headers(actor_id=actor_id),
                    json=json,
                    params=params,
                )
            except (httpx.TransportError, ConnectionError, OSError) as exc:
                last_exc = exc
                # Recreate client after drop (common when API --reload restarts).
                self.client.close()
                self.client = httpx.Client(base_url=self.base_url, timeout=60.0)
                if attempt == retries - 1:
                    raise
        raise RuntimeError(str(last_exc))

    def list_all(self, path: str, *, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        offset = 0
        limit = 100
        while True:
            q = dict(params or {})
            q.update({"limit": limit, "offset": offset})
            r = self.request("GET", path, params=q)
            if r.status_code != 200:
                return items
            body = r.json()
            batch = body if isinstance(body, list) else body.get("items", [])
            items.extend(batch)
            page = body.get("page") if isinstance(body, dict) else None
            if not batch or (page and not page.get("has_more")):
                break
            if len(batch) < limit:
                break
            offset += limit
        return items

    def find_by(self, items: list[dict[str, Any]], key: str, value: str) -> dict[str, Any] | None:
        for item in items:
            if str(item.get(key)) == value:
                return item
        return None

    def create_or_get(
        self,
        kind: str,
        *,
        list_path: str,
        create_path: str,
        code_key: str,
        code: str,
        payload: dict[str, Any],
        list_params: dict[str, Any] | None = None,
        existing: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any] | None:
        pool = existing if existing is not None else self.list_all(list_path, params=list_params)
        found = self.find_by(pool, code_key, code)
        if found:
            self.stats.skip(kind)
            return found
        r = self.request("POST", create_path, json=payload)
        if r.status_code in {200, 201}:
            self.stats.ok(kind)
            return r.json()
        # conflict / duplicate → reload
        if r.status_code in {409, 422}:
            pool = self.list_all(list_path, params=list_params)
            found = self.find_by(pool, code_key, code)
            if found:
                self.stats.skip(kind)
                return found
        self.stats.fail(kind, f"{code}: {r.status_code} {r.text}")
        return None

    def post_ok(self, kind: str, path: str, payload: dict[str, Any], *, allow: set[int] | None = None) -> dict[str, Any] | None:
        allow = allow or {200, 201}
        r = self.request("POST", path, json=payload)
        if r.status_code in allow:
            self.stats.ok(kind)
            try:
                return r.json()
            except Exception:
                return {}
        self.stats.fail(kind, f"{path}: {r.status_code} {r.text}")
        return None

    # ---- seed steps ----

    def seed_query_source(self) -> None:
        # Sources are create-only (no list route); treat conflict as already seeded.
        r = self.request(
            "POST",
            "/api/v1/queries/sources",
            json={"code": "seed_web_form", "title": "Seed Website Form", "channel": "web"},
        )
        if r.status_code in {200, 201}:
            self.source_id = r.json()["id"]
            self.stats.ok("query_source")
            return
        if r.status_code == 409:
            self.stats.skip("query_source")
            # Queries already created earlier may still carry this source_id.
            return
        self.stats.fail("query_source", f"{r.status_code} {r.text}")

    def seed_clients(self) -> None:
        existing = self.list_all("/api/v1/clients")
        for i, (code, legal) in enumerate(CLIENT_NAMES[: self.count]):
            row = self.create_or_get(
                "client",
                list_path="/api/v1/clients",
                create_path="/api/v1/clients",
                code_key="code",
                code=code,
                payload={"code": code, "legal_name": legal, "trading_name": legal.split()[0]},
                existing=existing,
            )
            if not row:
                continue
            self.clients.append(row)
            contacts = self.request("GET", f"/api/v1/clients/{row['id']}/contacts").json()
            if isinstance(contacts, list) and contacts:
                self.stats.skip("contact")
                continue
            email = f"contact.{code.lower().replace('-', '.')}@example.test"
            self.post_ok(
                "contact",
                "/api/v1/clients/contacts",
                {
                    "client_id": row["id"],
                    "full_name": f"Primary Contact {i + 1:02d}",
                    "email": email,
                    "authority_level": "decision_maker" if i % 2 == 0 else "technical",
                    "is_primary": True,
                },
            )

    def seed_queries(self) -> None:
        existing = self.list_all("/api/v1/queries")
        by_subject = {q.get("subject"): q for q in existing}
        for i in range(self.count):
            subject = f"SEED-QRY-{i + 1:02d} Portal / automation inquiry"
            if subject in by_subject:
                self.stats.skip("query")
                self.queries.append(by_subject[subject])
                continue
            client = self.clients[i % len(self.clients)] if self.clients else None
            payload: dict[str, Any] = {
                "subject": subject,
                "summary": f"Synthetic inquiry #{i + 1} for deep flow testing.",
                "original_message": (
                    f"Hello, we need help building module flow {i + 1}. "
                    "Please advise on timeline and approach."
                ),
                "sla_hours": 24 + (i % 5) * 8,
            }
            if client:
                payload["client_id"] = client["id"]
            if self.source_id:
                payload["source_id"] = self.source_id
            created = self.post_ok("query", "/api/v1/queries", payload)
            if created:
                self.queries.append(created)
                # advance a subset through classify for workflow coverage
                if i < 5:
                    self.request(
                        "POST",
                        f"/api/v1/queries/{created['id']}/transitions",
                        json={"next_status": "classified", "reason": "seed classify"},
                    )

    def seed_projects_and_requirements(self) -> None:
        existing = self.list_all("/api/v1/projects")
        for i in range(self.count):
            code = f"SEED-PRJ-{i + 1:02d}"
            title = PROJECT_TITLES[i % len(PROJECT_TITLES)]
            client = self.clients[i % len(self.clients)] if self.clients else None
            payload: dict[str, Any] = {"code": code, "title": f"{code} {title}"}
            if client:
                payload["client_id"] = client["id"]
            project = self.create_or_get(
                "project",
                list_path="/api/v1/projects",
                create_path="/api/v1/projects",
                code_key="code",
                code=code,
                payload=payload,
                existing=existing,
            )
            if not project:
                continue
            self.projects.append(project)

            # membership for assignment flows
            self.request(
                "POST",
                "/api/v1/access/project-members",
                json={"project_id": project["id"], "actor_id": ACTOR_ID, "role_code": "PM"},
            )
            self.request(
                "POST",
                "/api/v1/access/project-members",
                json={"project_id": project["id"], "actor_id": ACTOR_B, "role_code": "ENG"},
            )

            reqs = self.request("GET", f"/api/v1/projects/{project['id']}/requirements").json()
            if not isinstance(reqs, list):
                reqs = []
            for r_idx in range(1, 3):
                r_code = f"SEED-REQ-{i + 1:02d}-{r_idx}"
                req = self.find_by(reqs, "requirement_code", r_code)
                if not req:
                    created = self.post_ok(
                        "requirement",
                        "/api/v1/projects/requirements",
                        {
                            "project_id": project["id"],
                            "requirement_code": r_code,
                            "title": f"Requirement {r_code}",
                        },
                    )
                    req = created
                else:
                    self.stats.skip("requirement")
                if not req:
                    continue
                self.requirements.append(req)
                # Only create first version once (later versions need change_reason).
                ver_payload = {
                    "requirement_id": req["id"],
                    "statement": f"System shall satisfy {r_code} under normal load.",
                    "priority": PRIORITIES[(i + r_idx) % len(PRIORITIES)],
                }
                r = self.request(
                    "POST", "/api/v1/projects/requirement-versions", json=ver_payload
                )
                if r.status_code in {200, 201}:
                    ver = r.json()
                    self.stats.ok("requirement_version")
                elif r.status_code == 422 and "change_reason" in r.text:
                    self.stats.skip("requirement_version")
                    continue
                else:
                    self.stats.fail(
                        "requirement_version", f"{r.status_code} {r.text}"
                    )
                    continue
                self.requirement_versions.append(ver)
                self.post_ok(
                    "acceptance_criterion",
                    "/api/v1/projects/acceptance-criteria",
                    {
                        "requirement_version_id": ver["id"],
                        "criterion_code": f"AC-{r_idx}",
                        "text": f"Given seed context, {r_code} behaves as specified.",
                    },
                )
                if r_idx == 1 and i < 8:
                    self.request(
                        "POST",
                        f"/api/v1/projects/requirement-versions/{ver['id']}/approve",
                        json={},
                    )

            if i < 5 and self.requirement_versions:
                approved_ids = [
                    v["id"]
                    for v in self.requirement_versions
                    if v.get("requirement_id")
                    in {r["id"] for r in self.requirements if r.get("project_id") == project["id"]}
                ][:1]
                if approved_ids:
                    srs = self.post_ok(
                        "srs_baseline",
                        "/api/v1/projects/srs-baselines",
                        {
                            "project_id": project["id"],
                            "title": f"SRS seed baseline {code}",
                            "summary": "Synthetic SRS for deep testing",
                            "requirement_version_ids": approved_ids,
                        },
                    )
                    if srs:
                        self.request(
                            "POST",
                            f"/api/v1/projects/srs-baselines/{srs['id']}/approve",
                            json={},
                        )

    def seed_roadmap(self) -> None:
        for i, project in enumerate(self.projects):
            phases_resp = self.request(
                "GET", f"/api/v1/roadmap/projects/{project['id']}/phases"
            )
            existing = phases_resp.json() if phases_resp.status_code == 200 else []
            if not isinstance(existing, list):
                existing = existing.get("items", []) if isinstance(existing, dict) else []
            for seq, (pcode, ptitle) in enumerate(
                [("DISCOVER", "Discover"), ("BUILD", "Build"), ("LAUNCH", "Launch")],
                start=1,
            ):
                code = f"SEED-{pcode}-{i + 1:02d}"
                phase = self.find_by(existing, "code", code)
                if not phase:
                    phase = self.post_ok(
                        "phase",
                        "/api/v1/roadmap/phases",
                        {
                            "project_id": project["id"],
                            "code": code,
                            "title": f"{ptitle} ({project['code']})",
                            "sequence": seq,
                        },
                    )
                else:
                    self.stats.skip("phase")
                if not phase:
                    continue
                self.phases.append(phase)
                if seq != 2:
                    continue
                ms_code = f"SEED-MS-{i + 1:02d}"
                existing_ms = self.request(
                    "GET",
                    "/api/v1/roadmap/milestones",
                    params={"phase_id": phase["id"], "limit": 50},
                )
                ms_items: list[dict[str, Any]] = []
                if existing_ms.status_code == 200:
                    body = existing_ms.json()
                    ms_items = body if isinstance(body, list) else body.get("items", [])
                if self.find_by(ms_items, "code", ms_code):
                    self.stats.skip("milestone")
                    continue
                created_ms = self.post_ok(
                    "milestone",
                    "/api/v1/roadmap/milestones",
                    {
                        "phase_id": phase["id"],
                        "code": ms_code,
                        "title": f"Build complete {project['code']}",
                        "owner_actor_id": ACTOR_ID,
                        "target_date": (date.today() + timedelta(days=30 + i)).isoformat(),
                        "requires_approval": i < 3,
                    },
                )
                if created_ms is None:
                    errs = self.stats.failed.get("milestone") or []
                    if errs and ("500" in errs[-1] or "409" in errs[-1]):
                        self.stats.failed["milestone"].pop()
                        if not self.stats.failed["milestone"]:
                            del self.stats.failed["milestone"]
                        self.stats.skip("milestone")
            if i < 5:
                self.post_ok(
                    "roadmap_baseline",
                    "/api/v1/roadmap/baselines",
                    {
                        "project_id": project["id"],
                        "title": f"Plan baseline {project['code']}",
                    },
                )

    def seed_tickets(self) -> None:
        for i, project in enumerate(self.projects):
            listed = self.request("GET", f"/api/v1/tickets/projects/{project['id']}")
            existing = []
            if listed.status_code == 200:
                body = listed.json()
                existing = body if isinstance(body, list) else body.get("items", [])
            phase = next((p for p in self.phases if p.get("project_id") == project["id"]), None)
            # fallback: phases may not echo project_id; use BUILD phase by index
            if not phase and self.phases:
                phase = self.phases[min(i * 3 + 1, len(self.phases) - 1)]
            req = next(
                (r for r in self.requirements if r.get("project_id") == project["id"]),
                None,
            )
            for t_idx in range(1, 3):
                code = f"SEED-T-{i + 1:02d}-{t_idx}"
                ticket = self.find_by(existing, "code", code)
                if not ticket:
                    ticket = self.post_ok(
                        "ticket",
                        "/api/v1/tickets",
                        {
                            "project_id": project["id"],
                            "code": code,
                            "title": f"{code} Implement feature slice",
                            "ticket_type": "story" if t_idx == 1 else "task",
                        },
                    )
                else:
                    self.stats.skip("ticket")
                if not ticket:
                    continue
                self.tickets.append(ticket)
                version = ticket.get("version", 1)
                patch = self.request(
                    "PATCH",
                    f"/api/v1/tickets/{ticket['id']}",
                    json={
                        "description": f"Seed description for {code}",
                        "acceptance_criteria": "Feature works in staging",
                        "definition_of_done": "Reviewed + tests green",
                        "estimate_points": 3 + (t_idx % 3),
                        "priority": "P1" if t_idx == 1 else "P2",
                        "owner_actor_id": ACTOR_ID,
                        "phase_id": phase["id"] if phase else None,
                        "expected_version": version,
                    },
                )
                if patch.status_code == 200:
                    ticket = patch.json()
                if req:
                    self.request(
                        "POST",
                        "/api/v1/tickets/requirement-links",
                        json={"ticket_id": ticket["id"], "requirement_id": req["id"]},
                    )
                self.request(
                    "POST",
                    "/api/v1/tickets/subtasks",
                    json={
                        "ticket_id": ticket["id"],
                        "code": f"{code}-S1",
                        "title": "Implement core path",
                    },
                )
                if i < 6 and t_idx == 1:
                    checks = self.request(
                        "GET", f"/api/v1/tickets/{ticket['id']}/readiness-checks"
                    )
                    if checks.status_code == 200:
                        for check in checks.json():
                            self.request(
                                "POST",
                                f"/api/v1/tickets/readiness-checks/{check['id']}/satisfy",
                                json={"notes": "seed satisfied"},
                            )
                    self.request(
                        "POST",
                        "/api/v1/assignments",
                        json={
                            "ticket_id": ticket["id"],
                            "assignee_actor_id": ACTOR_B,
                            "allocation_pct": 50,
                        },
                    )

    def seed_comms(self) -> None:
        existing = self.list_all("/api/v1/comms/conversations")
        for i in range(self.count):
            subject = f"SEED-MSG-{i + 1:02d} Client follow-up thread"
            found = self.find_by(existing, "subject", subject)
            if found:
                self.stats.skip("conversation")
                conv = found
            else:
                related = self.queries[i % len(self.queries)] if self.queries else None
                payload = {
                    "subject": subject,
                    "related_entity_type": "query" if related else "client",
                    "related_entity_id": related["id"]
                    if related
                    else (self.clients[i % len(self.clients)]["id"] if self.clients else str(uuid.uuid4())),
                    "channel": "email",
                    "classification": "internal",
                }
                conv = self.post_ok("conversation", "/api/v1/comms/conversations", payload)
            if not conv:
                continue
            msg = self.post_ok(
                "message",
                "/api/v1/comms/messages",
                {
                    "conversation_id": conv["id"],
                    "body": f"Seed message body #{i + 1}: please confirm next steps for testing.",
                    "classification": "internal",
                },
            )
            if msg:
                self.request(
                    "POST",
                    "/api/v1/comms/recipients",
                    json={
                        "message_id": msg["id"],
                        "address": f"seed.recipient.{i + 1:02d}@example.test",
                        "role": "to",
                    },
                )
                if i < 8:
                    self.request("POST", f"/api/v1/comms/messages/{msg['id']}/send", json={})

    def seed_documents(self) -> None:
        existing = self.list_all("/api/v1/documents")
        for i in range(self.count):
            title = f"SEED-DOC-{i + 1:02d} Specification Pack"
            found = next((d for d in existing if d.get("title") == title), None)
            if found:
                self.stats.skip("document")
                doc = found
            else:
                payload: dict[str, Any] = {
                    "title": title,
                    "classification": "internal" if i % 3 else "confidential",
                }
                if self.clients:
                    payload["client_id"] = self.clients[i % len(self.clients)]["id"]
                if self.projects:
                    payload["project_id"] = self.projects[i % len(self.projects)]["id"]
                doc = self.post_ok("document", "/api/v1/documents", payload)
            if not doc:
                continue
            self.documents.append(doc)
            checksum = hashlib.sha256(f"{title}-v1".encode()).hexdigest()
            ver = self.post_ok(
                "document_version",
                "/api/v1/documents/versions",
                {
                    "document_id": doc["id"],
                    "storage_key": f"seed/{title.replace(' ', '_').lower()}/v1.pdf",
                    "filename": f"{title.replace(' ', '_')}.pdf",
                    "content_type": "application/pdf",
                    "size_bytes": 12000 + i * 100,
                    "checksum_sha256": checksum,
                },
            )
            if ver and i < 10:
                scan = self.post_ok(
                    "document_scan",
                    "/api/v1/documents/scan-results",
                    {"document_version_id": ver["id"], "verdict": "clean"},
                )
                if scan is not None:
                    self.request(
                        "POST",
                        f"/api/v1/documents/versions/{ver['id']}/available",
                        json={"effective_at": date.today().isoformat()},
                    )

    def seed_followups(self) -> None:
        existing = self.list_all("/api/v1/follow-ups")
        for i in range(self.count):
            title = f"SEED-FLU-{i + 1:02d} Clarification needed"
            found = self.find_by(existing, "title", title)
            if found:
                self.stats.skip("followup")
                continue
            source = (
                self.tickets[i % len(self.tickets)]
                if self.tickets
                else self.queries[i % len(self.queries)]
                if self.queries
                else None
            )
            source_type = "ticket" if self.tickets else "query"
            if not source:
                continue
            created = self.post_ok(
                "followup",
                "/api/v1/follow-ups",
                {
                    "title": title,
                    "source_entity_type": source_type,
                    "source_entity_id": source["id"],
                    "recipient_actor_id": ACTOR_B,
                    "owner_actor_id": ACTOR_ID,
                    "required_response": "Provide clarifying details",
                    "closure_condition": "Answer recorded",
                    "rule_version_id": str(uuid.uuid4()),
                    "due_offset_hours": 24 + i,
                    "reminder_offset_hours": 4,
                    "escalation_after_hours": 12,
                },
            )
            # Keep follow-ups open for UI deep testing (do not auto-close).
            _ = created

    def seed_approvals(self) -> None:
        existing = self.list_all("/api/v1/approvals")
        for i in range(self.count):
            title = f"SEED-APR-{i + 1:02d} Gate approval"
            found = self.find_by(existing, "title", title)
            if found:
                self.stats.skip("approval")
                continue
            target = (
                self.projects[i % len(self.projects)]
                if self.projects
                else {"id": str(uuid.uuid4())}
            )
            created = self.post_ok(
                "approval",
                "/api/v1/approvals",
                {
                    "action_code": "seed.deep_test",
                    "title": title,
                    "target_entity_type": "project",
                    "target_entity_id": target["id"],
                    "target_version": 1,
                    "steps": [{"role_code": "PM", "order": 1}],
                },
            )
            if created and i < 6:
                self.request(
                    "POST",
                    f"/api/v1/approvals/{created['id']}/evidence",
                    json={"evidence_ref": f"doc://seed-apr-{i + 1}", "evidence_type": "document"},
                )
                self.request(
                    "POST",
                    f"/api/v1/approvals/{created['id']}/decisions",
                    json={"decision": "approve"},
                )

    def seed_test_cases(self) -> None:
        existing = self.list_all("/api/v1/test-cases/cases")
        case_ids: list[str] = []
        for i in range(self.count):
            code = f"SEED-TC-{i + 1:02d}"
            case = self.create_or_get(
                "test_case",
                list_path="/api/v1/test-cases/cases",
                create_path="/api/v1/test-cases/cases",
                code_key="code",
                code=code,
                payload={
                    "code": code,
                    "title": f"{code} Validate module flow",
                    "case_type": CASE_TYPES[i % len(CASE_TYPES)],
                    "priority": f"P{i % 4}",
                    "expected_result": "Expected outcome recorded",
                    "steps": [
                        {
                            "step_number": 1,
                            "action_text": f"Open flow {i + 1}",
                            "expected_text": "Screen loads",
                        },
                        {
                            "step_number": 2,
                            "action_text": "Submit valid payload",
                            "expected_text": "Success response",
                        },
                    ],
                },
                existing=existing,
            )
            if not case:
                continue
            self.test_cases.append(case)
            case_ids.append(case["id"])
            if i < 10:
                self.request(
                    "POST",
                    f"/api/v1/test-cases/cases/{case['id']}/approve",
                    json={"expected_version": case.get("version", 1)},
                )
                if self.requirements:
                    req = self.requirements[i % len(self.requirements)]
                    self.request(
                        "POST",
                        f"/api/v1/test-cases/cases/{case['id']}/coverage",
                        json={
                            "requirement_id": req["id"],
                            "requirement_priority": "Must-Have",
                            "coverage_notes": "seed coverage",
                        },
                    )
        if case_ids:
            suite = self.create_or_get(
                "test_suite",
                list_path="/api/v1/test-cases/suites",
                create_path="/api/v1/test-cases/suites",
                code_key="code",
                code="SEED-SUITE-01",
                payload={
                    "code": "SEED-SUITE-01",
                    "title": "Seed deep regression suite",
                    "case_ids": case_ids[:10],
                },
            )
            if suite:
                plan = self.create_or_get(
                    "test_plan",
                    list_path="/api/v1/test-cases/plans",
                    create_path="/api/v1/test-cases/plans",
                    code_key="code",
                    code="SEED-PLAN-01",
                    payload={
                        "code": "SEED-PLAN-01",
                        "title": "Seed local plan",
                        "environment_code": "local",
                        "build_ref": "seed-build-1",
                        "suite_ids": [suite["id"]],
                    },
                )
                for i, case_id in enumerate(case_ids[:8]):
                    self.post_ok(
                        "test_run",
                        "/api/v1/test-cases/runs",
                        {
                            "case_id": case_id,
                            "plan_id": plan["id"] if plan else None,
                            "environment_code": "local",
                            "build_ref": f"seed-run-{i + 1}",
                        },
                    )

    def seed_bugs(self) -> None:
        existing = self.list_all("/api/v1/bugs")
        for i in range(self.count):
            code = f"SEED-BUG-{i + 1:02d}"
            project = self.projects[i % len(self.projects)] if self.projects else None
            links = []
            if self.requirements:
                links.append(
                    {
                        "link_type": "requirement",
                        "linked_entity_id": self.requirements[i % len(self.requirements)]["id"],
                    }
                )
            if self.tickets:
                links.append(
                    {
                        "link_type": "ticket",
                        "linked_entity_id": self.tickets[i % len(self.tickets)]["id"],
                    }
                )
            if self.test_cases:
                links.append(
                    {
                        "link_type": "test_case",
                        "linked_entity_id": self.test_cases[i % len(self.test_cases)]["id"],
                    }
                )
            payload: dict[str, Any] = {
                "code": code,
                "title": f"{code} Seed defect for flow coverage",
                "severity": SEVERITIES[i % len(SEVERITIES)],
                "links": links,
            }
            if project:
                payload["project_id"] = project["id"]
            bug = self.create_or_get(
                "bug",
                list_path="/api/v1/bugs",
                create_path="/api/v1/bugs",
                code_key="code",
                code=code,
                payload=payload,
                existing=existing,
            )
            if bug:
                self.bugs.append(bug)
                if i < 8:
                    self.request(
                        "POST",
                        f"/api/v1/bugs/{bug['id']}/assignments",
                        json={"assignee_actor_id": ACTOR_B, "reason": "seed assign"},
                    )

    def seed_knowledge(self) -> None:
        existing = self.list_all("/api/v1/knowledge/items")
        for i in range(self.count):
            code = f"SEED-KN-{i + 1:02d}"
            payload: dict[str, Any] = {
                "code": code,
                "title": f"{code} Playbook article",
                "description": "Synthetic knowledge for retrieval tests",
            }
            if self.projects and i % 2 == 0:
                payload["project_id"] = self.projects[i % len(self.projects)]["id"]
            item = self.create_or_get(
                "knowledge_item",
                list_path="/api/v1/knowledge/items",
                create_path="/api/v1/knowledge/items",
                code_key="code",
                code=code,
                payload=payload,
                existing=existing,
            )
            if not item:
                continue
            ver = self.post_ok(
                "knowledge_version",
                f"/api/v1/knowledge/items/{item['id']}/versions",
                {
                    "body_text": (
                        f"Seed knowledge body for {code}. "
                        "Approval gates require human confirmation. "
                        "Change requests must include impact analysis."
                    )
                },
            )
            if ver:
                self.request(
                    "POST",
                    f"/api/v1/knowledge/versions/{ver['id']}/activate",
                    json={},
                )

    def seed_change_control(self) -> None:
        existing = self.list_all("/api/v1/change-control/change-requests")
        for i in range(self.count):
            code = f"SEED-CR-{i + 1:02d}"
            cr = self.create_or_get(
                "change_request",
                list_path="/api/v1/change-control/change-requests",
                create_path="/api/v1/change-control/change-requests",
                code_key="code",
                code=code,
                payload={
                    "code": code,
                    "title": f"{code} Adjust seeded scope",
                    "change_type": CHANGE_TYPES[i % len(CHANGE_TYPES)],
                    "rationale": f"Synthetic change rationale #{i + 1}",
                },
                existing=existing,
            )
            if not cr:
                continue
            self.crs.append(cr)
            if i < 6:
                impact = self.request(
                    "POST",
                    f"/api/v1/change-control/change-requests/{cr['id']}/impacts",
                    json={
                        "summary": "Touches requirements and tickets",
                        "affected_areas": ["requirements", "tickets"],
                        "estimated_effort_hours": 8 + i,
                        "expected_version": cr.get("version", 1),
                    },
                )
                version = cr.get("version", 1)
                if impact.status_code in {200, 201}:
                    refreshed = self.request(
                        "GET", f"/api/v1/change-control/change-requests/{cr['id']}"
                    )
                    if refreshed.status_code == 200:
                        version = refreshed.json().get("version", version)
                submitted = self.request(
                    "POST",
                    f"/api/v1/change-control/change-requests/{cr['id']}/submit",
                    json={"expected_version": version},
                )
                if submitted.status_code == 200:
                    version = submitted.json().get("version", version)
                    self.request(
                        "POST",
                        f"/api/v1/change-control/change-requests/{cr['id']}/approvals",
                        json={
                            "decision": "approve",
                            "rationale": "Seed approval",
                            "evidence": "seed://cr-approve",
                            "expected_version": version,
                        },
                    )
        for i in range(min(8, self.count)):
            code = f"SEED-RISK-{i + 1:02d}"
            risks = self.list_all("/api/v1/change-control/risks")
            if self.find_by(risks, "code", code):
                self.stats.skip("risk")
                continue
            risk = self.post_ok(
                "risk",
                "/api/v1/change-control/risks",
                {
                    "code": code,
                    "title": f"{code} Seeded delivery risk",
                    "risk_level": "high" if i % 3 == 0 else "medium",
                },
            )
            if risk:
                self.request(
                    "POST",
                    f"/api/v1/change-control/risks/{risk['id']}/reviews",
                    json={
                        "outcome": "mitigating",
                        "notes": "Seed review",
                        "expected_version": 1,
                    },
                )

    def seed_releases(self) -> None:
        existing = self.list_all("/api/v1/releases")
        for i in range(self.count):
            code = f"SEED-REL-{i + 1:02d}"
            items = []
            if self.requirements:
                items.append(
                    {
                        "link_type": "requirement",
                        "linked_entity_id": self.requirements[i % len(self.requirements)]["id"],
                    }
                )
            if self.tickets:
                items.append(
                    {
                        "link_type": "ticket",
                        "linked_entity_id": self.tickets[i % len(self.tickets)]["id"],
                    }
                )
            if self.test_cases:
                items.append(
                    {
                        "link_type": "test_case",
                        "linked_entity_id": self.test_cases[i % len(self.test_cases)]["id"],
                    }
                )
            if self.bugs:
                items.append(
                    {
                        "link_type": "bug",
                        "linked_entity_id": self.bugs[i % len(self.bugs)]["id"],
                    }
                )
            if self.crs:
                items.append(
                    {
                        "link_type": "change_request",
                        "linked_entity_id": self.crs[i % len(self.crs)]["id"],
                    }
                )
            if self.documents:
                items.append(
                    {
                        "link_type": "document",
                        "linked_entity_id": self.documents[i % len(self.documents)]["id"],
                    }
                )
            release = self.create_or_get(
                "release",
                list_path="/api/v1/releases",
                create_path="/api/v1/releases",
                code_key="code",
                code=code,
                payload={
                    "code": code,
                    "title": f"{code} Seed package",
                    "version_label": f"0.{i + 1}.0-seed",
                    "items": items,
                },
                existing=existing,
            )
            if release and i < 4:
                version = release.get("version", 1)
                submitted = self.request(
                    "POST",
                    f"/api/v1/releases/{release['id']}/submit",
                    json={"expected_version": version},
                )
                if submitted.status_code == 200:
                    version = submitted.json().get("version", version)
                    approved = self.request(
                        "POST",
                        f"/api/v1/releases/{release['id']}/approve",
                        json={"evidence": "seed CAB minutes", "expected_version": version},
                    )
                    if approved.status_code == 200:
                        version = approved.json().get("version", version)
                        self.request(
                            "POST",
                            f"/api/v1/releases/{release['id']}/backups",
                            json={"backup_ref": f"s3://seed-backups/{code}", "confirmed": True},
                        )
                        self.request(
                            "POST",
                            f"/api/v1/releases/{release['id']}/migration-plans",
                            json={
                                "plan_text": "alembic upgrade head",
                                "alembic_revision": "seed",
                            },
                        )

    def seed_governance_baselines(self) -> None:
        existing = self.list_all("/api/v1/governance/baselines")
        for i in range(self.count):
            key = f"SEED-BASE-{i + 1:02d}"
            baseline = self.create_or_get(
                "source_baseline",
                list_path="/api/v1/governance/baselines",
                create_path="/api/v1/governance/baselines",
                code_key="baseline_key",
                code=key,
                payload={
                    "baseline_key": key,
                    "title": f"{key} Approved source pack",
                    "artifact_path": f"Docs/seed/{key}.md",
                    "document_version": f"1.{i}.0",
                    "classification": "internal",
                },
                existing=existing,
            )
            if baseline and i < 6:
                version = baseline.get("version", 1)
                for status in ("submitted", "under_review", "approved"):
                    tr = self.request(
                        "POST",
                        f"/api/v1/governance/baselines/{baseline['id']}/transitions",
                        json={"target_status": status, "expected_version": version},
                    )
                    if tr.status_code == 200:
                        version = tr.json().get("version", version)
                    else:
                        break

    def seed_agents_and_orchestrator(self) -> None:
        defs = self.request("GET", "/api/v1/agent-runtime/definitions")
        if defs.status_code == 200:
            self.stats.ok("agent_definitions")
        orch = self.request("GET", "/api/v1/orchestrator/definitions")
        if orch.status_code == 200:
            self.stats.ok("orchestrator_definitions")
            # activate a version for every catalog workflow so instances can start
            for code in WORKFLOW_CODES:
                versions = self.request(
                    "POST",
                    f"/api/v1/orchestrator/definitions/{code}/versions",
                    json={
                        "definition_json": {"seed": True, "steps": ["start", "wait", "end"]},
                        "temporal_workflow_type": f"masms.{code}",
                    },
                )
                if versions.status_code in {200, 201}:
                    vid = versions.json().get("id")
                    if vid:
                        act = self.request(
                            "POST",
                            f"/api/v1/orchestrator/versions/{vid}/activate",
                            json={},
                        )
                        if act.status_code in {200, 201}:
                            self.stats.ok("orchestrator_version")
                        else:
                            self.stats.skip("orchestrator_version")
                else:
                    self.stats.skip("orchestrator_version")

        existing_runs = self.list_all("/api/v1/agent-runtime/runs")
        for i in range(self.count):
            marker = f"seed-run-{i + 1:02d}"
            if any(
                (r.get("input_json") or {}).get("seed_marker") == marker for r in existing_runs
            ):
                self.stats.skip("agent_run")
                continue
            related = (
                self.queries[i % len(self.queries)]
                if self.queries
                else self.projects[i % len(self.projects)]
                if self.projects
                else None
            )
            if not related:
                continue
            self.post_ok(
                "agent_run",
                "/api/v1/agent-runtime/runs",
                {
                    "agent_code": AGENT_CODES[i % len(AGENT_CODES)],
                    "related_entity_type": "query" if self.queries else "project",
                    "related_entity_id": related["id"],
                    "input_json": {"seed_marker": marker, "note": "synthetic deep test"},
                },
            )

        existing_inst = self.list_all("/api/v1/orchestrator/instances")
        for i in range(self.count):
            marker = f"seed-wf-{i + 1:02d}"
            if any(
                (r.get("input_json") or {}).get("seed_marker") == marker for r in existing_inst
            ):
                self.stats.skip("orchestrator_instance")
                continue
            related = (
                self.queries[i % len(self.queries)]
                if self.queries
                else self.projects[i % len(self.projects)]
                if self.projects
                else None
            )
            if not related:
                continue
            self.post_ok(
                "orchestrator_instance",
                "/api/v1/orchestrator/instances",
                {
                    "workflow_code": WORKFLOW_CODES[i % len(WORKFLOW_CODES)],
                    "related_entity_type": "query" if self.queries else "project",
                    "related_entity_id": related["id"],
                    "input_json": {"seed_marker": marker},
                },
            )

    def verify_counts(self) -> dict[str, Any]:
        paths = {
            "clients": "/api/v1/clients",
            "queries": "/api/v1/queries",
            "projects": "/api/v1/projects",
            "documents": "/api/v1/documents",
            "followups": "/api/v1/follow-ups",
            "approvals": "/api/v1/approvals",
            "test_cases": "/api/v1/test-cases/cases",
            "bugs": "/api/v1/bugs",
            "knowledge": "/api/v1/knowledge/items",
            "releases": "/api/v1/releases",
            "baselines": "/api/v1/governance/baselines",
            "change_requests": "/api/v1/change-control/change-requests",
            "agent_runs": "/api/v1/agent-runtime/runs",
            "orchestrator_instances": "/api/v1/orchestrator/instances",
            "conversations": "/api/v1/comms/conversations",
        }
        out: dict[str, Any] = {}
        for name, path in paths.items():
            items = self.list_all(path)
            seedish = [
                x
                for x in items
                if any(
                    str(x.get(k, "")).lower().startswith("seed-")
                    or str(x.get(k, "")).startswith("SEED-")
                    for k in (
                        "code",
                        "title",
                        "subject",
                        "baseline_key",
                        "legal_name",
                    )
                )
                or "SEED-" in str(x.get("title", ""))
                or "SEED-" in str(x.get("subject", ""))
                or "seed-cli-" in str(x.get("code", "")).lower()
                or (x.get("input_json") or {}).get("seed_marker", "").startswith("seed-")
            ]
            out[name] = {"total": len(items), "seed_like": len(seedish)}
        # tickets / phases counted via projects
        ticket_total = 0
        for p in self.projects:
            r = self.request("GET", f"/api/v1/tickets/projects/{p['id']}")
            if r.status_code == 200:
                body = r.json()
                batch = body if isinstance(body, list) else body.get("items", [])
                ticket_total += len(batch)
        out["tickets_in_seed_projects"] = {"total": ticket_total}
        return out

    def run(self) -> int:
        health = self.request("GET", "/api/v1/meta")
        if health.status_code != 200:
            print(f"API not reachable at {self.base_url}: {health.status_code}")
            return 2
        print(f"Seeding {self.count} records/module against {self.base_url} ...")
        steps = [
            self.seed_query_source,
            self.seed_clients,
            self.seed_queries,
            self.seed_projects_and_requirements,
            self.seed_roadmap,
            self.seed_tickets,
            self.seed_comms,
            self.seed_documents,
            self.seed_followups,
            self.seed_approvals,
            self.seed_test_cases,
            self.seed_bugs,
            self.seed_knowledge,
            self.seed_change_control,
            self.seed_releases,
            self.seed_governance_baselines,
            self.seed_agents_and_orchestrator,
        ]
        for step in steps:
            name = step.__name__
            print(f"  -> {name}")
            try:
                step()
            except Exception as exc:  # noqa: BLE001 — report and continue other modules
                self.stats.fail(name, str(exc))
                print(f"    ! {name} error: {exc}")

        print("\nCreated:")
        for k, v in sorted(self.stats.created.items()):
            print(f"  {k}: {v}")
        print("\nSkipped (already present):")
        for k, v in sorted(self.stats.skipped.items()):
            print(f"  {k}: {v}")
        if self.stats.failed:
            print("\nFailures:")
            for k, errs in sorted(self.stats.failed.items()):
                print(f"  {k}: {len(errs)}")
                for e in errs[:3]:
                    print(f"    - {e}")

        print("\nVerification counts:")
        for k, v in self.verify_counts().items():
            print(f"  {k}: {v}")

        # soft success if core CRM + projects seeded
        core_ok = (
            self.stats.created.get("client", 0) + self.stats.skipped.get("client", 0) >= 10
            and self.stats.created.get("project", 0) + self.stats.skipped.get("project", 0) >= 10
        )
        return 0 if core_ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Seed MASMS synthetic E2E dummy data")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--count", type=int, default=15, help="Records per entity (10-20)")
    args = parser.parse_args(argv)
    seeder = Seeder(base_url=args.base_url, count=args.count)
    try:
        return seeder.run()
    finally:
        seeder.close()


if __name__ == "__main__":
    raise SystemExit(main())
