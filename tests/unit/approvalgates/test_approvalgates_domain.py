"""Unit tests for MOD-330 approval gate domain rules."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from masms_api.errors import (
    ApprovalRequiredError,
    ForbiddenError,
    InvalidTransitionError,
    ValidationAppError,
)
from masms_api.kernel.actor import ActorKind
from masms_api.modules.approvalgates import domain


def test_only_humans_decide() -> None:
    with pytest.raises(ForbiddenError, match="human"):
        domain.assert_human_decider(ActorKind.AGENT)
    domain.assert_human_decider(ActorKind.HUMAN)


def test_cannot_approve_own_recommendation() -> None:
    actor = uuid4()
    with pytest.raises(ForbiddenError, match="own recommendations"):
        domain.assert_not_self_recommendation(
            actor_id=actor,
            actor_kind=ActorKind.HUMAN,
            recommendation_source_actor_id=actor,
        )
    domain.assert_not_self_recommendation(
        actor_id=uuid4(),
        actor_kind=ActorKind.HUMAN,
        recommendation_source_actor_id=actor,
    )


def test_reject_requires_reason() -> None:
    with pytest.raises(ValidationAppError, match="Reason"):
        domain.assert_decision_reason(decision="reject", reason=" ")
    domain.assert_decision_reason(decision="approve", reason=None)


def test_gate_blocks_until_approved() -> None:
    with pytest.raises(ApprovalRequiredError):
        domain.assert_approved_for_action(approved=False, target_version_matches=False)
    with pytest.raises(ApprovalRequiredError, match="exact"):
        domain.assert_approved_for_action(approved=True, target_version_matches=False)
    domain.assert_approved_for_action(approved=True, target_version_matches=True)


def test_pending_and_delegation_window() -> None:
    with pytest.raises(InvalidTransitionError):
        domain.assert_pending("approved")
    now = datetime.now(UTC)
    with pytest.raises(ValidationAppError):
        domain.assert_delegation_window(
            starts_at=now, ends_at=now - timedelta(hours=1), now=now
        )
