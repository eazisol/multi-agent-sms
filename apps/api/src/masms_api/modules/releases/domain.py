"""Releases domain rules (MOD-430)."""

from __future__ import annotations

from masms_api.errors import (
    ApprovalRequiredError,
    ConflictError,
    InvalidTransitionError,
    ValidationAppError,
)

RELEASE_STATUSES = frozenset(
    {
        "draft",
        "ready_for_approval",
        "approved_for_production",
        "deploying",
        "deployed",
        "rolled_back",
        "closed",
        "cancelled",
    }
)
ITEM_LINK_TYPES = frozenset(
    {"requirement", "ticket", "test_case", "bug", "change_request", "document"}
)
ENVIRONMENTS = frozenset({"local", "staging", "production"})
CHECK_RESULTS = frozenset({"passed", "failed", "blocked", "skipped"})

RELEASE_TRANSITIONS: dict[str, frozenset[str]] = {
    "draft": frozenset({"ready_for_approval", "cancelled"}),
    "ready_for_approval": frozenset({"approved_for_production", "draft", "cancelled"}),
    "approved_for_production": frozenset({"deploying", "cancelled"}),
    "deploying": frozenset({"deployed", "rolled_back"}),
    "deployed": frozenset({"closed", "rolled_back"}),
    "rolled_back": frozenset({"draft", "cancelled"}),
    "closed": frozenset(),
    "cancelled": frozenset(),
}


def assert_link_type(value: str) -> None:
    if value not in ITEM_LINK_TYPES:
        raise ValidationAppError(f"Invalid release item link type '{value}'")


def assert_environment(value: str) -> None:
    if value not in ENVIRONMENTS:
        raise ValidationAppError(f"Invalid environment '{value}'")


def assert_release_transition(*, from_status: str, to_status: str) -> None:
    allowed = RELEASE_TRANSITIONS.get(from_status, frozenset())
    if to_status not in allowed:
        raise InvalidTransitionError(
            f"Invalid release transition {from_status} → {to_status}"
        )


def assert_expected_version(*, current: int, expected: int | None) -> None:
    if expected is not None and current != expected:
        raise ConflictError(
            f"Optimistic concurrency conflict: expected version {expected}, got {current}"
        )


def assert_production_may_start(*, release_status: str, has_approval_evidence: bool) -> None:
    """AC-001: production cannot start without approval evidence."""
    if release_status != "approved_for_production":
        raise ApprovalRequiredError(
            "Production deployment requires an approved release"
        )
    if not has_approval_evidence:
        raise ApprovalRequiredError(
            "Production deployment requires recorded approval evidence"
        )
