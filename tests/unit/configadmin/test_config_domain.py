"""Unit tests for MOD-140 config domain."""

from __future__ import annotations

import pytest
from masms_api.errors import ForbiddenError, InvalidTransitionError
from masms_api.modules.configadmin import domain


def test_draft_editable_and_live_gate() -> None:
    domain.assert_draft_editable("draft")
    with pytest.raises(ForbiddenError):
        domain.assert_draft_editable("effective")
    domain.assert_live_config("effective")
    with pytest.raises(ForbiddenError):
        domain.assert_live_config("draft")


def test_lifecycle_transitions() -> None:
    domain.assert_can_approve("draft")
    with pytest.raises(InvalidTransitionError):
        domain.assert_can_approve("approved")
    domain.assert_can_activate("approved")
    with pytest.raises(InvalidTransitionError):
        domain.assert_can_activate("draft")
    domain.assert_can_rollback("effective")
    with pytest.raises(InvalidTransitionError):
        domain.assert_can_rollback("draft")
