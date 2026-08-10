"""Governance domain rules (pure functions)."""

from __future__ import annotations

from masms_api.deps import ActorKind
from masms_api.errors import (
    ApprovalRequiredError,
    ForbiddenError,
    InvalidTransitionError,
    ValidationAppError,
)

APPROVED_STATUSES = frozenset({"approved", "accepted"})
IMMUTABLE_STATUSES = frozenset({"approved", "accepted", "superseded", "closed", "applied"})

BASELINE_TRANSITIONS: dict[str, frozenset[str]] = {
    "draft": frozenset({"submitted", "withdrawn"}),
    "submitted": frozenset({"under_review", "withdrawn"}),
    "under_review": frozenset({"approved", "rejected", "more_info_required", "withdrawn"}),
    "more_info_required": frozenset({"submitted", "withdrawn"}),
    "rejected": frozenset({"draft"}),
    "approved": frozenset({"superseded"}),
    "withdrawn": frozenset(),
    "superseded": frozenset(),
}

CR_TRANSITIONS: dict[str, frozenset[str]] = {
    "draft": frozenset({"submitted", "withdrawn"}),
    "submitted": frozenset({"under_review", "withdrawn"}),
    "under_review": frozenset({"approved", "rejected", "withdrawn"}),
    "approved": frozenset({"applied"}),
    "applied": frozenset({"closed"}),
    "rejected": frozenset({"closed"}),
    "withdrawn": frozenset({"closed"}),
    "closed": frozenset(),
}

ADR_TRANSITIONS: dict[str, frozenset[str]] = {
    "proposed": frozenset({"accepted", "deprecated", "superseded"}),
    "accepted": frozenset({"deprecated", "superseded"}),
    "deprecated": frozenset({"superseded"}),
    "superseded": frozenset(),
}


def assert_transition(current: str, target: str, table: dict[str, frozenset[str]]) -> None:
    allowed = table.get(current, frozenset())
    if target not in allowed:
        raise InvalidTransitionError(f"Transition from '{current}' to '{target}' is not allowed")


def assert_mutable(status: str, *, action: str = "update") -> None:
    if status in IMMUTABLE_STATUSES:
        raise ApprovalRequiredError(
            f"Cannot {action} a record in immutable status '{status}'; "
            "create a new version via change request"
        )


def assert_human_approver(actor_kind: ActorKind) -> None:
    if actor_kind != ActorKind.HUMAN:
        raise ForbiddenError("Only human actors may approve or reject governance records")


def assert_reason_when_required(decision: str, reason: str | None) -> None:
    if decision in {"rejected", "withdrawn", "override"} and not (reason and reason.strip()):
        raise ValidationAppError("Reason is required for reject, withdraw, and override decisions")


def next_version(current: int) -> int:
    if current < 1:
        raise ValidationAppError("Version must be >= 1")
    return current + 1
