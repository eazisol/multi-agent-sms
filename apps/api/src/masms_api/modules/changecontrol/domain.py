"""Change-control domain rules (MOD-420)."""

from __future__ import annotations

from masms_api.errors import (
    ApprovalRequiredError,
    ConflictError,
    InvalidTransitionError,
    ValidationAppError,
)

RISK_STATUSES = frozenset({"open", "mitigating", "accepted", "closed"})
RISK_LEVELS = frozenset({"low", "medium", "high", "critical"})
CR_STATUSES = frozenset(
    {"draft", "impact_ready", "pending_approval", "approved", "rejected", "deferred"}
)
APPROVAL_DECISIONS = frozenset({"approved", "rejected", "deferred"})
BASELINE_ARTIFACT_TYPES = frozenset(
    {"requirement", "design", "roadmap", "ticket", "document", "security", "release_plan"}
)

CR_TRANSITIONS: dict[str, frozenset[str]] = {
    "draft": frozenset({"impact_ready", "rejected"}),
    "impact_ready": frozenset({"pending_approval", "draft"}),
    "pending_approval": frozenset({"approved", "rejected", "deferred"}),
    "approved": frozenset(),
    "rejected": frozenset({"draft"}),
    "deferred": frozenset({"draft", "pending_approval"}),
}

DEVELOPMENT_GATE_STATUSES = frozenset({"approved"})


def assert_risk_level(value: str) -> None:
    if value not in RISK_LEVELS:
        raise ValidationAppError(f"Invalid risk level '{value}'")


def assert_cr_transition(*, from_status: str, to_status: str) -> None:
    allowed = CR_TRANSITIONS.get(from_status, frozenset())
    if to_status not in allowed:
        raise InvalidTransitionError(
            f"Invalid change-request transition {from_status} → {to_status}"
        )


def assert_expected_version(*, current: int, expected: int | None) -> None:
    if expected is not None and current != expected:
        raise ConflictError(
            f"Optimistic concurrency conflict: expected version {expected}, got {current}"
        )


def assert_may_enter_development(status: str) -> None:
    """AC-001: out-of-scope / unapproved CRs cannot silently enter development."""
    if status not in DEVELOPMENT_GATE_STATUSES:
        raise ApprovalRequiredError(
            "Change request must be approved before entering development or updating baselines"
        )


def assert_approval_decision(value: str) -> None:
    if value not in APPROVAL_DECISIONS:
        raise ValidationAppError(f"Invalid approval decision '{value}'")


def assert_artifact_type(value: str) -> None:
    if value not in BASELINE_ARTIFACT_TYPES:
        raise ValidationAppError(f"Invalid baseline artifact type '{value}'")
