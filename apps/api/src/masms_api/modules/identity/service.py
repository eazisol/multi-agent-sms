"""Application service for MOD-100 identity entities."""

from __future__ import annotations

from datetime import UTC
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from masms_api.deps import RequestContext
from masms_api.errors import ConflictError, NotFoundError, ValidationAppError
from masms_api.kernel.actor import ActorKind
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.identity import domain
from masms_api.modules.identity.models import (
    Actor,
    AgentIdentity,
    Department,
    HumanUser,
    Organization,
    ReportingLine,
    RoleDefinition,
    Team,
    TeamMember,
)
from masms_api.modules.identity.schemas import (
    AgentCreate,
    DepartmentCreate,
    HumanUserCreate,
    OrganizationCreate,
    ReportingLineCreate,
    RoleCreate,
    TeamCreate,
    TeamMemberCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class IdentityService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)

    def create_organization(self, data: OrganizationCreate) -> Organization:
        existing = self.db.scalar(select(Organization).where(Organization.slug == data.slug))
        if existing is not None:
            raise ConflictError(f"Organization slug '{data.slug}' already exists")
        row = Organization(
            id=uuid4(),
            name=data.name,
            slug=data.slug,
            status="active",
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.flush()
        self.obs.write_audit(
            action="create",
            entity_type="organization",
            entity_id=row.id,
            entity_version=row.version,
            payload={"slug": row.slug},
        )
        enqueue_outbox(
            self.db,
            organization_id=row.id,
            aggregate_type="organization",
            aggregate_id=row.id,
            event_type="identity.organization.created",
            payload={"slug": row.slug},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_organizations(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[Organization], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [Organization.deleted_at.is_(None)]
        total = self.db.scalar(select(func.count()).select_from(Organization).where(*filters)) or 0
        rows = self.db.scalars(
            select(Organization)
            .where(*filters)
            .order_by(Organization.slug)
            .offset(offset)
            .limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def create_human_user(self, data: HumanUserCreate) -> HumanUser:
        org_id = self.ctx.organization_id
        if data.idp_subject:
            linked = self.db.scalar(
                select(HumanUser).where(HumanUser.idp_subject == data.idp_subject.strip())
            )
            if linked is not None:
                raise ConflictError("Auth0 subject is already linked to a MASMS user")
        actor = Actor(
            id=uuid4(),
            organization_id=org_id,
            actor_kind=ActorKind.HUMAN.value,
            display_name=data.full_name,
            status="active",
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        domain.assert_human_actor_kind(actor.actor_kind)
        user = HumanUser(
            id=uuid4(),
            organization_id=org_id,
            actor_id=actor.id,
            email=data.email.lower(),
            full_name=data.full_name,
            idp_subject=data.idp_subject.strip() if data.idp_subject else None,
            status="active",
            primary_role_code=data.primary_role_code,
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(actor)
        self.uow.flush()
        user.actor_id = actor.id
        self.uow.add(user)
        self.uow.flush()
        self.obs.write_audit(
            action="create",
            entity_type="human_user",
            entity_id=user.id,
            entity_version=1,
            payload={"email": user.email},
        )
        self.uow.commit()
        self.uow.refresh(user)
        return user

    def create_agent(self, data: AgentCreate) -> AgentIdentity:
        org_id = self.ctx.organization_id
        supervisor = self.db.scalar(
            select(HumanUser).where(
                HumanUser.id == data.supervisor_human_user_id,
                HumanUser.organization_id == org_id,
                HumanUser.deleted_at.is_(None),
            )
        )
        if supervisor is None:
            raise NotFoundError("Supervisor human user not found in organization")
        supervisor_actor = self.db.scalar(select(Actor).where(Actor.id == supervisor.actor_id))
        if supervisor_actor is None:
            raise NotFoundError("Supervisor actor not found")
        domain.assert_operational_agent_has_active_supervisor(
            agent_status="active",
            supervisor_human_status=supervisor.status,
            supervisor_actor_kind=supervisor_actor.actor_kind,
        )
        agent_actor = Actor(
            id=uuid4(),
            organization_id=org_id,
            actor_kind=ActorKind.AGENT.value,
            display_name=data.display_name,
            status="active",
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        domain.assert_agent_actor_kind(agent_actor.actor_kind)
        domain.assert_identities_are_separate(supervisor.actor_id, agent_actor.id)
        agent = AgentIdentity(
            id=uuid4(),
            organization_id=org_id,
            actor_id=agent_actor.id,
            agent_key=data.agent_key,
            display_name=data.display_name,
            status="active",
            supervisor_human_user_id=supervisor.id,
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(agent_actor)
        self.uow.flush()
        agent.actor_id = agent_actor.id
        self.uow.add(agent)
        self.uow.flush()
        self.obs.write_audit(
            action="create",
            entity_type="agent",
            entity_id=agent.id,
            entity_version=1,
            payload={"agent_key": agent.agent_key, "supervisor_id": str(supervisor.id)},
        )
        self.uow.commit()
        self.uow.refresh(agent)
        return agent

    def create_role(self, data: RoleCreate) -> RoleDefinition:
        row = RoleDefinition(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code,
            title=data.title,
            description=data.description,
            status="active",
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_department(self, data: DepartmentCreate) -> Department:
        row = Department(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code,
            name=data.name,
            status="active",
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_team(self, data: TeamCreate) -> Team:
        if data.department_id is not None:
            dept = self.db.scalar(
                select(Department).where(
                    Department.id == data.department_id,
                    Department.organization_id == self.ctx.organization_id,
                )
            )
            if dept is None:
                raise NotFoundError("Department not found in organization")
        row = Team(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            department_id=data.department_id,
            code=data.code,
            name=data.name,
            status="active",
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def add_team_member(self, data: TeamMemberCreate) -> TeamMember:
        team = self.db.scalar(
            select(Team).where(
                Team.id == data.team_id,
                Team.organization_id == self.ctx.organization_id,
            )
        )
        if team is None:
            raise NotFoundError("Team not found")
        actor = self.db.scalar(
            select(Actor).where(
                Actor.id == data.actor_id,
                Actor.organization_id == self.ctx.organization_id,
            )
        )
        if actor is None:
            raise NotFoundError("Actor not found in organization")
        row = TeamMember(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            team_id=team.id,
            actor_id=actor.id,
            membership_role=data.membership_role,
            status="active",
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_reporting_line(self, data: ReportingLineCreate) -> ReportingLine:
        if data.subordinate_actor_id == data.manager_actor_id:
            raise ValidationAppError("Reporting line cannot be self-referential")
        for actor_id in (data.subordinate_actor_id, data.manager_actor_id):
            actor = self.db.scalar(
                select(Actor).where(
                    Actor.id == actor_id,
                    Actor.organization_id == self.ctx.organization_id,
                )
            )
            if actor is None:
                raise NotFoundError("Reporting line actors must belong to organization")
        row = ReportingLine(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            subordinate_actor_id=data.subordinate_actor_id,
            manager_actor_id=data.manager_actor_id,
            status="active",
            effective_from=data.effective_from.astimezone(UTC),
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_actors(self, *, limit: int = 20, offset: int = 0) -> tuple[list[Actor], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [
            Actor.organization_id == self.ctx.organization_id,
            Actor.deleted_at.is_(None),
        ]
        total = self.db.scalar(select(func.count()).select_from(Actor).where(*filters)) or 0
        rows = self.db.scalars(
            select(Actor).where(*filters).order_by(Actor.display_name).offset(offset).limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def list_humans(self, *, limit: int = 20, offset: int = 0) -> tuple[list[HumanUser], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [
            HumanUser.organization_id == self.ctx.organization_id,
            HumanUser.deleted_at.is_(None),
        ]
        total = self.db.scalar(select(func.count()).select_from(HumanUser).where(*filters)) or 0
        rows = self.db.scalars(
            select(HumanUser).where(*filters).order_by(HumanUser.email).offset(offset).limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def list_agents(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[AgentIdentity], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [
            AgentIdentity.organization_id == self.ctx.organization_id,
            AgentIdentity.deleted_at.is_(None),
        ]
        total = self.db.scalar(select(func.count()).select_from(AgentIdentity).where(*filters)) or 0
        rows = self.db.scalars(
            select(AgentIdentity)
            .where(*filters)
            .order_by(AgentIdentity.agent_key)
            .offset(offset)
            .limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def list_roles(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[RoleDefinition], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [
            RoleDefinition.organization_id == self.ctx.organization_id,
            RoleDefinition.deleted_at.is_(None),
        ]
        total = (
            self.db.scalar(select(func.count()).select_from(RoleDefinition).where(*filters)) or 0
        )
        rows = self.db.scalars(
            select(RoleDefinition)
            .where(*filters)
            .order_by(RoleDefinition.code)
            .offset(offset)
            .limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def list_teams(self, *, limit: int = 20, offset: int = 0) -> tuple[list[Team], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [
            Team.organization_id == self.ctx.organization_id,
            Team.deleted_at.is_(None),
        ]
        total = self.db.scalar(select(func.count()).select_from(Team).where(*filters)) or 0
        rows = self.db.scalars(
            select(Team).where(*filters).order_by(Team.code).offset(offset).limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))
