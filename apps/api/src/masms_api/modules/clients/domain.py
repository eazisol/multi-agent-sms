"""Client/contact domain rules (MOD-200)."""

from __future__ import annotations

from masms_api.errors import ValidationAppError

AUTHORITY_LEVELS = frozenset({"decision_maker", "commercial", "technical", "general"})


def assert_authority_level(level: str) -> None:
    if level not in AUTHORITY_LEVELS:
        raise ValidationAppError(
            f"authority_level must be one of: {', '.join(sorted(AUTHORITY_LEVELS))}"
        )


def assert_distinct_clients(left_id: object, right_id: object) -> None:
    if left_id == right_id:
        raise ValidationAppError("Duplicate suggestion requires two distinct clients")


def normalize_email(email: str) -> str:
    return email.strip().lower()
