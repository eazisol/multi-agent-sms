"""Access domain rules (MOD-120) — deny by default."""

from __future__ import annotations

from datetime import UTC, datetime

from masms_api.errors import ForbiddenError, ValidationAppError


def assert_active(status: str, *, entity: str) -> None:
    if status != "active":
        raise ForbiddenError(f"{entity} is not active")


def assert_effective_window(
    *,
    effective_from: datetime,
    effective_to: datetime | None,
    now: datetime | None = None,
    entity: str = "grant",
) -> None:
    current = now or datetime.now(UTC)
    start = effective_from if effective_from.tzinfo else effective_from.replace(tzinfo=UTC)
    if current < start:
        raise ForbiddenError(f"{entity} is not yet effective")
    if effective_to is not None:
        end = effective_to if effective_to.tzinfo else effective_to.replace(tzinfo=UTC)
        if current > end:
            raise ForbiddenError(f"{entity} has expired")


def require_project_membership(*, has_membership: bool, project_id: object) -> None:
    if not has_membership:
        raise ForbiddenError(f"Project access requires active membership for project {project_id}")


def require_permission_granted(*, granted: bool, permission_code: str) -> None:
    if not granted:
        raise ForbiddenError(f"Permission '{permission_code}' denied (deny-by-default)")


def assert_authority_subject(*, actor_id: object | None, role_code: str | None) -> None:
    if actor_id is None and not role_code:
        raise ValidationAppError(
            "Approval authority requires authority_actor_id or authority_role_code"
        )


def assert_document_principal(*, actor_id: object | None, role_code: str | None) -> None:
    if actor_id is None and not role_code:
        raise ValidationAppError("Document access requires actor_id or role_code")


def assert_review_open(status: str) -> None:
    if status != "open":
        raise ValidationAppError(f"Access review status '{status}' is not open")
