"""Application service for MOD-610 reliability."""

from __future__ import annotations

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
from masms_api.modules.reliability import domain
from masms_api.modules.reliability.models import (
    DrRunbook,
    IndexReview,
    IntegrationFailureTest,
    PerformanceTest,
    ResilienceTest,
    SloDashboard,
    WorkflowReplay,
)
from masms_api.modules.reliability.schemas import (
    DrRunbookApprove,
    DrRunbookCreate,
    IndexReviewCreate,
    IntegrationFailureTestCreate,
    PerformanceTestCreate,
    ResilienceTestCreate,
    SloDashboardUpsert,
    WorkflowReplayAction,
    WorkflowReplayCreate,
    WorkflowReplayFail,
)
from masms_api.observability.writer import ObservabilityWriter


class ReliabilityService:
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

    # --- Performance tests / API SLO (AC-001) ---

    def create_performance_test(self, data: PerformanceTestCreate) -> PerformanceTest:
        existing = self.db.scalar(
            select(PerformanceTest).where(
                PerformanceTest.organization_id == self.ctx.organization_id,
                PerformanceTest.code == data.code.strip(),
            )
        )
        if existing is not None:
            raise ConflictError(f"Performance test code '{data.code}' already exists")
        samples = domain.samples_as_list(data.samples)
        p95_ms, computed_count = domain.resolve_p95_ms(p95_ms=data.p95_ms, samples=samples)
        sample_count = data.sample_count if data.sample_count is not None else computed_count
        if samples is not None:
            sample_count = len(samples)
        status = domain.performance_status_for_p95(p95_ms, data.status)
        row = PerformanceTest(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code.strip(),
            suite_name=data.suite_name.strip(),
            p95_ms=p95_ms,
            sample_count=sample_count,
            samples_json=samples,
            status=status,
            notes=data.notes,
            version=1,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="rlb_performance_test_create",
            entity_type="rlb_performance_test",
            entity_id=row.id,
            payload={"code": row.code, "p95_ms": row.p95_ms, "status": row.status},
        )
        self._enqueue(
            aggregate_type="rlb_performance_test",
            aggregate_id=row.id,
            event_type="reliability.performance_test.recorded",
            payload={"performance_test_id": str(row.id), "p95_ms": row.p95_ms},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_performance_tests(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[PerformanceTest], PageMeta]:
        stmt = select(PerformanceTest).where(
            PerformanceTest.organization_id == self.ctx.organization_id
        )
        return self._page(stmt, limit=limit, offset=offset, order_col=PerformanceTest.created_at)

    def _latest_performance_test(self) -> PerformanceTest | None:
        return self.db.scalar(
            select(PerformanceTest)
            .where(PerformanceTest.organization_id == self.ctx.organization_id)
            .order_by(PerformanceTest.created_at.desc())
            .limit(1)
        )

    def api_slo(self) -> dict[str, Any]:
        row = self._latest_performance_test()
        if row is None:
            return {
                "performance_test_id": None,
                "p95_ms": None,
                "sample_count": 0,
                "budget_ms": domain.API_P95_BUDGET_MS,
                "slo_met": False,
            }
        samples = domain.samples_as_list(row.samples_json)
        if samples:
            p95_ms = domain.compute_p95_ms(samples)
        else:
            p95_ms = row.p95_ms
        return {
            "performance_test_id": row.id,
            "p95_ms": p95_ms,
            "sample_count": row.sample_count,
            "budget_ms": domain.API_P95_BUDGET_MS,
            "slo_met": domain.api_slo_met(p95_ms),
        }

    # --- Resilience tests ---

    def create_resilience_test(self, data: ResilienceTestCreate) -> ResilienceTest:
        domain.assert_resilience_result(data.result)
        existing = self.db.scalar(
            select(ResilienceTest).where(
                ResilienceTest.organization_id == self.ctx.organization_id,
                ResilienceTest.code == data.code.strip(),
            )
        )
        if existing is not None:
            raise ConflictError(f"Resilience test code '{data.code}' already exists")
        row = ResilienceTest(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code.strip(),
            scenario=data.scenario.strip(),
            result=data.result,
            evidence=data.evidence,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="rlb_resilience_test_create",
            entity_type="rlb_resilience_test",
            entity_id=row.id,
            payload={"code": row.code, "result": row.result},
        )
        self._enqueue(
            aggregate_type="rlb_resilience_test",
            aggregate_id=row.id,
            event_type="reliability.resilience_test.recorded",
            payload={"resilience_test_id": str(row.id), "result": row.result},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_resilience_tests(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[ResilienceTest], PageMeta]:
        stmt = select(ResilienceTest).where(
            ResilienceTest.organization_id == self.ctx.organization_id
        )
        return self._page(stmt, limit=limit, offset=offset, order_col=ResilienceTest.created_at)

    # --- Index reviews ---

    def create_index_review(self, data: IndexReviewCreate) -> IndexReview:
        domain.assert_index_recommendation(data.recommendation)
        domain.assert_index_review_status(data.status)
        row = IndexReview(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            table_name=data.table_name.strip(),
            index_name=data.index_name.strip(),
            recommendation=data.recommendation,
            status=data.status,
            notes=data.notes,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="rlb_index_review_create",
            entity_type="rlb_index_review",
            entity_id=row.id,
            payload={
                "table_name": row.table_name,
                "index_name": row.index_name,
                "recommendation": row.recommendation,
            },
        )
        self._enqueue(
            aggregate_type="rlb_index_review",
            aggregate_id=row.id,
            event_type="reliability.index_review.created",
            payload={"index_review_id": str(row.id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_index_reviews(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[IndexReview], PageMeta]:
        stmt = select(IndexReview).where(IndexReview.organization_id == self.ctx.organization_id)
        return self._page(stmt, limit=limit, offset=offset, order_col=IndexReview.created_at)

    # --- SLO dashboards / dashboard SLO (AC-002) ---

    def upsert_slo_dashboard(self, data: SloDashboardUpsert) -> SloDashboard:
        domain.assert_slo_dashboard_status(data.status)
        samples = domain.samples_as_list(data.samples)
        dashboard_p95_ms, _ = domain.resolve_p95_ms(
            p95_ms=data.dashboard_p95_ms, samples=samples
        )
        existing = self.db.scalar(
            select(SloDashboard).where(
                SloDashboard.organization_id == self.ctx.organization_id,
                SloDashboard.name == data.name.strip(),
            )
        )
        if existing is not None:
            existing.dashboard_p95_ms = dashboard_p95_ms
            existing.api_p95_ms = data.api_p95_ms
            existing.samples_json = samples
            existing.status = data.status
            existing.version += 1
            existing.updated_by_actor_id = self.ctx.actor_id
            self._audit(
                action="rlb_slo_dashboard_update",
                entity_type="rlb_slo_dashboard",
                entity_id=existing.id,
                payload={
                    "name": existing.name,
                    "dashboard_p95_ms": existing.dashboard_p95_ms,
                    "version": existing.version,
                },
            )
            self._enqueue(
                aggregate_type="rlb_slo_dashboard",
                aggregate_id=existing.id,
                event_type="reliability.slo_dashboard.updated",
                payload={"slo_dashboard_id": str(existing.id)},
            )
            self.uow.commit()
            self.db.refresh(existing)
            return existing
        row = SloDashboard(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            name=data.name.strip(),
            dashboard_p95_ms=dashboard_p95_ms,
            api_p95_ms=data.api_p95_ms,
            samples_json=samples,
            status=data.status,
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="rlb_slo_dashboard_create",
            entity_type="rlb_slo_dashboard",
            entity_id=row.id,
            payload={"name": row.name, "dashboard_p95_ms": row.dashboard_p95_ms},
        )
        self._enqueue(
            aggregate_type="rlb_slo_dashboard",
            aggregate_id=row.id,
            event_type="reliability.slo_dashboard.created",
            payload={"slo_dashboard_id": str(row.id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_slo_dashboards(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[SloDashboard], PageMeta]:
        stmt = select(SloDashboard).where(
            SloDashboard.organization_id == self.ctx.organization_id
        )
        return self._page(stmt, limit=limit, offset=offset, order_col=SloDashboard.updated_at)

    def _latest_slo_dashboard(self) -> SloDashboard | None:
        active = self.db.scalar(
            select(SloDashboard)
            .where(
                SloDashboard.organization_id == self.ctx.organization_id,
                SloDashboard.status == "active",
            )
            .order_by(SloDashboard.updated_at.desc(), SloDashboard.created_at.desc())
            .limit(1)
        )
        if active is not None:
            return active
        return self.db.scalar(
            select(SloDashboard)
            .where(SloDashboard.organization_id == self.ctx.organization_id)
            .order_by(SloDashboard.updated_at.desc(), SloDashboard.created_at.desc())
            .limit(1)
        )

    def dashboard_slo(self) -> dict[str, Any]:
        row = self._latest_slo_dashboard()
        if row is None:
            return {
                "slo_dashboard_id": None,
                "dashboard_p95_ms": None,
                "sample_count": 0,
                "budget_ms": domain.DASHBOARD_P95_BUDGET_MS,
                "slo_met": False,
            }
        samples = domain.samples_as_list(row.samples_json)
        if samples:
            p95_ms = domain.compute_p95_ms(samples)
        else:
            p95_ms = row.dashboard_p95_ms
        return {
            "slo_dashboard_id": row.id,
            "dashboard_p95_ms": p95_ms,
            "sample_count": len(samples) if samples else 0,
            "budget_ms": domain.DASHBOARD_P95_BUDGET_MS,
            "slo_met": domain.dashboard_slo_met(p95_ms),
        }

    # --- Workflow replays (AC-003) ---

    def create_replay(self, data: WorkflowReplayCreate) -> WorkflowReplay:
        key = data.idempotency_key.strip()
        existing = self.db.scalar(
            select(WorkflowReplay).where(
                WorkflowReplay.organization_id == self.ctx.organization_id,
                WorkflowReplay.idempotency_key == key,
            )
        )
        if existing is not None:
            raise ConflictError(
                f"Workflow replay idempotency_key '{key}' already exists"
            )
        row = WorkflowReplay(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            workflow_name=data.workflow_name.strip(),
            idempotency_key=key,
            status="pending",
            attempt_count=0,
            last_error=None,
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="rlb_workflow_replay_create",
            entity_type="rlb_workflow_replay",
            entity_id=row.id,
            payload={"idempotency_key": row.idempotency_key, "status": row.status},
        )
        self._enqueue(
            aggregate_type="rlb_workflow_replay",
            aggregate_id=row.id,
            event_type="reliability.workflow_replay.created",
            payload={"workflow_replay_id": str(row.id), "idempotency_key": row.idempotency_key},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_replays(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[WorkflowReplay], PageMeta]:
        stmt = select(WorkflowReplay).where(
            WorkflowReplay.organization_id == self.ctx.organization_id
        )
        return self._page(stmt, limit=limit, offset=offset, order_col=WorkflowReplay.created_at)

    def get_replay(self, replay_id: UUID) -> WorkflowReplay:
        row = self.db.get(WorkflowReplay, replay_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Workflow replay not found")
        return row

    def fail_replay(self, replay_id: UUID, data: WorkflowReplayFail) -> WorkflowReplay:
        row = self.get_replay(replay_id)
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        domain.assert_replay_transition(from_status=row.status, to_status="failed")
        row.status = "failed"
        row.last_error = data.last_error
        row.attempt_count += 1
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self._audit(
            action="rlb_workflow_replay_fail",
            entity_type="rlb_workflow_replay",
            entity_id=row.id,
            payload={"status": row.status, "attempt_count": row.attempt_count},
        )
        self._enqueue(
            aggregate_type="rlb_workflow_replay",
            aggregate_id=row.id,
            event_type="reliability.workflow_replay.failed",
            payload={"workflow_replay_id": str(row.id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def resume_replay(self, replay_id: UUID, data: WorkflowReplayAction) -> WorkflowReplay:
        row = self.get_replay(replay_id)
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        domain.assert_replay_transition(from_status=row.status, to_status="resumed")
        row.status = "resumed"
        row.attempt_count += 1
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self._audit(
            action="rlb_workflow_replay_resume",
            entity_type="rlb_workflow_replay",
            entity_id=row.id,
            payload={"status": row.status, "attempt_count": row.attempt_count},
        )
        self._enqueue(
            aggregate_type="rlb_workflow_replay",
            aggregate_id=row.id,
            event_type="reliability.workflow_replay.resumed",
            payload={"workflow_replay_id": str(row.id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def complete_replay(self, replay_id: UUID, data: WorkflowReplayAction) -> WorkflowReplay:
        row = self.get_replay(replay_id)
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        domain.assert_replay_transition(from_status=row.status, to_status="completed")
        row.status = "completed"
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self._audit(
            action="rlb_workflow_replay_complete",
            entity_type="rlb_workflow_replay",
            entity_id=row.id,
            payload={"status": row.status},
        )
        self._enqueue(
            aggregate_type="rlb_workflow_replay",
            aggregate_id=row.id,
            event_type="reliability.workflow_replay.completed",
            payload={"workflow_replay_id": str(row.id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    # --- Integration failure tests ---

    def create_integration_failure_test(
        self, data: IntegrationFailureTestCreate
    ) -> IntegrationFailureTest:
        domain.assert_integration_result(data.result)
        existing = self.db.scalar(
            select(IntegrationFailureTest).where(
                IntegrationFailureTest.organization_id == self.ctx.organization_id,
                IntegrationFailureTest.code == data.code.strip(),
            )
        )
        if existing is not None:
            raise ConflictError(
                f"Integration failure test code '{data.code}' already exists"
            )
        row = IntegrationFailureTest(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code.strip(),
            provider=data.provider.strip(),
            result=data.result,
            failure_mode=data.failure_mode.strip(),
            recovered=data.recovered,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="rlb_integration_failure_test_create",
            entity_type="rlb_integration_failure_test",
            entity_id=row.id,
            payload={"code": row.code, "provider": row.provider, "result": row.result},
        )
        self._enqueue(
            aggregate_type="rlb_integration_failure_test",
            aggregate_id=row.id,
            event_type="reliability.integration_failure_test.recorded",
            payload={"integration_failure_test_id": str(row.id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_integration_failure_tests(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[IntegrationFailureTest], PageMeta]:
        stmt = select(IntegrationFailureTest).where(
            IntegrationFailureTest.organization_id == self.ctx.organization_id
        )
        return self._page(
            stmt, limit=limit, offset=offset, order_col=IntegrationFailureTest.created_at
        )

    def mark_integration_recovered(self, test_id: UUID) -> IntegrationFailureTest:
        row = self.db.get(IntegrationFailureTest, test_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Integration failure test not found")
        row.recovered = True
        self._audit(
            action="rlb_integration_failure_test_recovered",
            entity_type="rlb_integration_failure_test",
            entity_id=row.id,
            payload={"code": row.code, "recovered": True},
        )
        self._enqueue(
            aggregate_type="rlb_integration_failure_test",
            aggregate_id=row.id,
            event_type="reliability.integration_failure_test.recovered",
            payload={"integration_failure_test_id": str(row.id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    # --- DR runbooks ---

    def create_dr_runbook(self, data: DrRunbookCreate) -> DrRunbook:
        domain.assert_dr_runbook_status(data.status)
        existing = self.db.scalar(
            select(DrRunbook).where(
                DrRunbook.organization_id == self.ctx.organization_id,
                DrRunbook.code == data.code.strip(),
            )
        )
        if existing is not None:
            raise ConflictError(f"DR runbook code '{data.code}' already exists")
        row = DrRunbook(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code.strip(),
            title=data.title.strip(),
            rto_minutes=data.rto_minutes,
            rpo_minutes=data.rpo_minutes,
            status=data.status,
            body_preview=data.body_preview,
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="rlb_dr_runbook_create",
            entity_type="rlb_dr_runbook",
            entity_id=row.id,
            payload={"code": row.code, "status": row.status},
        )
        self._enqueue(
            aggregate_type="rlb_dr_runbook",
            aggregate_id=row.id,
            event_type="reliability.dr_runbook.created",
            payload={"dr_runbook_id": str(row.id), "code": row.code},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_dr_runbooks(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[DrRunbook], PageMeta]:
        stmt = select(DrRunbook).where(DrRunbook.organization_id == self.ctx.organization_id)
        return self._page(stmt, limit=limit, offset=offset, order_col=DrRunbook.created_at)

    def approve_dr_runbook(self, runbook_id: UUID, data: DrRunbookApprove) -> DrRunbook:
        row = self.db.get(DrRunbook, runbook_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("DR runbook not found")
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        domain.assert_dr_approvable(row.status)
        row.status = "approved"
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self._audit(
            action="rlb_dr_runbook_approve",
            entity_type="rlb_dr_runbook",
            entity_id=row.id,
            payload={"code": row.code, "version": row.version},
        )
        self._enqueue(
            aggregate_type="rlb_dr_runbook",
            aggregate_id=row.id,
            event_type="reliability.dr_runbook.approved",
            payload={"dr_runbook_id": str(row.id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row
