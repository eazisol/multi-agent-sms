"""HTTP routes for MOD-100 identity module."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.identity.schemas import (
    ActorPage,
    ActorRead,
    AgentCreate,
    AgentPage,
    AgentRead,
    DepartmentCreate,
    DepartmentRead,
    HumanUserCreate,
    HumanUserPage,
    HumanUserRead,
    OrganizationCreate,
    OrganizationPage,
    OrganizationRead,
    ReportingLineCreate,
    ReportingLineRead,
    RoleCreate,
    RolePage,
    RoleRead,
    TeamCreate,
    TeamMemberCreate,
    TeamMemberRead,
    TeamPage,
    TeamRead,
)
from masms_api.modules.identity.service import IdentityService

router = APIRouter(prefix="/identity", tags=["identity"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> IdentityService:
    return IdentityService(db, ctx)


@router.post("/organizations", response_model=OrganizationRead, status_code=201)
def create_organization(
    body: OrganizationCreate,
    service: IdentityService = Depends(_service),
) -> OrganizationRead:
    return OrganizationRead.model_validate(service.create_organization(body))


@router.get("/organizations", response_model=OrganizationPage)
def list_organizations(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: IdentityService = Depends(_service),
) -> OrganizationPage:
    items, page = service.list_organizations(limit=limit, offset=offset)
    return OrganizationPage(
        items=[OrganizationRead.model_validate(i) for i in items],
        page=page,
    )


@router.post("/humans", response_model=HumanUserRead, status_code=201)
def create_human(
    body: HumanUserCreate,
    service: IdentityService = Depends(_service),
) -> HumanUserRead:
    return HumanUserRead.model_validate(service.create_human_user(body))


@router.get("/humans", response_model=HumanUserPage)
def list_humans(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: IdentityService = Depends(_service),
) -> HumanUserPage:
    items, page = service.list_humans(limit=limit, offset=offset)
    return HumanUserPage(items=[HumanUserRead.model_validate(i) for i in items], page=page)


@router.post("/agents", response_model=AgentRead, status_code=201)
def create_agent(
    body: AgentCreate,
    service: IdentityService = Depends(_service),
) -> AgentRead:
    return AgentRead.model_validate(service.create_agent(body))


@router.get("/agents", response_model=AgentPage)
def list_agents(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: IdentityService = Depends(_service),
) -> AgentPage:
    items, page = service.list_agents(limit=limit, offset=offset)
    return AgentPage(items=[AgentRead.model_validate(i) for i in items], page=page)


@router.get("/actors", response_model=ActorPage)
def list_actors(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: IdentityService = Depends(_service),
) -> ActorPage:
    items, page = service.list_actors(limit=limit, offset=offset)
    return ActorPage(items=[ActorRead.model_validate(i) for i in items], page=page)


@router.post("/roles", response_model=RoleRead, status_code=201)
def create_role(
    body: RoleCreate,
    service: IdentityService = Depends(_service),
) -> RoleRead:
    return RoleRead.model_validate(service.create_role(body))


@router.get("/roles", response_model=RolePage)
def list_roles(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: IdentityService = Depends(_service),
) -> RolePage:
    items, page = service.list_roles(limit=limit, offset=offset)
    return RolePage(items=[RoleRead.model_validate(i) for i in items], page=page)


@router.post("/departments", response_model=DepartmentRead, status_code=201)
def create_department(
    body: DepartmentCreate,
    service: IdentityService = Depends(_service),
) -> DepartmentRead:
    return DepartmentRead.model_validate(service.create_department(body))


@router.post("/teams", response_model=TeamRead, status_code=201)
def create_team(
    body: TeamCreate,
    service: IdentityService = Depends(_service),
) -> TeamRead:
    return TeamRead.model_validate(service.create_team(body))


@router.get("/teams", response_model=TeamPage)
def list_teams(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: IdentityService = Depends(_service),
) -> TeamPage:
    items, page = service.list_teams(limit=limit, offset=offset)
    return TeamPage(items=[TeamRead.model_validate(i) for i in items], page=page)


@router.post("/team-members", response_model=TeamMemberRead, status_code=201)
def add_team_member(
    body: TeamMemberCreate,
    service: IdentityService = Depends(_service),
) -> TeamMemberRead:
    return TeamMemberRead.model_validate(service.add_team_member(body))


@router.post("/reporting-lines", response_model=ReportingLineRead, status_code=201)
def create_reporting_line(
    body: ReportingLineCreate,
    service: IdentityService = Depends(_service),
) -> ReportingLineRead:
    return ReportingLineRead.model_validate(service.create_reporting_line(body))
