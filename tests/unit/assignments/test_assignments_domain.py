"""Unit tests for MOD-310 assignment domain rules."""

from __future__ import annotations

from decimal import Decimal

import pytest
from masms_api.errors import ForbiddenError, ValidationAppError
from masms_api.modules.assignments import domain


def test_unauthorized_actor_blocked() -> None:
    with pytest.raises(ForbiddenError, match="authorized"):
        domain.assert_project_authorized(is_member=False)


def test_unavailable_requires_override_reason() -> None:
    with pytest.raises(ForbiddenError, match="unavailable"):
        domain.assert_actor_available(
            eligible=False,
            reasons=["actor is on leave"],
            allow_override=False,
            override_reason=None,
        )
    with pytest.raises(ValidationAppError, match="Override requires"):
        domain.assert_actor_available(
            eligible=False,
            reasons=["actor is on leave"],
            allow_override=True,
            override_reason="  ",
        )
    domain.assert_actor_available(
        eligible=False,
        reasons=["actor is on leave"],
        allow_override=True,
        override_reason="Emergency coverage",
    )


def test_history_immutable() -> None:
    with pytest.raises(ForbiddenError, match="immutable"):
        domain.assert_history_immutable()


def test_score_candidate() -> None:
    assert domain.score_candidate(
        eligible=False,
        remaining_capacity_pct=Decimal("80"),
        proficiency=5,
        min_proficiency=3,
    ) == Decimal("0")
    score = domain.score_candidate(
        eligible=True,
        remaining_capacity_pct=Decimal("50"),
        proficiency=4,
        min_proficiency=3,
    )
    assert score == Decimal("70.0000")
