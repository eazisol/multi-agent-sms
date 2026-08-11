"""Client query domain rules (MOD-210)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from masms_api.errors import InvalidTransitionError, ValidationAppError

# Configuration-driven in spirit; M1 uses an approved starter set (not DB enums).
ALLOWED_TRANSITIONS: dict[str, frozenset[str]] = {
    "received": frozenset({"classified", "rejected"}),
    "classified": frozenset({"qualifying", "rejected"}),
    "qualifying": frozenset({"qualified", "rejected"}),
    "qualified": frozenset({"converted"}),
    "rejected": frozenset(),
    "converted": frozenset(),
}


def assert_transition(previous: str, next_status: str) -> None:
    allowed = ALLOWED_TRANSITIONS.get(previous, frozenset())
    if next_status not in allowed:
        raise InvalidTransitionError(
            f"Invalid query transition {previous}->{next_status}"
        )


def compute_sla_due(*, received_at: datetime, hours: int = 24) -> datetime:
    if hours < 1:
        raise ValidationAppError("SLA hours must be >= 1")
    base = received_at if received_at.tzinfo else received_at.replace(tzinfo=UTC)
    return base + timedelta(hours=hours)


def evaluate_sla(
    *,
    due_at: datetime | None,
    responded_at: datetime | None,
    now: datetime | None = None,
) -> str:
    if responded_at is not None:
        if due_at is None:
            return "met"
        due = due_at if due_at.tzinfo else due_at.replace(tzinfo=UTC)
        resp = responded_at if responded_at.tzinfo else responded_at.replace(tzinfo=UTC)
        return "met" if resp <= due else "breached"
    current = now or datetime.now(UTC)
    if due_at is None:
        return "pending"
    due = due_at if due_at.tzinfo else due_at.replace(tzinfo=UTC)
    return "breached" if current > due else "pending"
