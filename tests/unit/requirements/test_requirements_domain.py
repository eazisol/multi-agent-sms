"""Unit tests for MOD-230 requirement gathering domain."""

from __future__ import annotations

from decimal import Decimal

import pytest
from masms_api.errors import ForbiddenError, ValidationAppError
from masms_api.modules.requirements import domain


def _questions(n: int, *, mandatory: bool = True) -> list[dict]:
    return [
        {"key": f"q{i}", "text": f"Question {i}", "mandatory": mandatory, "answer_type": "text"}
        for i in range(1, n + 1)
    ]


def test_completeness_threshold_and_unavailable() -> None:
    questions = _questions(20)
    answers = {f"q{i}": (f"a{i}", False) for i in range(1, 20)}
    answers["q20"] = (None, True)
    result = domain.compute_completeness(questions, answers)
    assert result.percentage == Decimal("1.0000")
    assert result.meets_threshold is True
    assert result.gap_keys == []


def test_completeness_below_threshold() -> None:
    questions = _questions(20)
    answers = {f"q{i}": (f"a{i}", False) for i in range(1, 19)}
    result = domain.compute_completeness(questions, answers)
    assert result.covered_count == 18
    assert result.percentage == Decimal("0.9000")
    assert result.meets_threshold is False
    assert set(result.gap_keys) == {"q19", "q20"}


def test_gaps_require_owners_and_brief_gate() -> None:
    with pytest.raises(ValidationAppError):
        domain.assert_gaps_have_owners(["q1"], set())
    domain.assert_gaps_have_owners(["q1"], {"q1"})
    with pytest.raises(ValidationAppError):
        domain.assert_brief_completeness_gate(
            meets_threshold=False,
            gap_keys=["q1"],
            open_clarification_keys={"q1"},
        )
    domain.assert_brief_completeness_gate(
        meets_threshold=True,
        gap_keys=["q20"],
        open_clarification_keys={"q20"},
    )


def test_published_and_approved_immutable() -> None:
    domain.assert_version_editable("draft")
    with pytest.raises(ForbiddenError):
        domain.assert_version_editable("published")
    with pytest.raises(ForbiddenError):
        domain.assert_brief_editable("approved")
