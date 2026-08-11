"""Requirement gathering application service (MOD-230)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from masms_api.errors import ForbiddenError, NotFoundError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.requirements import domain
from masms_api.modules.requirements.models import (
    ClarificationRequest,
    CompletenessScore,
    Questionnaire,
    QuestionnaireVersion,
    RequirementAnswer,
    RequirementBrief,
)
from masms_api.modules.requirements.schemas import (
    AnswerUpsert,
    BriefCreate,
    ClarificationCreate,
    CompletenessCompute,
    QuestionnaireCreate,
    QuestionnaireVersionCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class RequirementsService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_questionnaire(self, data: QuestionnaireCreate) -> Questionnaire:
        row = Questionnaire(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code,
            title=data.title,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="questionnaire_create",
            entity_type="req_questionnaire",
            entity_id=row.id,
            payload={"code": data.code},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_questionnaires(
        self,
        *,
        status: str | None = None,
        q: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Questionnaire]:
        stmt = select(Questionnaire).where(
            Questionnaire.organization_id == self.ctx.organization_id
        )
        if status:
            stmt = stmt.where(Questionnaire.status == status)
        if q and q.strip():
            like = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(Questionnaire.code.ilike(like), Questionnaire.title.ilike(like))
            )
        stmt = (
            stmt.order_by(Questionnaire.created_at.desc())
            .offset(max(0, offset))
            .limit(max(1, min(limit, 200)))
        )
        return list(self.db.scalars(stmt).all())

    def get_questionnaire(self, questionnaire_id: UUID) -> Questionnaire:
        return self._get_questionnaire(questionnaire_id)

    def list_questionnaire_versions(
        self, questionnaire_id: UUID
    ) -> list[QuestionnaireVersion]:
        self._get_questionnaire(questionnaire_id)
        return list(
            self.db.scalars(
                select(QuestionnaireVersion)
                .where(
                    QuestionnaireVersion.organization_id == self.ctx.organization_id,
                    QuestionnaireVersion.questionnaire_id == questionnaire_id,
                )
                .order_by(QuestionnaireVersion.version_number.desc())
            )
        )

    def get_latest_published_version(
        self, questionnaire_id: UUID
    ) -> QuestionnaireVersion | None:
        self._get_questionnaire(questionnaire_id)
        return self.db.scalar(
            select(QuestionnaireVersion)
            .where(
                QuestionnaireVersion.organization_id == self.ctx.organization_id,
                QuestionnaireVersion.questionnaire_id == questionnaire_id,
                QuestionnaireVersion.status == "published",
            )
            .order_by(QuestionnaireVersion.version_number.desc())
            .limit(1)
        )

    def list_answers(
        self,
        *,
        questionnaire_version_id: UUID,
        related_entity_type: str,
        related_entity_id: UUID,
    ) -> list[RequirementAnswer]:
        self._get_version(questionnaire_version_id)
        stmt = select(RequirementAnswer).where(
            RequirementAnswer.organization_id == self.ctx.organization_id,
            RequirementAnswer.questionnaire_version_id == questionnaire_version_id,
            RequirementAnswer.related_entity_type == related_entity_type,
            RequirementAnswer.related_entity_id == related_entity_id,
        )
        ctx_client = self.ctx.tenant.client_id
        if ctx_client is not None:
            stmt = stmt.where(RequirementAnswer.client_id == ctx_client)
        return list(self.db.scalars(stmt.order_by(RequirementAnswer.question_key)).all())

    def create_version(self, data: QuestionnaireVersionCreate) -> QuestionnaireVersion:
        questionnaire = self._get_questionnaire(data.questionnaire_id)
        questions = [q.model_dump() for q in data.questions]
        domain.assert_questions_valid(questions)
        next_version = (
            self.db.scalar(
                select(func.max(QuestionnaireVersion.version_number)).where(
                    QuestionnaireVersion.questionnaire_id == questionnaire.id
                )
            )
            or 0
        ) + 1
        row = QuestionnaireVersion(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            questionnaire_id=questionnaire.id,
            version_number=next_version,
            status="draft",
            questions_json=questions,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="questionnaire_version_create",
            entity_type="req_questionnaire_version",
            entity_id=row.id,
            payload={"version_number": next_version},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def publish_version(self, version_id: UUID) -> QuestionnaireVersion:
        row = self._get_version(version_id)
        domain.assert_can_publish(row.status)
        published = list(
            self.db.scalars(
                select(QuestionnaireVersion).where(
                    QuestionnaireVersion.questionnaire_id == row.questionnaire_id,
                    QuestionnaireVersion.status == "published",
                )
            )
        )
        for prior in published:
            prior.status = "superseded"
            self.uow.add(prior)
        row.status = "published"
        row.published_at = datetime.now(UTC)
        self.uow.add(row)
        self.obs.write_audit(
            action="questionnaire_version_publish",
            entity_type="req_questionnaire_version",
            entity_id=row.id,
            payload={"version_number": row.version_number},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def upsert_answer(self, data: AnswerUpsert) -> RequirementAnswer:
        version = self._get_version(data.questionnaire_version_id)
        domain.assert_version_accepts_answers(version.status)
        domain.assert_answer_value(
            answer_text=data.answer_text,
            explicitly_unavailable=data.explicitly_unavailable,
        )
        question_keys = {str(q["key"]) for q in version.questions_json}
        if data.question_key not in question_keys:
            raise NotFoundError(f"Question key '{data.question_key}' not on version")
        client_id = data.client_id or self.ctx.tenant.client_id
        if self.ctx.tenant.client_id and client_id and client_id != self.ctx.tenant.client_id:
            raise ForbiddenError("Cross-client access denied")
        existing = self.db.scalar(
            select(RequirementAnswer).where(
                RequirementAnswer.questionnaire_version_id == version.id,
                RequirementAnswer.related_entity_type == data.related_entity_type,
                RequirementAnswer.related_entity_id == data.related_entity_id,
                RequirementAnswer.question_key == data.question_key,
            )
        )
        if existing is None:
            row = RequirementAnswer(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                questionnaire_version_id=version.id,
                related_entity_type=data.related_entity_type,
                related_entity_id=data.related_entity_id,
                client_id=client_id,
                project_id=data.project_id or self.ctx.tenant.project_id,
                question_key=data.question_key,
                answer_text=data.answer_text,
                explicitly_unavailable=data.explicitly_unavailable,
                answered_by_actor_id=self.ctx.actor_id,
            )
            self.uow.add(row)
            action = "answer_create"
        else:
            row = existing
            row.answer_text = data.answer_text
            row.explicitly_unavailable = data.explicitly_unavailable
            row.answered_by_actor_id = self.ctx.actor_id
            self.uow.add(row)
            action = "answer_update"
        self.obs.write_audit(
            action=action,
            entity_type="req_answer",
            entity_id=row.id,
            payload={
                "question_key": data.question_key,
                "explicitly_unavailable": data.explicitly_unavailable,
            },
            project_id=row.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def compute_completeness(self, data: CompletenessCompute) -> CompletenessScore:
        version = self._get_version(data.questionnaire_version_id)
        domain.assert_version_accepts_answers(version.status)
        answers = list(
            self.db.scalars(
                select(RequirementAnswer).where(
                    RequirementAnswer.organization_id == self.ctx.organization_id,
                    RequirementAnswer.questionnaire_version_id == version.id,
                    RequirementAnswer.related_entity_type == data.related_entity_type,
                    RequirementAnswer.related_entity_id == data.related_entity_id,
                )
            )
        )
        answers_by_key = {
            a.question_key: (a.answer_text, a.explicitly_unavailable) for a in answers
        }
        result = domain.compute_completeness(version.questions_json, answers_by_key)
        row = CompletenessScore(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            questionnaire_version_id=version.id,
            related_entity_type=data.related_entity_type,
            related_entity_id=data.related_entity_id,
            mandatory_total=result.mandatory_total,
            covered_count=result.covered_count,
            percentage=result.percentage,
            meets_threshold=result.meets_threshold,
            gap_question_keys=result.gap_keys,
            computed_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="completeness_compute",
            entity_type="req_completeness_score",
            entity_id=row.id,
            payload={
                "percentage": str(result.percentage),
                "meets_threshold": result.meets_threshold,
                "gap_count": len(result.gap_keys),
            },
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_clarification(self, data: ClarificationCreate) -> ClarificationRequest:
        version = self._get_version(data.questionnaire_version_id)
        row = ClarificationRequest(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            questionnaire_version_id=version.id,
            related_entity_type=data.related_entity_type,
            related_entity_id=data.related_entity_id,
            question_key=data.question_key,
            question_text=data.question_text,
            owner_actor_id=data.owner_actor_id,
            status="open",
            due_at=data.due_at,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="clarification_create",
            entity_type="req_clarification_request",
            entity_id=row.id,
            payload={"question_key": data.question_key, "owner": str(data.owner_actor_id)},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_brief(self, data: BriefCreate) -> RequirementBrief:
        client_id = data.client_id or self.ctx.tenant.client_id
        if self.ctx.tenant.client_id and client_id and client_id != self.ctx.tenant.client_id:
            raise ForbiddenError("Cross-client access denied")
        next_version = (
            self.db.scalar(
                select(func.max(RequirementBrief.version_number)).where(
                    RequirementBrief.organization_id == self.ctx.organization_id,
                    RequirementBrief.related_entity_type == data.related_entity_type,
                    RequirementBrief.related_entity_id == data.related_entity_id,
                )
            )
            or 0
        ) + 1
        if data.completeness_score_id is not None:
            score = self.db.scalar(
                select(CompletenessScore).where(CompletenessScore.id == data.completeness_score_id)
            )
            if score is None or score.organization_id != self.ctx.organization_id:
                raise NotFoundError("Completeness score not found")
        row = RequirementBrief(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            related_entity_type=data.related_entity_type,
            related_entity_id=data.related_entity_id,
            client_id=client_id,
            project_id=data.project_id or self.ctx.tenant.project_id,
            questionnaire_version_id=data.questionnaire_version_id,
            completeness_score_id=data.completeness_score_id,
            version_number=next_version,
            title=data.title,
            summary=data.summary,
            status="draft",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="brief_create",
            entity_type="req_requirement_brief",
            entity_id=row.id,
            payload={"version_number": next_version, "title": data.title},
            project_id=row.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def approve_brief(self, brief_id: UUID) -> RequirementBrief:
        row = self._get_brief(brief_id)
        domain.assert_can_approve_brief(row.status)
        if row.completeness_score_id is None:
            raise ForbiddenError("Brief requires a completeness score before approval")
        score = self.db.scalar(
            select(CompletenessScore).where(CompletenessScore.id == row.completeness_score_id)
        )
        if score is None:
            raise NotFoundError("Completeness score not found")
        open_keys = {
            c.question_key
            for c in self.db.scalars(
                select(ClarificationRequest).where(
                    ClarificationRequest.organization_id == self.ctx.organization_id,
                    ClarificationRequest.related_entity_type == row.related_entity_type,
                    ClarificationRequest.related_entity_id == row.related_entity_id,
                    ClarificationRequest.status == "open",
                )
            )
        }
        domain.assert_brief_completeness_gate(
            meets_threshold=score.meets_threshold,
            gap_keys=list(score.gap_question_keys or []),
            open_clarification_keys=open_keys,
        )
        prior = list(
            self.db.scalars(
                select(RequirementBrief).where(
                    RequirementBrief.organization_id == self.ctx.organization_id,
                    RequirementBrief.related_entity_type == row.related_entity_type,
                    RequirementBrief.related_entity_id == row.related_entity_id,
                    RequirementBrief.status == "approved",
                    RequirementBrief.id != row.id,
                )
            )
        )
        for old in prior:
            old.status = "superseded"
            self.uow.add(old)
        row.status = "approved"
        row.approved_by_actor_id = self.ctx.actor_id
        row.approved_at = datetime.now(UTC)
        self.uow.add(row)
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="req_requirement_brief",
            aggregate_id=row.id,
            event_type="requirements.brief.approved",
            payload={"version_number": row.version_number},
            correlation_id=self.ctx.correlation_id,
        )
        self.obs.write_audit(
            action="brief_approve",
            entity_type="req_requirement_brief",
            entity_id=row.id,
            payload={"version_number": row.version_number},
            project_id=row.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_briefs(
        self,
        *,
        related_entity_type: str | None = None,
        related_entity_id: UUID | None = None,
        status: str | None = None,
        q: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[RequirementBrief]:
        stmt = select(RequirementBrief).where(
            RequirementBrief.organization_id == self.ctx.organization_id
        )
        ctx_client = self.ctx.tenant.client_id
        if ctx_client is not None:
            stmt = stmt.where(RequirementBrief.client_id == ctx_client)
        if related_entity_type:
            stmt = stmt.where(RequirementBrief.related_entity_type == related_entity_type)
        if related_entity_id is not None:
            stmt = stmt.where(RequirementBrief.related_entity_id == related_entity_id)
        if status:
            stmt = stmt.where(RequirementBrief.status == status)
        if q and q.strip():
            like = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(RequirementBrief.title.ilike(like), RequirementBrief.summary.ilike(like))
            )
        stmt = (
            stmt.order_by(RequirementBrief.created_at.desc())
            .offset(max(0, offset))
            .limit(max(1, min(limit, 200)))
        )
        return list(self.db.scalars(stmt).all())

    def get_brief(self, brief_id: UUID) -> RequirementBrief:
        return self._get_brief(brief_id)

    def _get_questionnaire(self, questionnaire_id: UUID) -> Questionnaire:
        row = self.db.scalar(select(Questionnaire).where(Questionnaire.id == questionnaire_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Questionnaire not found")
        return row

    def _get_version(self, version_id: UUID) -> QuestionnaireVersion:
        row = self.db.scalar(
            select(QuestionnaireVersion).where(QuestionnaireVersion.id == version_id)
        )
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Questionnaire version not found")
        return row

    def _get_brief(self, brief_id: UUID) -> RequirementBrief:
        row = self.db.scalar(select(RequirementBrief).where(RequirementBrief.id == brief_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Requirement brief not found")
        ctx_client = self.ctx.tenant.client_id
        if ctx_client and row.client_id and row.client_id != ctx_client:
            raise ForbiddenError("Cross-client access denied")
        return row
