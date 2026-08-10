"""Generate implementation progress checklist from the module-wise plan."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "MASMS_CURSOR_MODULE_WISE_IMPLEMENTATION_PLAN.md"
OUT = ROOT / "MASMS_IMPLEMENTATION_PROGRESS_CHECKLIST.md"

# Evidence-based status for current workspace (2026-08-10 MOD-000 session).
# Keys: exact task IDs. Values: ("done"|"partial"|"n/a"|"blocked", note)
STATUS: dict[str, tuple[str, str]] = {
    # MOD-000 main points
    "MOD-000-MP-001": ("done", "Baseline register docs + API entity gov_source_baselines"),
    "MOD-000-MP-002": ("done", "REQUIREMENT_MODULE_MAP.md + API requirement-mappings"),
    "MOD-000-MP-003": ("done", "docs/governance/adrs + API architecture-decisions"),
    "MOD-000-MP-004": ("done", "CHANGE_CONTROL.md + API change-requests"),
    "MOD-000-MP-005": ("done", "APPROVAL_RECORDS.md + API approvals"),
    # DB
    "MOD-000-DB-001": ("done", "Model + Alembic 20260810_0001; retention policy pending formal legal"),
    "MOD-000-DB-002": ("done", "Model + migration + unique constraints"),
    "MOD-000-DB-003": ("done", "Model + migration"),
    "MOD-000-DB-004": ("done", "Model + migration + idempotency unique"),
    "MOD-000-DB-005": ("done", "Model + migration"),
    # BE
    "MOD-000-BE-001": ("done", "domain.py + service.py typed application service"),
    "MOD-000-BE-002": ("done", "Human-only approve, transitions, optimistic version, CR idempotency"),
    "MOD-000-BE-003": ("n/a", "Outbox not required yet for governance stub; deferred MOD-020/350"),
    "MOD-000-BE-004": ("done", "Structured AppError codes mapped in FastAPI handler"),
    # API
    "MOD-000-API-001": ("done", "CRUD/query/transition + baseline history endpoint"),
    "MOD-000-API-002": ("done", "Pagination/filter/sort + concurrency/idempotency/problem errors"),
    "MOD-000-API-003": ("done", "OpenAPI models + ProblemDetails/BaselineRead examples + error responses"),
    # FE
    "MOD-000-FE-001": ("partial", "Baselines list with filter/pagination/empty/loading/error; saved views not yet"),
    "MOD-000-FE-002": ("partial", "Detail summary + audit history tabs; other related tabs deferred"),
    "MOD-000-FE-003": ("done", "Create/edit/transition forms with role gates and stale-version handling"),
    "MOD-000-FE-004": ("partial", "Skip link, labels, UTC dates, responsive layout; formal a11y audit pending"),
    # WF
    "MOD-000-WF-001": ("done", "docs/governance/WORKFLOW.md defines triggers/owners/statuses/approvals/closure"),
    "MOD-000-WF-002": ("n/a", "No durable waits/AI in MOD-000; FastAPI owns mutations (WORKFLOW.md)"),
    "MOD-000-WF-003": ("done", "Event/outbox/idempotency/correlation/retry/DLQ rules defined; runtime outbox deferred MOD-020"),
    "MOD-000-WF-004": ("n/a", "Notifications deferred to MOD-440 (WORKFLOW.md)"),
    # SEC
    "MOD-000-SEC-001": ("partial", "Org-scoped header principal + human-approve gate; full RBAC deferred MOD-110/120"),
    "MOD-000-SEC-002": ("partial", "App-level org filter + RLS SQL in migration; live GUC/RLS tests not run"),
    "MOD-000-SEC-003": ("partial", "Audit payload_redacted + no secrets in .env.example; broader redaction plumbing later"),
    "MOD-000-SEC-004": ("partial", "Audit on create/update/transition/approval; not all action types yet"),
    # QA
    "MOD-000-QA-001": ("done", "tests/unit/governance/test_domain.py"),
    "MOD-000-QA-002": ("done", "tests/integration/governance/test_governance_api.py"),
    "MOD-000-QA-003": ("partial", "Agent approve negative + org list isolation; full RBAC matrix pending"),
    "MOD-000-QA-004": ("n/a", "No Temporal/agent/integration capabilities in this module stub"),
    "MOD-000-QA-005": ("partial", "pytest/ruff/mypy passed; alembic/frontend/security scan not run"),
    # DOC
    "MOD-000-DOC-001": ("partial", "Module README, data dictionary, governance docs; full audit catalog pending"),
    "MOD-000-DOC-002": ("done", "README limitations + VERIFICATION.md"),
    # AC
    "MOD-000-AC-001": ("partial", "SoT candidates registered; human approval of BL-SRS-001 still PENDING"),
    "MOD-000-AC-002": ("done", "Documented and enforced for approved records"),
    "MOD-000-AC-003": ("done", "REQUIREMENT_MODULE_MAP.md published"),
    "MOD-000-AC-900": ("done", "No Critical/High defects filed against module"),
    "MOD-000-AC-901": ("blocked", "Requires named human owner approval"),
    # MOD-010 partial scaffold overlap
    "MOD-010-MP-001": ("done", "Monorepo layout documented + present under apps/, packages/, migrations/, tests/"),
    "MOD-010-MP-002": ("done", ".python-version 3.12 + .nvmrc 22 + engines"),
    "MOD-010-MP-003": ("done", "uv.lock + npm package-lock; pnpm deferred (host EPERM)"),
    "MOD-010-MP-004": ("done", "compose up healthy; alembic upgrade head -> 20260810_0001"),
    "MOD-010-MP-005": ("done", "ruff + next lint configured"),
    "MOD-010-MP-006": ("done", "mypy strict for masms_api"),
    "MOD-010-MP-007": ("done", "pytest suite + web build as verification"),
    "MOD-010-MP-008": ("done", ".github/workflows/ci.yml"),
    "MOD-010-DB-001": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-DB-002": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-DB-003": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-DB-004": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-DB-005": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-DB-006": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-DB-007": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-DB-008": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-BE-001": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-BE-002": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-BE-003": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-BE-004": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-API-001": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-API-002": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-API-003": ("n/a", "Toolchain module — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-FE-001": ("n/a", "No MOD-010 UI; web app serves MOD-000 — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-FE-002": ("n/a", "No MOD-010 UI — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-FE-003": ("n/a", "No MOD-010 UI — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-FE-004": ("n/a", "No MOD-010 UI — see TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-WF-001": ("n/a", "Dev workflow documented as start commands — not business WF"),
    "MOD-010-WF-002": ("n/a", "Workers are placeholders only"),
    "MOD-010-WF-003": ("n/a", "No MOD-010 domain events"),
    "MOD-010-WF-004": ("n/a", "No MOD-010 notifications"),
    "MOD-010-SEC-001": ("n/a", "No MOD-010 tenant resources"),
    "MOD-010-SEC-002": ("n/a", "No MOD-010 RLS resources"),
    "MOD-010-SEC-003": ("done", ".env.example only; .gitignore excludes .env/.env.local"),
    "MOD-010-SEC-004": ("n/a", "No MOD-010 audit entity"),
    "MOD-010-QA-001": ("n/a", "No MOD-010 domain unit tests"),
    "MOD-010-QA-002": ("n/a", "No MOD-010 API module"),
    "MOD-010-QA-003": ("n/a", "No MOD-010 authz surface"),
    "MOD-010-QA-004": ("n/a", "No MOD-010 WF/agent tests"),
    "MOD-010-QA-005": ("done", "scripts/dev-check.* runs ruff/mypy/pytest/web lint/build"),
    "MOD-010-DOC-001": ("done", "docs/modules/MOD-010/README.md"),
    "MOD-010-DOC-002": ("done", "VERIFICATION.md + TEMPLATE_TASK_RATIONALE.md"),
    "MOD-010-AC-001": ("done", "Start commands documented in MOD-010 README"),
    "MOD-010-AC-002": ("done", "CI run 31386826793 success on b9038a9 (main)"),
    "MOD-010-AC-003": ("done", "No real secrets in examples"),
    "MOD-010-AC-900": ("done", "No Critical/High tooling defects filed"),
    "MOD-010-AC-901": ("blocked", "Human owner approval required"),
    "MOD-020-MP-001": ("done", "kernel/ids.py NewType brands"),
    "MOD-020-MP-002": ("done", "kernel/actor.py ActorContext"),
    "MOD-020-MP-003": ("done", "kernel/tenant.py TenantContext"),
    "MOD-020-MP-004": ("done", "kernel/errors.py AppError hierarchy"),
    "MOD-020-MP-005": ("done", "kernel/uow.py SqlAlchemyUnitOfWork"),
    "MOD-020-MP-006": ("done", "sys_outbox_messages + enqueue_outbox"),
    "MOD-020-MP-007": ("done", "application/problem+json via kernel/problem.py"),
    "MOD-020-MP-008": ("done", "kernel/pagination.py PageMeta helpers"),
    "MOD-020-MP-009": ("done", "kernel/concurrency.py assert_expected_version"),
    "MOD-020-DB-001": ("done", "DATA_CONVENTIONS.md — typed IDs are brands, not tables"),
    "MOD-020-DB-002": ("done", "DATA_CONVENTIONS.md actor kind conventions"),
    "MOD-020-DB-003": ("done", "DATA_CONVENTIONS.md tenant scope conventions"),
    "MOD-020-DB-004": ("done", "DATA_CONVENTIONS.md errors are ephemeral API contracts"),
    "MOD-020-DB-005": ("done", "UoW is session contract — no dedicated table"),
    "MOD-020-DB-006": ("done", "migration 20260810_0002 sys_outbox_messages + RLS"),
    "MOD-020-DB-007": ("done", "problem details are response contract, not a table"),
    "MOD-020-DB-008": ("done", "pagination meta is response contract, not a table"),
    "MOD-020-DB-009": ("done", "version columns already on entities; helper shared"),
    "MOD-020-BE-001": ("partial", "kernel + governance uses UoW/outbox/helpers"),
    "MOD-020-BE-002": ("partial", "concurrency+approval rules via helpers; full authz later"),
    "MOD-020-BE-003": ("partial", "outbox enqueue on baseline create; publisher runtime pending"),
    "MOD-020-BE-004": ("done", "structured errors via kernel + FastAPI handler"),
    "MOD-020-API-002": ("partial", "problem+json + paging/concurrency shared; full OpenAPI polish pending"),
    "MOD-020-API-003": ("partial", "ProblemDetails schema examples updated"),
    "MOD-020-FE-001": ("n/a", "kernel library — no entity UI"),
    "MOD-020-FE-002": ("n/a", "kernel library — no entity UI"),
    "MOD-020-FE-003": ("n/a", "kernel library — no entity UI"),
    "MOD-020-FE-004": ("n/a", "kernel library — no entity UI"),
    "MOD-020-WF-002": ("partial", "boundary documented; Temporal/LangGraph not wired yet"),
    "MOD-020-WF-003": ("partial", "outbox table+enqueue; consumer/publisher runtime pending"),
    "MOD-020-SEC-002": ("partial", "outbox RLS + tenant context shape"),
    "MOD-020-QA-001": ("done", "tests/unit/kernel"),
    "MOD-020-QA-002": ("partial", "governance API still green with outbox/problem+json"),
    "MOD-020-QA-005": ("done", "ruff/mypy/pytest + alembic upgrade head"),
    "MOD-020-DOC-001": ("partial", "docs/modules/MOD-020/README.md"),
    "MOD-020-DOC-002": ("done", "DATA_CONVENTIONS + VERIFICATION"),
    "MOD-020-AC-001": ("partial", "RequestContext in kernel; governance wired"),
    "MOD-020-AC-002": ("partial", "UoW/API boundary documented; not yet enforced platform-wide"),
    "MOD-020-AC-003": ("partial", "problem+json + shared PageMeta"),
    "MOD-020-AC-900": ("done", "No Critical/High kernel defects filed"),
    "MOD-020-AC-901": ("blocked", "Human owner approval required"),
    "MOD-030-MP-001": ("done", "Environment enum + config/environments examples"),
    "MOD-030-MP-002": ("done", "SecretBackend local + Key Vault fail-closed stub"),
    "MOD-030-MP-003": ("done", "CI concurrency + junit/build-identity artifacts"),
    "MOD-030-MP-004": ("done", "deploy-staging.yml dry-run skeleton"),
    "MOD-030-MP-005": ("done", "deploy-production.yml + check_production_gate.py"),
    "MOD-030-MP-006": ("done", "infra/bicep Key Vault skeleton"),
    "MOD-030-DB-001": ("n/a", "No env matrix table — config files"),
    "MOD-030-DB-002": ("n/a", "Secrets in Key Vault / GH Environments — not DB"),
    "MOD-030-DB-003": ("n/a", "CI is GitHub Actions — not DB"),
    "MOD-030-DB-004": ("n/a", "Staging deploy is workflow — not DB"),
    "MOD-030-DB-005": ("n/a", "Prod gate is workflow/script — not DB"),
    "MOD-030-DB-006": ("n/a", "IaC is Bicep files — not DB"),
    "MOD-030-BE-001": ("n/a", "Platform helpers only; see TEMPLATE_TASK_RATIONALE"),
    "MOD-030-BE-002": ("n/a", "No MOD-030 entity mutations"),
    "MOD-030-BE-003": ("n/a", "No MOD-030 outbox entity"),
    "MOD-030-BE-004": ("n/a", "No MOD-030 entity API errors"),
    "MOD-030-API-001": ("n/a", "No MOD-030 CRUD API"),
    "MOD-030-API-002": ("n/a", "No MOD-030 CRUD API"),
    "MOD-030-API-003": ("n/a", "No MOD-030 CRUD API"),
    "MOD-030-FE-001": ("n/a", "No MOD-030 UI"),
    "MOD-030-FE-002": ("n/a", "No MOD-030 UI"),
    "MOD-030-FE-003": ("n/a", "No MOD-030 UI"),
    "MOD-030-FE-004": ("n/a", "No MOD-030 UI"),
    "MOD-030-WF-001": ("n/a", "Deploy via GitHub Actions — not Temporal WF"),
    "MOD-030-WF-002": ("n/a", "No Temporal/LangGraph in MOD-030"),
    "MOD-030-WF-003": ("n/a", "No MOD-030 domain events"),
    "MOD-030-WF-004": ("n/a", "No MOD-030 notifications"),
    "MOD-030-SEC-001": ("partial", "GitHub Environment + prod gate; Auth0 later"),
    "MOD-030-SEC-002": ("n/a", "No MOD-030 tenant tables"),
    "MOD-030-SEC-003": ("done", "Examples only; prod forbids local_env backend"),
    "MOD-030-SEC-004": ("n/a", "No MOD-030 audit entity"),
    "MOD-030-QA-001": ("done", "tests/unit/platform"),
    "MOD-030-QA-002": ("n/a", "No MOD-030 API module"),
    "MOD-030-QA-003": ("n/a", "No MOD-030 tenant surface"),
    "MOD-030-QA-004": ("n/a", "No MOD-030 Temporal/agent tests"),
    "MOD-030-QA-005": ("done", "ruff/mypy/pytest + gate script smoke"),
    "MOD-030-DOC-001": ("done", "docs/modules/MOD-030/README.md"),
    "MOD-030-DOC-002": ("done", "VERIFICATION + TEMPLATE_TASK_RATIONALE"),
    "MOD-030-AC-001": ("partial", "Matrix + secret backend rules; live KV not wired"),
    "MOD-030-AC-002": ("done", "Production workflow requires confirm+approver+reason+sha"),
    "MOD-030-AC-003": ("done", "CI build-identity artifact keyed by git sha"),
    "MOD-030-AC-900": ("done", "No Critical/High MOD-030 defects filed"),
    "MOD-030-AC-901": ("blocked", "Human owner approval required"),
}

def ascii_dash(text: str) -> str:
    return (
        text.replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u2011", "-")
        .replace("\ufffd", "-")
    )


def box(status: str) -> str:
    if status == "done":
        return "[x]"
    if status == "partial":
        return "[~]"
    if status == "n/a":
        return "[-]"
    if status == "blocked":
        return "[!]"
    return "[ ]"


def main() -> None:
    plan = ascii_dash(PLAN.read_text(encoding="utf-8"))
    module_header = re.compile(r"^### (MOD-\d{3}) - (.+)$", re.M)
    phase_header = re.compile(r"^## (Phase \d+ - .+)$", re.M)
    # Plan bold form is **MOD-000-MP-001:** (colon inside closing marks)
    task_re = re.compile(
        r"\*\*(MOD-\d{3}-(?:MP|DB|BE|API|FE|WF|SEC|QA|DOC|AC)-\d{3}):\*\*\s*(.+)"
    )
    req_re = re.compile(r"\*\*Requirement Mapping:\*\*\s*(.+)")
    dep_re = re.compile(r"\*\*Dependencies:\*\*\s*(.+)")
    purpose_re = re.compile(r"\*\*Purpose:\*\*\s*(.+)")

    matches = list(module_header.finditer(plan))
    phases = list(phase_header.finditer(plan))

    def current_phase(pos: int) -> str:
        cur = "Unscoped"
        for p in phases:
            if p.start() <= pos:
                cur = p.group(1)
            else:
                break
        return cur

    modules: list[dict] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(plan)
        body = plan[start:end]
        modules.append(
            {
                "id": m.group(1),
                "title": m.group(2).strip(),
                "phase": current_phase(start),
                "purpose": (purpose_re.search(body).group(1).strip() if purpose_re.search(body) else ""),
                "requirements": (req_re.search(body).group(1).strip() if req_re.search(body) else ""),
                "dependencies": (dep_re.search(body).group(1).strip() if dep_re.search(body) else ""),
                "tasks": task_re.findall(body),
            }
        )

    # Counts
    status_counts: Counter[str] = Counter()
    lines: list[str] = []
    lines.append("# MASMS Implementation Progress Checklist")
    lines.append("")
    lines.append("**Source:** `MASMS_CURSOR_MODULE_WISE_IMPLEMENTATION_PLAN.md`")
    lines.append("**Companion evidence gate checklist:** `MASMS_CURSOR_COMPLETE_DEVELOPMENT_CHECKLIST.md`")
    lines.append("**Last updated (workspace):** 2026-08-10")
    lines.append("**Rule:** checkmarks reflect repository evidence only; human Done approval is separate.")
    lines.append("")
    lines.append("## Legend")
    lines.append("")
    lines.append("| Mark | Meaning |")
    lines.append("|---|---|")
    lines.append("| `[x]` | Done with evidence |")
    lines.append("| `[~]` | Partial / scaffold only |")
    lines.append("| `[-]` | N/A for current scope (deferred by design) |")
    lines.append("| `[!]` | Blocked (needs human or external dependency) |")
    lines.append("| `[ ]` | Not started |")
    lines.append("")
    lines.append("## Summary roll-up")
    lines.append("")
    lines.append("| Module | Phase | Tasks | Done | Partial | N/A | Blocked | Open | Module status |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---|")

    module_summaries: list[tuple[str, str, Counter[str], str]] = []
    for mod in modules:
        c: Counter[str] = Counter()
        for tid, _desc in mod["tasks"]:
            st = STATUS.get(tid, ("", ""))[0]
            key = st if st else "open"
            c[key] += 1
            status_counts[key] += 1
        total = len(mod["tasks"])
        if c["blocked"]:
            mod_status = "Blocked"
        elif c["done"] == total:
            mod_status = "Complete"
        elif c["done"] or c["partial"] or c["n/a"]:
            mod_status = "In progress"
        else:
            mod_status = "Not started"
        # Special-case MOD-000: not Complete because AC-901 blocked / FE open
        if mod["id"] == "MOD-000" and c["blocked"]:
            mod_status = "In progress (human approval blocked)"
        module_summaries.append((mod["id"], mod["phase"], c, mod_status))

    for mid, phase, c, mod_status in module_summaries:
        total = sum(c.values())
        lines.append(
            f"| {mid} | {phase} | {total} | {c['done']} | {c['partial']} | {c['n/a']} | {c['blocked']} | {c['open']} | {mod_status} |"
        )

    lines.append("")
    lines.append(
        f"**Totals:** {sum(status_counts.values())} tasks — "
        f"done {status_counts['done']}, partial {status_counts['partial']}, "
        f"n/a {status_counts['n/a']}, blocked {status_counts['blocked']}, open {status_counts['open']}"
    )
    lines.append("")
    lines.append("## Module index (plan order)")
    lines.append("")
    for i, mod in enumerate(modules, start=1):
        lines.append(f"{i}. [{mod['id']}](#{mod['id'].lower()}) — {mod['title']}")
    lines.append("")

    current_phase_name = None
    for mod in modules:
        if mod["phase"] != current_phase_name:
            current_phase_name = mod["phase"]
            lines.append(f"## {current_phase_name}")
            lines.append("")

        lines.append(f"### {mod['id']}")
        lines.append("")
        lines.append(f"**Title:** {mod['title']}  ")
        lines.append(f"**Purpose:** {mod['purpose']}  ")
        lines.append(f"**Requirements:** {mod['requirements']}  ")
        lines.append(f"**Dependencies:** {mod['dependencies']}")
        lines.append("")

        # Group by category
        groups: dict[str, list[tuple[str, str]]] = {}
        order = ["MP", "DB", "BE", "API", "FE", "WF", "SEC", "QA", "DOC", "AC"]
        labels = {
            "MP": "Main points",
            "DB": "Database / data design",
            "BE": "Backend",
            "API": "API",
            "FE": "Frontend",
            "WF": "Workflow / agent / events / notifications",
            "SEC": "Security / privacy / audit",
            "QA": "Testing / verification",
            "DOC": "Documentation",
            "AC": "Acceptance gate",
        }
        for tid, desc in mod["tasks"]:
            cat = tid.split("-")[2]
            groups.setdefault(cat, []).append((tid, desc.strip()))

        for cat in order:
            items = groups.get(cat)
            if not items:
                continue
            lines.append(f"#### {labels[cat]}")
            lines.append("")
            for tid, desc in items:
                st, note = STATUS.get(tid, ("", ""))
                mark = box(st)
                if note:
                    lines.append(f"- {mark} **{tid}:** {desc}  ")
                    lines.append(f"  - Evidence/note: {note}")
                else:
                    lines.append(f"- {mark} **{tid}:** {desc}")
            lines.append("")

        # Derived module Done checkbox (AC-901 style)
        lines.append(f"#### Module completion")
        lines.append("")
        if mod["id"] == "MOD-000":
            lines.append(
                f"- [!] **{mod['id']}-DONE:** Module marked Done before dependents  "
            )
            lines.append(
                "  - Evidence/note: Not Done — AC-901 human approval pending; FE deferred"
            )
        else:
            lines.append(f"- [ ] **{mod['id']}-DONE:** Module marked Done before dependents")
        lines.append("")

    lines.append("## Final MVP sequence (from plan)")
    lines.append("")
    finals = re.findall(r"\*\*(FINAL-\d{3}):\*\*\s*(.+)", plan)
    for tid, desc in finals:
        lines.append(f"- [ ] **{tid}:** {desc.strip()}")
    lines.append("")
    lines.append("## Cross-module release gates (from plan)")
    lines.append("")
    gates = re.findall(r"\*\*(GATE-\d{3}):\*\*\s*(.+)", plan)
    for tid, desc in gates:
        lines.append(f"- [ ] **{tid}:** {desc.strip()}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "Generated by `scripts/generate_implementation_progress_checklist.py`. "
        "Update the `STATUS` map in that script when work completes, then regenerate."
    )

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} with {len(modules)} modules, {sum(len(m['tasks']) for m in modules)} tasks")
    print(dict(status_counts))


if __name__ == "__main__":
    main()
