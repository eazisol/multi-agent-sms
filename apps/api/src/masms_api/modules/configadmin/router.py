"""HTTP routes for MOD-140 configuration administration."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.configadmin.schemas import (
    ApprovalWorkflowCreate,
    ApprovalWorkflowRead,
    ConfigurationVersionCreate,
    ConfigurationVersionRead,
    EscalationRuleCreate,
    EscalationRuleRead,
    FollowUpRuleCreate,
    FollowUpRuleRead,
    LiveTransitionCheckRequest,
    LiveTransitionCheckResponse,
    ReminderRuleCreate,
    ReminderRuleRead,
    StatusCreate,
    StatusRead,
    TransitionCreate,
    TransitionRead,
    WorkflowCreate,
    WorkflowRead,
)
from masms_api.modules.configadmin.service import ConfigAdminService

router = APIRouter(prefix="/config", tags=["config"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> ConfigAdminService:
    return ConfigAdminService(db, ctx)


@router.post("/versions", response_model=ConfigurationVersionRead, status_code=201)
def create_version(
    body: ConfigurationVersionCreate,
    service: ConfigAdminService = Depends(_service),
) -> ConfigurationVersionRead:
    return ConfigurationVersionRead.model_validate(service.create_version(body))


@router.post("/versions/{version_id}/approve", response_model=ConfigurationVersionRead)
def approve_version(
    version_id: UUID,
    service: ConfigAdminService = Depends(_service),
) -> ConfigurationVersionRead:
    return ConfigurationVersionRead.model_validate(service.approve_version(version_id))


@router.post("/versions/{version_id}/activate", response_model=ConfigurationVersionRead)
def activate_version(
    version_id: UUID,
    service: ConfigAdminService = Depends(_service),
) -> ConfigurationVersionRead:
    return ConfigurationVersionRead.model_validate(service.activate_version(version_id))


@router.post("/versions/rollback", response_model=ConfigurationVersionRead)
def rollback_version(
    restore_version_id: UUID | None = Query(default=None),
    service: ConfigAdminService = Depends(_service),
) -> ConfigurationVersionRead:
    return ConfigurationVersionRead.model_validate(
        service.rollback_effective(restore_version_id=restore_version_id)
    )


@router.post("/workflows", response_model=WorkflowRead, status_code=201)
def create_workflow(
    body: WorkflowCreate,
    service: ConfigAdminService = Depends(_service),
) -> WorkflowRead:
    return WorkflowRead.model_validate(service.create_workflow(body))


@router.post("/statuses", response_model=StatusRead, status_code=201)
def create_status(
    body: StatusCreate,
    service: ConfigAdminService = Depends(_service),
) -> StatusRead:
    return StatusRead.model_validate(service.create_status(body))


@router.post("/transitions", response_model=TransitionRead, status_code=201)
def create_transition(
    body: TransitionCreate,
    service: ConfigAdminService = Depends(_service),
) -> TransitionRead:
    return TransitionRead.model_validate(service.create_transition(body))


@router.post("/followup-rules", response_model=FollowUpRuleRead, status_code=201)
def create_followup(
    body: FollowUpRuleCreate,
    service: ConfigAdminService = Depends(_service),
) -> FollowUpRuleRead:
    return FollowUpRuleRead.model_validate(service.create_followup(body))


@router.post("/reminder-rules", response_model=ReminderRuleRead, status_code=201)
def create_reminder(
    body: ReminderRuleCreate,
    service: ConfigAdminService = Depends(_service),
) -> ReminderRuleRead:
    return ReminderRuleRead.model_validate(service.create_reminder(body))


@router.post("/escalation-rules", response_model=EscalationRuleRead, status_code=201)
def create_escalation(
    body: EscalationRuleCreate,
    service: ConfigAdminService = Depends(_service),
) -> EscalationRuleRead:
    return EscalationRuleRead.model_validate(service.create_escalation(body))


@router.post("/approval-workflows", response_model=ApprovalWorkflowRead, status_code=201)
def create_approval_workflow(
    body: ApprovalWorkflowCreate,
    service: ConfigAdminService = Depends(_service),
) -> ApprovalWorkflowRead:
    return ApprovalWorkflowRead.model_validate(service.create_approval_workflow(body))


@router.post("/live/transitions/check", response_model=LiveTransitionCheckResponse)
def check_live_transition(
    body: LiveTransitionCheckRequest,
    service: ConfigAdminService = Depends(_service),
) -> LiveTransitionCheckResponse:
    return service.check_live_transition(
        workflow_code=body.workflow_code,
        from_status_code=body.from_status_code,
        to_status_code=body.to_status_code,
    )
