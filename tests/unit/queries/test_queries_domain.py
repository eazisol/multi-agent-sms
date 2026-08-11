"""Unit tests for MOD-210 query domain."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from masms_api.errors import InvalidTransitionError
from masms_api.modules.queries import domain


def test_transitions_and_sla() -> None:
    domain.assert_transition("received", "classified")
    with pytest.raises(InvalidTransitionError):
        domain.assert_transition("received", "converted")
    due = domain.compute_sla_due(received_at=datetime(2026, 8, 11, tzinfo=UTC), hours=24)
    assert due == datetime(2026, 8, 12, tzinfo=UTC)
    met = domain.evaluate_sla(
        due_at=due,
        responded_at=datetime(2026, 8, 11, 12, tzinfo=UTC),
    )
    assert met == "met"
    breached = domain.evaluate_sla(
        due_at=due,
        responded_at=None,
        now=due + timedelta(hours=1),
    )
    assert breached == "breached"
