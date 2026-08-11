"""Configuration domain rules (MOD-140)."""

from __future__ import annotations

from masms_api.errors import ForbiddenError, InvalidTransitionError, ValidationAppError

STATUS_DRAFT = "draft"
STATUS_APPROVED = "approved"
STATUS_EFFECTIVE = "effective"
STATUS_SUPERSEDED = "superseded"
STATUS_ROLLED_BACK = "rolled_back"

EDITABLE_STATUSES = frozenset({STATUS_DRAFT})
LIVE_CONTROLLING_STATUS = STATUS_EFFECTIVE


def assert_draft_editable(status: str) -> None:
    if status not in EDITABLE_STATUSES:
        raise ForbiddenError(
            f"Configuration version status '{status}' is not editable; only draft may change"
        )


def assert_can_approve(status: str) -> None:
    if status != STATUS_DRAFT:
        raise InvalidTransitionError(
            f"Only draft configuration can be approved; current='{status}'"
        )


def assert_can_activate(status: str) -> None:
    if status != STATUS_APPROVED:
        raise InvalidTransitionError(
            f"Only approved configuration can become effective; current='{status}'"
        )


def assert_can_rollback(status: str) -> None:
    if status != STATUS_EFFECTIVE:
        raise InvalidTransitionError(
            f"Only effective configuration can be rolled back; current='{status}'"
        )


def assert_live_config(status: str) -> None:
    """AC-001 / AC-003: draft (and non-effective) must not control live execution."""
    if status != LIVE_CONTROLLING_STATUS:
        raise ForbiddenError(
            f"Only effective configuration controls live execution; current='{status}'"
        )


def assert_transition_allowed(
    *,
    allowed: bool,
    from_status: str,
    to_status: str,
    workflow_code: str,
) -> None:
    if not allowed:
        raise InvalidTransitionError(
            f"Transition {from_status}->{to_status} is not allowed on workflow '{workflow_code}'"
        )


def assert_positive_hours(value: int, *, field: str) -> None:
    if value < 0:
        raise ValidationAppError(f"{field} must be >= 0")
