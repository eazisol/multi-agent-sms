"""Notifications domain rules (MOD-440)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from masms_api.errors import ConflictError, InvalidTransitionError, ValidationAppError

MAX_DELIVERY_ATTEMPTS = 3

CHANNELS = frozenset({"in_app", "email"})
PRIORITIES = frozenset({"low", "normal", "high", "critical"})
NOTIFICATION_TYPES = frozenset(
    {
        "assignment",
        "reminder",
        "escalation",
        "approval",
        "blocker",
        "bug",
        "release",
        "client_response",
        "system_alert",
    }
)
STATUSES = frozenset(
    {
        "pending",
        "queued",
        "sent",
        "delivered",
        "read",
        "failed",
        "dead_lettered",
        "cancelled",
    }
)

NOTIFICATION_TRANSITIONS: dict[str, frozenset[str]] = {
    "pending": frozenset(
        {"queued", "sent", "delivered", "failed", "dead_lettered", "cancelled"}
    ),
    "queued": frozenset({"sent", "delivered", "failed", "dead_lettered", "cancelled"}),
    "sent": frozenset({"delivered", "read", "failed"}),
    "delivered": frozenset({"read"}),
    "read": frozenset(),
    "failed": frozenset(
        {"pending", "queued", "sent", "delivered", "dead_lettered", "cancelled"}
    ),
    "dead_lettered": frozenset({"pending", "queued"}),
    "cancelled": frozenset(),
}


class PreferenceLike(Protocol):
    notification_type: str
    channel: str
    enabled: bool


class NotificationLike(Protocol):
    notification_type: str
    channel: str
    priority: str


def assert_channel(value: str) -> None:
    if value not in CHANNELS:
        raise ValidationAppError(f"Invalid channel '{value}'")


def assert_priority(value: str) -> None:
    if value not in PRIORITIES:
        raise ValidationAppError(f"Invalid priority '{value}'")


def assert_type(value: str) -> None:
    if value not in NOTIFICATION_TYPES:
        raise ValidationAppError(f"Invalid notification_type '{value}'")


def assert_status(value: str) -> None:
    if value not in STATUSES:
        raise ValidationAppError(f"Invalid status '{value}'")


def assert_expected_version(*, current: int, expected: int | None) -> None:
    if expected is not None and current != expected:
        raise ConflictError(
            f"Optimistic concurrency conflict: expected version {expected}, got {current}"
        )


def assert_preference_allows_mute(
    *,
    notification_type: str,
    enabled: bool,
) -> None:
    """AC-002: cannot disable system_alert preferences."""
    if notification_type == "system_alert" and not enabled:
        raise ValidationAppError(
            "Cannot disable preferences for notification_type 'system_alert'"
        )


def is_delivery_suppressed(
    prefs: Sequence[PreferenceLike],
    notification: NotificationLike,
) -> bool:
    """Critical and system_alert always deliver; other prefs may mute type/channel."""
    if notification.priority == "critical":
        return False
    if notification.notification_type == "system_alert":
        return False
    for pref in prefs:
        if (
            pref.notification_type == notification.notification_type
            and pref.channel == notification.channel
            and not pref.enabled
        ):
            return True
    return False


def assert_notification_transition(*, from_status: str, to_status: str) -> None:
    allowed = NOTIFICATION_TRANSITIONS.get(from_status, frozenset())
    if to_status not in allowed:
        raise InvalidTransitionError(
            f"Invalid notification transition {from_status} → {to_status}"
        )
