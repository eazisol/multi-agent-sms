"""MOD-100 identity domain rules."""

from __future__ import annotations

from masms_api.errors import ValidationAppError
from masms_api.kernel.actor import ActorKind

OPERATIONAL_AGENT_STATUSES = frozenset({"active", "enabled"})


def assert_human_actor_kind(kind: str | ActorKind) -> None:
    value = kind.value if isinstance(kind, ActorKind) else kind
    if value != ActorKind.HUMAN.value:
        raise ValidationAppError("Human user must link to an actor with kind=human")


def assert_agent_actor_kind(kind: str | ActorKind) -> None:
    value = kind.value if isinstance(kind, ActorKind) else kind
    if value != ActorKind.AGENT.value:
        raise ValidationAppError("Agent must link to an actor with kind=agent")


def assert_identities_are_separate(human_actor_id: object, agent_actor_id: object) -> None:
    if human_actor_id == agent_actor_id:
        raise ValidationAppError("Agent and human identities must be separate actors")


def assert_operational_agent_has_active_supervisor(
    *,
    agent_status: str,
    supervisor_human_status: str | None,
    supervisor_actor_kind: str | None,
) -> None:
    if agent_status not in OPERATIONAL_AGENT_STATUSES:
        return
    if supervisor_human_status != "active":
        raise ValidationAppError(
            "Every operational agent requires an active human supervisor"
        )
    if supervisor_actor_kind != ActorKind.HUMAN.value:
        raise ValidationAppError("Agent supervisor must be a human actor")
