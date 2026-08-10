"""Actor identity shared by humans, agents, system, and integrations."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from masms_api.kernel.ids import ActorId


class ActorKind(StrEnum):
    HUMAN = "human"
    AGENT = "agent"
    SYSTEM = "system"
    INTEGRATION = "integration"


@dataclass(frozen=True, slots=True)
class ActorContext:
    """Who is performing the current action."""

    actor_id: ActorId
    actor_kind: ActorKind
    display_name: str = "unknown"

    @property
    def is_human(self) -> bool:
        return self.actor_kind is ActorKind.HUMAN

    @property
    def may_approve_human_gates(self) -> bool:
        """Human approval gates reject non-human actors by default."""
        return self.actor_kind is ActorKind.HUMAN
