"""HTTP routes for MOD-340 follow-ups."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.followups.schemas import (
    BusinessDeadlineRead,
    ChildLinkCreate,
    ClosureEvidenceCreate,
    ClosureEvidenceRead,
    EscalationRead,
    FollowUpCreate,
    FollowUpRead,
    LinkRead,
    ProcessOverdueResult,
    ReminderRead,
    SlaPauseCreate,
    SlaPauseRead,
)
from masms_api.modules.followups.service import FollowUpService

router = APIRouter(prefix="/follow-ups", tags=["follow-ups"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> FollowUpService:
    return FollowUpService(db, ctx)


@router.post("", response_model=FollowUpRead, status_code=201)
def create_followup(
    body: FollowUpCreate, service: FollowUpService = Depends(_service)
) -> FollowUpRead:
    return FollowUpRead.model_validate(service.create(body))


@router.get("", response_model=list[FollowUpRead])
def list_open(service: FollowUpService = Depends(_service)) -> list[FollowUpRead]:
    return [FollowUpRead.model_validate(r) for r in service.list_open()]


@router.get("/{followup_id}", response_model=FollowUpRead)
def get_followup(
    followup_id: UUID, service: FollowUpService = Depends(_service)
) -> FollowUpRead:
    return FollowUpRead.model_validate(service.get(followup_id))


@router.post("/{followup_id}/children", response_model=LinkRead, status_code=201)
def link_child(
    followup_id: UUID,
    body: ChildLinkCreate,
    service: FollowUpService = Depends(_service),
) -> LinkRead:
    return LinkRead.model_validate(service.link_child(followup_id, body))


@router.get("/{followup_id}/children", response_model=list[LinkRead])
def list_children(
    followup_id: UUID, service: FollowUpService = Depends(_service)
) -> list[LinkRead]:
    return [LinkRead.model_validate(r) for r in service.list_links(followup_id)]


@router.get("/{followup_id}/reminders", response_model=list[ReminderRead])
def list_reminders(
    followup_id: UUID, service: FollowUpService = Depends(_service)
) -> list[ReminderRead]:
    return [ReminderRead.model_validate(r) for r in service.list_reminders(followup_id)]


@router.get("/{followup_id}/escalations", response_model=list[EscalationRead])
def list_escalations(
    followup_id: UUID, service: FollowUpService = Depends(_service)
) -> list[EscalationRead]:
    return [EscalationRead.model_validate(r) for r in service.list_escalations(followup_id)]


@router.get("/{followup_id}/deadline", response_model=BusinessDeadlineRead)
def get_deadline(
    followup_id: UUID, service: FollowUpService = Depends(_service)
) -> BusinessDeadlineRead:
    return BusinessDeadlineRead.model_validate(service.get_deadline(followup_id))


@router.post("/{followup_id}/sla-pauses", response_model=SlaPauseRead, status_code=201)
def pause_sla(
    followup_id: UUID,
    body: SlaPauseCreate,
    service: FollowUpService = Depends(_service),
) -> SlaPauseRead:
    return SlaPauseRead.model_validate(service.pause_sla(followup_id, body))


@router.post("/{followup_id}/sla-pauses/resume", response_model=SlaPauseRead)
def resume_sla(
    followup_id: UUID, service: FollowUpService = Depends(_service)
) -> SlaPauseRead:
    return SlaPauseRead.model_validate(service.resume_sla(followup_id))


@router.post(
    "/{followup_id}/closure-evidence",
    response_model=ClosureEvidenceRead,
    status_code=201,
)
def add_closure_evidence(
    followup_id: UUID,
    body: ClosureEvidenceCreate,
    service: FollowUpService = Depends(_service),
) -> ClosureEvidenceRead:
    return ClosureEvidenceRead.model_validate(service.add_closure_evidence(followup_id, body))


@router.post("/{followup_id}/close", response_model=FollowUpRead)
def close_followup(
    followup_id: UUID, service: FollowUpService = Depends(_service)
) -> FollowUpRead:
    return FollowUpRead.model_validate(service.close(followup_id))


@router.post("/{followup_id}/process-overdue", response_model=ProcessOverdueResult)
def process_overdue(
    followup_id: UUID, service: FollowUpService = Depends(_service)
) -> ProcessOverdueResult:
    return service.process_overdue(followup_id)
