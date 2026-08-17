"""Unit tests for MOD-360 agent catalog and run-status rules."""

from __future__ import annotations

import pytest
from masms_api.errors import ValidationAppError
from masms_api.modules.agents import domain


def test_catalog_has_exactly_six_approved_codes() -> None:
    assert domain.ALLOWED_CODES == frozenset(domain.AGENT_TITLES)
    assert domain.ALLOWED_CODES == frozenset(domain.AGENT_DEPARTMENTS)
    assert len(domain.ALLOWED_CODES) == 6
    assert domain.ALLOWED_CODES == frozenset(
        {
            "query_intake_agent",
            "requirements_clarifier",
            "roadmap_planner",
            "ticket_triage_agent",
            "qa_review_assistant",
            "status_report_drafter",
        }
    )


@pytest.mark.parametrize("code", sorted(domain.ALLOWED_CODES))
def test_each_catalog_code_is_allowed(code: str) -> None:
    domain.assert_allowed_agent_code(code)


def test_unknown_agent_code_is_rejected() -> None:
    with pytest.raises(ValidationAppError, match="Unknown agent_code"):
        domain.assert_allowed_agent_code("followup_chaser")


def test_low_confidence_requires_human_review() -> None:
    assert (
        domain.resolve_run_status_after_stub(confidence=0.59, review_required_flag=False)
        == "review_required"
    )
    assert (
        domain.resolve_run_status_after_stub(confidence=0.9, review_required_flag=True)
        == "review_required"
    )
    assert (
        domain.resolve_run_status_after_stub(confidence=0.6, review_required_flag=False)
        == "completed"
    )
