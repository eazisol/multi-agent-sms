"""Queries application service (MOD-210)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, ForbiddenError, NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.queries import domain
from masms_api.modules.queries.models import (
    ClientQuery,
    Opportunity,
    QualificationAnswer,
    QuerySource,
    QueryStatusHistory,
)
from masms_api.modules.queries.schemas import (
    ClientQueryCreate,
    ConvertQueryRequest,
    FirstResponseRequest,
    QualificationAnswerCreate,
    QuerySourceCreate,
    QueryTransitionRequest,
)
from masms_api.observability.writer import ObservabilityWriter


class QueriesService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_source(self, data: QuerySourceCreate) -> QuerySource:
        if self.db.scalar(
            select(QuerySource).where(
                QuerySource.organization_id == self.ctx.organization_id,
                QuerySource.code == data.code,
            )
        ):
            raise ConflictError(f"Query source '{data.code}' already exists")
        row = QuerySource(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code,
            title=data.title,
            channel=data.channel,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_query(self, data: ClientQueryCreate) -> ClientQuery:
        ctx_client = self.ctx.tenant.client_id
        if ctx_client and data.client_id and data.client_id != ctx_client:
            raise ForbiddenError("Cross-client access denied")
        now = datetime.now(UTC)
        row = ClientQuery(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            client_id=data.client_id or self.ctx.tenant.client_id,
            contact_id=data.contact_id,
            source_id=data.source_id,
            subject=data.subject,
            summary=data.summary,
            original_message=data.original_message,
            status="received",
            owner_actor_id=data.owner_actor_id or self.ctx.actor_id,
            sla_due_at=domain.compute_sla_due(received_at=now, hours=data.sla_hours),
            sla_status="pending",
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._record_history(
            query_id=row.id,
            previous="none",
            next_status="received",
            reason="inquiry captured",
            rule_code="create",
        )
        self.obs.write_audit(
            action="query_create",
            entity_type="crm_query",
            entity_id=row.id,
            payload={"subject": data.subject, "status": "received"},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="crm_query",
            aggregate_id=row.id,
            event_type="queries.query.created",
            payload={"subject": data.subject},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def transition(self, query_id: UUID, data: QueryTransitionRequest) -> ClientQuery:
        row = self._get_query(query_id)
        domain.assert_transition(row.status, data.next_status)
        if data.next_status == "rejected" and not data.reason:
            raise ValidationAppError("Rejection requires a reason")
        if data.next_status == "classified" and not data.classification:
            raise ValidationAppError("Classification transition requires classification")
        previous = row.status
        row.status = data.next_status
        if data.classification:
            row.classification = data.classification
        if data.next_status == "rejected":
            row.rejection_reason = data.reason
        row.updated_by_actor_id = self.ctx.actor_id
        row.version += 1
        self.uow.add(row)
        self._record_history(
            query_id=row.id,
            previous=previous,
            next_status=data.next_status,
            reason=data.reason,
            rule_code=data.rule_code,
        )
        self.obs.write_audit(
            action="query_transition",
            entity_type="crm_query",
            entity_id=row.id,
            entity_version=row.version,
            payload={"from": previous, "to": data.next_status},
            reason=data.reason,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def record_first_response(
        self, query_id: UUID, data: FirstResponseRequest
    ) -> ClientQuery:
        row = self._get_query(query_id)
        responded = data.responded_at or datetime.now(UTC)
        if responded.tzinfo is None:
            responded = responded.replace(tzinfo=UTC)
        row.first_responded_at = responded
        row.sla_status = domain.evaluate_sla(
            due_at=row.sla_due_at, responded_at=responded
        )
        row.updated_by_actor_id = self.ctx.actor_id
        row.version += 1
        self.uow.add(row)
        self.obs.write_audit(
            action="query_first_response",
            entity_type="crm_query",
            entity_id=row.id,
            payload={"sla_status": row.sla_status, "note": data.note},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def add_qualification(self, data: QualificationAnswerCreate) -> QualificationAnswer:
        query = self._get_query(data.query_id)
        if query.status not in {"qualifying", "classified", "qualified"}:
            raise ValidationAppError("Qualification answers require qualifying/classified state")
        existing = self.db.scalar(
            select(QualificationAnswer).where(
                QualificationAnswer.query_id == query.id,
                QualificationAnswer.question_key == data.question_key,
            )
        )
        if existing is not None:
            raise ConflictError("Qualification answer already exists for this question")
        row = QualificationAnswer(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            query_id=query.id,
            question_key=data.question_key,
            question_text=data.question_text,
            answer_text=data.answer_text,
            rationale=data.rationale,
            answered_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="qualification_answer_create",
            entity_type="crm_qualification_answer",
            entity_id=row.id,
            payload={"question_key": data.question_key, "query_id": str(query.id)},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def convert_to_opportunity(
        self, query_id: UUID, data: ConvertQueryRequest
    ) -> Opportunity:
        query = self._get_query(query_id)
        domain.assert_transition(query.status, "converted")
        answers = list(
            self.db.scalars(
                select(QualificationAnswer).where(
                    QualificationAnswer.query_id == query.id
                )
            )
        )
        opportunity = Opportunity(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            query_id=query.id,
            client_id=query.client_id,
            title=data.title,
            status="open",
            estimated_value=data.estimated_value,
            currency=data.currency,
            owner_actor_id=query.owner_actor_id,
            conversion_notes=data.conversion_notes,
            version=1,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(opportunity)
        self.uow.flush()
        previous = query.status
        query.status = "converted"
        query.opportunity_id = opportunity.id
        query.updated_by_actor_id = self.ctx.actor_id
        query.version += 1
        self.uow.add(query)
        self._record_history(
            query_id=query.id,
            previous=previous,
            next_status="converted",
            reason=data.conversion_notes or "converted to opportunity",
            rule_code="convert",
            evidence={
                "opportunity_id": str(opportunity.id),
                "qualification_answer_ids": [str(a.id) for a in answers],
                "original_message_preserved": bool(query.original_message),
            },
        )
        self.obs.write_audit(
            action="query_convert",
            entity_type="crm_opportunity",
            entity_id=opportunity.id,
            payload={
                "query_id": str(query.id),
                "qualification_count": len(answers),
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="crm_opportunity",
            aggregate_id=opportunity.id,
            event_type="queries.opportunity.created",
            payload={"query_id": str(query.id)},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(opportunity)
        return opportunity

    def list_queries(
        self,
        *,
        status: str | None = None,
        sla_status: str | None = None,
        q: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[ClientQuery], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [ClientQuery.organization_id == self.ctx.organization_id]
        ctx_client = self.ctx.tenant.client_id
        if ctx_client is not None:
            filters.append(ClientQuery.client_id == ctx_client)
        if status:
            filters.append(ClientQuery.status == status)
        if sla_status:
            filters.append(ClientQuery.sla_status == sla_status)
        if q and q.strip():
            like = f"%{q.strip()}%"
            filters.append(
                or_(ClientQuery.subject.ilike(like), ClientQuery.summary.ilike(like))
            )
        total = (
            self.db.scalar(select(func.count()).select_from(ClientQuery).where(*filters))
            or 0
        )
        rows = list(
            self.db.scalars(
                select(ClientQuery)
                .where(*filters)
                .order_by(ClientQuery.created_at.desc())
                .offset(offset)
                .limit(limit)
            )
        )
        return rows, build_page_meta(limit=limit, offset=offset, total=int(total))

    def get_query(self, query_id: UUID) -> ClientQuery:
        return self._get_query(query_id)

    def list_history(self, query_id: UUID) -> list[QueryStatusHistory]:
        self._get_query(query_id)
        rows = self.db.scalars(
            select(QueryStatusHistory)
            .where(
                QueryStatusHistory.organization_id == self.ctx.organization_id,
                QueryStatusHistory.query_id == query_id,
            )
            .order_by(QueryStatusHistory.created_at)
        )
        return list(rows)

    def list_qualification(self, query_id: UUID) -> list[QualificationAnswer]:
        self._get_query(query_id)
        rows = self.db.scalars(
            select(QualificationAnswer).where(
                QualificationAnswer.organization_id == self.ctx.organization_id,
                QualificationAnswer.query_id == query_id,
            )
        )
        return list(rows)

    def _get_query(self, query_id: UUID) -> ClientQuery:
        row = self.db.scalar(select(ClientQuery).where(ClientQuery.id == query_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Query not found")
        ctx_client = self.ctx.tenant.client_id
        if ctx_client and row.client_id and row.client_id != ctx_client:
            raise ForbiddenError("Cross-client access denied")
        return row

    def _record_history(
        self,
        *,
        query_id: UUID,
        previous: str,
        next_status: str,
        reason: str | None,
        rule_code: str | None,
        evidence: dict[str, Any] | None = None,
    ) -> None:
        self.uow.add(
            QueryStatusHistory(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                query_id=query_id,
                previous_status=previous,
                next_status=next_status,
                actor_id=self.ctx.actor_id,
                reason=reason,
                rule_code=rule_code,
                evidence_json=evidence or {},
            )
        )
