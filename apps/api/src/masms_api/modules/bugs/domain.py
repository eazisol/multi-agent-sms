"""Bugs domain rules (MOD-410)."""

from __future__ import annotations

from masms_api.errors import ConflictError, InvalidTransitionError, ValidationAppError

SEVERITIES = frozenset({"critical", "high", "medium", "low"})
BUG_STATUSES = frozenset(
    {
        "open",
        "in_fix",
        "fixed",
        "retesting",
        "rejected",
        "verified",
        "closed",
        "known_issue",
    }
)
LINK_TYPES = frozenset(
    {
        "requirement",
        "ticket",
        "test_case",
        "test_run",
        "fix",
        "retest",
        "release",
    }
)
TERMINAL_BUGS = frozenset({"closed", "verified"})
BLOCKING_SEVERITIES = frozenset({"critical", "high"})

BUG_TRANSITIONS: dict[str, frozenset[str]] = {
    "open": frozenset({"in_fix", "rejected", "closed", "known_issue"}),
    "rejected": frozenset({"open"}),  # reopen
    "in_fix": frozenset({"fixed", "open", "rejected", "known_issue"}),
    "fixed": frozenset({"retesting", "in_fix"}),
    "retesting": frozenset({"verified", "in_fix", "rejected"}),
    "verified": frozenset({"closed"}),
    "closed": frozenset(),
    "known_issue": frozenset({"open", "in_fix", "closed"}),
}


def assert_severity(value: str) -> None:
    if value not in SEVERITIES:
        raise ValidationAppError(f"Invalid severity '{value}'")


def assert_link_type(value: str) -> None:
    if value not in LINK_TYPES:
        raise ValidationAppError(f"Invalid link type '{value}'")


def assert_bug_transition(*, from_status: str, to_status: str) -> None:
    allowed = BUG_TRANSITIONS.get(from_status, frozenset())
    if to_status not in allowed:
        raise InvalidTransitionError(
            f"Invalid bug transition {from_status} → {to_status}"
        )


def assert_expected_version(*, current: int, expected: int | None) -> None:
    if expected is not None and current != expected:
        raise ConflictError(
            f"Optimistic concurrency conflict: expected version {expected}, got {current}"
        )


def severity_blocks_release(severity: str, *, blocks_release_flag: bool) -> bool:
    return blocks_release_flag or severity in BLOCKING_SEVERITIES


def is_actively_blocking(
    *,
    status: str,
    severity: str,
    blocks_release_flag: bool,
    has_approved_known_issue: bool,
) -> bool:
    """AC-002: unresolved blocking defects without known-issue approval block release."""
    if status in TERMINAL_BUGS:
        return False
    if status == "known_issue" or has_approved_known_issue:
        return False
    return severity_blocks_release(severity, blocks_release_flag=blocks_release_flag)
