"""HTTP routes for MOD-230 requirement gathering."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.modules.requirements.schemas import (
    AnswerRead,
    AnswerUpsert,
    BriefCreate,
    BriefRead,
    ClarificationCreate,
    ClarificationRead,
    CompletenessCompute,
    CompletenessScoreRead,
    QuestionnaireCreate,
    QuestionnaireRead,
    QuestionnaireVersionCreate,
    QuestionnaireVersionRead,
)
from masms_api.modules.requirements.service import RequirementsService

router = APIRouter(prefix="/requirements", tags=["requirements"])


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> RequirementsService:
    return RequirementsService(db, ctx)


@router.post("/questionnaires", response_model=QuestionnaireRead, status_code=201)
def create_questionnaire(
    body: QuestionnaireCreate, service: RequirementsService = Depends(_service)
) -> QuestionnaireRead:
    return QuestionnaireRead.model_validate(service.create_questionnaire(body))


@router.post("/questionnaire-versions", response_model=QuestionnaireVersionRead, status_code=201)
def create_version(
    body: QuestionnaireVersionCreate, service: RequirementsService = Depends(_service)
) -> QuestionnaireVersionRead:
    return QuestionnaireVersionRead.model_validate(service.create_version(body))


@router.post(
    "/questionnaire-versions/{version_id}/publish",
    response_model=QuestionnaireVersionRead,
)
def publish_version(
    version_id: UUID, service: RequirementsService = Depends(_service)
) -> QuestionnaireVersionRead:
    return QuestionnaireVersionRead.model_validate(service.publish_version(version_id))


@router.post("/answers", response_model=AnswerRead, status_code=201)
def upsert_answer(
    body: AnswerUpsert, service: RequirementsService = Depends(_service)
) -> AnswerRead:
    return AnswerRead.model_validate(service.upsert_answer(body))


@router.post("/completeness-scores", response_model=CompletenessScoreRead, status_code=201)
def compute_completeness(
    body: CompletenessCompute, service: RequirementsService = Depends(_service)
) -> CompletenessScoreRead:
    return CompletenessScoreRead.model_validate(service.compute_completeness(body))


@router.post("/clarifications", response_model=ClarificationRead, status_code=201)
def create_clarification(
    body: ClarificationCreate, service: RequirementsService = Depends(_service)
) -> ClarificationRead:
    return ClarificationRead.model_validate(service.create_clarification(body))


@router.post("/briefs", response_model=BriefRead, status_code=201)
def create_brief(
    body: BriefCreate, service: RequirementsService = Depends(_service)
) -> BriefRead:
    return BriefRead.model_validate(service.create_brief(body))


@router.post("/briefs/{brief_id}/approve", response_model=BriefRead)
def approve_brief(
    brief_id: UUID, service: RequirementsService = Depends(_service)
) -> BriefRead:
    return BriefRead.model_validate(service.approve_brief(brief_id))


@router.get("/briefs", response_model=list[BriefRead])
def list_briefs(
    related_entity_type: str = Query(min_length=2, max_length=64),
    related_entity_id: UUID = Query(),
    service: RequirementsService = Depends(_service),
) -> list[BriefRead]:
    return [
        BriefRead.model_validate(b)
        for b in service.list_briefs(
            related_entity_type=related_entity_type,
            related_entity_id=related_entity_id,
        )
    ]
