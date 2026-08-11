"""Agent runtime domain rules (MOD-360)."""

from __future__ import annotations

from masms_api.errors import ConflictError, InvalidTransitionError, ValidationAppError

ALLOWED_CODES: frozenset[str] = frozenset(
    {
        "query_intake_agent",
        "requirements_clarifier",
        "roadmap_planner",
        "ticket_triage_agent",
        "qa_review_assistant",
        "status_report_drafter",
    }
)

AGENT_TITLES: dict[str, str] = {
    "query_intake_agent": "Query Intake Agent",
    "requirements_clarifier": "Requirements Clarifier",
    "roadmap_planner": "Roadmap Planner",
    "ticket_triage_agent": "Ticket Triage Agent",
    "qa_review_assistant": "QA Review Assistant",
    "status_report_drafter": "Status Report Drafter",
}

AGENT_DEPARTMENTS: dict[str, str] = {
    "query_intake_agent": "sales",
    "requirements_clarifier": "ba",
    "roadmap_planner": "pm",
    "ticket_triage_agent": "engineering",
    "qa_review_assistant": "qa",
    "status_report_drafter": "pm",
}

RUN_TRANSITIONS: dict[str, frozenset[str]] = {
    "pending": frozenset({"running", "cancelled"}),
    "running": frozenset({"completed", "failed", "review_required", "cancelled"}),
    "review_required": frozenset({"completed", "failed", "cancelled"}),
    "failed": frozenset({"running", "cancelled"}),
    "completed": frozenset(),
    "cancelled": frozenset(),
}

TERMINAL_RUN_STATUSES = frozenset({"completed", "cancelled"})
OPEN_RUN_STATUSES = frozenset({"pending", "running", "review_required", "failed"})

VERSION_STATUSES = frozenset({"draft", "active", "retired"})
REVIEW_STATUSES = frozenset({"pending", "approved", "rejected", "changes_requested"})
REVIEW_DECISIONS = frozenset({"approved", "rejected", "changes_requested"})

LOW_CONFIDENCE_THRESHOLD = 0.6


def assert_allowed_agent_code(code: str) -> None:
    if code not in ALLOWED_CODES:
        raise ValidationAppError(
            f"Unknown agent_code '{code}'. Only the approved catalog codes may be used."
        )


def assert_run_transition(*, from_status: str, to_status: str) -> None:
    allowed = RUN_TRANSITIONS.get(from_status, frozenset())
    if to_status not in allowed:
        raise InvalidTransitionError(
            f"Invalid agent run transition {from_status} → {to_status}"
        )


def assert_run_open(status: str) -> None:
    if status in TERMINAL_RUN_STATUSES:
        raise ConflictError(f"Agent run is closed (status={status})")
    if status not in OPEN_RUN_STATUSES:
        raise ConflictError(f"Agent run is not open (status={status})")


def assert_version_status(status: str) -> None:
    if status not in VERSION_STATUSES:
        raise ValidationAppError(f"Invalid prompt version status '{status}'")


def assert_review_decision(decision: str) -> None:
    if decision not in REVIEW_DECISIONS:
        raise ValidationAppError(f"Invalid review decision '{decision}'")


def assert_expected_version(*, current: int, expected: int | None) -> None:
    if expected is not None and current != expected:
        raise ConflictError(
            f"Optimistic concurrency conflict: expected version {expected}, got {current}"
        )


def resolve_run_status_after_stub(*, confidence: float, review_required_flag: bool) -> str:
    if review_required_flag or confidence < LOW_CONFIDENCE_THRESHOLD:
        return "review_required"
    return "completed"
