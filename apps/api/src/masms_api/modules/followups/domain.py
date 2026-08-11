"""Follow-up domain rules (MOD-340)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from masms_api.errors import ConflictError, ForbiddenError, ValidationAppError


def assert_required_fields(
    *,
    owner_actor_id: object | None,
    due_at: datetime | None,
    rule_version_id: object | None,
    closure_condition: str | None,
    required_response: str | None,
) -> None:
    """AC-001: every follow-up has owner, deadline, rule version, closure condition."""
    missing: list[str] = []
    if owner_actor_id is None:
        missing.append("owner_actor_id")
    if due_at is None:
        missing.append("due_at")
    if rule_version_id is None:
        missing.append("rule_version_id")
    if not (closure_condition and closure_condition.strip()):
        missing.append("closure_condition")
    if not (required_response and required_response.strip()):
        missing.append("required_response")
    if missing:
        raise ValidationAppError("Follow-up missing required fields: " + ", ".join(missing))


def assert_open(status: str) -> None:
    if status != "open":
        raise ConflictError(f"Follow-up is not open (status={status})")


def assert_pause_fields(
    *,
    reason: str | None,
    next_action: str | None,
    review_at: datetime | None,
) -> None:
    if not (reason and reason.strip()):
        raise ValidationAppError("SLA pause requires a reason")
    if not (next_action and next_action.strip()):
        raise ValidationAppError("SLA pause requires a next_action")
    if review_at is None:
        raise ValidationAppError("SLA pause requires a review_at")


def assert_closure_evidence(evidence_ref: str | None) -> None:
    if not (evidence_ref and evidence_ref.strip()):
        raise ValidationAppError("Closure requires evidence_ref")


def assert_can_close_parent(*, unresolved_mandatory_children: int) -> None:
    if unresolved_mandatory_children > 0:
        raise ForbiddenError(
            "Parent follow-up remains open while mandatory child follow-ups are unresolved"
        )


def add_business_hours(*, start: datetime, hours: int) -> datetime:
    """Simple business-time: skip Saturday/Sunday; 1 hour = 1 weekday hour."""
    if hours < 0:
        raise ValidationAppError("Business hours offset must be >= 0")
    cursor = start if start.tzinfo else start.replace(tzinfo=UTC)
    remaining = hours
    # Advance in 1-hour steps on weekdays only
    safety = hours * 4 + 48
    while remaining > 0 and safety > 0:
        safety -= 1
        cursor = cursor + timedelta(hours=1)
        if cursor.weekday() < 5:  # Mon-Fri
            remaining -= 1
    return cursor


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def reminder_due(*, due_at: datetime, offset_hours: int, now: datetime) -> bool:
    """True when now is within offset_hours before due (or past due)."""
    due = _as_utc(due_at)
    current = _as_utc(now)
    threshold = due - timedelta(hours=offset_hours)
    return current >= threshold


def escalation_due(*, due_at: datetime, after_hours: int, now: datetime) -> bool:
    return _as_utc(now) >= (_as_utc(due_at) + timedelta(hours=after_hours))
