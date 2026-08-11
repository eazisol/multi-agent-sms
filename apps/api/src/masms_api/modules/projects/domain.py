"""Project / requirement / SRS domain rules (MOD-240)."""

from __future__ import annotations

from masms_api.errors import ForbiddenError, InvalidTransitionError, ValidationAppError

DRAFT = "draft"
APPROVED = "approved"
PRIORITIES = frozenset({"must_have", "should_have", "could_have"})
EDITABLE_VERSION = frozenset({DRAFT})


def assert_requirement_code(code: str) -> None:
    cleaned = code.strip()
    if len(cleaned) < 2:
        raise ValidationAppError("requirement_code must be at least 2 characters")


def assert_priority(priority: str) -> None:
    if priority not in PRIORITIES:
        raise ValidationAppError(
            "priority must be one of: " + ", ".join(sorted(PRIORITIES))
        )


def assert_version_editable(status: str) -> None:
    if status not in EDITABLE_VERSION:
        raise ForbiddenError(
            f"Requirement version status '{status}' is immutable; create a new version"
        )


def assert_can_approve_requirement_version(
    *,
    status: str,
    requirement_code: str,
    acceptance_criteria_count: int,
) -> None:
    if status != DRAFT:
        raise InvalidTransitionError(
            f"Only draft requirement versions can be approved; current='{status}'"
        )
    assert_requirement_code(requirement_code)
    if acceptance_criteria_count < 1:
        raise ValidationAppError(
            "Approved requirements require at least one acceptance criterion"
        )


def assert_srs_editable(status: str) -> None:
    if status != DRAFT:
        raise ForbiddenError(
            f"SRS baseline status '{status}' is immutable; create a new version"
        )


def assert_can_approve_srs(*, status: str, approved_requirement_version_count: int) -> None:
    """AC-002: SRS becomes authoritative only via human approval of a draft."""
    if status != DRAFT:
        raise InvalidTransitionError(
            f"Only draft SRS baselines can be approved; current='{status}'"
        )
    if approved_requirement_version_count < 1:
        raise ValidationAppError(
            "SRS baseline must reference at least one approved requirement version"
        )


def assert_change_reason_for_new_version(*, version_number: int, change_reason: str | None) -> None:
    """AC-003: material changes after v1 require change-control reason."""
    if version_number > 1 and not (change_reason and change_reason.strip()):
        raise ValidationAppError("change_reason is required for versions after 1")
