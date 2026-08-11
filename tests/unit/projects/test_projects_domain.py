"""Unit tests for MOD-240 project/SRS domain."""

from __future__ import annotations

import pytest
from masms_api.errors import ForbiddenError, ValidationAppError
from masms_api.modules.projects import domain


def test_approve_requirement_needs_acceptance_criteria() -> None:
    with pytest.raises(ValidationAppError):
        domain.assert_can_approve_requirement_version(
            status="draft",
            requirement_code="REQ-1",
            acceptance_criteria_count=0,
        )
    domain.assert_can_approve_requirement_version(
        status="draft",
        requirement_code="REQ-1",
        acceptance_criteria_count=1,
    )


def test_srs_requires_human_approval_path() -> None:
    with pytest.raises(ValidationAppError):
        domain.assert_can_approve_srs(status="draft", approved_requirement_version_count=0)
    domain.assert_can_approve_srs(status="draft", approved_requirement_version_count=1)
    with pytest.raises(ForbiddenError):
        domain.assert_srs_editable("approved")


def test_material_change_needs_reason() -> None:
    domain.assert_change_reason_for_new_version(version_number=1, change_reason=None)
    with pytest.raises(ValidationAppError):
        domain.assert_change_reason_for_new_version(version_number=2, change_reason=None)
    domain.assert_change_reason_for_new_version(
        version_number=2, change_reason="Scope change CR-1"
    )
