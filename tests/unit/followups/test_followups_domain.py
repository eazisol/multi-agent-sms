"""Unit tests for MOD-340 follow-up domain rules."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from masms_api.errors import ConflictError, ForbiddenError, ValidationAppError
from masms_api.modules.followups import domain


def test_required_fields_ac001() -> None:
    with pytest.raises(ValidationAppError, match="missing required"):
        domain.assert_required_fields(
            owner_actor_id=None,
            due_at=datetime.now(UTC),
            rule_version_id=uuid4(),
            closure_condition="done",
            required_response="ack",
        )
    domain.assert_required_fields(
        owner_actor_id=uuid4(),
        due_at=datetime.now(UTC),
        rule_version_id=uuid4(),
        closure_condition="Client replied",
        required_response="Acknowledge",
    )


def test_parent_blocks_while_children_open() -> None:
    with pytest.raises(ForbiddenError, match="mandatory child"):
        domain.assert_can_close_parent(unresolved_mandatory_children=1)
    domain.assert_can_close_parent(unresolved_mandatory_children=0)


def test_business_hours_skips_weekend() -> None:
    # Friday 17:00 UTC
    start = datetime(2026, 8, 14, 17, 0, tzinfo=UTC)
    result = domain.add_business_hours(start=start, hours=2)
    assert result.weekday() < 5
    assert result > start


def test_reminder_and_escalation_windows() -> None:
    due = datetime.now(UTC) + timedelta(hours=2)
    now = datetime.now(UTC)
    assert domain.reminder_due(due_at=due, offset_hours=4, now=now) is True
    assert domain.escalation_due(due_at=due, after_hours=24, now=now) is False


def test_pause_and_open() -> None:
    with pytest.raises(ConflictError):
        domain.assert_open("closed")
    with pytest.raises(ValidationAppError):
        domain.assert_pause_fields(reason=" ", next_action="x", review_at=datetime.now(UTC))
