"""Domain rules for MOD-620 sample-project UAT and agent evaluation."""

from __future__ import annotations

from masms_api.errors import (
    ApprovalRequiredError,
    ConflictError,
    InvalidTransitionError,
    ValidationAppError,
)
from masms_api.kernel.actor import ActorKind

SAMPLE_REQUIRED = 3
AGENT_QUALITY_TARGET_PCT = 80

SAMPLE_PROJECT_SPECS: tuple[tuple[str, str], ...] = (
    ("SAMPLE-A", "Synthetic sample project A"),
    ("SAMPLE-B", "Synthetic sample project B"),
    ("SAMPLE-C", "Synthetic sample project C"),
)

SEED_SCRIPT_STATUSES = frozenset({"registered", "applied", "failed"})
EXPECTED_DECISION_STATUSES = frozenset({"pending", "matched", "mismatched"})
AGENT_EVAL_STATUSES = frozenset({"recorded", "passed", "failed"})
E2E_RESULTS = frozenset({"passed", "failed", "blocked"})
ROLE_UAT_RESULTS = frozenset({"passed", "failed", "blocked"})
EVIDENCE_STATUSES = frozenset({"draft", "submitted", "accepted", "rejected"})
SAMPLE_WORKFLOW_STATUSES = frozenset({"pending", "passed", "failed"})

EVIDENCE_ACCEPT_FROM = frozenset({"draft", "submitted"})


def sample_gate_passed(passed_count: int, required: int = SAMPLE_REQUIRED) -> bool:
    return passed_count >= required


def agent_quality_met(score: int | None, target: int = AGENT_QUALITY_TARGET_PCT) -> bool:
    if score is None:
        return False
    return score >= target


def assert_human_approval_only(actor_kind: ActorKind | str) -> None:
    kind = actor_kind.value if isinstance(actor_kind, ActorKind) else str(actor_kind)
    if kind != ActorKind.HUMAN.value:
        raise ApprovalRequiredError(
            "Agents cannot approve or accept UAT/acceptance records; a human approver is required"
        )


def assert_expected_version(*, current: int, expected: int | None) -> None:
    if expected is not None and current != expected:
        raise ConflictError(
            f"Optimistic concurrency conflict: expected version {expected}, got {current}"
        )


def assert_accuracy_pct(value: int) -> None:
    if value < 0 or value > 100:
        raise ValidationAppError("accuracy_pct must be between 0 and 100")


def assert_seed_script_status(value: str) -> None:
    if value not in SEED_SCRIPT_STATUSES:
        raise ValidationAppError(f"Invalid seed script status '{value}'")


def assert_expected_decision_status(value: str) -> None:
    if value not in EXPECTED_DECISION_STATUSES:
        raise ValidationAppError(f"Invalid expected decision status '{value}'")


def assert_agent_eval_status(value: str) -> None:
    if value not in AGENT_EVAL_STATUSES:
        raise ValidationAppError(f"Invalid agent evaluation status '{value}'")


def assert_e2e_result(value: str) -> None:
    if value not in E2E_RESULTS:
        raise ValidationAppError(f"Invalid E2E test result '{value}'")


def assert_role_uat_result(value: str) -> None:
    if value not in ROLE_UAT_RESULTS:
        raise ValidationAppError(f"Invalid role UAT result '{value}'")


def assert_evidence_status(value: str) -> None:
    if value not in EVIDENCE_STATUSES:
        raise ValidationAppError(f"Invalid acceptance evidence status '{value}'")


def assert_sample_workflow_status(value: str) -> None:
    if value not in SAMPLE_WORKFLOW_STATUSES:
        raise ValidationAppError(f"Invalid sample project workflow status '{value}'")


def assert_evidence_acceptable(status: str) -> None:
    if status not in EVIDENCE_ACCEPT_FROM:
        raise InvalidTransitionError(
            f"Only draft or submitted acceptance evidence can be accepted (status={status})"
        )


def evaluation_status_for_score(accuracy_pct: int, requested: str | None = None) -> str:
    if requested is not None:
        assert_agent_eval_status(requested)
        return requested
    return "passed" if agent_quality_met(accuracy_pct) else "failed"
