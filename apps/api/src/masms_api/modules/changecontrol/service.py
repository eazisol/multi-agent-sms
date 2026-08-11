"""Change-control application service (MOD-420)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.changecontrol import domain
from masms_api.modules.changecontrol.models import (
    BaselineUpdate,
    ChangeApproval,
    ChangeRequest,
    ImpactAnalysis,
    Risk,
    RiskReview,
)
from masms_api.modules.changecontrol.schemas import (
    ApprovalCreate,
    BaselineUpdateCreate,
    ChangeRequestCreate,
    DevelopmentGateResult,
    ImpactCreate,
    RiskCreate,
    RiskReviewCreate,
    SubmitForApproval,
)
from masms_api.observability.writer import ObservabilityWriter


class ChangeControlService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    # --- Risks ---

    def create_risk(self, data: RiskCreate) -> Risk:
        domain.assert_risk_level(data.risk_level)
        existing = self.db.scalar(
            select(Risk).where(
                Risk.organization_id == self.ctx.organization_id,
                Risk.code == data.code,
            )
        )
        if existing is not None:
            raise ConflictError(f"Risk code '{data.code}' already exists")
        row = Risk(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            code=data.code.strip(),
            title=data.title.strip(),
            description=data.description,
            risk_level=data.risk_level,
            status="open",
            owner_actor_id=self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="cc_risk_create",
            entity_type="cc_risk",
            entity_id=row.id,
            payload={"code": row.code, "risk_level": row.risk_level},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="cc_risk",
            aggregate_id=row.id,
            event_type="changecontrol.risk.created",
            payload={"risk_id": str(row.id), "code": row.code},
            correlation_id=self.ctx.correlation_id,
            project_id=data.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def get_risk(self, risk_id: UUID) -> Risk:
        row = self.db.get(Risk, risk_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Risk not found")
        return row

    def list_risks(
        self,
        *,
        status: str | None = None,
        project_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Risk], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(Risk).where(Risk.organization_id == self.ctx.organization_id)
        if status:
            stmt = stmt.where(Risk.status == status)
        if project_id is not None:
            stmt = stmt.where(Risk.project_id == project_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(stmt.order_by(Risk.updated_at.desc()).limit(limit).offset(offset))
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def review_risk(self, risk_id: UUID, data: RiskReviewCreate) -> RiskReview:
        risk = self.get_risk(risk_id)
        domain.assert_expected_version(current=risk.version, expected=data.expected_version)
        if data.outcome not in {"mitigating", "accepted", "closed", "open"}:
            raise ValidationAppError(f"Invalid risk review outcome '{data.outcome}'")
        risk.status = data.outcome
        risk.version += 1
        risk.updated_by_actor_id = self.ctx.actor_id
        risk.updated_at = datetime.now(UTC)
        row = RiskReview(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            risk_id=risk_id,
            outcome=data.outcome,
            notes=data.notes,
            reviewed_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="cc_risk_review",
            entity_type="cc_risk",
            entity_id=risk_id,
            payload={"outcome": data.outcome},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_risk_reviews(self, risk_id: UUID) -> list[RiskReview]:
        self.get_risk(risk_id)
        return list(
            self.db.scalars(
                select(RiskReview)
                .where(
                    RiskReview.organization_id == self.ctx.organization_id,
                    RiskReview.risk_id == risk_id,
                )
                .order_by(RiskReview.created_at.desc())
            )
        )

    # --- Change requests ---

    def create_change_request(self, data: ChangeRequestCreate) -> ChangeRequest:
        existing = self.db.scalar(
            select(ChangeRequest).where(
                ChangeRequest.organization_id == self.ctx.organization_id,
                ChangeRequest.code == data.code,
            )
        )
        if existing is not None:
            raise ConflictError(f"Change request code '{data.code}' already exists")
        row = ChangeRequest(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            code=data.code.strip(),
            title=data.title.strip(),
            description=data.description,
            change_type=data.change_type,
            status="draft",
            rationale=data.rationale,
            owner_actor_id=self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="cc_cr_create",
            entity_type="cc_change_request",
            entity_id=row.id,
            payload={"code": row.code, "change_type": row.change_type},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="cc_change_request",
            aggregate_id=row.id,
            event_type="changecontrol.cr.created",
            payload={"change_request_id": str(row.id), "code": row.code},
            correlation_id=self.ctx.correlation_id,
            project_id=data.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def get_change_request(self, cr_id: UUID) -> ChangeRequest:
        row = self.db.get(ChangeRequest, cr_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Change request not found")
        return row

    def list_change_requests(
        self,
        *,
        status: str | None = None,
        project_id: UUID | None = None,
        q: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[ChangeRequest], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(ChangeRequest).where(
            ChangeRequest.organization_id == self.ctx.organization_id
        )
        if status:
            stmt = stmt.where(ChangeRequest.status == status)
        if project_id is not None:
            stmt = stmt.where(ChangeRequest.project_id == project_id)
        if q:
            like = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(ChangeRequest.code.ilike(like), ChangeRequest.title.ilike(like))
            )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(ChangeRequest.updated_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def add_impact(self, cr_id: UUID, data: ImpactCreate) -> ImpactAnalysis:
        cr = self.get_change_request(cr_id)
        domain.assert_expected_version(current=cr.version, expected=data.expected_version)
        if cr.status not in {"draft", "impact_ready"}:
            raise ValidationAppError(f"Cannot attach impact in status {cr.status}")
        row = ImpactAnalysis(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            change_request_id=cr_id,
            summary=data.summary,
            affected_areas=list(data.affected_areas),
            estimated_effort_hours=data.estimated_effort_hours,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        if cr.status == "draft":
            domain.assert_cr_transition(from_status="draft", to_status="impact_ready")
            cr.status = "impact_ready"
            cr.version += 1
            cr.updated_by_actor_id = self.ctx.actor_id
            cr.updated_at = datetime.now(UTC)
        self.obs.write_audit(
            action="cc_impact_create",
            entity_type="cc_change_request",
            entity_id=cr_id,
            payload={"impact_id": str(row.id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_impacts(self, cr_id: UUID) -> list[ImpactAnalysis]:
        self.get_change_request(cr_id)
        return list(
            self.db.scalars(
                select(ImpactAnalysis).where(
                    ImpactAnalysis.organization_id == self.ctx.organization_id,
                    ImpactAnalysis.change_request_id == cr_id,
                )
            )
        )

    def submit_for_approval(self, cr_id: UUID, data: SubmitForApproval) -> ChangeRequest:
        cr = self.get_change_request(cr_id)
        domain.assert_expected_version(current=cr.version, expected=data.expected_version)
        impacts = self.list_impacts(cr_id)
        if not impacts:
            raise ValidationAppError("Impact analysis is required before submission")
        domain.assert_cr_transition(from_status=cr.status, to_status="pending_approval")
        cr.status = "pending_approval"
        cr.version += 1
        cr.updated_by_actor_id = self.ctx.actor_id
        cr.updated_at = datetime.now(UTC)
        self.obs.write_audit(
            action="cc_cr_submit",
            entity_type="cc_change_request",
            entity_id=cr_id,
            payload={"status": cr.status},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="cc_change_request",
            aggregate_id=cr_id,
            event_type="changecontrol.cr.submitted",
            payload={"change_request_id": str(cr_id)},
            correlation_id=self.ctx.correlation_id,
            project_id=cr.project_id,
        )
        self.uow.commit()
        self.db.refresh(cr)
        return cr

    def decide(self, cr_id: UUID, data: ApprovalCreate) -> ChangeApproval:
        cr = self.get_change_request(cr_id)
        domain.assert_expected_version(current=cr.version, expected=data.expected_version)
        domain.assert_approval_decision(data.decision)
        domain.assert_cr_transition(from_status=cr.status, to_status=data.decision)
        # AC-003: rejected/deferred preserve rationale + evidence
        cr.status = data.decision
        cr.rationale = data.rationale
        cr.decision_evidence = data.evidence
        cr.version += 1
        cr.updated_by_actor_id = self.ctx.actor_id
        cr.updated_at = datetime.now(UTC)
        row = ChangeApproval(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            change_request_id=cr_id,
            decision=data.decision,
            rationale=data.rationale,
            evidence=data.evidence,
            decided_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="cc_cr_decide",
            entity_type="cc_change_request",
            entity_id=cr_id,
            payload={"decision": data.decision},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="cc_change_request",
            aggregate_id=cr_id,
            event_type=f"changecontrol.cr.{data.decision}",
            payload={"change_request_id": str(cr_id), "decision": data.decision},
            correlation_id=self.ctx.correlation_id,
            project_id=cr.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_approvals(self, cr_id: UUID) -> list[ChangeApproval]:
        self.get_change_request(cr_id)
        return list(
            self.db.scalars(
                select(ChangeApproval)
                .where(
                    ChangeApproval.organization_id == self.ctx.organization_id,
                    ChangeApproval.change_request_id == cr_id,
                )
                .order_by(ChangeApproval.created_at.desc())
            )
        )

    def apply_baseline_update(
        self, cr_id: UUID, data: BaselineUpdateCreate
    ) -> BaselineUpdate:
        cr = self.get_change_request(cr_id)
        # AC-001 + AC-002: only approved CRs may update baselines / tickets
        domain.assert_may_enter_development(cr.status)
        domain.assert_artifact_type(data.artifact_type)
        row = BaselineUpdate(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            change_request_id=cr_id,
            artifact_type=data.artifact_type,
            artifact_id=data.artifact_id,
            from_version=data.from_version,
            to_version=data.to_version,
            ticket_id=data.ticket_id,
            notes=data.notes,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="cc_baseline_update",
            entity_type="cc_change_request",
            entity_id=cr_id,
            payload={
                "artifact_type": data.artifact_type,
                "artifact_id": str(data.artifact_id),
                "to_version": data.to_version,
                "ticket_id": str(data.ticket_id) if data.ticket_id else None,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="cc_change_request",
            aggregate_id=cr_id,
            event_type="changecontrol.baseline.updated",
            payload={
                "change_request_id": str(cr_id),
                "baseline_update_id": str(row.id),
                "to_version": data.to_version,
            },
            correlation_id=self.ctx.correlation_id,
            project_id=cr.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_baseline_updates(self, cr_id: UUID) -> list[BaselineUpdate]:
        self.get_change_request(cr_id)
        return list(
            self.db.scalars(
                select(BaselineUpdate).where(
                    BaselineUpdate.organization_id == self.ctx.organization_id,
                    BaselineUpdate.change_request_id == cr_id,
                )
            )
        )

    def development_gate(self, cr_id: UUID) -> DevelopmentGateResult:
        cr = self.get_change_request(cr_id)
        allowed = cr.status in domain.DEVELOPMENT_GATE_STATUSES
        return DevelopmentGateResult(
            change_request_id=cr.id,
            status=cr.status,
            allowed=allowed,
            reason=(
                "Approved — development and baseline updates allowed"
                if allowed
                else "Change request is not approved; out-of-scope work cannot enter development"
            ),
        )
