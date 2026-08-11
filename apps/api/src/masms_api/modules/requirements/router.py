"""HTTP routes for MOD-230 requirement gathering."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.errors import NotFoundError
from masms_api.kernel.pagination import PageMeta
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


class QuestionnairePage(BaseModel):
    items: list[QuestionnaireRead]
    page: PageMeta = Field(description="Pagination metadata")


class BriefPage(BaseModel):
    items: list[BriefRead]
    page: PageMeta = Field(description="Pagination metadata")


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


@router.get("/questionnaires", response_model=QuestionnairePage)
def list_questionnaires(
    status: str | None = Query(default=None),
    q: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: RequirementsService = Depends(_service),
) -> QuestionnairePage:
    items, page = service.list_questionnaires(
        status=status, q=q, limit=limit, offset=offset
    )
    return QuestionnairePage(
        items=[QuestionnaireRead.model_validate(r) for r in items], page=page
    )


@router.get("/questionnaires/{questionnaire_id}", response_model=QuestionnaireRead)
def get_questionnaire(
    questionnaire_id: UUID, service: RequirementsService = Depends(_service)
) -> QuestionnaireRead:
    return QuestionnaireRead.model_validate(service.get_questionnaire(questionnaire_id))


@router.get(
    "/questionnaires/{questionnaire_id}/versions",
    response_model=list[QuestionnaireVersionRead],
)
def list_questionnaire_versions(
    questionnaire_id: UUID, service: RequirementsService = Depends(_service)
) -> list[QuestionnaireVersionRead]:
    return [
        QuestionnaireVersionRead.model_validate(r)
        for r in service.list_questionnaire_versions(questionnaire_id)
    ]


@router.get(
    "/questionnaires/{questionnaire_id}/published-version",
    response_model=QuestionnaireVersionRead,
)
def get_published_version(
    questionnaire_id: UUID, service: RequirementsService = Depends(_service)
) -> QuestionnaireVersionRead:
    row = service.get_latest_published_version(questionnaire_id)
    if row is None:
        raise NotFoundError("No published questionnaire version found")
    return QuestionnaireVersionRead.model_validate(row)


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


@router.get("/answers", response_model=list[AnswerRead])
def list_answers(
    questionnaire_version_id: UUID = Query(),
    related_entity_type: str = Query(min_length=2, max_length=64),
    related_entity_id: UUID = Query(),
    service: RequirementsService = Depends(_service),
) -> list[AnswerRead]:
    rows = service.list_answers(
        questionnaire_version_id=questionnaire_version_id,
        related_entity_type=related_entity_type,
        related_entity_id=related_entity_id,
    )
    return [AnswerRead.model_validate(r) for r in rows]


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


@router.get("/briefs", response_model=BriefPage)
def list_briefs(
    related_entity_type: str | None = Query(default=None, min_length=2, max_length=64),
    related_entity_id: UUID | None = Query(default=None),
    status: str | None = Query(default=None),
    q: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: RequirementsService = Depends(_service),
) -> BriefPage:
    items, page = service.list_briefs(
        related_entity_type=related_entity_type,
        related_entity_id=related_entity_id,
        status=status,
        q=q,
        limit=limit,
        offset=offset,
    )
    return BriefPage(items=[BriefRead.model_validate(b) for b in items], page=page)


@router.get("/briefs/{brief_id}", response_model=BriefRead)
def get_brief(
    brief_id: UUID, service: RequirementsService = Depends(_service)
) -> BriefRead:
    return BriefRead.model_validate(service.get_brief(brief_id))
