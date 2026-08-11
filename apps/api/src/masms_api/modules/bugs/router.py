"""HTTP routes for MOD-410 bugs."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.bugs.schemas import (
    AssignmentCreate,
    AssignmentRead,
    BugCreate,
    BugHistory,
    BugRead,
    BugReject,
    BugReopen,
    BugTransition,
    FixCreate,
    FixRead,
    KnownIssueCreate,
    KnownIssueDecide,
    KnownIssueRead,
    LinkCreate,
    LinkRead,
    ReleaseGateResult,
    RetestCreate,
    RetestRead,
    SeveritySlaRead,
    SeveritySlaUpsert,
)
from masms_api.modules.bugs.service import BugService

router = APIRouter(prefix="/bugs", tags=["bugs"])


class BugPage(BaseModel):
    items: list[BugRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> BugService:
    return BugService(db, ctx)


@router.post("", response_model=BugRead, status_code=201)
def create_bug(body: BugCreate, service: BugService = Depends(_service)) -> BugRead:
    return BugRead.model_validate(service.create_bug(body))


@router.get("", response_model=BugPage)
def list_bugs(
    status: str | None = Query(default=None),
    severity: str | None = Query(default=None),
    project_id: UUID | None = Query(default=None),
    q: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: BugService = Depends(_service),
) -> BugPage:
    items, page = service.list_bugs(
        status=status,
        severity=severity,
        project_id=project_id,
        q=q,
        limit=limit,
        offset=offset,
    )
    return BugPage(items=[BugRead.model_validate(r) for r in items], page=page)


@router.get("/release-gate", response_model=ReleaseGateResult)
def release_gate(
    project_id: UUID | None = Query(default=None),
    service: BugService = Depends(_service),
) -> ReleaseGateResult:
    return service.release_gate(project_id=project_id)


@router.get("/severity-slas", response_model=list[SeveritySlaRead])
def list_slas(service: BugService = Depends(_service)) -> list[SeveritySlaRead]:
    return [SeveritySlaRead.model_validate(r) for r in service.list_severity_slas()]


@router.put("/severity-slas", response_model=SeveritySlaRead)
def upsert_sla(
    body: SeveritySlaUpsert,
    service: BugService = Depends(_service),
) -> SeveritySlaRead:
    return SeveritySlaRead.model_validate(service.upsert_severity_sla(body))


@router.get("/{bug_id}", response_model=BugRead)
def get_bug(bug_id: UUID, service: BugService = Depends(_service)) -> BugRead:
    return BugRead.model_validate(service.get_bug(bug_id))


@router.get("/{bug_id}/history", response_model=BugHistory)
def bug_history(bug_id: UUID, service: BugService = Depends(_service)) -> BugHistory:
    return service.history(bug_id)


@router.post("/{bug_id}/reject", response_model=BugRead)
def reject_bug(
    bug_id: UUID,
    body: BugReject,
    service: BugService = Depends(_service),
) -> BugRead:
    return BugRead.model_validate(service.reject_bug(bug_id, body))


@router.post("/{bug_id}/reopen", response_model=BugRead)
def reopen_bug(
    bug_id: UUID,
    body: BugReopen,
    service: BugService = Depends(_service),
) -> BugRead:
    return BugRead.model_validate(service.reopen_bug(bug_id, body))


@router.post("/{bug_id}/transition", response_model=BugRead)
def transition_bug(
    bug_id: UUID,
    body: BugTransition,
    service: BugService = Depends(_service),
) -> BugRead:
    return BugRead.model_validate(service.transition_bug(bug_id, body))


@router.post("/{bug_id}/links", response_model=LinkRead, status_code=201)
def add_link(
    bug_id: UUID,
    body: LinkCreate,
    service: BugService = Depends(_service),
) -> LinkRead:
    return LinkRead.model_validate(service.add_link(bug_id, body))


@router.get("/{bug_id}/links", response_model=list[LinkRead])
def list_links(bug_id: UUID, service: BugService = Depends(_service)) -> list[LinkRead]:
    return [LinkRead.model_validate(r) for r in service.list_links(bug_id)]


@router.post("/{bug_id}/assignments", response_model=AssignmentRead, status_code=201)
def assign(
    bug_id: UUID,
    body: AssignmentCreate,
    service: BugService = Depends(_service),
) -> AssignmentRead:
    return AssignmentRead.model_validate(service.assign(bug_id, body))


@router.get("/{bug_id}/assignments", response_model=list[AssignmentRead])
def list_assignments(
    bug_id: UUID, service: BugService = Depends(_service)
) -> list[AssignmentRead]:
    return [AssignmentRead.model_validate(r) for r in service.list_assignments(bug_id)]


@router.post("/{bug_id}/fixes", response_model=FixRead, status_code=201)
def submit_fix(
    bug_id: UUID,
    body: FixCreate,
    service: BugService = Depends(_service),
) -> FixRead:
    return FixRead.model_validate(service.submit_fix(bug_id, body))


@router.get("/{bug_id}/fixes", response_model=list[FixRead])
def list_fixes(bug_id: UUID, service: BugService = Depends(_service)) -> list[FixRead]:
    return [FixRead.model_validate(r) for r in service.list_fixes(bug_id)]


@router.post("/{bug_id}/retests", response_model=RetestRead, status_code=201)
def record_retest(
    bug_id: UUID,
    body: RetestCreate,
    service: BugService = Depends(_service),
) -> RetestRead:
    return RetestRead.model_validate(service.record_retest(bug_id, body))


@router.get("/{bug_id}/retests", response_model=list[RetestRead])
def list_retests(bug_id: UUID, service: BugService = Depends(_service)) -> list[RetestRead]:
    return [RetestRead.model_validate(r) for r in service.list_retests(bug_id)]


@router.post("/{bug_id}/known-issues", response_model=KnownIssueRead, status_code=201)
def request_known_issue(
    bug_id: UUID,
    body: KnownIssueCreate,
    service: BugService = Depends(_service),
) -> KnownIssueRead:
    return KnownIssueRead.model_validate(service.request_known_issue(bug_id, body))


@router.post("/known-issues/{approval_id}/decide", response_model=KnownIssueRead)
def decide_known_issue(
    approval_id: UUID,
    body: KnownIssueDecide,
    service: BugService = Depends(_service),
) -> KnownIssueRead:
    return KnownIssueRead.model_validate(service.decide_known_issue(approval_id, body))


@router.get("/{bug_id}/known-issues", response_model=list[KnownIssueRead])
def list_known_issues(
    bug_id: UUID, service: BugService = Depends(_service)
) -> list[KnownIssueRead]:
    return [KnownIssueRead.model_validate(r) for r in service.list_known_issues(bug_id)]
