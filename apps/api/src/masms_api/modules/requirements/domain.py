"""Requirement gathering domain rules (MOD-230)."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from masms_api.errors import ForbiddenError, InvalidTransitionError, ValidationAppError

COMPLETENESS_THRESHOLD = Decimal("0.95")
PUBLISHED = "published"
BRIEF_EDITABLE = frozenset({"draft", "pending_approval"})


@dataclass(frozen=True)
class CompletenessResult:
    mandatory_total: int
    covered_count: int
    percentage: Decimal
    meets_threshold: bool
    gap_keys: list[str]


def assert_questions_valid(questions: list[dict[str, Any]]) -> None:
    if not questions:
        raise ValidationAppError("Questionnaire version requires at least one question")
    keys: set[str] = set()
    for question in questions:
        key = str(question.get("key", "")).strip()
        if not key:
            raise ValidationAppError("Each question requires a non-empty key")
        if key in keys:
            raise ValidationAppError(f"Duplicate question key '{key}'")
        keys.add(key)
        if "text" not in question or not str(question["text"]).strip():
            raise ValidationAppError(f"Question '{key}' requires text")
        if "mandatory" not in question:
            raise ValidationAppError(f"Question '{key}' requires mandatory flag")


def assert_version_editable(status: str) -> None:
    if status != "draft":
        raise ForbiddenError(
            f"Questionnaire version status '{status}' is immutable; only draft may change"
        )


def assert_can_publish(status: str) -> None:
    if status != "draft":
        raise InvalidTransitionError(
            f"Only draft questionnaire versions can be published; current='{status}'"
        )


def assert_version_accepts_answers(status: str) -> None:
    if status != PUBLISHED:
        raise ForbiddenError("Answers require a published questionnaire version")


def assert_answer_value(*, answer_text: str | None, explicitly_unavailable: bool) -> None:
    has_text = bool(answer_text and answer_text.strip())
    if has_text and explicitly_unavailable:
        raise ValidationAppError("Answer cannot be both provided and explicitly unavailable")
    if not has_text and not explicitly_unavailable:
        raise ValidationAppError("Provide answer_text or mark explicitly_unavailable")


def is_answer_covered(*, answer_text: str | None, explicitly_unavailable: bool) -> bool:
    return explicitly_unavailable or bool(answer_text and answer_text.strip())


def mandatory_keys(questions: list[dict[str, Any]]) -> list[str]:
    return [str(q["key"]) for q in questions if bool(q.get("mandatory"))]


def compute_completeness(
    questions: list[dict[str, Any]],
    answers_by_key: dict[str, tuple[str | None, bool]],
) -> CompletenessResult:
    keys = mandatory_keys(questions)
    if not keys:
        return CompletenessResult(
            mandatory_total=0,
            covered_count=0,
            percentage=Decimal("1.0000"),
            meets_threshold=True,
            gap_keys=[],
        )
    gaps: list[str] = []
    covered = 0
    for key in keys:
        value = answers_by_key.get(key)
        if value is None or not is_answer_covered(
            answer_text=value[0], explicitly_unavailable=value[1]
        ):
            gaps.append(key)
        else:
            covered += 1
    total = len(keys)
    percentage = (Decimal(covered) / Decimal(total)).quantize(Decimal("0.0001"))
    return CompletenessResult(
        mandatory_total=total,
        covered_count=covered,
        percentage=percentage,
        meets_threshold=percentage >= COMPLETENESS_THRESHOLD,
        gap_keys=gaps,
    )


def assert_gaps_have_owners(
    gap_keys: list[str],
    open_clarification_keys: set[str],
) -> None:
    """AC-002: unanswered mandatory items need an owned clarification/follow-up."""
    missing = [key for key in gap_keys if key not in open_clarification_keys]
    if missing:
        raise ValidationAppError(
            "Unanswered mandatory items require an owner follow-up: " + ", ".join(missing)
        )


def assert_brief_editable(status: str) -> None:
    if status not in BRIEF_EDITABLE:
        raise ForbiddenError(
            f"Requirement brief status '{status}' is immutable; create a new version"
        )


def assert_can_approve_brief(status: str) -> None:
    if status not in BRIEF_EDITABLE:
        raise InvalidTransitionError(
            f"Only draft/pending_approval briefs can be approved; current='{status}'"
        )


def assert_brief_completeness_gate(
    *,
    meets_threshold: bool,
    gap_keys: list[str],
    open_clarification_keys: set[str],
) -> None:
    """Approve only when AC-001 and AC-002 are satisfied."""
    if not meets_threshold:
        raise ValidationAppError(
            f"Completeness must be at least {COMPLETENESS_THRESHOLD} of mandatory fields"
        )
    assert_gaps_have_owners(gap_keys, open_clarification_keys)
