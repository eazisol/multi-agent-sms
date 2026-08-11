"""Assignment domain rules (MOD-310)."""

from __future__ import annotations

from decimal import Decimal

from masms_api.errors import ForbiddenError, ValidationAppError


def assert_project_authorized(*, is_member: bool) -> None:
    """AC-001: no assignment to unauthorized actor."""
    if not is_member:
        raise ForbiddenError("Assignee is not an authorized project member")


def assert_actor_available(
    *,
    eligible: bool,
    reasons: list[str],
    allow_override: bool,
    override_reason: str | None,
) -> None:
    """AC-001/AC-002: unavailable actors require override + reason."""
    if eligible:
        return
    if not allow_override:
        detail = ", ".join(reasons) if reasons else "unavailable"
        raise ForbiddenError(f"Assignee is unavailable: {detail}")
    assert_override_reason(override_reason)


def assert_override_reason(reason: str | None) -> None:
    """AC-002: overrides require a reason."""
    if not (reason and reason.strip()):
        raise ValidationAppError("Override requires a reason")


def assert_history_immutable() -> None:
    """AC-003 marker: history rows are append-only."""
    raise ForbiddenError("Assignment history is immutable")


def score_candidate(
    *,
    eligible: bool,
    remaining_capacity_pct: Decimal | None,
    proficiency: int | None,
    min_proficiency: int,
) -> Decimal:
    if not eligible:
        return Decimal("0")
    capacity = remaining_capacity_pct if remaining_capacity_pct is not None else Decimal("0")
    skill_bonus = Decimal("0")
    if proficiency is not None and proficiency >= min_proficiency:
        skill_bonus = Decimal(proficiency) * Decimal("5")
    return (capacity + skill_bonus).quantize(Decimal("0.0001"))
