"""Status / transition engine domain rules (MOD-320)."""

from __future__ import annotations

from masms_api.errors import (
    ApprovalRequiredError,
    ForbiddenError,
    InvalidTransitionError,
    ValidationAppError,
)
from masms_api.kernel.actor import ActorKind


def assert_not_on_hold(*, on_hold: bool) -> None:
    if on_hold:
        raise ForbiddenError("Entity is on hold; release hold before transitioning")


def assert_transition_exists(*, allowed: bool, from_status: str, to_status: str) -> None:
    if not allowed:
        raise InvalidTransitionError(f"Transition {from_status} -> {to_status} is not configured")


def assert_reason_if_required(*, requires_reason: bool, reason: str | None) -> None:
    if requires_reason and not (reason and reason.strip()):
        raise ValidationAppError("This transition requires a reason")


def assert_evidence_if_required(*, requires_evidence: bool, evidence_ref: str | None) -> None:
    if requires_evidence and not (evidence_ref and evidence_ref.strip()):
        raise ValidationAppError("This transition requires evidence")


def assert_required_fields(
    *,
    required_fields: list[str],
    provided_fields: dict[str, object | None],
) -> None:
    missing = []
    for name in required_fields:
        value = provided_fields.get(name)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(name)
    if missing:
        raise ValidationAppError("Missing required fields: " + ", ".join(missing))


def assert_approval_gate(
    *,
    requires_approval: bool,
    approval_id: object | None,
    actor_kind: ActorKind,
) -> None:
    """AC-003: agents cannot skip required approval gates."""
    if not requires_approval:
        return
    if actor_kind != ActorKind.HUMAN:
        raise ForbiddenError("Agents cannot skip required approval gates")
    if approval_id is None:
        raise ApprovalRequiredError("This transition requires a human approval record")


def assert_can_reopen(*, is_terminal: bool, actor_kind: ActorKind, reason: str | None) -> None:
    if not is_terminal:
        raise InvalidTransitionError("Only terminal statuses can be reopened")
    if actor_kind != ActorKind.HUMAN:
        raise ForbiddenError("Only a human actor may reopen a terminal status")
    if not (reason and reason.strip()):
        raise ValidationAppError("Reopen requires a reason")


def assert_hold_reason(reason: str | None) -> None:
    if not (reason and reason.strip()):
        raise ValidationAppError("Hold requires a reason")
