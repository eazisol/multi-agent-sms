"""Auth domain rules for sessions, MFA, and step-up (MOD-110)."""

from __future__ import annotations

from masms_api.errors import ForbiddenError, ValidationAppError

ASSURANCE_PASSWORD = 1
ASSURANCE_MFA = 2
ASSURANCE_STEP_UP = 3


def require_assurance(current: int, required: int, *, action: str) -> None:
    if current < required:
        raise ForbiddenError(
            f"Privileged action '{action}' requires assurance_level>={required}; "
            f"current={current}"
        )


def assert_session_active(status: str) -> None:
    if status != "active":
        raise ForbiddenError("Session is not active")


def assert_invitation_pending(status: str) -> None:
    if status != "pending":
        raise ValidationAppError(f"Invitation status '{status}' is not pending")
