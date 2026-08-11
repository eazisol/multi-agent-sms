"""Unit tests for MOD-220 communication domain."""

from __future__ import annotations

import pytest
from masms_api.errors import ForbiddenError, ValidationAppError
from masms_api.modules.comms import domain


def test_sent_immutable_and_editable() -> None:
    domain.assert_message_editable("draft")
    domain.assert_message_editable("pending_approval")
    with pytest.raises(ForbiddenError):
        domain.assert_message_editable("sent")
    with pytest.raises(ForbiddenError):
        domain.assert_sent_immutable("sent")


def test_sensitive_requires_approval_before_send() -> None:
    assert domain.requires_approval_for_classification("confidential") is True
    assert domain.requires_approval_for_classification("internal") is False
    with pytest.raises(ForbiddenError):
        domain.assert_can_send(status="pending_approval", requires_approval=True, approved=False)
    domain.assert_can_send(status="pending_approval", requires_approval=True, approved=True)
    domain.assert_can_send(status="draft", requires_approval=False, approved=False)


def test_recipient_role_and_count() -> None:
    domain.assert_recipient_role("to")
    with pytest.raises(ValidationAppError):
        domain.assert_recipient_role("xyz")
    with pytest.raises(ValidationAppError):
        domain.assert_has_recipients(0)
    domain.assert_has_recipients(1)
