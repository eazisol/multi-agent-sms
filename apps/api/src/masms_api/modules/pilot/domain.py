"""Domain rules for MOD-630 controlled pilot and production sign-off records."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from masms_api.errors import (
    ApprovalRequiredError,
    ConflictError,
    InvalidTransitionError,
    ValidationAppError,
)
from masms_api.kernel.actor import ActorKind

REQUIRED_SIGNOFF_FUNCTIONS: tuple[str, ...] = ("product", "security", "operations", "qa")

PLAN_STATUSES = frozenset({"draft", "active", "completed", "cancelled"})
TRAINING_STATUSES = frozenset({"planned", "completed"})
LIMITATION_SEVERITIES = frozenset({"low", "medium", "high", "critical"})
LIMITATION_STATUSES = frozenset({"open", "accepted", "mitigated"})
ACCEPTANCE_SEVERITIES = frozenset({"critical", "high", "medium", "low"})
ACCEPTANCE_RESULTS = frozenset({"passed", "failed", "blocked"})
DEPLOYMENT_ENVIRONMENTS = frozenset({"production"})
DEPLOYMENT_STATUSES = frozenset({"recorded", "rolled_back"})
ROLLBACK_STATUSES = frozenset({"recorded"})
SIGNOFF_STATUSES = frozenset({"pending", "signed"})
CRITICAL_HIGH = frozenset({"critical", "high"})
FAILED_OR_BLOCKED = frozenset({"failed", "blocked"})


def assert_expected_version(*, current: int, expected: int | None) -> None:
    if expected is not None and current != expected:
        raise ConflictError(
            f"Optimistic concurrency conflict: expected version {expected}, got {current}"
        )


def assert_human_signoff(actor_kind: ActorKind | str) -> None:
    kind = actor_kind.value if isinstance(actor_kind, ActorKind) else str(actor_kind)
    if kind != ActorKind.HUMAN.value:
        raise ApprovalRequiredError(
            "Agents cannot sign production readiness or record production "
            "deployment; a human actor is required"
        )


def assert_plan_status(value: str) -> None:
    if value not in PLAN_STATUSES:
        raise ValidationAppError(f"Invalid pilot plan status '{value}'")


def assert_training_status(value: str) -> None:
    if value not in TRAINING_STATUSES:
        raise ValidationAppError(f"Invalid training status '{value}'")


def assert_limitation_severity(value: str) -> None:
    if value not in LIMITATION_SEVERITIES:
        raise ValidationAppError(f"Invalid known limitation severity '{value}'")


def assert_limitation_status(value: str) -> None:
    if value not in LIMITATION_STATUSES:
        raise ValidationAppError(f"Invalid known limitation status '{value}'")


def assert_acceptance_severity(value: str) -> None:
    if value not in ACCEPTANCE_SEVERITIES:
        raise ValidationAppError(f"Invalid acceptance test severity '{value}'")


def assert_acceptance_result(value: str) -> None:
    if value not in ACCEPTANCE_RESULTS:
        raise ValidationAppError(f"Invalid acceptance test result '{value}'")


def assert_deployment_environment(value: str) -> None:
    if value not in DEPLOYMENT_ENVIRONMENTS:
        raise ValidationAppError(f"Invalid deployment environment '{value}'")


def assert_signoff_function(value: str) -> None:
    if value not in REQUIRED_SIGNOFF_FUNCTIONS:
        raise ValidationAppError(f"Invalid sign-off function '{value}'")


def assert_signoff_pending(status: str) -> None:
    if status != "pending":
        raise InvalidTransitionError(
            f"Only pending sign-offs can be signed (status={status})"
        )


def critical_high_failed_count(tests: Sequence[Any]) -> int:
    count = 0
    for row in tests:
        severity = str(getattr(row, "severity", ""))
        result = str(getattr(row, "result", ""))
        if severity in CRITICAL_HIGH and result in FAILED_OR_BLOCKED:
            count += 1
    return count


def acceptance_gate_passed(tests: Sequence[Any]) -> bool:
    return critical_high_failed_count(tests) == 0


def pilot_approval_counts(users: Sequence[Any]) -> tuple[int, int, int]:
    registered = len(users)
    approved = sum(1 for row in users if bool(getattr(row, "approved_production_use", False)))
    pending = registered - approved
    return registered, approved, pending


def pilot_approval_gate(users: Sequence[Any]) -> bool:
    _registered, approved, pending = pilot_approval_counts(users)
    return approved >= 1 and pending == 0


def readiness_signed_functions(signoffs: Sequence[Any]) -> set[str]:
    return {
        str(getattr(row, "function_code", ""))
        for row in signoffs
        if str(getattr(row, "status", "")) == "signed"
    }


def readiness_gate(signoffs: Sequence[Any]) -> bool:
    signed = readiness_signed_functions(signoffs)
    return all(code in signed for code in REQUIRED_SIGNOFF_FUNCTIONS)


def assert_production_may_record(*, gates_ok: bool, evidence: str | None) -> None:
    text = (evidence or "").strip()
    if not gates_ok or not text:
        raise ApprovalRequiredError(
            "Production deployment records require all three gates passed "
            "and non-empty human_approval_evidence"
        )
