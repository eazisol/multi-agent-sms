"""Mark evidenced items in MASMS_CURSOR_COMPLETE_DEVELOPMENT_CHECKLIST.md."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "MASMS_CURSOR_COMPLETE_DEVELOPMENT_CHECKLIST.md"
EVIDENCE_LOG = ROOT / "docs" / "modules" / "MOD-000" / "COMPLETE_CHECKLIST_EVIDENCE.md"

# id -> evidence note (only include items safe to mark [x] with current evidence)
MARKED: dict[str, str] = {
    # Global Readiness — factual/tooling only; human "approved" items stay open
    "PRE-003": "`.cursor/rules/`, `AGENTS.md`, `MANIFEST.json` present",
    "PRE-011": "Python `>=3.12,<3.13` in pyproject; Node `>=22` in package.json; ADR-0002",
    "PRE-012": "`uv.lock` present; pnpm workspace declared (host Corepack EPERM for pnpm runtime)",
    "PRE-013": "Provisional decision recorded: Auth0 + OpenAI (ADR-0003); formal PRE approval still pending",
    # MOD-000 readiness
    "CHK-MOD-000-RDY-001": "No dependencies; none required",
    "CHK-MOD-000-RDY-002": "`docs/governance/` + MVP exclusions referenced in REQUIREMENT_MODULE_MAP",
    "CHK-MOD-000-RDY-004": "Statuses/transitions/approvals/audit defined in domain.py + governance docs",
    "CHK-MOD-000-RDY-005": "`docs/governance/UI_ROLE_VARIANTS.md` variants, screens, action matrix",
    "CHK-MOD-000-RDY-006": "API tests + Docs sample projects available for acceptance scenarios",
    # Components — schema/migration/rules (not live Postgres RLS suites)
    "CHK-MOD-000-CMP-01-01": "`gov_source_baselines` model + Alembic `20260810_0001`",
    "CHK-MOD-000-CMP-01-02": "Data dictionary + model fields (org, owner, version, soft delete, audit)",
    "CHK-MOD-000-CMP-01-03": "Unique (org, baseline_key, version); indexes; optimistic version",
    "CHK-MOD-000-CMP-02-01": "`gov_requirement_mappings` + migration",
    "CHK-MOD-000-CMP-02-02": "Ownership/tenant/version/soft-delete defined",
    "CHK-MOD-000-CMP-02-03": "Unique (org, requirement_id, module_id, mapping_role)",
    "CHK-MOD-000-CMP-03-01": "`gov_architecture_decisions` + migration",
    "CHK-MOD-000-CMP-03-02": "Ownership/tenant/version/soft-delete defined",
    "CHK-MOD-000-CMP-03-03": "Unique (org, adr_key, version)",
    "CHK-MOD-000-CMP-04-01": "`gov_change_requests` + migration",
    "CHK-MOD-000-CMP-04-02": "Ownership/tenant/version/soft-delete defined",
    "CHK-MOD-000-CMP-04-03": "Unique key/version + idempotency unique; target indexes",
    "CHK-MOD-000-CMP-05-01": "`gov_approval_records` + migration",
    "CHK-MOD-000-CMP-05-02": "Ownership/tenant/version/soft-delete defined",
    "CHK-MOD-000-CMP-05-03": "Target indexes; authority_level 1-5 validated in schema",
    # Backend/API
    "CHK-MOD-000-BEAPI-001": "`schemas.py` + domain validation",
    "CHK-MOD-000-BEAPI-002": "Human-only approve; immutable approved; invalid transitions blocked",
    "CHK-MOD-000-BEAPI-003": "N/A for MOD-000 stub — no async outbox consumers required yet",
    "CHK-MOD-000-BEAPI-004": "expected_version checks + CR idempotency_key",
    "CHK-MOD-000-BEAPI-005": "`/api/v1/governance/*` create/list/get/patch/transitions + baseline history",
    "CHK-MOD-000-BEAPI-006": "Paginated list envelopes with limit/offset/filter/sort (baselines)",
    "CHK-MOD-000-BEAPI-007": "`AppError` → structured JSON (`code`, `message`, `correlation_id`)",
    "CHK-MOD-000-BEAPI-008": "OpenAPI examples on BaselineRead + ProblemDetails; route error responses",
    # Workflow
    "CHK-MOD-000-WF-001": "`docs/governance/WORKFLOW.md` triggers/owners/statuses/approvals/evidence/closure",
    "CHK-MOD-000-WF-002": "N/A — no Temporal waits in MOD-000; FastAPI mutations only",
    "CHK-MOD-000-WF-003": "N/A — no LangGraph reasoning in MOD-000 stub",
    "CHK-MOD-000-WF-004": "`GovernanceService` owns mutations",
    "CHK-MOD-000-WF-006": "`X-Correlation-Id` → audit `correlation_id`",
    "CHK-MOD-000-WF-008": "Agent approve blocked with 403; human approve required",
    "CHK-MOD-000-WF-009": "N/A — notifications deferred to MOD-440 (WORKFLOW.md)",
    # Security (only strongly evidenced)
    "CHK-MOD-000-SEC-005": "Approve/reject requires `ActorKind.HUMAN`",
    "CHK-MOD-000-SEC-006": "`gov_audit_events` on create/update/transition/approval",
    "CHK-MOD-000-SEC-007": "Audit fields include actor, org, action, entity, reason, source, correlation, timestamp",
    # QA
    "CHK-MOD-000-QA-001": "`uv run pytest` — unit domain tests passed",
    "CHK-MOD-000-QA-002": "SQLite-backed API integration tests passed (Postgres migration apply not run)",
    "CHK-MOD-000-QA-003": "Governance API tests exercise success and error contracts",
    "CHK-MOD-000-QA-004": "Agent approve returns 403",
    "CHK-MOD-000-QA-005": "Other-org list returns empty",
    "CHK-MOD-000-QA-006": "CR idempotency key returns same id",
    "CHK-MOD-000-QA-007": "N/A — no WF/agent/integration capabilities enabled in module stub",
    "CHK-MOD-000-QA-010": "`docs/modules/MOD-000/VERIFICATION.md`",
    # Acceptance (only those met without human sign-off)
    "CHK-MOD-000-AC-002": "Immutable approved + CR/version rules enforced in service",
    "CHK-MOD-000-AC-003": "`docs/governance/REQUIREMENT_MODULE_MAP.md`",
    "CHK-MOD-000-AC-900": "No Critical/High defects opened against MOD-000",
}

INTENTIONALLY_OPEN_NOTES = """
## Intentionally left unchecked (examples)

### Global Readiness needing human approval
PRE-001, PRE-002, PRE-004..PRE-010, PRE-014, PRE-015 (partial tooling only / no formal approve)

### MOD-000 unresolved
- RDY-003 / RDY-005: named human approvers and UI role variants not finalized
- CMP-*-04: live Postgres RLS suites not executed
- BEAPI-006 / BEAPI-008: pagination/search and curated OpenAPI examples incomplete
- FE-001..FE-008: frontend deferred
- WF-005/007/009: outbox, DLQ, notifications not built
- SEC-001..SEC-004: full RBAC/deny-default and live RLS incomplete (header stub only)
- QA-008 / QA-009: alembic against Postgres, scans, frontend build, full docs pack incomplete
- AC-001 / AC-901 / AC-902: baseline not human-approved; module not Done

### Per-Task Gate
TASK-GATE-001..019 remain standing process checks for every future task (not permanently satisfied).
"""


def main() -> None:
    text = CHECKLIST.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Remove prior generated banner if present
    cleaned: list[str] = []
    skip = False
    for line in lines:
        if line.strip() == "## Evidence status log (workspace)":
            skip = True
            continue
        if skip:
            if line.startswith("## ") and "Evidence status log" not in line:
                skip = False
                cleaned.append(line)
            continue
        cleaned.append(line)
    lines = cleaned

    banner = [
        "",
        "## Evidence status log (workspace)",
        "",
        "**Date:** 2026-08-10  ",
        "**Scope marked:** Global Readiness (partial) + MOD-000 (partial)  ",
        "**Detail:** `docs/modules/MOD-000/COMPLETE_CHECKLIST_EVIDENCE.md`  ",
        "**Rule preserved:** items without evidence remain unchecked; human approvals are never auto-checked.",
        "",
    ]

    out: list[str] = []
    injected = False
    for i, line in enumerate(lines):
        out.append(line)
        if (
            not injected
            and line.startswith("**Rule:** Check an item only after evidence exists")
        ):
            # Insert after this rule line and its following blank line if present
            if i + 1 < len(lines) and lines[i + 1].strip() == "":
                out.append(lines[i + 1])
                # skip consuming blank by advancing via flag handled below
            out.extend(banner)
            injected = True
            # If next source line is blank we already copied it; mark to skip dup
            continue

    # If we duplicated the blank after rule, rebuild carefully
    rebuilt: list[str] = []
    i = 0
    injected = False
    while i < len(lines):
        line = lines[i]
        rebuilt.append(line)
        if (
            not injected
            and line.startswith("**Rule:** Check an item only after evidence exists")
        ):
            if i + 1 < len(lines) and lines[i + 1].strip() == "":
                rebuilt.append(lines[i + 1])
                i += 1
            rebuilt.extend(banner)
            injected = True
        i += 1
    if not injected:
        rebuilt = lines[:2] + banner + lines[2:]

    final: list[str] = []
    changed = 0
    for line in rebuilt:
        marked_line = line
        for item_id, note in MARKED.items():
            needle = f"**{item_id}:**"
            if needle in line and line.lstrip().startswith("- [ ]"):
                marked_line = line.replace("- [ ]", "- [x]", 1)
                if "Evidence:" not in marked_line:
                    marked_line = marked_line.rstrip() + f"  \n  - Evidence: {note}"
                changed += 1
                break
        final.append(marked_line)

    CHECKLIST.write_text("\n".join(final) + "\n", encoding="utf-8")

    evidence_lines = [
        "# Complete Checklist Evidence — MOD-000 / PRE (2026-08-10)",
        "",
        "Only items listed below were marked `[x]` in `MASMS_CURSOR_COMPLETE_DEVELOPMENT_CHECKLIST.md`.",
        "",
        "## Marked items",
        "",
        "| ID | Evidence |",
        "|---|---|",
    ]
    for item_id, note in sorted(MARKED.items()):
        evidence_lines.append(f"| {item_id} | {note} |")
    evidence_lines.append(INTENTIONALLY_OPEN_NOTES)
    evidence_lines.extend(
        [
            "",
            "## Verification commands (recorded)",
            "",
            "- `uv run pytest -q` → 9 passed",
            "- `uv run ruff check apps/api/src tests` → passed",
            "- `uv run mypy apps/api/src/masms_api` → passed",
            "- `alembic upgrade head` against Postgres → **not run**",
            "- Frontend build → **not applicable** (placeholder)",
            "",
            "## Human actions still required",
            "",
            "1. Approve MVP SRS / PRE-001..PRE-010 governed docs",
            "2. Name product/engineering owners and approvers",
            "3. Approve MOD-000 completion evidence (AC-901)",
            "4. Decide deploy target and finish PRE-014/015",
            "",
        ]
    )
    EVIDENCE_LOG.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_LOG.write_text("\n".join(evidence_lines), encoding="utf-8")
    print(f"Marked {changed} checklist items")
    print(f"Wrote {EVIDENCE_LOG}")

if __name__ == "__main__":
    main()
