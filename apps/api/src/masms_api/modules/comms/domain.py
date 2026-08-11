"""Communication domain rules (MOD-220)."""

from __future__ import annotations

from masms_api.errors import ForbiddenError, ValidationAppError

EDITABLE_MESSAGE_STATUSES = frozenset({"draft", "pending_approval"})
SENT_STATUSES = frozenset({"sent"})
SENSITIVE_CLASSIFICATIONS = frozenset({"confidential", "restricted"})
RECIPIENT_ROLES = frozenset({"to", "cc", "bcc"})


def assert_message_editable(status: str) -> None:
    if status not in EDITABLE_MESSAGE_STATUSES:
        raise ForbiddenError(
            f"Message status '{status}' is immutable; only draft/pending_approval may change"
        )


def assert_sent_immutable(status: str) -> None:
    if status in SENT_STATUSES:
        raise ForbiddenError("Sent-message history is immutable")


def assert_can_send(*, status: str, requires_approval: bool, approved: bool) -> None:
    if status == "sent":
        raise ValidationAppError("Message is already sent")
    if requires_approval and not approved:
        raise ForbiddenError("Sensitive message requires approval before send")
    if status not in {"draft", "pending_approval"}:
        raise ValidationAppError(f"Cannot send message in status '{status}'")


def assert_recipient_role(role: str) -> None:
    if role not in RECIPIENT_ROLES:
        allowed = ", ".join(sorted(RECIPIENT_ROLES))
        raise ValidationAppError(f"recipient role must be one of: {allowed}")


def requires_approval_for_classification(classification: str) -> bool:
    return classification in SENSITIVE_CLASSIFICATIONS


def assert_has_recipients(count: int) -> None:
    if count < 1:
        raise ValidationAppError("At least one recipient is required to send")
