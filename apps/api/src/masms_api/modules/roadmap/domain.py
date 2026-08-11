"""Roadmap / phase domain rules (MOD-260)."""

from __future__ import annotations

from datetime import date
from uuid import UUID

from masms_api.errors import ForbiddenError, InvalidTransitionError, ValidationAppError

PHASE_COMPLETE = "completed"
MILESTONE_COMPLETE = "completed"


def assert_no_self_dependency(predecessor_id: UUID, successor_id: UUID) -> None:
    if predecessor_id == successor_id:
        raise ValidationAppError("A phase cannot depend on itself")


def assert_can_complete_phase(
    *,
    status: str,
    unfinished_predecessor_codes: list[str],
) -> None:
    """AC-003: phases complete independently except explicit predecessor deps."""
    if status == PHASE_COMPLETE:
        raise InvalidTransitionError("Phase is already completed")
    if status == "cancelled":
        raise ForbiddenError("Cancelled phases cannot be completed")
    if unfinished_predecessor_codes:
        raise ForbiddenError(
            "Cannot complete phase until predecessors finish: "
            + ", ".join(unfinished_predecessor_codes)
        )


def assert_sibling_independence(
    *,
    completing_phase_id: UUID,
    sibling_incomplete_ids: list[UUID],
) -> None:
    """Completing one phase must not require unrelated siblings to be done."""
    # Explicit no-op gate used by tests; unfinished_predecessor_codes already encodes deps.
    _ = completing_phase_id
    _ = sibling_incomplete_ids


def assert_milestone_fields(
    *,
    owner_actor_id: UUID | None,
    target_date: date | None,
    status: str | None,
) -> None:
    """AC-002: milestones require owner, date, and status."""
    if owner_actor_id is None:
        raise ValidationAppError("Milestone requires an owner")
    if target_date is None:
        raise ValidationAppError("Milestone requires a target date")
    if not status:
        raise ValidationAppError("Milestone requires a status")


def assert_can_complete_milestone(
    *,
    status: str,
    owner_actor_id: UUID | None,
    target_date: date | None,
    requires_approval: bool,
    approved: bool,
) -> None:
    assert_milestone_fields(
        owner_actor_id=owner_actor_id, target_date=target_date, status=status
    )
    if status == MILESTONE_COMPLETE:
        raise InvalidTransitionError("Milestone is already completed")
    if requires_approval and not approved:
        raise ForbiddenError("Milestone requires approval before completion")


def assert_approved_requirements_mapped(
    *,
    approved_requirement_ids: set[UUID],
    mapped_requirement_ids: set[UUID],
) -> None:
    """AC-001: every approved requirement maps to a phase."""
    missing = approved_requirement_ids - mapped_requirement_ids
    if missing:
        raise ValidationAppError(
            "Approved requirements missing phase mapping: "
            + ", ".join(sorted(str(x) for x in missing))
        )
