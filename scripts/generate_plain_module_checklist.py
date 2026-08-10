"""Generate an easy hierarchical plain checklist from the module-wise plan."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "MASMS_CURSOR_MODULE_WISE_IMPLEMENTATION_PLAN.md"
OUT = ROOT / "MASMS_PLAIN_MODULE_CHECKLIST.md"

# Keep in sync with scripts/generate_implementation_progress_checklist.py STATUS
STATUS: dict[str, tuple[str, str]] = {
    "MOD-000-MP-001": ("done", ""),
    "MOD-000-MP-002": ("done", ""),
    "MOD-000-MP-003": ("done", ""),
    "MOD-000-MP-004": ("done", ""),
    "MOD-000-MP-005": ("done", ""),
    "MOD-000-DB-001": ("done", ""),
    "MOD-000-DB-002": ("done", ""),
    "MOD-000-DB-003": ("done", ""),
    "MOD-000-DB-004": ("done", ""),
    "MOD-000-DB-005": ("done", ""),
    "MOD-000-BE-001": ("done", ""),
    "MOD-000-BE-002": ("done", ""),
    "MOD-000-BE-003": ("n/a", ""),
    "MOD-000-BE-004": ("done", ""),
    "MOD-000-API-001": ("done", ""),
    "MOD-000-API-002": ("done", ""),
    "MOD-000-API-003": ("done", ""),
    "MOD-000-FE-001": ("partial", ""),
    "MOD-000-FE-002": ("partial", ""),
    "MOD-000-FE-003": ("done", ""),
    "MOD-000-FE-004": ("partial", ""),
    "MOD-000-WF-001": ("done", ""),
    "MOD-000-WF-002": ("n/a", ""),
    "MOD-000-WF-003": ("done", ""),
    "MOD-000-WF-004": ("n/a", ""),
    "MOD-000-SEC-001": ("partial", ""),
    "MOD-000-SEC-002": ("partial", ""),
    "MOD-000-SEC-003": ("partial", ""),
    "MOD-000-SEC-004": ("partial", ""),
    "MOD-000-QA-001": ("done", ""),
    "MOD-000-QA-002": ("done", ""),
    "MOD-000-QA-003": ("partial", ""),
    "MOD-000-QA-004": ("n/a", ""),
    "MOD-000-QA-005": ("partial", ""),
    "MOD-000-DOC-001": ("partial", ""),
    "MOD-000-DOC-002": ("done", ""),
    "MOD-000-AC-001": ("partial", ""),
    "MOD-000-AC-002": ("done", ""),
    "MOD-000-AC-003": ("done", ""),
    "MOD-000-AC-900": ("done", ""),
    "MOD-000-AC-901": ("blocked", ""),
    "MOD-010-MP-001": ("done", ""),
    "MOD-010-MP-002": ("done", ""),
    "MOD-010-MP-003": ("done", ""),
    "MOD-010-MP-004": ("done", ""),
    "MOD-010-MP-005": ("done", ""),
    "MOD-010-MP-006": ("done", ""),
    "MOD-010-MP-007": ("done", ""),
    "MOD-010-MP-008": ("done", ""),
    "MOD-010-DB-001": ("n/a", ""),
    "MOD-010-DB-002": ("n/a", ""),
    "MOD-010-DB-003": ("n/a", ""),
    "MOD-010-DB-004": ("n/a", ""),
    "MOD-010-DB-005": ("n/a", ""),
    "MOD-010-DB-006": ("n/a", ""),
    "MOD-010-DB-007": ("n/a", ""),
    "MOD-010-DB-008": ("n/a", ""),
    "MOD-010-BE-001": ("n/a", ""),
    "MOD-010-BE-002": ("n/a", ""),
    "MOD-010-BE-003": ("n/a", ""),
    "MOD-010-BE-004": ("n/a", ""),
    "MOD-010-API-001": ("n/a", ""),
    "MOD-010-API-002": ("n/a", ""),
    "MOD-010-API-003": ("n/a", ""),
    "MOD-010-FE-001": ("n/a", ""),
    "MOD-010-FE-002": ("n/a", ""),
    "MOD-010-FE-003": ("n/a", ""),
    "MOD-010-FE-004": ("n/a", ""),
    "MOD-010-WF-001": ("n/a", ""),
    "MOD-010-WF-002": ("n/a", ""),
    "MOD-010-WF-003": ("n/a", ""),
    "MOD-010-WF-004": ("n/a", ""),
    "MOD-010-SEC-001": ("n/a", ""),
    "MOD-010-SEC-002": ("n/a", ""),
    "MOD-010-SEC-003": ("done", ""),
    "MOD-010-SEC-004": ("n/a", ""),
    "MOD-010-QA-001": ("n/a", ""),
    "MOD-010-QA-002": ("n/a", ""),
    "MOD-010-QA-003": ("n/a", ""),
    "MOD-010-QA-004": ("n/a", ""),
    "MOD-010-QA-005": ("done", ""),
    "MOD-010-DOC-001": ("done", ""),
    "MOD-010-DOC-002": ("done", ""),
    "MOD-010-AC-001": ("done", ""),
    "MOD-010-AC-002": ("done", ""),
    "MOD-010-AC-003": ("done", ""),
    "MOD-010-AC-900": ("done", ""),
    "MOD-010-AC-901": ("blocked", ""),
    "MOD-020-MP-001": ("done", ""),
    "MOD-020-MP-002": ("done", ""),
    "MOD-020-MP-003": ("done", ""),
    "MOD-020-MP-004": ("done", ""),
    "MOD-020-MP-005": ("done", ""),
    "MOD-020-MP-006": ("done", ""),
    "MOD-020-MP-007": ("done", ""),
    "MOD-020-MP-008": ("done", ""),
    "MOD-020-MP-009": ("done", ""),
    "MOD-020-DB-001": ("done", ""),
    "MOD-020-DB-002": ("done", ""),
    "MOD-020-DB-003": ("done", ""),
    "MOD-020-DB-004": ("done", ""),
    "MOD-020-DB-005": ("done", ""),
    "MOD-020-DB-006": ("done", ""),
    "MOD-020-DB-007": ("done", ""),
    "MOD-020-DB-008": ("done", ""),
    "MOD-020-DB-009": ("done", ""),
    "MOD-020-BE-001": ("partial", ""),
    "MOD-020-BE-002": ("partial", ""),
    "MOD-020-BE-003": ("partial", ""),
    "MOD-020-BE-004": ("done", ""),
    "MOD-020-API-002": ("partial", ""),
    "MOD-020-API-003": ("partial", ""),
    "MOD-020-FE-001": ("n/a", ""),
    "MOD-020-FE-002": ("n/a", ""),
    "MOD-020-FE-003": ("n/a", ""),
    "MOD-020-FE-004": ("n/a", ""),
    "MOD-020-WF-002": ("partial", ""),
    "MOD-020-WF-003": ("partial", ""),
    "MOD-020-SEC-002": ("partial", ""),
    "MOD-020-QA-001": ("done", ""),
    "MOD-020-QA-002": ("partial", ""),
    "MOD-020-QA-005": ("done", ""),
    "MOD-020-DOC-001": ("partial", ""),
    "MOD-020-DOC-002": ("done", ""),
    "MOD-020-AC-001": ("partial", ""),
    "MOD-020-AC-002": ("partial", ""),
    "MOD-020-AC-003": ("partial", ""),
    "MOD-020-AC-900": ("done", ""),
    "MOD-020-AC-901": ("blocked", ""),
    "MOD-030-MP-001": ("done", ""),
    "MOD-030-MP-002": ("done", ""),
    "MOD-030-MP-003": ("done", ""),
    "MOD-030-MP-004": ("done", ""),
    "MOD-030-MP-005": ("done", ""),
    "MOD-030-MP-006": ("done", ""),
    "MOD-030-DB-001": ("n/a", ""),
    "MOD-030-DB-002": ("n/a", ""),
    "MOD-030-DB-003": ("n/a", ""),
    "MOD-030-DB-004": ("n/a", ""),
    "MOD-030-DB-005": ("n/a", ""),
    "MOD-030-DB-006": ("n/a", ""),
    "MOD-030-BE-001": ("n/a", ""),
    "MOD-030-BE-002": ("n/a", ""),
    "MOD-030-BE-003": ("n/a", ""),
    "MOD-030-BE-004": ("n/a", ""),
    "MOD-030-API-001": ("n/a", ""),
    "MOD-030-API-002": ("n/a", ""),
    "MOD-030-API-003": ("n/a", ""),
    "MOD-030-FE-001": ("n/a", ""),
    "MOD-030-FE-002": ("n/a", ""),
    "MOD-030-FE-003": ("n/a", ""),
    "MOD-030-FE-004": ("n/a", ""),
    "MOD-030-WF-001": ("n/a", ""),
    "MOD-030-WF-002": ("n/a", ""),
    "MOD-030-WF-003": ("n/a", ""),
    "MOD-030-WF-004": ("n/a", ""),
    "MOD-030-SEC-001": ("partial", ""),
    "MOD-030-SEC-002": ("n/a", ""),
    "MOD-030-SEC-003": ("done", ""),
    "MOD-030-SEC-004": ("n/a", ""),
    "MOD-030-QA-001": ("done", ""),
    "MOD-030-QA-002": ("n/a", ""),
    "MOD-030-QA-003": ("n/a", ""),
    "MOD-030-QA-004": ("n/a", ""),
    "MOD-030-QA-005": ("done", ""),
    "MOD-030-DOC-001": ("done", ""),
    "MOD-030-DOC-002": ("done", ""),
    "MOD-030-AC-001": ("partial", ""),
    "MOD-030-AC-002": ("done", ""),
    "MOD-030-AC-003": ("done", ""),
    "MOD-030-AC-900": ("done", ""),
    "MOD-030-AC-901": ("blocked", ""),
    "MOD-040-MP-001": ("done", ""),
    "MOD-040-MP-002": ("done", ""),
    "MOD-040-MP-003": ("done", ""),
    "MOD-040-MP-004": ("done", ""),
    "MOD-040-MP-005": ("done", ""),
    "MOD-040-MP-006": ("done", ""),
    "MOD-040-MP-007": ("done", ""),
    "MOD-040-DB-001": ("done", ""),
    "MOD-040-DB-002": ("done", ""),
    "MOD-040-DB-003": ("done", ""),
    "MOD-040-DB-004": ("done", ""),
    "MOD-040-DB-005": ("done", ""),
    "MOD-040-DB-006": ("n/a", ""),
    "MOD-040-DB-007": ("n/a", ""),
    "MOD-040-BE-001": ("done", ""),
    "MOD-040-BE-002": ("partial", ""),
    "MOD-040-BE-003": ("partial", ""),
    "MOD-040-BE-004": ("done", ""),
    "MOD-040-API-001": ("partial", ""),
    "MOD-040-API-002": ("partial", ""),
    "MOD-040-API-003": ("partial", ""),
    "MOD-040-FE-001": ("n/a", ""),
    "MOD-040-FE-002": ("n/a", ""),
    "MOD-040-FE-003": ("n/a", ""),
    "MOD-040-FE-004": ("n/a", ""),
    "MOD-040-WF-001": ("n/a", ""),
    "MOD-040-WF-002": ("n/a", ""),
    "MOD-040-WF-003": ("partial", ""),
    "MOD-040-WF-004": ("n/a", ""),
    "MOD-040-SEC-001": ("partial", ""),
    "MOD-040-SEC-002": ("done", ""),
    "MOD-040-SEC-003": ("done", ""),
    "MOD-040-SEC-004": ("done", ""),
    "MOD-040-QA-001": ("done", ""),
    "MOD-040-QA-002": ("done", ""),
    "MOD-040-QA-003": ("partial", ""),
    "MOD-040-QA-004": ("n/a", ""),
    "MOD-040-QA-005": ("done", ""),
    "MOD-040-DOC-001": ("done", ""),
    "MOD-040-DOC-002": ("done", ""),
    "MOD-040-AC-001": ("partial", ""),
    "MOD-040-AC-002": ("done", ""),
    "MOD-040-AC-003": ("done", ""),
    "MOD-040-AC-900": ("done", ""),
    "MOD-040-AC-901": ("blocked", ""),
    "MOD-100-MP-001": ("done", ""),
    "MOD-100-MP-002": ("done", ""),
    "MOD-100-MP-003": ("done", ""),
    "MOD-100-MP-004": ("done", ""),
    "MOD-100-MP-005": ("done", ""),
    "MOD-100-MP-006": ("done", ""),
    "MOD-100-MP-007": ("done", ""),
    "MOD-100-MP-008": ("done", ""),
    "MOD-100-MP-009": ("done", ""),
    "MOD-100-DB-001": ("done", ""),
    "MOD-100-DB-002": ("done", ""),
    "MOD-100-DB-003": ("done", ""),
    "MOD-100-DB-004": ("done", ""),
    "MOD-100-DB-005": ("done", ""),
    "MOD-100-DB-006": ("done", ""),
    "MOD-100-DB-007": ("done", ""),
    "MOD-100-DB-008": ("done", ""),
    "MOD-100-DB-009": ("done", ""),
    "MOD-100-BE-001": ("done", ""),
    "MOD-100-BE-002": ("partial", ""),
    "MOD-100-BE-003": ("partial", ""),
    "MOD-100-BE-004": ("done", ""),
    "MOD-100-API-001": ("done", ""),
    "MOD-100-API-002": ("partial", ""),
    "MOD-100-API-003": ("partial", ""),
    "MOD-100-FE-001": ("n/a", ""),
    "MOD-100-FE-002": ("n/a", ""),
    "MOD-100-FE-003": ("n/a", ""),
    "MOD-100-FE-004": ("n/a", ""),
    "MOD-100-WF-001": ("n/a", ""),
    "MOD-100-WF-002": ("n/a", ""),
    "MOD-100-WF-003": ("partial", ""),
    "MOD-100-WF-004": ("n/a", ""),
    "MOD-100-SEC-001": ("partial", ""),
    "MOD-100-SEC-002": ("done", ""),
    "MOD-100-SEC-003": ("partial", ""),
    "MOD-100-SEC-004": ("done", ""),
    "MOD-100-QA-001": ("done", ""),
    "MOD-100-QA-002": ("done", ""),
    "MOD-100-QA-003": ("partial", ""),
    "MOD-100-QA-004": ("n/a", ""),
    "MOD-100-QA-005": ("done", ""),
    "MOD-100-DOC-001": ("done", ""),
    "MOD-100-DOC-002": ("done", ""),
    "MOD-100-AC-001": ("partial", ""),
    "MOD-100-AC-002": ("done", ""),
    "MOD-100-AC-003": ("done", ""),
    "MOD-100-AC-900": ("done", ""),
    "MOD-100-AC-901": ("blocked", ""),
    "MOD-110-MP-001": ("done", ""),
    "MOD-110-MP-002": ("done", ""),
    "MOD-110-MP-003": ("done", ""),
    "MOD-110-MP-004": ("done", ""),
    "MOD-110-MP-005": ("done", ""),
    "MOD-110-MP-006": ("done", ""),
    "MOD-110-MP-007": ("done", ""),
    "MOD-110-DB-001": ("partial", ""),
    "MOD-110-DB-002": ("done", ""),
    "MOD-110-DB-003": ("done", ""),
    "MOD-110-DB-004": ("done", ""),
    "MOD-110-DB-005": ("partial", ""),
    "MOD-110-DB-006": ("done", ""),
    "MOD-110-DB-007": ("done", ""),
    "MOD-110-BE-001": ("done", ""),
    "MOD-110-BE-002": ("partial", ""),
    "MOD-110-BE-003": ("n/a", ""),
    "MOD-110-BE-004": ("done", ""),
    "MOD-110-API-001": ("done", ""),
    "MOD-110-API-002": ("partial", ""),
    "MOD-110-API-003": ("partial", ""),
    "MOD-110-FE-001": ("n/a", ""),
    "MOD-110-FE-002": ("n/a", ""),
    "MOD-110-FE-003": ("n/a", ""),
    "MOD-110-FE-004": ("n/a", ""),
    "MOD-110-WF-001": ("n/a", ""),
    "MOD-110-WF-002": ("n/a", ""),
    "MOD-110-WF-003": ("n/a", ""),
    "MOD-110-WF-004": ("n/a", ""),
    "MOD-110-SEC-001": ("partial", ""),
    "MOD-110-SEC-002": ("done", ""),
    "MOD-110-SEC-003": ("done", ""),
    "MOD-110-SEC-004": ("done", ""),
    "MOD-110-QA-001": ("done", ""),
    "MOD-110-QA-002": ("done", ""),
    "MOD-110-QA-003": ("partial", ""),
    "MOD-110-QA-004": ("n/a", ""),
    "MOD-110-QA-005": ("done", ""),
    "MOD-110-DOC-001": ("done", ""),
    "MOD-110-DOC-002": ("done", ""),
    "MOD-110-AC-001": ("partial", ""),
    "MOD-110-AC-002": ("done", ""),
    "MOD-110-AC-003": ("done", ""),
    "MOD-110-AC-900": ("done", ""),
    "MOD-110-AC-901": ("blocked", ""),
    "MOD-120-MP-001": ("done", ""),
    "MOD-120-MP-002": ("done", ""),
    "MOD-120-MP-003": ("done", ""),
    "MOD-120-MP-004": ("done", ""),
    "MOD-120-MP-005": ("done", ""),
    "MOD-120-MP-006": ("done", ""),
    "MOD-120-MP-007": ("done", ""),
    "MOD-120-MP-008": ("done", ""),
    "MOD-120-DB-001": ("done", ""),
    "MOD-120-DB-002": ("done", ""),
    "MOD-120-DB-003": ("done", ""),
    "MOD-120-DB-004": ("done", ""),
    "MOD-120-DB-005": ("done", ""),
    "MOD-120-DB-006": ("done", ""),
    "MOD-120-DB-007": ("done", ""),
    "MOD-120-DB-008": ("done", ""),
    "MOD-120-BE-001": ("done", ""),
    "MOD-120-BE-002": ("partial", ""),
    "MOD-120-BE-003": ("n/a", ""),
    "MOD-120-BE-004": ("done", ""),
    "MOD-120-API-001": ("done", ""),
    "MOD-120-API-002": ("partial", ""),
    "MOD-120-API-003": ("partial", ""),
    "MOD-120-FE-001": ("n/a", ""),
    "MOD-120-FE-002": ("n/a", ""),
    "MOD-120-FE-003": ("n/a", ""),
    "MOD-120-FE-004": ("n/a", ""),
    "MOD-120-WF-001": ("n/a", ""),
    "MOD-120-WF-002": ("n/a", ""),
    "MOD-120-WF-003": ("n/a", ""),
    "MOD-120-WF-004": ("n/a", ""),
    "MOD-120-SEC-001": ("partial", ""),
    "MOD-120-SEC-002": ("done", ""),
    "MOD-120-SEC-003": ("partial", ""),
    "MOD-120-SEC-004": ("done", ""),
    "MOD-120-QA-001": ("done", ""),
    "MOD-120-QA-002": ("done", ""),
    "MOD-120-QA-003": ("done", ""),
    "MOD-120-QA-004": ("n/a", ""),
    "MOD-120-QA-005": ("done", ""),
    "MOD-120-DOC-001": ("done", ""),
    "MOD-120-DOC-002": ("done", ""),
    "MOD-120-AC-001": ("partial", ""),
    "MOD-120-AC-002": ("done", ""),
    "MOD-120-AC-003": ("done", ""),
    "MOD-120-AC-900": ("done", ""),
    "MOD-120-AC-901": ("blocked", ""),
    "MOD-130-MP-001": ("done", ""),
    "MOD-130-MP-002": ("done", ""),
    "MOD-130-MP-003": ("done", ""),
    "MOD-130-MP-004": ("done", ""),
    "MOD-130-MP-005": ("done", ""),
    "MOD-130-MP-006": ("done", ""),
    "MOD-130-MP-007": ("done", ""),
    "MOD-130-MP-008": ("done", ""),
    "MOD-130-DB-001": ("done", ""),
    "MOD-130-DB-002": ("done", ""),
    "MOD-130-DB-003": ("done", ""),
    "MOD-130-DB-004": ("done", ""),
    "MOD-130-DB-005": ("done", ""),
    "MOD-130-DB-006": ("done", ""),
    "MOD-130-DB-007": ("done", ""),
    "MOD-130-DB-008": ("done", ""),
    "MOD-130-BE-001": ("done", ""),
    "MOD-130-BE-002": ("partial", ""),
    "MOD-130-BE-003": ("n/a", ""),
    "MOD-130-BE-004": ("done", ""),
    "MOD-130-API-001": ("done", ""),
    "MOD-130-API-002": ("partial", ""),
    "MOD-130-API-003": ("partial", ""),
    "MOD-130-FE-001": ("n/a", ""),
    "MOD-130-FE-002": ("n/a", ""),
    "MOD-130-FE-003": ("n/a", ""),
    "MOD-130-FE-004": ("n/a", ""),
    "MOD-130-WF-001": ("n/a", ""),
    "MOD-130-WF-002": ("n/a", ""),
    "MOD-130-WF-003": ("n/a", ""),
    "MOD-130-WF-004": ("n/a", ""),
    "MOD-130-SEC-001": ("partial", ""),
    "MOD-130-SEC-002": ("done", ""),
    "MOD-130-SEC-003": ("done", ""),
    "MOD-130-SEC-004": ("partial", ""),
    "MOD-130-QA-001": ("done", ""),
    "MOD-130-QA-002": ("done", ""),
    "MOD-130-QA-003": ("partial", ""),
    "MOD-130-QA-004": ("n/a", ""),
    "MOD-130-QA-005": ("done", ""),
    "MOD-130-DOC-001": ("done", ""),
    "MOD-130-DOC-002": ("done", ""),
    "MOD-130-AC-001": ("done", ""),
    "MOD-130-AC-002": ("done", ""),
    "MOD-130-AC-003": ("done", ""),
    "MOD-130-AC-900": ("done", ""),
    "MOD-130-AC-901": ("blocked", ""),
}

CAT_ORDER = ["MP", "DB", "BE", "API", "FE", "WF", "SEC", "QA", "DOC", "AC"]
CAT_LABELS = {
    "MP": "Main goals",
    "DB": "Database",
    "BE": "Backend",
    "API": "API",
    "FE": "Frontend",
    "WF": "Workflow / agents / events",
    "SEC": "Security / audit",
    "QA": "Testing",
    "DOC": "Docs",
    "AC": "Acceptance / Done gate",
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


def group_status(statuses: list[str]) -> str:
    if not statuses:
        return ""
    if all(s == "done" for s in statuses):
        return "done"
    if any(s == "blocked" for s in statuses):
        return "blocked"
    if all(s in {"done", "n/a"} for s in statuses) and any(s == "done" for s in statuses):
        return "done"
    if any(s in {"done", "partial", "n/a", "blocked"} for s in statuses):
        return "partial"
    return ""


def clean_desc(desc: str) -> str:
    desc = re.sub(r"\*\*(.+?)\*\*", r"\1", desc)
    desc = desc.strip()
    # Shorten boilerplate DB lines for readability
    prefix = (
        "Define the data model, ownership, tenant/project scope, constraints, "
        "indexes, versioning, retention, RLS, audit, and migration behavior for "
    )
    if desc.startswith(prefix):
        rest = desc[len(prefix) :].strip().rstrip(".")
        return f"Design and migrate data for: {rest}"
    prefix2 = "Implement and verify "
    if desc.startswith(prefix2):
        return "Build and verify: " + desc[len(prefix2) :].rstrip(".")
    return desc


def main() -> None:
    plan = ascii_dash(PLAN.read_text(encoding="utf-8"))
    module_header = re.compile(r"^### (MOD-\d{3}) - (.+)$", re.M)
    phase_header = re.compile(r"^## (Phase \d+ - .+)$", re.M)
    task_re = re.compile(
        r"\*\*(MOD-\d{3}-(?:MP|DB|BE|API|FE|WF|SEC|QA|DOC|AC)-\d{3}):\*\*\s*(.+)"
    )
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
                "tasks": task_re.findall(body),
            }
        )

    lines: list[str] = []
    lines.append("# MASMS Plain Module Checklist")
    lines.append("")
    lines.append("Easy view of the implementation plan: **Module -> Main task -> Sub-task**.")
    lines.append("")
    lines.append("Sources: `MASMS_CURSOR_MODULE_WISE_IMPLEMENTATION_PLAN.md` · status also tracked in")
    lines.append("`MASMS_IMPLEMENTATION_PROGRESS_CHECKLIST.md` and `MASMS_CURSOR_COMPLETE_DEVELOPMENT_CHECKLIST.md`.")
    lines.append("")
    lines.append("## How to read this")
    lines.append("")
    lines.append("```")
    lines.append("Module N: MOD-xxx Title")
    lines.append("  M1: [ ] Main task group (example: API)")
    lines.append("       M1-1: [ ] First sub-task")
    lines.append("       M1-2: [ ] Second sub-task")
    lines.append("```")
    lines.append("")
    lines.append("| Mark | Meaning |")
    lines.append("|---|---|")
    lines.append("| `[x]` | Done |")
    lines.append("| `[~]` | Partial |")
    lines.append("| `[-]` | Not needed for current stub / deferred by design |")
    lines.append("| `[!]` | Blocked (needs human or external dependency) |")
    lines.append("| `[ ]` | Not started |")
    lines.append("")
    lines.append("Plan IDs (like `MOD-000-API-001`) are shown in parentheses for traceability.")
    lines.append("")

    # Quick scoreboard
    lines.append("## Scoreboard")
    lines.append("")
    lines.append("| # | Module | Status | Done | Partial | Open |")
    lines.append("|---:|---|---|---:|---:|---:|")
    totals: Counter[str] = Counter()
    for idx, mod in enumerate(modules, start=1):
        c: Counter[str] = Counter()
        for tid, _ in mod["tasks"]:
            st = STATUS.get(tid, ("", ""))[0]
            key = st if st else "open"
            c[key] += 1
            totals[key] += 1
        open_n = c["open"]
        done_n = c["done"]
        if c["blocked"]:
            status = "Blocked"
        elif done_n == len(mod["tasks"]):
            status = "Complete"
        elif done_n or c["partial"] or c["n/a"]:
            status = "In progress"
        else:
            status = "Not started"
        if mod["id"] == "MOD-000" and c["blocked"]:
            status = "In progress (human approval blocked)"
        lines.append(
            f"| {idx} | {mod['id']} | {status} | {done_n} | {c['partial']} | {open_n} |"
        )

    lines.append("")
    lines.append(
        f"**All tasks:** {sum(totals.values())} · "
        f"done {totals['done']} · partial {totals['partial']} · "
        f"n/a {totals['n/a']} · blocked {totals['blocked']} · open {totals['open']}"
    )
    lines.append("")

    current_phase = None
    for mod_num, mod in enumerate(modules, start=1):
        if mod["phase"] != current_phase:
            current_phase = mod["phase"]
            lines.append(f"## {current_phase}")
            lines.append("")

        # Group tasks
        groups: dict[str, list[tuple[str, str]]] = {}
        for tid, desc in mod["tasks"]:
            cat = tid.split("-")[2]
            groups.setdefault(cat, []).append((tid, desc))

        mod_statuses = [STATUS.get(tid, ("", ""))[0] for tid, _ in mod["tasks"]]
        mod_box = box(group_status(mod_statuses))
        lines.append(f"### Module {mod_num}: {mod_box} {mod['id']} — {mod['title']}")
        lines.append("")

        m_idx = 0
        for cat in CAT_ORDER:
            items = groups.get(cat)
            if not items:
                continue
            m_idx += 1
            sub_statuses = [STATUS.get(tid, ("", ""))[0] for tid, _ in items]
            main_box = box(group_status(sub_statuses))
            lines.append(f"M{m_idx}: {main_box} {CAT_LABELS[cat]}")
            for sub_i, (tid, desc) in enumerate(items, start=1):
                st = STATUS.get(tid, ("", ""))[0]
                lines.append(
                    f"     M{m_idx}-{sub_i}: {box(st)} {clean_desc(desc)}  "
                    f"({tid})"
                )
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "Generated by `scripts/generate_plain_module_checklist.py`. "
        "Update STATUS in that script (keep aligned with the progress checklist), then regenerate."
    )
    lines.append("")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(modules)} modules, {sum(len(m['tasks']) for m in modules)} tasks)")


if __name__ == "__main__":
    main()
