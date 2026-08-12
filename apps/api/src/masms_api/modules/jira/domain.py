"""Domain rules for MOD-520 Jira integration."""

from __future__ import annotations

from uuid import uuid4

from masms_api.errors import ValidationAppError

APPROVAL_STATUSES = frozenset({"approved", "pending", "rejected"})
COMMENT_SYNC_STATUSES = frozenset({"synced", "failed"})
LOCAL_JIRA_KEY_PREFIX = "SIM-"


def assert_approval_status(value: str) -> None:
    if value not in APPROVAL_STATUSES:
        raise ValidationAppError(f"Invalid approval status '{value}'")


def assert_approved_for_push(value: str) -> None:
    assert_approval_status(value)
    if value != "approved":
        raise ValidationAppError("Only approved internal tickets can be pushed to Jira")


def assert_comment_sync_status(value: str) -> None:
    if value not in COMMENT_SYNC_STATUSES:
        raise ValidationAppError(f"Invalid comment sync status '{value}'")


def simulate_jira_key() -> str:
    return f"{LOCAL_JIRA_KEY_PREFIX}{str(uuid4())[:8].upper()}"
