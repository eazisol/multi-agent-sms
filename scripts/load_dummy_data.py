#!/usr/bin/env python3
"""Load realistic dummy data (up to 20 records per entity) for local UI testing.

Wipes previous local Postgres rows (default), then creates linked records via
the running MASMS API. Synthetic data only — no real PII or secrets.

Usage (API must be up, Postgres migrated):

  .\\.venv\\Scripts\\python.exe scripts/load_dummy_data.py
  .\\.venv\\Scripts\\python.exe scripts/load_dummy_data.py --count 20 --wipe
  .\\.venv\\Scripts\\python.exe scripts/load_dummy_data.py --no-wipe
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
import uuid
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dummy_catalogs import (  # noqa: E402
    ADRS,
    AGENT_CODES,
    APPROVAL_ACTIONS,
    BUGS,
    CLIENTS,
    CONFIG_WORKFLOW_CODES,
    CONTACTS,
    DEPARTMENTS,
    IDENTITY_AGENT_KEYS,
    KNOWLEDGE,
    NOTIFICATIONS,
    PEOPLE,
    PERMISSIONS,
    PROJECTS,
    QUERIES,
    QUERY_SOURCES,
    ROLES,
    SKILLS,
    TEAMS,
    WORKFLOW_CODES,
)

ORG_ID = "00000000-0000-4000-8000-000000000001"
ACTOR_ID = "00000000-0000-4000-8000-000000000101"
DEFAULT_DB = "postgresql+psycopg://masms:masms_dev_only@localhost:5432/masms"


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


def wipe_local_database(url: str) -> None:
    from sqlalchemy import create_engine, text

    engine = create_engine(url)
    with engine.begin() as conn:
        rows = conn.execute(
            text(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname = 'public' AND tablename <> 'alembic_version'"
            )
        ).fetchall()
        names = [row[0] for row in rows]
        if not names:
            print("Wipe: no application tables found")
            return
        quoted = ", ".join(f'"{name}"' for name in names)
        conn.execute(text(f"TRUNCATE TABLE {quoted} CASCADE"))
        conn.execute(
            text(
                """
                INSERT INTO org_organizations (
                    id, name, slug, status, version,
                    created_by_actor_id, updated_by_actor_id, metadata
                ) VALUES (
                    :org_id, 'Eazisols', 'eazisols', 'active', 1,
                    :actor_id, :actor_id, CAST(:meta AS json)
                )
                """
            ),
            {"org_id": ORG_ID, "actor_id": ACTOR_ID, "meta": "{}"},
        )
        conn.execute(
            text(
                """
                INSERT INTO org_actors (
                    id, organization_id, actor_kind, display_name, status, version,
                    created_by_actor_id, updated_by_actor_id
                ) VALUES (
                    :actor_id, :org_id, 'human', 'Session Operator', 'active', 1,
                    :actor_id, :actor_id
                )
                """
            ),
            {"org_id": ORG_ID, "actor_id": ACTOR_ID},
        )
    print(f"Wipe: truncated {len(names)} tables and restored default org/actor")


class Loader:
    def __init__(self, base_url: str, count: int) -> None:
        self.base_url = base_url.rstrip("/")
        self.count = max(1, min(count, 20))
        self.stats = Stats()
        self.client = httpx.Client(base_url=self.base_url, timeout=60.0)
        self.humans: list[dict[str, Any]] = []
        self.roles: list[dict[str, Any]] = []
        self.teams: list[dict[str, Any]] = []
        self.skills: list[dict[str, Any]] = []
        self.clients: list[dict[str, Any]] = []
        self.queries: list[dict[str, Any]] = []
        self.opportunities: list[dict[str, Any]] = []
        self.projects: list[dict[str, Any]] = []
        self.requirements: list[dict[str, Any]] = []
        self.phases: list[dict[str, Any]] = []
        self.tickets: list[dict[str, Any]] = []
        self.documents: list[dict[str, Any]] = []
        self.test_cases: list[dict[str, Any]] = []
        self.conversations: list[dict[str, Any]] = []
        self.config_version_id: str | None = None
        self.source_id: str | None = None
        self.source_ids: list[str] = []

    def close(self) -> None:
        self.client.close()

    def headers(self) -> dict[str, str]:
        return {
            "X-Organization-Id": ORG_ID,
            "X-Actor-Id": ACTOR_ID,
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
        retries: int = 3,
    ) -> httpx.Response:
        last_exc: Exception | None = None
        for attempt in range(retries):
            try:
                return self.client.request(
                    method, path, headers=self.headers(), json=json, params=params
                )
            except (httpx.TransportError, ConnectionError, OSError) as exc:
                last_exc = exc
                self.client.close()
                self.client = httpx.Client(base_url=self.base_url, timeout=60.0)
                if attempt == retries - 1:
                    raise
        raise RuntimeError(str(last_exc))

    def post_ok(self, kind: str, path: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        r = self.request("POST", path, json=payload)
        if r.status_code in {200, 201}:
            self.stats.ok(kind)
            try:
                return r.json()
            except Exception:
                return {}
        if r.status_code in {409, 422} and "already" in r.text.lower():
            self.stats.skip(kind)
            return None
        self.stats.fail(kind, f"{path}: {r.status_code} {r.text}")
        return None

    def take(self, rows: list[Any]) -> list[Any]:
        return rows[: self.count]

    def load_identity(self) -> None:
        for code, title in self.take(ROLES):
            row = self.post_ok(
                "role", "/api/v1/identity/roles", {"code": code, "title": title}
            )
            if row:
                self.roles.append(row)
        dept_ids: dict[str, str] = {}
        for code, name in DEPARTMENTS:
            row = self.post_ok(
                "department",
                "/api/v1/identity/departments",
                {"code": code, "name": name},
            )
            if row:
                dept_ids[code] = row["id"]
        for code, name, dept in self.take(TEAMS):
            payload: dict[str, Any] = {"code": code, "name": name}
            if dept in dept_ids:
                payload["department_id"] = dept_ids[dept]
            row = self.post_ok("team", "/api/v1/identity/teams", payload)
            if row:
                self.teams.append(row)
        for full_name, email, role in self.take(PEOPLE):
            row = self.post_ok(
                "human",
                "/api/v1/identity/humans",
                {
                    "email": email,
                    "full_name": full_name,
                    "primary_role_code": role,
                },
            )
            if row:
                self.humans.append(row)
        for i, human in enumerate(self.humans):
            if not self.teams:
                break
            team = self.teams[i % len(self.teams)]
            self.post_ok(
                "team_member",
                "/api/v1/identity/team-members",
                {
                    "team_id": team["id"],
                    "actor_id": human["actor_id"],
                    "membership_role": "member" if i else "lead",
                },
            )
        manager = self.humans[-1] if self.humans else None
        if manager:
            for human in self.humans[:-1]:
                self.post_ok(
                    "reporting_line",
                    "/api/v1/identity/reporting-lines",
                    {
                        "subordinate_actor_id": human["actor_id"],
                        "manager_actor_id": manager["actor_id"],
                        "effective_from": datetime(2026, 1, 1, tzinfo=UTC).isoformat(),
                    },
                )
        supervisor_id = self.humans[0]["id"] if self.humans else None
        if supervisor_id:
            for code in self.take(IDENTITY_AGENT_KEYS):
                self.post_ok(
                    "agent",
                    "/api/v1/identity/agents",
                    {
                        "agent_key": code,
                        "display_name": code.replace("_", " ").title(),
                        "supervisor_human_user_id": supervisor_id,
                    },
                )

    def load_access_and_capacity(self) -> None:
        perms: list[dict[str, Any]] = []
        for code, module_key, action_key, title in self.take(PERMISSIONS):
            row = self.post_ok(
                "permission",
                "/api/v1/access/permissions",
                {
                    "code": code,
                    "module_key": module_key,
                    "action_key": action_key,
                    "title": title,
                },
            )
            if row:
                perms.append(row)
        for i, role in enumerate(self.roles):
            if not perms:
                break
            perm = perms[i % len(perms)]
            self.post_ok(
                "role_permission",
                "/api/v1/access/role-permissions",
                {"role_id": role["id"], "permission_id": perm["id"]},
            )
        for code, title, category in self.take(SKILLS):
            row = self.post_ok(
                "skill",
                "/api/v1/capacity/skills",
                {"code": code, "title": title, "category": category},
            )
            if row:
                self.skills.append(row)
        for i, human in enumerate(self.humans):
            if self.skills:
                skill = self.skills[i % len(self.skills)]
                self.post_ok(
                    "actor_skill",
                    "/api/v1/capacity/actor-skills",
                    {
                        "actor_id": human["actor_id"],
                        "skill_id": skill["id"],
                        "proficiency": 2 + (i % 4),
                    },
                )
            self.post_ok(
                "allocation",
                "/api/v1/capacity/allocations",
                {
                    "actor_id": human["actor_id"],
                    "allocation_pct": str(20 + (i % 6) * 10),
                    "effective_from": date(2026, 8, 1).isoformat(),
                },
            )
            self.post_ok(
                "availability",
                "/api/v1/capacity/availability",
                {
                    "actor_id": human["actor_id"],
                    "weekday": i % 5,
                    "start_time": "09:00:00",
                    "end_time": "18:00:00",
                    "timezone": "Asia/Karachi",
                },
            )
            self.post_ok(
                "leave",
                "/api/v1/capacity/leave",
                {
                    "actor_id": human["actor_id"],
                    "leave_type": ["annual", "sick", "casual"][i % 3],
                    "starts_on": date(2026, 9, 1 + (i % 20)).isoformat(),
                    "ends_on": date(2026, 9, 2 + (i % 20)).isoformat(),
                    "notes": "Planned leave for local testing",
                },
            )
            start = datetime(2026, 8, 18, 9, 0, tzinfo=UTC) + timedelta(days=i)
            self.post_ok(
                "oncall",
                "/api/v1/capacity/oncall",
                {
                    "actor_id": human["actor_id"],
                    "rotation_name": f"Delivery on-call week {i + 1}",
                    "starts_at": start.isoformat(),
                    "ends_at": (start + timedelta(days=7)).isoformat(),
                },
            )
        for i in range(self.count):
            cal = self.post_ok(
                "calendar",
                "/api/v1/capacity/calendars",
                {
                    "code": f"pk_cal_{i + 1:02d}",
                    "title": f"Pakistan delivery calendar {i + 1}",
                    "timezone": "Asia/Karachi",
                },
            )
            if cal:
                self.post_ok(
                    "holiday",
                    "/api/v1/capacity/holidays",
                    {
                        "calendar_id": cal["id"],
                        "holiday_date": date(2026, 8, 14).isoformat()
                        if i % 2 == 0
                        else date(2026, 12, 25).isoformat(),
                        "title": "Independence Day" if i % 2 == 0 else "Public holiday",
                    },
                )

    def load_config(self) -> None:
        version = self.post_ok(
            "config_version",
            "/api/v1/config/versions",
            {
                "title": "Eazisols delivery configuration v1",
                "change_reason": "Baseline workflow, follow-up, and approval rules for local testing",
            },
        )
        if not version:
            return
        vid = version["id"]
        self.config_version_id = vid
        for i, code in enumerate(self.take(CONFIG_WORKFLOW_CODES)):
            wf = self.post_ok(
                "config_workflow",
                "/api/v1/config/workflows",
                {
                    "configuration_version_id": vid,
                    "code": code,
                    "title": code.replace("_", " ").title(),
                    "entity_type": "query" if i % 2 == 0 else "ticket",
                    "description": f"Configured {code.replace('_', ' ')} path for delivery work.",
                },
            )
            if wf:
                self.post_ok(
                    "config_status",
                    "/api/v1/config/statuses",
                    {
                        "configuration_version_id": vid,
                        "workflow_definition_id": wf["id"],
                        "code": "open",
                        "title": "Open",
                        "sort_order": 1,
                    },
                )
                if i < 10:
                    closed = self.post_ok(
                        "config_status",
                        "/api/v1/config/statuses",
                        {
                            "configuration_version_id": vid,
                            "workflow_definition_id": wf["id"],
                            "code": "closed",
                            "title": "Closed",
                            "is_terminal": True,
                            "sort_order": 2,
                        },
                    )
                    if closed:
                        self.post_ok(
                            "config_transition",
                            "/api/v1/config/transitions",
                            {
                                "configuration_version_id": vid,
                                "workflow_definition_id": wf["id"],
                                "from_status_code": "open",
                                "to_status_code": "closed",
                                "requires_reason": i % 3 == 0,
                            },
                        )
            self.post_ok(
                "followup_rule",
                "/api/v1/config/followup-rules",
                {
                    "configuration_version_id": vid,
                    "workflow_code": code,
                    "trigger_status_code": "open",
                    "due_offset_hours": 24 + i,
                    "required_response": "Written confirmation of next action",
                },
            )
            self.post_ok(
                "reminder_rule",
                "/api/v1/config/reminder-rules",
                {
                    "configuration_version_id": vid,
                    "workflow_code": code,
                    "offset_hours_before_due": 4,
                    "channel": "in_app",
                },
            )
            self.post_ok(
                "escalation_rule",
                "/api/v1/config/escalation-rules",
                {
                    "configuration_version_id": vid,
                    "workflow_code": code,
                    "after_hours_overdue": 24,
                    "escalate_to_role_code": "pm",
                },
            )
            self.post_ok(
                "approval_workflow",
                "/api/v1/config/approval-workflows",
                {
                    "configuration_version_id": vid,
                    "code": f"gate_{code}",
                    "title": f"Approve {code.replace('_', ' ')}",
                    "action_code": APPROVAL_ACTIONS[i % len(APPROVAL_ACTIONS)],
                    "steps": [{"role_code": "pm", "order": 1}],
                },
            )
        approved = self.request("POST", f"/api/v1/config/versions/{vid}/approve", json={})
        if approved.status_code == 200:
            self.stats.ok("config_version_approve")
            activated = self.request("POST", f"/api/v1/config/versions/{vid}/activate", json={})
            if activated.status_code == 200:
                self.stats.ok("config_version_activate")
            else:
                self.stats.fail(
                    "config_version_activate", f"{activated.status_code} {activated.text}"
                )
        else:
            self.stats.fail("config_version_approve", f"{approved.status_code} {approved.text}")

    def load_clients_queries_opportunities(self) -> None:
        for code, title, channel in self.take(QUERY_SOURCES):
            source = self.post_ok(
                "query_source",
                "/api/v1/queries/sources",
                {"code": code, "title": title, "channel": channel},
            )
            if source:
                self.source_ids.append(source["id"])
        self.source_id = self.source_ids[0] if self.source_ids else None
        for i, (code, legal, industry, website) in enumerate(self.take(CLIENTS)):
            row = self.post_ok(
                "client",
                "/api/v1/clients",
                {
                    "code": code,
                    "legal_name": legal,
                    "trading_name": legal.split()[0],
                    "industry": industry,
                    "website": website,
                },
            )
            if not row:
                continue
            self.clients.append(row)
            cname, title, authority = CONTACTS[i % len(CONTACTS)]
            domain = website.replace("https://www.", "").replace("https://", "").split("/")[0]
            self.post_ok(
                "contact",
                "/api/v1/clients/contacts",
                {
                    "client_id": row["id"],
                    "full_name": cname,
                    "email": f"{cname.split()[0].lower()}.{code}@mail.{domain}",
                    "job_title": title,
                    "authority_level": authority,
                    "is_primary": True,
                },
            )
        for i, (subject, summary) in enumerate(self.take(QUERIES)):
            client = self.clients[i % len(self.clients)] if self.clients else None
            payload: dict[str, Any] = {
                "subject": subject,
                "summary": summary,
                "original_message": (
                    f"Assalamualaikum,\n\n{summary}\n\nPlease share a proposal and timeline.\n\nRegards"
                ),
                "sla_hours": 24,
            }
            if client:
                payload["client_id"] = client["id"]
            if self.source_ids:
                payload["source_id"] = self.source_ids[i % len(self.source_ids)]
            elif self.source_id:
                payload["source_id"] = self.source_id
            query = self.post_ok("query", "/api/v1/queries", payload)
            if not query:
                continue
            self.queries.append(query)
            qid = query["id"]
            self.request(
                "POST",
                f"/api/v1/queries/{qid}/transitions",
                json={"next_status": "classified", "classification": "new_build"},
            )
            self.request(
                "POST",
                f"/api/v1/queries/{qid}/transitions",
                json={"next_status": "qualifying"},
            )
            self.post_ok(
                "qualification",
                "/api/v1/queries/qualification-answers",
                {
                    "query_id": qid,
                    "question_key": "budget",
                    "question_text": "Is budget approved?",
                    "answer_text": "Yes, FY26 digital budget is approved.",
                    "rationale": "Confirmed by the commercial contact",
                },
            )
            self.request(
                "POST",
                f"/api/v1/queries/{qid}/first-response",
                json={"note": "Acknowledged; discovery call scheduled."},
            )
            self.request(
                "POST",
                f"/api/v1/queries/{qid}/transitions",
                json={"next_status": "qualified", "reason": "Budget and fit confirmed"},
            )
            opp = self.post_ok(
                "opportunity",
                f"/api/v1/queries/{qid}/convert",
                {
                    "title": f"{client['legal_name'] if client else 'Prospect'} — {subject[:48]}",
                    "estimated_value": str(25000 + i * 7500),
                    "conversion_notes": "Qualified after discovery call",
                },
            )
            if opp:
                self.opportunities.append(opp)

    def load_projects_delivery(self) -> None:
        for i, (code, title) in enumerate(self.take(PROJECTS)):
            payload: dict[str, Any] = {"code": code, "title": title}
            if self.clients:
                payload["client_id"] = self.clients[i % len(self.clients)]["id"]
            project = self.post_ok("project", "/api/v1/projects", payload)
            if not project:
                continue
            self.projects.append(project)
            self.post_ok(
                "project_member",
                "/api/v1/access/project-members",
                {"project_id": project["id"], "actor_id": ACTOR_ID, "role_code": "pm"},
            )
            req = self.post_ok(
                "requirement",
                "/api/v1/projects/requirements",
                {
                    "project_id": project["id"],
                    "requirement_code": f"{code}-MH-01",
                    "title": f"Must-have: {title} authentication and audit trail",
                },
            )
            if req:
                self.requirements.append(req)
                ver = self.post_ok(
                    "requirement_version",
                    "/api/v1/projects/requirement-versions",
                    {
                        "requirement_id": req["id"],
                        "statement": (
                            f"The system shall authenticate named users for {title} "
                            "and record an append-only audit event for each status change."
                        ),
                        "priority": "must_have",
                    },
                )
                if ver:
                    self.post_ok(
                        "acceptance_criterion",
                        "/api/v1/projects/acceptance-criteria",
                        {
                            "requirement_version_id": ver["id"],
                            "criterion_code": f"{code}-AC-01",
                            "text": "Given a valid user, when they change status, then an audit row is stored.",
                        },
                    )
            phase = self.post_ok(
                "phase",
                "/api/v1/roadmap/phases",
                {
                    "project_id": project["id"],
                    "code": f"{code}-P1",
                    "title": "Discovery and build",
                    "sequence": 1,
                    "planned_start": date(2026, 8, 18).isoformat(),
                    "planned_end": date(2026, 11, 30).isoformat(),
                },
            )
            if phase:
                self.phases.append(phase)
                self.post_ok(
                    "milestone",
                    "/api/v1/roadmap/milestones",
                    {
                        "phase_id": phase["id"],
                        "code": f"{code}-M1",
                        "title": "UAT ready",
                        "owner_actor_id": ACTOR_ID,
                        "target_date": date(2026, 11, 15).isoformat(),
                    },
                )
            ticket_payload: dict[str, Any] = {
                "project_id": project["id"],
                "code": f"{code}-T01",
                "title": f"Implement login and session for {title}",
                "description": "Build SSO-ready login, session timeout, and audit events.",
                "ticket_type": "story",
                "priority": "high",
                "owner_actor_id": ACTOR_ID,
                "acceptance_criteria": "User can sign in and see an audit event.",
                "definition_of_done": "Reviewed, tested, and linked to the must-have.",
            }
            if phase:
                ticket_payload["phase_id"] = phase["id"]
            if req:
                ticket_payload["requirement_id"] = req["id"]
            ticket = self.post_ok("ticket", "/api/v1/tickets", ticket_payload)
            if ticket:
                self.tickets.append(ticket)
                self.post_ok(
                    "subtask",
                    "/api/v1/tickets/subtasks",
                    {
                        "ticket_id": ticket["id"],
                        "code": f"{code}-T01-S1",
                        "title": "Write login acceptance tests",
                        "owner_actor_id": ACTOR_ID,
                        "sequence": 1,
                    },
                )
                assignee = (
                    self.humans[i % len(self.humans)]["actor_id"]
                    if self.humans
                    else ACTOR_ID
                )
                if assignee != ACTOR_ID:
                    self.post_ok(
                        "project_member",
                        "/api/v1/access/project-members",
                        {
                            "project_id": project["id"],
                            "actor_id": assignee,
                            "role_code": "developer",
                        },
                    )
                self.post_ok(
                    "assignment",
                    "/api/v1/assignments",
                    {
                        "ticket_id": ticket["id"],
                        "assignee_actor_id": assignee,
                        "role_code": "developer",
                        "allocation_pct": "25.00",
                        "allow_override": True,
                        "override_reason": "Named dummy assignment for local UI testing",
                    },
                )

    def load_coordination_quality(self) -> None:
        for i, query in enumerate(self.queries):
            followup_payload: dict[str, Any] = {
                "title": f"Confirm discovery notes: {query['subject'][:60]}",
                "source_entity_type": "query",
                "source_entity_id": query["id"],
                "recipient_actor_id": ACTOR_ID,
                "owner_actor_id": ACTOR_ID,
                "required_response": "Written confirmation of scope and budget",
                "closure_condition": "Client email recorded on the query",
                "due_offset_hours": 48,
                "project_id": self.projects[i]["id"] if i < len(self.projects) else None,
            }
            if self.config_version_id:
                followup_payload["rule_version_id"] = self.config_version_id
            self.post_ok("followup", "/api/v1/follow-ups", followup_payload)
            conv = self.post_ok(
                "conversation",
                "/api/v1/comms/conversations",
                {
                    "subject": f"Re: {query['subject'][:80]}",
                    "related_entity_type": "query",
                    "related_entity_id": query["id"],
                    "channel": "email",
                    "client_id": query.get("client_id"),
                    "project_id": self.projects[i]["id"] if i < len(self.projects) else None,
                },
            )
            if conv:
                self.conversations.append(conv)
                self.post_ok(
                    "message",
                    "/api/v1/comms/messages",
                    {
                        "conversation_id": conv["id"],
                        "body": (
                            f"Thank you for the enquiry about {query['subject'][:80]}. "
                            "We have scheduled a discovery call and will share notes after."
                        ),
                    },
                )
        for i, project in enumerate(self.projects):
            self.post_ok(
                "approval",
                "/api/v1/approvals",
                {
                    "action_code": "srs.baseline.approve",
                    "title": f"Approve SRS kickoff for {project['title']}",
                    "target_entity_type": "project",
                    "target_entity_id": project["id"],
                    "target_version": 1,
                    "project_id": project["id"],
                    "steps": [{"role_code": "pm", "order": 1, "assignee_actor_id": ACTOR_ID}],
                },
            )
            doc = self.post_ok(
                "document",
                "/api/v1/documents",
                {
                    "title": f"{project['code']} Statement of Work",
                    "classification": "confidential" if i % 3 == 0 else "internal",
                    "client_id": project.get("client_id"),
                    "project_id": project["id"],
                },
            )
            if doc:
                self.documents.append(doc)
                checksum = hashlib.sha256(f"{project['code']}-sow".encode()).hexdigest()
                self.post_ok(
                    "document_version",
                    "/api/v1/documents/versions",
                    {
                        "document_id": doc["id"],
                        "storage_key": f"docs/{project['code'].lower()}/sow-v1.pdf",
                        "filename": f"{project['code']}-SOW.pdf",
                        "checksum_sha256": checksum,
                        "size_bytes": 12000 + i * 100,
                    },
                )
            case = self.post_ok(
                "test_case",
                "/api/v1/test-cases/cases",
                {
                    "code": f"{project['code']}-TC01",
                    "title": f"Login and audit for {project['title']}",
                    "project_id": project["id"],
                    "case_type": "functional",
                    "priority": "P1",
                    "expected_result": "User is authenticated and an audit event exists.",
                    "steps": [
                        {"step_number": 1, "action_text": "Open login", "expected_text": "Form shown"},
                        {"step_number": 2, "action_text": "Sign in", "expected_text": "Dashboard loads"},
                    ],
                },
            )
            if case:
                self.test_cases.append(case)
                approved = self.request(
                    "POST",
                    f"/api/v1/test-cases/cases/{case['id']}/approve",
                    json={"expected_version": case.get("version", 1)},
                )
                if approved.status_code == 200:
                    self.stats.ok("test_case_approve")
                suite = self.post_ok(
                    "test_suite",
                    "/api/v1/test-cases/suites",
                    {
                        "code": f"{project['code']}-SUITE",
                        "title": f"{project['title']} regression suite",
                        "project_id": project["id"],
                        "case_ids": [case["id"]],
                    },
                )
                if suite:
                    plan = self.post_ok(
                        "test_plan",
                        "/api/v1/test-cases/plans",
                        {
                            "code": f"{project['code']}-PLAN",
                            "title": f"{project['title']} UAT plan",
                            "project_id": project["id"],
                            "environment_code": "staging",
                            "suite_ids": [suite["id"]],
                        },
                    )
                    self.post_ok(
                        "test_run",
                        "/api/v1/test-cases/runs",
                        {
                            "case_id": case["id"],
                            "plan_id": plan["id"] if plan else None,
                            "project_id": project["id"],
                            "environment_code": "staging",
                        },
                    )
            self.post_ok(
                "bug",
                "/api/v1/bugs",
                {
                    "code": f"{project['code']}-BUG01",
                    "title": BUGS[i % len(BUGS)],
                    "description": "Reproduced on staging with a named test account.",
                    "project_id": project["id"],
                    "severity": ["high", "medium", "low", "critical"][i % 4],
                    "blocks_release": i % 5 == 0,
                },
            )

    def load_knowledge_change_release(self) -> None:
        for i, (code, title) in enumerate(self.take(KNOWLEDGE)):
            item = self.post_ok(
                "knowledge",
                "/api/v1/knowledge/items",
                {
                    "code": code,
                    "title": title,
                    "description": f"Internal playbook: {title}.",
                    "project_id": self.projects[i]["id"] if i < len(self.projects) else None,
                    "classification": "internal",
                },
            )
            if item:
                self.post_ok(
                    "knowledge_version",
                    f"/api/v1/knowledge/items/{item['id']}/versions",
                    {
                        "body_text": f"# {title}\n\nUse this playbook during delivery. Do not copy client data across tenants.",
                        "change_summary": "Initial version",
                    },
                )
        for i, project in enumerate(self.projects):
            self.post_ok(
                "risk",
                "/api/v1/change-control/risks",
                {
                    "code": f"RSK-{project['code']}-01",
                    "title": f"Key-person risk on {project['title']}",
                    "description": "Delivery depends on one named engineer for the auth module.",
                    "project_id": project["id"],
                    "risk_level": ["low", "medium", "high", "critical"][i % 4],
                },
            )
            self.post_ok(
                "change_request",
                "/api/v1/change-control/change-requests",
                {
                    "code": f"CR-{project['code']}-01",
                    "title": f"Add SMS OTP to {project['title']}",
                    "description": "Client asked for SMS OTP in addition to email OTP.",
                    "project_id": project["id"],
                    "change_type": "scope",
                    "rationale": "Reduces account-takeover risk for retail users.",
                },
            )
            req = self.requirements[i] if i < len(self.requirements) else None
            ticket = self.tickets[i] if i < len(self.tickets) else None
            items = []
            if req:
                items.append({"link_type": "requirement", "linked_entity_id": req["id"]})
            if ticket:
                items.append({"link_type": "ticket", "linked_entity_id": ticket["id"]})
            release = self.post_ok(
                "release",
                "/api/v1/releases",
                {
                    "code": f"REL-{project['code']}-1.0",
                    "title": f"{project['title']} 1.0",
                    "project_id": project["id"],
                    "version_label": "1.0.0",
                    "items": items,
                },
            )
            if not release:
                continue
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
                    json={"evidence": "CAB minutes recorded", "expected_version": version},
                )
                if approved.status_code == 200:
                    version = approved.json().get("version", version)
                    self.request(
                        "POST",
                        f"/api/v1/releases/{release['id']}/backups",
                        json={"backup_ref": f"s3://masms-backups/{project['code'].lower()}", "confirmed": True},
                    )
                    self.request(
                        "POST",
                        f"/api/v1/releases/{release['id']}/migration-plans",
                        json={"plan_text": "alembic upgrade head", "alembic_revision": "20260811_0037"},
                    )
                    env = "staging" if i % 2 else "production"
                    self.post_ok(
                        "deployment",
                        f"/api/v1/releases/{release['id']}/deployments",
                        {
                            "environment_code": env,
                            "build_ref": f"sha-{project['code'].lower()}-1",
                            "expected_version": version,
                        },
                    )

    def load_governance_notifications(self) -> None:
        for i, (key, title) in enumerate(self.take(ADRS)):
            adr = self.post_ok(
                "adr",
                "/api/v1/governance/architecture-decisions",
                {
                    "adr_key": key,
                    "title": title,
                    "context": f"Delivery teams asked how MASMS should handle {title.lower()}.",
                    "decision": f"We will adopt {title} for all delivery work.",
                    "consequences": "Teams must follow this decision unless a change request supersedes it.",
                    "security_notes": "Tenant isolation and audit remain mandatory.",
                },
            )
            if adr and i % 3 == 0:
                self.request(
                    "POST",
                    f"/api/v1/governance/architecture-decisions/{adr['id']}/transitions",
                    json={
                        "target_status": "accepted",
                        "expected_version": adr.get("version", 1),
                        "reason": "Accepted by architecture review",
                    },
                )
            self.post_ok(
                "baseline",
                "/api/v1/governance/baselines",
                {
                    "baseline_key": f"SRS-{key}",
                    "title": f"SRS pack for {title}",
                    "artifact_path": f"Docs/srs/{key.lower()}.md",
                    "document_version": "1.0",
                    "classification": "internal",
                },
            )
        for i, title in enumerate(self.take(NOTIFICATIONS)):
            self.post_ok(
                "notification",
                "/api/v1/notifications",
                {
                    "title": title,
                    "body": f"{title}. Open the related desk to act.",
                    "recipient_actor_id": ACTOR_ID,
                    "notification_type": ["assignment", "reminder", "system_alert"][i % 3],
                    "channel": "in_app",
                    "priority": "high" if i % 4 == 0 else "normal",
                    "project_id": self.projects[i]["id"] if i < len(self.projects) else None,
                    "idempotency_key": f"dummy-ntf-{i + 1:02d}",
                },
            )
        for i, req in enumerate(self.requirements):
            self.post_ok(
                "must_have",
                "/api/v1/traceability/must-haves",
                {
                    "requirement_id": req["id"],
                    "requirement_code": req.get("requirement_code", f"MH-{i + 1:02d}"),
                    "title": req.get("title", "Must-have requirement"),
                    "project_id": req.get("project_id"),
                },
            )
            self.post_ok(
                "activity",
                "/api/v1/insights/activity",
                {
                    "event_type": "requirement.registered",
                    "entity_type": "requirement",
                    "entity_id": req["id"],
                    "summary": f"Registered must-have {req.get('requirement_code')}",
                    "project_id": req.get("project_id"),
                },
            )

    def load_agents_integrations_ops(self) -> None:
        for code in self.take(WORKFLOW_CODES):
            versions = self.request(
                "POST",
                f"/api/v1/orchestrator/definitions/{code}/versions",
                json={
                    "definition_json": {"steps": ["start", "wait", "end"]},
                    "temporal_workflow_type": f"masms.{code}",
                },
            )
            if versions.status_code in {200, 201}:
                vid = versions.json().get("id")
                if vid:
                    self.request("POST", f"/api/v1/orchestrator/versions/{vid}/activate", json={})
                    self.stats.ok("orchestrator_version")
        for i in range(self.count):
            related = self.queries[i] if i < len(self.queries) else None
            if not related:
                continue
            self.post_ok(
                "agent_run",
                "/api/v1/agent-runtime/runs",
                {
                    "agent_code": AGENT_CODES[i % len(AGENT_CODES)],
                    "related_entity_type": "query",
                    "related_entity_id": related["id"],
                    "input_json": {"note": "Draft a discovery summary"},
                },
            )
            self.post_ok(
                "workflow_instance",
                "/api/v1/orchestrator/instances",
                {
                    "workflow_code": WORKFLOW_CODES[i % len(WORKFLOW_CODES)],
                    "related_entity_type": "query",
                    "related_entity_id": related["id"],
                    "input_json": {"note": "Coordinate discovery"},
                },
            )
        providers = [
            ("github_delivery", "github", "oauth2", "sm://masms/github-delivery"),
            ("jira_delivery", "jira", "oauth2", "sm://masms/jira-delivery"),
            ("slack_alerts", "slack", "oauth2", "sm://masms/slack-alerts"),
        ]
        for i in range(self.count):
            code, provider, auth, cred = providers[i % len(providers)]
            self.post_ok(
                "integration",
                "/api/v1/integrations/connections",
                {
                    "code": f"{code}_{i + 1:02d}",
                    "provider": provider,
                    "auth_type": auth,
                    "credential_ref": f"{cred}-{i + 1:02d}",
                },
            )
        for i in range(self.count):
            self.post_ok(
                "gmail_connection",
                "/api/v1/gmail/connections",
                {
                    "code": f"gmail_inbox_{i + 1:02d}",
                    "email_address": f"ops{i + 1:02d}@eazisols.example",
                    "credential_ref": f"sm://masms/gmail-inbox-{i + 1:02d}",
                },
            )
        for i, ticket in enumerate(self.tickets[: self.count]):
            self.post_ok(
                "jira_push",
                "/api/v1/jira/issues/push",
                {
                    "internal_ticket_id": ticket["id"],
                    "summary": ticket["title"],
                    "approval_status": "approved",
                    "simulated_jira_key": f"EZ-{100 + i}",
                },
            )
        for i in range(self.count):
            self.post_ok(
                "security_incident",
                "/api/v1/security/incidents",
                {
                    "code": f"INC-{i + 1:03d}",
                    "title": f"Suspicious login spike on desk {i + 1}",
                    "severity": ["low", "medium", "high", "critical"][i % 4],
                    "summary": "Rate-limit triggered; session review required.",
                },
            )
            self.post_ok(
                "legal_hold",
                "/api/v1/security/legal-holds",
                {
                    "code": f"HOLD-{i + 1:03d}",
                    "reason": "Preserve dispute evidence until legal review closes.",
                    "scope_json": {"module": "documents"},
                },
            )
            self.post_ok(
                "perf_test",
                "/api/v1/reliability/performance-tests",
                {
                    "code": f"PERF-{i + 1:02d}",
                    "suite_name": "API p95 login",
                    "p95_ms": 180 + i * 5,
                    "sample_count": 200,
                    "status": "passed",
                },
            )
            self.post_ok(
                "dr_runbook",
                "/api/v1/reliability/dr-runbooks",
                {
                    "code": f"DR-{i + 1:02d}",
                    "title": f"Restore Postgres replica {i + 1}",
                    "rto_minutes": 30,
                    "rpo_minutes": 5,
                    "body_preview": "Promote replica, replay WAL, verify RLS.",
                },
            )
            self.post_ok(
                "e2e_test",
                "/api/v1/uat/e2e-tests",
                {
                    "code": f"E2E-{i + 1:02d}",
                    "suite_name": "Query to opportunity",
                    "result": "passed" if i % 4 else "failed",
                    "evidence": "Playwright trace stored in CI artifacts.",
                },
            )
            self.post_ok(
                "pilot_plan",
                "/api/v1/pilot/plans",
                {
                    "code": f"PILOT-{i + 1:02d}",
                    "title": f"Controlled pilot wave {i + 1}",
                    "status": "draft",
                },
            )

    def run(self) -> int:
        health = self.request("GET", "/api/v1/meta")
        if health.status_code != 200:
            print(f"API not reachable at {self.base_url}: {health.status_code}")
            return 2
        print(f"Loading up to {self.count} records/entity against {self.base_url} ...")
        steps = [
            self.load_identity,
            self.load_access_and_capacity,
            self.load_config,
            self.load_clients_queries_opportunities,
            self.load_projects_delivery,
            self.load_coordination_quality,
            self.load_knowledge_change_release,
            self.load_governance_notifications,
            self.load_agents_integrations_ops,
        ]
        for step in steps:
            print(f"  -> {step.__name__}")
            try:
                step()
            except Exception as exc:  # noqa: BLE001
                self.stats.fail(step.__name__, str(exc))
                print(f"    ! {step.__name__} error: {exc}")
        print("\nCreated:")
        for key, value in sorted(self.stats.created.items()):
            print(f"  {key}: {value}")
        print("\nSkipped:")
        for key, value in sorted(self.stats.skipped.items()):
            print(f"  {key}: {value}")
        if self.stats.failed:
            print("\nFailures:")
            for key, errs in sorted(self.stats.failed.items()):
                print(f"  {key}: {len(errs)}")
                for err in errs[:2]:
                    print(f"    - {err}")
        core_ok = self.stats.created.get("client", 0) >= min(10, self.count)
        return 0 if core_ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Load MASMS realistic dummy data")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--count", type=int, default=20, help="Records per entity (1-20)")
    parser.add_argument(
        "--wipe",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Truncate local Postgres application tables before load (default: true)",
    )
    parser.add_argument(
        "--database-url",
        default=os.environ.get("MASMS_DATABASE_URL", DEFAULT_DB),
    )
    args = parser.parse_args(argv)
    if args.wipe:
        try:
            wipe_local_database(args.database_url)
        except Exception as exc:  # noqa: BLE001
            print(f"Wipe failed: {exc}")
            return 2
    loader = Loader(base_url=args.base_url, count=args.count)
    try:
        return loader.run()
    finally:
        loader.close()


if __name__ == "__main__":
    raise SystemExit(main())
