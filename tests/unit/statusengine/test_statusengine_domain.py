"""Unit tests for MOD-320 status engine domain rules."""

from __future__ import annotations

from uuid import uuid4

import pytest
from masms_api.errors import (
    ApprovalRequiredError,
    ForbiddenError,
    InvalidTransitionError,
    ValidationAppError,
)
from masms_api.kernel.actor import ActorKind
from masms_api.modules.statusengine import domain


def test_hold_blocks_transition() -> None:
    with pytest.raises(ForbiddenError, match="on hold"):
        domain.assert_not_on_hold(on_hold=True)
    domain.assert_not_on_hold(on_hold=False)


def test_invalid_transition() -> None:
    with pytest.raises(InvalidTransitionError, match="not configured"):
        domain.assert_transition_exists(
            allowed=False, from_status="open", to_status="done"
        )


def test_reason_and_evidence_required() -> None:
    with pytest.raises(ValidationAppError, match="reason"):
        domain.assert_reason_if_required(requires_reason=True, reason="  ")
    domain.assert_reason_if_required(requires_reason=True, reason="ok")
    with pytest.raises(ValidationAppError, match="evidence"):
        domain.assert_evidence_if_required(requires_evidence=True, evidence_ref=None)


def test_required_fields() -> None:
    with pytest.raises(ValidationAppError, match="Missing required"):
        domain.assert_required_fields(
            required_fields=["note", "owner"],
            provided_fields={"note": "x", "owner": None},
        )


def test_agent_cannot_skip_approval_gate() -> None:
    with pytest.raises(ForbiddenError, match="Agents cannot skip"):
        domain.assert_approval_gate(
            requires_approval=True,
            approval_id=uuid4(),
            actor_kind=ActorKind.AGENT,
        )
    with pytest.raises(ApprovalRequiredError, match="approval"):
        domain.assert_approval_gate(
            requires_approval=True,
            approval_id=None,
            actor_kind=ActorKind.HUMAN,
        )
    domain.assert_approval_gate(
        requires_approval=True,
        approval_id=uuid4(),
        actor_kind=ActorKind.HUMAN,
    )
    domain.assert_approval_gate(
        requires_approval=False,
        approval_id=None,
        actor_kind=ActorKind.AGENT,
    )


def test_reopen_rules() -> None:
    with pytest.raises(InvalidTransitionError, match="terminal"):
        domain.assert_can_reopen(
            is_terminal=False, actor_kind=ActorKind.HUMAN, reason="x"
        )
    with pytest.raises(ForbiddenError, match="human"):
        domain.assert_can_reopen(
            is_terminal=True, actor_kind=ActorKind.AGENT, reason="x"
        )
    with pytest.raises(ValidationAppError, match="reason"):
        domain.assert_can_reopen(
            is_terminal=True, actor_kind=ActorKind.HUMAN, reason=" "
        )
    domain.assert_can_reopen(
        is_terminal=True, actor_kind=ActorKind.HUMAN, reason="Needed"
    )


def test_hold_reason() -> None:
    with pytest.raises(ValidationAppError, match="Hold requires"):
        domain.assert_hold_reason(None)
