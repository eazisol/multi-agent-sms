"""Unit tests for governance domain rules."""

import pytest
from masms_api.deps import ActorKind
from masms_api.errors import ForbiddenError, InvalidTransitionError, ValidationAppError
from masms_api.modules.governance import domain


def test_baseline_transition_happy_path() -> None:
    domain.assert_transition("draft", "submitted", domain.BASELINE_TRANSITIONS)
    domain.assert_transition("submitted", "under_review", domain.BASELINE_TRANSITIONS)
    domain.assert_transition("under_review", "approved", domain.BASELINE_TRANSITIONS)


def test_baseline_transition_rejects_skip() -> None:
    with pytest.raises(InvalidTransitionError):
        domain.assert_transition("draft", "approved", domain.BASELINE_TRANSITIONS)


def test_agent_cannot_approve() -> None:
    with pytest.raises(ForbiddenError):
        domain.assert_human_approver(ActorKind.AGENT)


def test_reject_requires_reason() -> None:
    with pytest.raises(ValidationAppError):
        domain.assert_reason_when_required("rejected", None)


def test_next_version() -> None:
    assert domain.next_version(1) == 2
