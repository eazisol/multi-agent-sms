"""Application service for MOD-630 controlled pilot and production sign-off records."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, NotFoundError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.pilot import domain
from masms_api.modules.pilot.models import (
    AcceptanceTest,
    FinalSignoff,
    KnownLimitation,
    PilotPlan,
    PilotUser,
    ProductionDeployment,
    RollbackRecord,
    SupportReadiness,
    TrainingRecord,
)
from masms_api.modules.pilot.schemas import (
    AcceptanceTestCreate,
    AcceptanceTestResultUpdate,
    FinalSignoffCreate,
    FinalSignoffSign,
    KnownLimitationCreate,
    PilotPlanCreate,
    PilotUserCreate,
    ProductionDeploymentCreate,
    RollbackCreate,
    SupportReadinessCreate,
    TrainingRecordCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class PilotService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def _audit(
        self,
        *,
        action: str,
        entity_type: str,
        entity_id: UUID,
        payload: dict[str, Any] | None = None,
    ) -> None:
        self.obs.write_audit(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload,
        )

    def _enqueue(
        self,
        *,
        aggregate_type: str,
        aggregate_id: UUID,
        event_type: str,
        payload: dict[str, Any],
    ) -> None:
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=event_type,
            payload=payload,
            correlation_id=self.ctx.correlation_id,
        )

    def _page(
        self, stmt: Any, *, limit: int, offset: int, order_col: Any
    ) -> tuple[list[Any], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(stmt.order_by(order_col.desc()).limit(limit).offset(offset))
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def get_plan(self, plan_id: UUID) -> PilotPlan:
        row = self.db.get(PilotPlan, plan_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Pilot plan not found")
        return row

    def _plan_users(self, plan_id: UUID) -> list[PilotUser]:
        return list(
            self.db.scalars(
                select(PilotUser).where(
                    PilotUser.organization_id == self.ctx.organization_id,
                    PilotUser.plan_id == plan_id,
                )
            )
        )

    def _plan_tests(self, plan_id: UUID) -> list[AcceptanceTest]:
        return list(
            self.db.scalars(
                select(AcceptanceTest).where(
                    AcceptanceTest.organization_id == self.ctx.organization_id,
                    AcceptanceTest.plan_id == plan_id,
                )
            )
        )

    def _plan_signoffs(self, plan_id: UUID) -> list[FinalSignoff]:
        return list(
            self.db.scalars(
                select(FinalSignoff).where(
                    FinalSignoff.organization_id == self.ctx.organization_id,
                    FinalSignoff.plan_id == plan_id,
                )
            )
        )

    def _seed_signoffs(self, plan: PilotPlan) -> None:
        for function_code in domain.REQUIRED_SIGNOFF_FUNCTIONS:
            row = FinalSignoff(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                plan_id=plan.id,
                function_code=function_code,
                status="pending",
                evidence="",
                signed_by_actor_id=None,
                signed_at=None,
                created_by_actor_id=self.ctx.actor_id,
            )
            self.uow.add(row)

    # --- Plans ---

    def create_plan(self, data: PilotPlanCreate) -> PilotPlan:
        domain.assert_plan_status(data.status)
        code = data.code.strip()
        existing = self.db.scalar(
            select(PilotPlan).where(
                PilotPlan.organization_id == self.ctx.organization_id,
                PilotPlan.code == code,
            )
        )
        if existing is not None:
            raise ConflictError(f"Pilot plan code '{code}' already exists")
        row = PilotPlan(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=code,
            title=data.title.strip(),
            status=data.status,
            start_at=data.start_at,
            end_at=data.end_at,
            version=1,
            owner_actor_id=data.owner_actor_id or self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._seed_signoffs(row)
        self._audit(
            action="pl_pilot_plan_create",
            entity_type="pl_pilot_plan",
            entity_id=row.id,
            payload={"code": row.code, "status": row.status},
        )
        self._enqueue(
            aggregate_type="pl_pilot_plan",
            aggregate_id=row.id,
            event_type="pilot.plan.created",
            payload={"plan_id": str(row.id), "code": row.code},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_plans(self, *, limit: int = 20, offset: int = 0) -> tuple[list[PilotPlan], PageMeta]:
        stmt = select(PilotPlan).where(PilotPlan.organization_id == self.ctx.organization_id)
        return self._page(stmt, limit=limit, offset=offset, order_col=PilotPlan.created_at)

    # --- Users / AC-002 ---

    def add_user(self, plan_id: UUID, data: PilotUserCreate) -> PilotUser:
        self.get_plan(plan_id)
        existing = self.db.scalar(
            select(PilotUser).where(
                PilotUser.organization_id == self.ctx.organization_id,
                PilotUser.plan_id == plan_id,
                PilotUser.actor_id == data.actor_id,
            )
        )
        if existing is not None:
            raise ConflictError("Pilot user already registered for this plan")
        row = PilotUser(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            plan_id=plan_id,
            actor_id=data.actor_id,
            role_label=data.role_label.strip(),
            approved_production_use=False,
            approved_at=None,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="pl_pilot_user_add",
            entity_type="pl_pilot_user",
            entity_id=row.id,
            payload={"plan_id": str(plan_id), "actor_id": str(row.actor_id)},
        )
        self._enqueue(
            aggregate_type="pl_pilot_user",
            aggregate_id=row.id,
            event_type="pilot.user.registered",
            payload={"user_id": str(row.id), "plan_id": str(plan_id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_users(
        self, plan_id: UUID, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[PilotUser], PageMeta]:
        self.get_plan(plan_id)
        stmt = select(PilotUser).where(
            PilotUser.organization_id == self.ctx.organization_id,
            PilotUser.plan_id == plan_id,
        )
        return self._page(stmt, limit=limit, offset=offset, order_col=PilotUser.created_at)

    def get_user(self, plan_id: UUID, user_id: UUID) -> PilotUser:
        row = self.db.get(PilotUser, user_id)
        if (
            row is None
            or row.organization_id != self.ctx.organization_id
            or row.plan_id != plan_id
        ):
            raise NotFoundError("Pilot user not found")
        return row

    def approve_user(self, plan_id: UUID, user_id: UUID) -> PilotUser:
        domain.assert_human_signoff(self.ctx.actor_kind)
        row = self.get_user(plan_id, user_id)
        if not row.approved_production_use:
            row.approved_production_use = True
            row.approved_at = datetime.now(UTC)
            self._audit(
                action="pl_pilot_user_approve",
                entity_type="pl_pilot_user",
                entity_id=row.id,
                payload={"plan_id": str(plan_id), "actor_id": str(row.actor_id)},
            )
            self._enqueue(
                aggregate_type="pl_pilot_user",
                aggregate_id=row.id,
                event_type="pilot.user.approved",
                payload={"user_id": str(row.id), "plan_id": str(plan_id)},
            )
            self.uow.commit()
            self.db.refresh(row)
        return row

    # --- Training ---

    def create_training(self, plan_id: UUID, data: TrainingRecordCreate) -> TrainingRecord:
        self.get_plan(plan_id)
        domain.assert_training_status(data.status)
        completed_at = datetime.now(UTC) if data.status == "completed" else None
        row = TrainingRecord(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            plan_id=plan_id,
            title=data.title.strip(),
            audience=data.audience.strip(),
            status=data.status,
            completed_at=completed_at,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="pl_training_record_create",
            entity_type="pl_training_record",
            entity_id=row.id,
            payload={"plan_id": str(plan_id), "status": row.status},
        )
        self._enqueue(
            aggregate_type="pl_training_record",
            aggregate_id=row.id,
            event_type="pilot.training.recorded",
            payload={"training_id": str(row.id), "plan_id": str(plan_id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_training(
        self, plan_id: UUID, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[TrainingRecord], PageMeta]:
        self.get_plan(plan_id)
        stmt = select(TrainingRecord).where(
            TrainingRecord.organization_id == self.ctx.organization_id,
            TrainingRecord.plan_id == plan_id,
        )
        return self._page(stmt, limit=limit, offset=offset, order_col=TrainingRecord.created_at)

    # --- Support readiness ---

    def create_support(self, plan_id: UUID, data: SupportReadinessCreate) -> SupportReadiness:
        self.get_plan(plan_id)
        row = SupportReadiness(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            plan_id=plan_id,
            checklist_item=data.checklist_item.strip(),
            ready=data.ready,
            notes=data.notes,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="pl_support_readiness_create",
            entity_type="pl_support_readiness",
            entity_id=row.id,
            payload={"plan_id": str(plan_id), "ready": row.ready},
        )
        self._enqueue(
            aggregate_type="pl_support_readiness",
            aggregate_id=row.id,
            event_type="pilot.support.recorded",
            payload={"support_id": str(row.id), "plan_id": str(plan_id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_support(
        self, plan_id: UUID, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[SupportReadiness], PageMeta]:
        self.get_plan(plan_id)
        stmt = select(SupportReadiness).where(
            SupportReadiness.organization_id == self.ctx.organization_id,
            SupportReadiness.plan_id == plan_id,
        )
        return self._page(stmt, limit=limit, offset=offset, order_col=SupportReadiness.created_at)

    # --- Known limitations ---

    def create_limitation(self, plan_id: UUID, data: KnownLimitationCreate) -> KnownLimitation:
        self.get_plan(plan_id)
        domain.assert_limitation_severity(data.severity)
        domain.assert_limitation_status(data.status)
        code = data.code.strip()
        existing = self.db.scalar(
            select(KnownLimitation).where(
                KnownLimitation.organization_id == self.ctx.organization_id,
                KnownLimitation.plan_id == plan_id,
                KnownLimitation.code == code,
            )
        )
        if existing is not None:
            raise ConflictError(f"Known limitation code '{code}' already exists for this plan")
        row = KnownLimitation(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            plan_id=plan_id,
            code=code,
            summary=data.summary.strip(),
            severity=data.severity,
            status=data.status,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="pl_known_limitation_create",
            entity_type="pl_known_limitation",
            entity_id=row.id,
            payload={"plan_id": str(plan_id), "code": row.code, "severity": row.severity},
        )
        self._enqueue(
            aggregate_type="pl_known_limitation",
            aggregate_id=row.id,
            event_type="pilot.limitation.recorded",
            payload={"limitation_id": str(row.id), "code": row.code},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_limitations(
        self, plan_id: UUID, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[KnownLimitation], PageMeta]:
        self.get_plan(plan_id)
        stmt = select(KnownLimitation).where(
            KnownLimitation.organization_id == self.ctx.organization_id,
            KnownLimitation.plan_id == plan_id,
        )
        return self._page(stmt, limit=limit, offset=offset, order_col=KnownLimitation.created_at)

    # --- Acceptance tests / AC-001 ---

    def create_acceptance_test(self, plan_id: UUID, data: AcceptanceTestCreate) -> AcceptanceTest:
        self.get_plan(plan_id)
        domain.assert_acceptance_severity(data.severity)
        domain.assert_acceptance_result(data.result)
        code = data.code.strip()
        existing = self.db.scalar(
            select(AcceptanceTest).where(
                AcceptanceTest.organization_id == self.ctx.organization_id,
                AcceptanceTest.plan_id == plan_id,
                AcceptanceTest.code == code,
            )
        )
        if existing is not None:
            raise ConflictError(f"Acceptance test code '{code}' already exists for this plan")
        row = AcceptanceTest(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            plan_id=plan_id,
            code=code,
            title=data.title.strip(),
            severity=data.severity,
            result=data.result,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="pl_acceptance_test_create",
            entity_type="pl_acceptance_test",
            entity_id=row.id,
            payload={"plan_id": str(plan_id), "code": row.code, "result": row.result},
        )
        self._enqueue(
            aggregate_type="pl_acceptance_test",
            aggregate_id=row.id,
            event_type="pilot.acceptance_test.recorded",
            payload={"test_id": str(row.id), "result": row.result},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_acceptance_tests(
        self, plan_id: UUID, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[AcceptanceTest], PageMeta]:
        self.get_plan(plan_id)
        stmt = select(AcceptanceTest).where(
            AcceptanceTest.organization_id == self.ctx.organization_id,
            AcceptanceTest.plan_id == plan_id,
        )
        return self._page(stmt, limit=limit, offset=offset, order_col=AcceptanceTest.created_at)

    def get_acceptance_test(self, plan_id: UUID, test_id: UUID) -> AcceptanceTest:
        row = self.db.get(AcceptanceTest, test_id)
        if (
            row is None
            or row.organization_id != self.ctx.organization_id
            or row.plan_id != plan_id
        ):
            raise NotFoundError("Acceptance test not found")
        return row

    def update_acceptance_result(
        self, plan_id: UUID, test_id: UUID, data: AcceptanceTestResultUpdate
    ) -> AcceptanceTest:
        domain.assert_acceptance_result(data.result)
        row = self.get_acceptance_test(plan_id, test_id)
        row.result = data.result
        self._audit(
            action="pl_acceptance_test_result",
            entity_type="pl_acceptance_test",
            entity_id=row.id,
            payload={"plan_id": str(plan_id), "code": row.code, "result": row.result},
        )
        self._enqueue(
            aggregate_type="pl_acceptance_test",
            aggregate_id=row.id,
            event_type="pilot.acceptance_test.updated",
            payload={"test_id": str(row.id), "result": row.result},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    # --- Sign-offs / AC-003 ---

    def create_signoff(self, data: FinalSignoffCreate) -> FinalSignoff:
        self.get_plan(data.plan_id)
        domain.assert_signoff_function(data.function_code)
        existing = self.db.scalar(
            select(FinalSignoff).where(
                FinalSignoff.organization_id == self.ctx.organization_id,
                FinalSignoff.plan_id == data.plan_id,
                FinalSignoff.function_code == data.function_code,
            )
        )
        if existing is not None:
            raise ConflictError(
                f"Sign-off for function '{data.function_code}' already exists for this plan"
            )
        row = FinalSignoff(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            plan_id=data.plan_id,
            function_code=data.function_code,
            status="pending",
            evidence=data.evidence,
            signed_by_actor_id=None,
            signed_at=None,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="pl_final_signoff_create",
            entity_type="pl_final_signoff",
            entity_id=row.id,
            payload={"plan_id": str(data.plan_id), "function_code": row.function_code},
        )
        self._enqueue(
            aggregate_type="pl_final_signoff",
            aggregate_id=row.id,
            event_type="pilot.signoff.created",
            payload={"signoff_id": str(row.id), "function_code": row.function_code},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_signoffs(
        self, *, plan_id: UUID | None = None, limit: int = 20, offset: int = 0
    ) -> tuple[list[FinalSignoff], PageMeta]:
        stmt = select(FinalSignoff).where(
            FinalSignoff.organization_id == self.ctx.organization_id
        )
        if plan_id is not None:
            self.get_plan(plan_id)
            stmt = stmt.where(FinalSignoff.plan_id == plan_id)
        return self._page(stmt, limit=limit, offset=offset, order_col=FinalSignoff.created_at)

    def get_signoff(self, signoff_id: UUID) -> FinalSignoff:
        row = self.db.get(FinalSignoff, signoff_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Final sign-off not found")
        return row

    def sign_off(self, signoff_id: UUID, data: FinalSignoffSign) -> FinalSignoff:
        domain.assert_human_signoff(self.ctx.actor_kind)
        row = self.get_signoff(signoff_id)
        domain.assert_signoff_pending(row.status)
        row.status = "signed"
        row.evidence = data.evidence.strip()
        row.signed_by_actor_id = self.ctx.actor_id
        row.signed_at = datetime.now(UTC)
        self._audit(
            action="pl_final_signoff_sign",
            entity_type="pl_final_signoff",
            entity_id=row.id,
            payload={"function_code": row.function_code, "plan_id": str(row.plan_id)},
        )
        self._enqueue(
            aggregate_type="pl_final_signoff",
            aggregate_id=row.id,
            event_type="pilot.signoff.signed",
            payload={"signoff_id": str(row.id), "function_code": row.function_code},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    # --- Gates ---

    def acceptance_gate(self, plan_id: UUID) -> dict[str, Any]:
        self.get_plan(plan_id)
        tests = self._plan_tests(plan_id)
        failed = domain.critical_high_failed_count(tests)
        return {
            "plan_id": plan_id,
            "critical_high_failed_count": failed,
            "gate_passed": domain.acceptance_gate_passed(tests),
        }

    def pilot_approval_gate(self, plan_id: UUID) -> dict[str, Any]:
        self.get_plan(plan_id)
        users = self._plan_users(plan_id)
        registered, approved, pending = domain.pilot_approval_counts(users)
        return {
            "plan_id": plan_id,
            "registered_count": registered,
            "approved_count": approved,
            "pending_count": pending,
            "gate_passed": domain.pilot_approval_gate(users),
        }

    def readiness_gate(self, plan_id: UUID) -> dict[str, Any]:
        self.get_plan(plan_id)
        signoffs = self._plan_signoffs(plan_id)
        signed = sorted(domain.readiness_signed_functions(signoffs))
        return {
            "plan_id": plan_id,
            "required_functions": list(domain.REQUIRED_SIGNOFF_FUNCTIONS),
            "signed_functions": signed,
            "gate_passed": domain.readiness_gate(signoffs),
        }

    def _all_gates_passed(self, plan_id: UUID) -> bool:
        return bool(
            self.acceptance_gate(plan_id)["gate_passed"]
            and self.pilot_approval_gate(plan_id)["gate_passed"]
            and self.readiness_gate(plan_id)["gate_passed"]
        )

    # --- Deployments (records only; agents must not deploy) ---

    def record_deployment(self, data: ProductionDeploymentCreate) -> ProductionDeployment:
        domain.assert_human_signoff(self.ctx.actor_kind)
        self.get_plan(data.plan_id)
        domain.assert_deployment_environment(data.environment)
        domain.assert_production_may_record(
            gates_ok=self._all_gates_passed(data.plan_id),
            evidence=data.human_approval_evidence,
        )
        row = ProductionDeployment(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            plan_id=data.plan_id,
            environment=data.environment,
            status="recorded",
            human_approval_evidence=data.human_approval_evidence.strip(),
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="pl_production_deployment_record",
            entity_type="pl_production_deployment",
            entity_id=row.id,
            payload={"plan_id": str(data.plan_id), "status": row.status},
        )
        self._enqueue(
            aggregate_type="pl_production_deployment",
            aggregate_id=row.id,
            event_type="pilot.deployment.recorded",
            payload={"deployment_id": str(row.id), "plan_id": str(data.plan_id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_deployments(
        self, *, plan_id: UUID | None = None, limit: int = 20, offset: int = 0
    ) -> tuple[list[ProductionDeployment], PageMeta]:
        stmt = select(ProductionDeployment).where(
            ProductionDeployment.organization_id == self.ctx.organization_id
        )
        if plan_id is not None:
            self.get_plan(plan_id)
            stmt = stmt.where(ProductionDeployment.plan_id == plan_id)
        return self._page(
            stmt, limit=limit, offset=offset, order_col=ProductionDeployment.created_at
        )

    def get_deployment(self, deployment_id: UUID) -> ProductionDeployment:
        row = self.db.get(ProductionDeployment, deployment_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Production deployment record not found")
        return row

    def record_rollback(self, deployment_id: UUID, data: RollbackCreate) -> RollbackRecord:
        deployment = self.get_deployment(deployment_id)
        row = RollbackRecord(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            deployment_id=deployment.id,
            reason=data.reason.strip(),
            status="recorded",
            created_by_actor_id=self.ctx.actor_id,
        )
        deployment.status = "rolled_back"
        self.uow.add(row)
        self._audit(
            action="pl_rollback_record",
            entity_type="pl_rollback",
            entity_id=row.id,
            payload={"deployment_id": str(deployment_id)},
        )
        self._enqueue(
            aggregate_type="pl_rollback",
            aggregate_id=row.id,
            event_type="pilot.rollback.recorded",
            payload={"rollback_id": str(row.id), "deployment_id": str(deployment_id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row
