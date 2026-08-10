"""Branded UUID identifiers shared across modules (MOD-020-MP-001)."""

from __future__ import annotations

from typing import NewType
from uuid import UUID

OrganizationId = NewType("OrganizationId", UUID)
ClientId = NewType("ClientId", UUID)
ProjectId = NewType("ProjectId", UUID)
ActorId = NewType("ActorId", UUID)
CorrelationId = NewType("CorrelationId", UUID)
EntityId = NewType("EntityId", UUID)


def as_organization_id(value: UUID | str) -> OrganizationId:
    return OrganizationId(value if isinstance(value, UUID) else UUID(str(value)))


def as_client_id(value: UUID | str) -> ClientId:
    return ClientId(value if isinstance(value, UUID) else UUID(str(value)))


def as_project_id(value: UUID | str) -> ProjectId:
    return ProjectId(value if isinstance(value, UUID) else UUID(str(value)))


def as_actor_id(value: UUID | str) -> ActorId:
    return ActorId(value if isinstance(value, UUID) else UUID(str(value)))


def as_correlation_id(value: UUID | str) -> CorrelationId:
    return CorrelationId(value if isinstance(value, UUID) else UUID(str(value)))


def as_entity_id(value: UUID | str) -> EntityId:
    return EntityId(value if isinstance(value, UUID) else UUID(str(value)))
