"""Approval gate domain rules (MOD-330)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from masms_api.errors import (
    ApprovalRequiredError,
    ForbiddenError,
    InvalidTransitionError,
    ValidationAppError,
)
from masms_api.kernel.actor import ActorKind

TERMINAL_STATUSES = frozenset({"approved", "rejected", "withdrawn", "superseded"})
DECISION_VALUES = frozenset({"approve", "reject", "withdraw"})


def assert_human_decider(actor_kind: ActorKind) -> None:
    if actor_kind != ActorKind.HUMAN:
        raise ForbiddenError("Only human actors may approve, reject, or override")


def assert_not_self_recommendation(
    *,
    actor_id: UUID,
    actor_kind: ActorKind,
    recommendation_source_actor_id: UUID | None,
) -> None:
    """AC-003: agents cannot approve their own recommendations."""
    if recommendation_source_actor_id is None:
        return
    if actor_id == recommendation_source_actor_id:
        raise ForbiddenError("Actors cannot approve their own recommendations")
    if actor_kind == ActorKind.AGENT:
        raise ForbiddenError("Agents cannot approve their own recommendations")


def assert_decision_reason(*, decision: str, reason: str | None) -> None:
    if decision not in DECISION_VALUES:
        raise ValidationAppError(f"Invalid decision '{decision}'")
    if decision in {"reject", "withdraw"} and not (reason and reason.strip()):
        raise ValidationAppError("Reason is required for reject and withdraw")


def assert_pending(status: str) -> None:
    if status != "pending":
        raise InvalidTransitionError(f"Approval is not pending (status={status})")


def assert_step_pending(status: str) -> None:
    if status != "pending":
        raise InvalidTransitionError(f"Step is not pending (status={status})")


def assert_override_reason(reason: str | None) -> None:
    if not (reason and reason.strip()):
        raise ValidationAppError("Override requires a reason")


def assert_delegation_reason(reason: str | None) -> None:
    if not (reason and reason.strip()):
        raise ValidationAppError("Delegation requires a reason")


def assert_delegation_window(*, starts_at: datetime, ends_at: datetime, now: datetime) -> None:
    if ends_at <= starts_at:
        raise ValidationAppError("Delegation ends_at must be after starts_at")
    if ends_at <= now:
        raise ValidationAppError("Delegation end must be in the future")


def assert_approved_for_action(
    *,
    approved: bool,
    target_version_matches: bool,
) -> None:
    """AC-001 / AC-002: block dependents until exact-version approval exists."""
    if not approved:
        raise ApprovalRequiredError("Dependent action is blocked until approval")
    if not target_version_matches:
        raise ApprovalRequiredError(
            "Approval does not bind to the exact target version; resubmit approval"
        )


def assert_evidence_ref(evidence_ref: str | None) -> None:
    if not (evidence_ref and evidence_ref.strip()):
        raise ValidationAppError("Evidence reference is required")
