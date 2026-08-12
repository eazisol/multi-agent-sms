"""Insights domain rules (MOD-450)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from masms_api.errors import ConflictError, ValidationAppError

FRESHNESS_SECONDS = 60

HEALTH_STATUSES = frozenset({"healthy", "watch", "at_risk", "critical"})
REPORT_STATUSES = frozenset({"draft", "ready", "archived"})
EXPORT_FORMATS = frozenset({"json", "csv"})
EXPORT_STATUSES = frozenset({"pending", "ready", "failed", "expired"})
SEARCH_ENTITY_TYPES = frozenset(
    {
        "project",
        "ticket",
        "bug",
        "query",
        "followup",
        "approval",
        "document",
        "report",
        "other",
    }
)
CLASSIFICATIONS = frozenset({"internal", "restricted"})
SCOPE_ORG = "org"


def assert_health_status(value: str) -> None:
    if value not in HEALTH_STATUSES:
        raise ValidationAppError(f"Invalid health_status '{value}'")


def assert_report_status(value: str) -> None:
    if value not in REPORT_STATUSES:
        raise ValidationAppError(f"Invalid report status '{value}'")


def assert_export_format(value: str) -> None:
    if value not in EXPORT_FORMATS:
        raise ValidationAppError(f"Invalid export_format '{value}'")


def assert_export_status(value: str) -> None:
    if value not in EXPORT_STATUSES:
        raise ValidationAppError(f"Invalid export status '{value}'")


def assert_entity_type(value: str) -> None:
    if value not in SEARCH_ENTITY_TYPES:
        raise ValidationAppError(f"Invalid entity_type '{value}'")


def assert_classification(value: str) -> None:
    if value not in CLASSIFICATIONS:
        raise ValidationAppError(f"Invalid classification '{value}'")


def assert_score(value: int) -> None:
    if value < 0 or value > 100:
        raise ValidationAppError("score must be between 0 and 100")


def assert_expected_version(*, current: int, expected: int | None) -> None:
    if expected is not None and current != expected:
        raise ConflictError(
            f"Optimistic concurrency conflict: expected version {expected}, got {current}"
        )


def scope_key_for_project(project_id: object | None) -> str:
    if project_id is None:
        return SCOPE_ORG
    return f"project:{project_id}"


def is_snapshot_fresh(computed_at: datetime, now: datetime | None = None) -> bool:
    """AC-002: snapshot is fresh when age < FRESHNESS_SECONDS."""
    current = now or datetime.now(UTC)
    computed = computed_at
    if computed.tzinfo is None:
        computed = computed.replace(tzinfo=UTC)
    if current.tzinfo is None:
        current = current.replace(tzinfo=UTC)
    return (current - computed) < timedelta(seconds=FRESHNESS_SECONDS)
