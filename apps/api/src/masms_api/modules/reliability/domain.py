"""Domain rules for MOD-610 reliability, SLOs, replay, and DR."""

from __future__ import annotations

import math
from typing import Any

from masms_api.errors import ConflictError, InvalidTransitionError, ValidationAppError

API_P95_BUDGET_MS = 2000
DASHBOARD_P95_BUDGET_MS = 3000

PERFORMANCE_STATUSES = frozenset({"recorded", "passed", "failed"})
RESILIENCE_RESULTS = frozenset({"passed", "failed"})
INDEX_RECOMMENDATIONS = frozenset({"keep", "add", "drop"})
INDEX_REVIEW_STATUSES = frozenset({"open", "accepted", "deferred"})
SLO_DASHBOARD_STATUSES = frozenset({"draft", "active"})
REPLAY_STATUSES = frozenset({"pending", "failed", "resumed", "completed"})
INTEGRATION_RESULTS = frozenset({"passed", "failed"})
DR_RUNBOOK_STATUSES = frozenset({"draft", "approved", "retired"})

REPLAY_TRANSITIONS: dict[str, frozenset[str]] = {
    "pending": frozenset({"failed", "completed"}),
    "failed": frozenset({"resumed"}),
    "resumed": frozenset({"completed"}),
    "completed": frozenset(),
}


def assert_performance_status(value: str) -> None:
    if value not in PERFORMANCE_STATUSES:
        raise ValidationAppError(f"Invalid performance test status '{value}'")


def assert_resilience_result(value: str) -> None:
    if value not in RESILIENCE_RESULTS:
        raise ValidationAppError(f"Invalid resilience result '{value}'")


def assert_index_recommendation(value: str) -> None:
    if value not in INDEX_RECOMMENDATIONS:
        raise ValidationAppError(f"Invalid index recommendation '{value}'")


def assert_index_review_status(value: str) -> None:
    if value not in INDEX_REVIEW_STATUSES:
        raise ValidationAppError(f"Invalid index review status '{value}'")


def assert_slo_dashboard_status(value: str) -> None:
    if value not in SLO_DASHBOARD_STATUSES:
        raise ValidationAppError(f"Invalid SLO dashboard status '{value}'")


def assert_replay_status(value: str) -> None:
    if value not in REPLAY_STATUSES:
        raise ValidationAppError(f"Invalid workflow replay status '{value}'")


def assert_integration_result(value: str) -> None:
    if value not in INTEGRATION_RESULTS:
        raise ValidationAppError(f"Invalid integration failure test result '{value}'")


def assert_dr_runbook_status(value: str) -> None:
    if value not in DR_RUNBOOK_STATUSES:
        raise ValidationAppError(f"Invalid DR runbook status '{value}'")


def assert_expected_version(*, current: int, expected: int | None) -> None:
    if expected is not None and current != expected:
        raise ConflictError(
            f"Optimistic concurrency conflict: expected version {expected}, got {current}"
        )


def compute_p95_ms(samples: list[int]) -> int:
    """Nearest-rank p95 from recorded latency samples (milliseconds)."""
    if not samples:
        raise ValidationAppError("Cannot compute p95 from empty samples")
    ordered = sorted(int(value) for value in samples)
    rank = max(1, math.ceil(0.95 * len(ordered)))
    return ordered[min(len(ordered), rank) - 1]


def resolve_p95_ms(*, p95_ms: int | None, samples: list[int] | None) -> tuple[int, int]:
    """Return (p95_ms, sample_count) preferring recorded samples when present."""
    if samples:
        return compute_p95_ms(samples), len(samples)
    if p95_ms is None:
        raise ValidationAppError("p95_ms is required when samples are omitted")
    if p95_ms < 0:
        raise ValidationAppError("p95_ms must be >= 0")
    return p95_ms, 0


def api_slo_met(p95_ms: int) -> bool:
    return p95_ms <= API_P95_BUDGET_MS


def dashboard_slo_met(p95_ms: int) -> bool:
    return p95_ms <= DASHBOARD_P95_BUDGET_MS


def performance_status_for_p95(p95_ms: int, requested: str | None = None) -> str:
    if requested is not None:
        assert_performance_status(requested)
        return requested
    return "passed" if api_slo_met(p95_ms) else "failed"


def assert_replay_transition(*, from_status: str, to_status: str) -> None:
    allowed = REPLAY_TRANSITIONS.get(from_status, frozenset())
    if to_status not in allowed:
        raise InvalidTransitionError(
            f"Invalid workflow replay transition {from_status} → {to_status}"
        )


def assert_dr_approvable(status: str) -> None:
    if status != "draft":
        raise InvalidTransitionError(
            f"Only draft DR runbooks can be approved (status={status})"
        )


def samples_as_list(value: Any) -> list[int] | None:
    if value is None:
        return None
    if not isinstance(value, list):
        raise ValidationAppError("samples must be a list of latency milliseconds")
    return [int(item) for item in value]
