"""Unit tests for MOD-300 ticket domain rules."""

from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

import pytest
from masms_api.errors import ForbiddenError, InvalidTransitionError, ValidationAppError
from masms_api.modules.tickets import domain


def test_ready_blocked_without_required_fields() -> None:
    with pytest.raises(ValidationAppError, match="not Ready"):
        domain.assert_can_become_ready(
            status=domain.STATUS_BACKLOG,
            description=None,
            acceptance_criteria=None,
            priority="medium",
            estimate_points=None,
            definition_of_done=None,
            phase_id=None,
            has_requirement_link=False,
            owner_actor_id=None,
            queue_code=None,
            unsatisfied_required_checks=["description"],
        )


def test_ready_allowed_when_complete() -> None:
    domain.assert_can_become_ready(
        status=domain.STATUS_BACKLOG,
        description="Build login",
        acceptance_criteria="User can log in",
        priority="high",
        estimate_points=Decimal("3"),
        definition_of_done="Tests pass",
        phase_id=uuid4(),
        has_requirement_link=True,
        owner_actor_id=uuid4(),
        queue_code=None,
        unsatisfied_required_checks=[],
    )


def test_done_requires_passed_qa_and_checks() -> None:
    with pytest.raises(InvalidTransitionError):
        domain.assert_can_complete(
            status=domain.STATUS_IN_PROGRESS,
            unsatisfied_required_checks=[],
        )
    with pytest.raises(ValidationAppError, match="unsatisfied"):
        domain.assert_can_complete(
            status=domain.STATUS_PASSED_QA,
            unsatisfied_required_checks=["qa_evidence"],
        )
    domain.assert_can_complete(
        status=domain.STATUS_PASSED_QA,
        unsatisfied_required_checks=[],
    )


def test_reopen_requires_human_reason_evidence() -> None:
    with pytest.raises(ForbiddenError):
        domain.assert_can_reopen(
            status=domain.STATUS_DONE,
            actor_kind="agent",
            reopen_reason="bug found",
            evidence_id=uuid4(),
        )
    with pytest.raises(ValidationAppError, match="reason"):
        domain.assert_can_reopen(
            status=domain.STATUS_DONE,
            actor_kind="human",
            reopen_reason="  ",
            evidence_id=uuid4(),
        )
    with pytest.raises(ValidationAppError, match="evidence"):
        domain.assert_can_reopen(
            status=domain.STATUS_DONE,
            actor_kind="human",
            reopen_reason="Regression",
            evidence_id=None,
        )
    domain.assert_can_reopen(
        status=domain.STATUS_DONE,
        actor_kind="human",
        reopen_reason="Confirmed defect",
        evidence_id=uuid4(),
    )


def test_no_self_dependency() -> None:
    tid = uuid4()
    with pytest.raises(ValidationAppError, match="itself"):
        domain.assert_no_self_dependency(tid, tid)


def test_owner_or_queue_required() -> None:
    with pytest.raises(ValidationAppError, match="owner or a queue"):
        domain.assert_owner_or_queue(owner_actor_id=None, queue_code=None)
    domain.assert_owner_or_queue(owner_actor_id=None, queue_code="dev-queue")
