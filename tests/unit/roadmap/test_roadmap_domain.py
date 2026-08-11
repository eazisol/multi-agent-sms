"""Unit tests for MOD-260 roadmap domain."""

from __future__ import annotations

from datetime import date
from uuid import uuid4

import pytest
from masms_api.errors import ForbiddenError, ValidationAppError
from masms_api.modules.roadmap import domain


def test_requirement_mapping_gate() -> None:
    a, b = uuid4(), uuid4()
    with pytest.raises(ValidationAppError):
        domain.assert_approved_requirements_mapped(
            approved_requirement_ids={a, b},
            mapped_requirement_ids={a},
        )
    domain.assert_approved_requirements_mapped(
        approved_requirement_ids={a},
        mapped_requirement_ids={a},
    )


def test_milestone_requires_owner_date_status_and_approval() -> None:
    with pytest.raises(ValidationAppError):
        domain.assert_milestone_fields(
            owner_actor_id=None, target_date=date(2026, 9, 1), status="planned"
        )
    with pytest.raises(ForbiddenError):
        domain.assert_can_complete_milestone(
            status="planned",
            owner_actor_id=uuid4(),
            target_date=date(2026, 9, 1),
            requires_approval=True,
            approved=False,
        )
    domain.assert_can_complete_milestone(
        status="in_progress",
        owner_actor_id=uuid4(),
        target_date=date(2026, 9, 1),
        requires_approval=True,
        approved=True,
    )


def test_independent_phase_completion_honors_only_predecessors() -> None:
    domain.assert_can_complete_phase(status="active", unfinished_predecessor_codes=[])
    with pytest.raises(ForbiddenError):
        domain.assert_can_complete_phase(
            status="active", unfinished_predecessor_codes=["DISCOVER"]
        )
    # siblings incomplete is allowed
    domain.assert_sibling_independence(
        completing_phase_id=uuid4(),
        sibling_incomplete_ids=[uuid4(), uuid4()],
    )
