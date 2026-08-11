"""Testcases domain rules (MOD-400)."""

from __future__ import annotations

from masms_api.errors import ConflictError, InvalidTransitionError, ValidationAppError

CASE_PRIORITIES = frozenset({"P0", "P1", "P2", "P3"})
CASE_TYPES = frozenset(
    {
        "functional",
        "negative",
        "boundary",
        "validation",
        "permission",
        "integration",
        "concurrency",
        "regression",
        "browser",
        "device",
    }
)
CASE_STATUSES = frozenset({"draft", "approved", "retired"})
RUN_STATUSES = frozenset({"pending", "running", "passed", "failed", "blocked", "skipped"})
PLAN_STATUSES = frozenset({"draft", "active", "completed", "cancelled"})
SUITE_STATUSES = frozenset({"draft", "active", "retired"})

RUN_TRANSITIONS: dict[str, frozenset[str]] = {
    "pending": frozenset({"running", "cancelled", "skipped"}),
    "running": frozenset({"passed", "failed", "blocked", "skipped"}),
    "passed": frozenset(),
    "failed": frozenset({"running"}),
    "blocked": frozenset({"running", "skipped"}),
    "skipped": frozenset(),
    "cancelled": frozenset(),
}

# Treat cancelled as terminal even if not in RUN_STATUSES set above for transitions
TERMINAL_RUNS = frozenset({"passed", "failed", "skipped", "cancelled"})


def assert_case_type(value: str) -> None:
    if value not in CASE_TYPES:
        raise ValidationAppError(f"Invalid test case type '{value}'")


def assert_case_priority(value: str) -> None:
    if value not in CASE_PRIORITIES:
        raise ValidationAppError(f"Invalid test case priority '{value}'")


def assert_run_transition(*, from_status: str, to_status: str) -> None:
    allowed = RUN_TRANSITIONS.get(from_status, frozenset())
    if to_status not in allowed:
        raise InvalidTransitionError(
            f"Invalid test run transition {from_status} → {to_status}"
        )


def assert_expected_version(*, current: int, expected: int | None) -> None:
    if expected is not None and current != expected:
        raise ConflictError(
            f"Optimistic concurrency conflict: expected version {expected}, got {current}"
        )
