"""Pydantic schemas for MOD-100 identity APIs."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from masms_api.kernel.pagination import PageMeta


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    slug: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9-]+$")


class OrganizationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    status: str
    version: int
    created_at: datetime


class ActorCreate(BaseModel):
    actor_kind: str = Field(min_length=4, max_length=32)
    display_name: str = Field(min_length=2, max_length=255)


class ActorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    actor_kind: str
    display_name: str
    status: str
    version: int


class HumanUserCreate(BaseModel):
    email: str = Field(min_length=3, max_length=320, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    full_name: str = Field(min_length=2, max_length=255)
    primary_role_code: str | None = Field(default=None, max_length=64)


class HumanUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    actor_id: UUID
    email: str
    full_name: str
    status: str
    primary_role_code: str | None
    version: int


class AgentCreate(BaseModel):
    agent_key: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9_-]+$")
    display_name: str = Field(min_length=2, max_length=255)
    supervisor_human_user_id: UUID


class AgentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    actor_id: UUID
    agent_key: str
    display_name: str
    status: str
    supervisor_human_user_id: UUID
    version: int


class RoleCreate(BaseModel):
    code: str = Field(min_length=2, max_length=64)
    title: str = Field(min_length=2, max_length=255)
    description: str | None = None


class RoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    title: str
    status: str
    version: int


class DepartmentCreate(BaseModel):
    code: str = Field(min_length=2, max_length=64)
    name: str = Field(min_length=2, max_length=255)


class DepartmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    code: str
    name: str
    status: str
    version: int


class TeamCreate(BaseModel):
    code: str = Field(min_length=2, max_length=64)
    name: str = Field(min_length=2, max_length=255)
    department_id: UUID | None = None


class TeamRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    department_id: UUID | None
    code: str
    name: str
    status: str
    version: int


class TeamMemberCreate(BaseModel):
    team_id: UUID
    actor_id: UUID
    membership_role: str = Field(default="member", max_length=64)


class TeamMemberRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    team_id: UUID
    actor_id: UUID
    membership_role: str
    status: str
    version: int


class ReportingLineCreate(BaseModel):
    subordinate_actor_id: UUID
    manager_actor_id: UUID
    effective_from: datetime


class ReportingLineRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    subordinate_actor_id: UUID
    manager_actor_id: UUID
    status: str
    effective_from: datetime
    effective_to: datetime | None
    version: int


class OrganizationPage(BaseModel):
    items: list[OrganizationRead]
    page: PageMeta


class ActorPage(BaseModel):
    items: list[ActorRead]
    page: PageMeta


class HumanUserPage(BaseModel):
    items: list[HumanUserRead]
    page: PageMeta


class AgentPage(BaseModel):
    items: list[AgentRead]
    page: PageMeta
