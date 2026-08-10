"""Unit tests for MOD-100 identity domain rules."""

from __future__ import annotations

import pytest
from masms_api.errors import ValidationAppError
from masms_api.kernel.actor import ActorKind
from masms_api.modules.identity import domain


def test_agent_requires_active_human_supervisor() -> None:
    with pytest.raises(ValidationAppError):
        domain.assert_operational_agent_has_active_supervisor(
            agent_status="active",
            supervisor_human_status="inactive",
            supervisor_actor_kind=ActorKind.HUMAN.value,
        )
    with pytest.raises(ValidationAppError):
        domain.assert_operational_agent_has_active_supervisor(
            agent_status="active",
            supervisor_human_status="active",
            supervisor_actor_kind=ActorKind.AGENT.value,
        )
    domain.assert_operational_agent_has_active_supervisor(
        agent_status="active",
        supervisor_human_status="active",
        supervisor_actor_kind=ActorKind.HUMAN.value,
    )


def test_identities_must_be_separate() -> None:
    with pytest.raises(ValidationAppError):
        domain.assert_identities_are_separate("same", "same")
    domain.assert_identities_are_separate("a", "b")
