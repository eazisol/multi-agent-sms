"""Knowledge domain rules (MOD-370)."""

from __future__ import annotations

from masms_api.errors import ConflictError, InvalidTransitionError, ValidationAppError

VERSION_STATUSES = frozenset({"draft", "active", "retired", "rejected", "superseded"})
ITEM_STATUSES = frozenset({"draft", "approved", "retired"})
EXCLUDED_FROM_RETRIEVAL = frozenset({"draft", "retired", "rejected", "superseded"})
RETRIEVABLE_STATUSES = frozenset({"active"})

PERMISSION_EFFECTS = frozenset({"allow", "deny"})
CONFLICT_STATUSES = frozenset({"open", "resolved", "dismissed"})

VERSION_TRANSITIONS: dict[str, frozenset[str]] = {
    "draft": frozenset({"active", "rejected", "retired"}),
    "active": frozenset({"retired", "superseded"}),
    "rejected": frozenset({"draft"}),
    "retired": frozenset(),
    "superseded": frozenset(),
}


def assert_version_status(status: str) -> None:
    if status not in VERSION_STATUSES:
        raise ValidationAppError(f"Invalid knowledge version status '{status}'")


def assert_version_transition(*, from_status: str, to_status: str) -> None:
    allowed = VERSION_TRANSITIONS.get(from_status, frozenset())
    if to_status not in allowed:
        raise InvalidTransitionError(
            f"Invalid knowledge version transition {from_status} → {to_status}"
        )


def assert_permission_effect(effect: str) -> None:
    if effect not in PERMISSION_EFFECTS:
        raise ValidationAppError(f"Invalid permission effect '{effect}'")


def assert_conflict_status(status: str) -> None:
    if status not in CONFLICT_STATUSES:
        raise ValidationAppError(f"Invalid conflict status '{status}'")


def assert_expected_version(*, current: int, expected: int | None) -> None:
    if expected is not None and current != expected:
        raise ConflictError(
            f"Optimistic concurrency conflict: expected version {expected}, got {current}"
        )


def is_retrievable_version(
    *,
    status: str,
    effective_from_ok: bool,
    effective_to_ok: bool,
) -> bool:
    """AC-003: exclude unauthorized/expired/rejected/superseded (auth checked separately)."""
    if status not in RETRIEVABLE_STATUSES:
        return False
    return effective_from_ok and effective_to_ok
