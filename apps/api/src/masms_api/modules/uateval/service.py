"""Application service for MOD-620 UAT evaluation."""

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
from masms_api.modules.uateval import domain
from masms_api.modules.uateval.models import (
    AcceptanceEvidence,
    AgentEvaluation,
    E2eTest,
    ExpectedDecision,
    RoleUat,
    SampleProject,
    SeedScript,
)
from masms_api.modules.uateval.schemas import (
    AcceptanceEvidenceAccept,
    AcceptanceEvidenceCreate,
    AgentEvaluationCreate,
    E2eTestCreate,
    ExpectedDecisionCreate,
    RoleUatCreate,
    SeedScriptCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class UatEvalService:
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

    def _org_by_code(self, model: type[Any], code: str) -> Any | None:
        return self.db.scalar(
            select(model).where(
                model.organization_id == self.ctx.organization_id,
                model.code == code,
            )
        )

    # --- Sample projects / AC-001 ---

    def seed_sample_projects(self) -> list[SampleProject]:
        created: list[SampleProject] = []
        existing_by_code = {
            row.code: row
            for row in self.db.scalars(
                select(SampleProject).where(
                    SampleProject.organization_id == self.ctx.organization_id,
                    SampleProject.code.in_([code for code, _ in domain.SAMPLE_PROJECT_SPECS]),
                )
            )
        }
        for code, title in domain.SAMPLE_PROJECT_SPECS:
            row = existing_by_code.get(code)
            if row is not None:
                created.append(row)
                continue
            row = SampleProject(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                code=code,
                title=title,
                workflow_status="pending",
                created_by_actor_id=self.ctx.actor_id,
            )
            self.uow.add(row)
            self._audit(
                action="ua_sample_project_seed",
                entity_type="ua_sample_project",
                entity_id=row.id,
                payload={"code": row.code, "workflow_status": row.workflow_status},
            )
            self._enqueue(
                aggregate_type="ua_sample_project",
                aggregate_id=row.id,
                event_type="uat.sample_project.seeded",
                payload={"sample_project_id": str(row.id), "code": row.code},
            )
            created.append(row)
        self.uow.commit()
        for row in created:
            self.db.refresh(row)
        return created

    def list_sample_projects(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[SampleProject], PageMeta]:
        stmt = select(SampleProject).where(
            SampleProject.organization_id == self.ctx.organization_id
        )
        return self._page(stmt, limit=limit, offset=offset, order_col=SampleProject.created_at)

    def get_sample_project(self, code: str) -> SampleProject:
        row = self._org_by_code(SampleProject, code.strip())
        if row is None:
            raise NotFoundError("Sample project not found")
        return row

    def mark_sample_passed(self, code: str) -> SampleProject:
        row = self.get_sample_project(code)
        domain.assert_sample_workflow_status(row.workflow_status)
        if row.workflow_status != "passed":
            row.workflow_status = "passed"
            self._audit(
                action="ua_sample_project_pass",
                entity_type="ua_sample_project",
                entity_id=row.id,
                payload={"code": row.code, "workflow_status": row.workflow_status},
            )
            self._enqueue(
                aggregate_type="ua_sample_project",
                aggregate_id=row.id,
                event_type="uat.sample_project.passed",
                payload={"sample_project_id": str(row.id), "code": row.code},
            )
            self.uow.commit()
            self.db.refresh(row)
        return row

    def sample_gate(self) -> dict[str, Any]:
        passed_count = self.db.scalar(
            select(func.count())
            .select_from(SampleProject)
            .where(
                SampleProject.organization_id == self.ctx.organization_id,
                SampleProject.workflow_status == "passed",
            )
        ) or 0
        required = domain.SAMPLE_REQUIRED
        return {
            "passed_count": int(passed_count),
            "required_count": required,
            "gate_passed": domain.sample_gate_passed(int(passed_count), required),
        }

    # --- Seed scripts ---

    def create_seed_script(self, data: SeedScriptCreate) -> SeedScript:
        domain.assert_seed_script_status(data.status)
        code = data.code.strip()
        if self._org_by_code(SeedScript, code) is not None:
            raise ConflictError(f"Seed script code '{code}' already exists")
        row = SeedScript(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=code,
            title=data.title.strip(),
            sample_project_code=data.sample_project_code.strip(),
            status=data.status,
            checksum=data.checksum,
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="ua_seed_script_create",
            entity_type="ua_seed_script",
            entity_id=row.id,
            payload={"code": row.code, "status": row.status},
        )
        self._enqueue(
            aggregate_type="ua_seed_script",
            aggregate_id=row.id,
            event_type="uat.seed_script.registered",
            payload={"seed_script_id": str(row.id), "code": row.code},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_seed_scripts(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[SeedScript], PageMeta]:
        stmt = select(SeedScript).where(SeedScript.organization_id == self.ctx.organization_id)
        return self._page(stmt, limit=limit, offset=offset, order_col=SeedScript.created_at)

    def get_seed_script(self, seed_script_id: UUID) -> SeedScript:
        row = self.db.get(SeedScript, seed_script_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Seed script not found")
        return row

    # --- Expected decisions ---

    def create_expected_decision(self, data: ExpectedDecisionCreate) -> ExpectedDecision:
        domain.assert_expected_decision_status(data.status)
        key = data.decision_key.strip()
        existing = self.db.scalar(
            select(ExpectedDecision).where(
                ExpectedDecision.organization_id == self.ctx.organization_id,
                ExpectedDecision.decision_key == key,
            )
        )
        if existing is not None:
            raise ConflictError(f"Expected decision key '{key}' already exists")
        if data.seed_script_id is not None:
            self.get_seed_script(data.seed_script_id)
        row = ExpectedDecision(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            seed_script_id=data.seed_script_id,
            decision_key=key,
            expected_outcome=data.expected_outcome.strip(),
            status=data.status,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="ua_expected_decision_create",
            entity_type="ua_expected_decision",
            entity_id=row.id,
            payload={"decision_key": row.decision_key, "status": row.status},
        )
        self._enqueue(
            aggregate_type="ua_expected_decision",
            aggregate_id=row.id,
            event_type="uat.expected_decision.recorded",
            payload={"expected_decision_id": str(row.id), "decision_key": row.decision_key},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_expected_decisions(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[ExpectedDecision], PageMeta]:
        stmt = select(ExpectedDecision).where(
            ExpectedDecision.organization_id == self.ctx.organization_id
        )
        return self._page(stmt, limit=limit, offset=offset, order_col=ExpectedDecision.created_at)

    # --- Agent evaluations / AC-002 ---

    def create_agent_evaluation(self, data: AgentEvaluationCreate) -> AgentEvaluation:
        domain.assert_accuracy_pct(data.accuracy_pct)
        status = domain.evaluation_status_for_score(data.accuracy_pct, data.status)
        code = data.code.strip()
        if self._org_by_code(AgentEvaluation, code) is not None:
            raise ConflictError(f"Agent evaluation code '{code}' already exists")
        row = AgentEvaluation(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=code,
            agent_code=data.agent_code.strip(),
            accuracy_pct=data.accuracy_pct,
            sample_count=data.sample_count,
            status=status,
            notes=data.notes,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="ua_agent_evaluation_create",
            entity_type="ua_agent_evaluation",
            entity_id=row.id,
            payload={"code": row.code, "accuracy_pct": row.accuracy_pct, "status": row.status},
        )
        self._enqueue(
            aggregate_type="ua_agent_evaluation",
            aggregate_id=row.id,
            event_type="uat.agent_evaluation.recorded",
            payload={"agent_evaluation_id": str(row.id), "accuracy_pct": row.accuracy_pct},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_agent_evaluations(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[AgentEvaluation], PageMeta]:
        stmt = select(AgentEvaluation).where(
            AgentEvaluation.organization_id == self.ctx.organization_id
        )
        return self._page(stmt, limit=limit, offset=offset, order_col=AgentEvaluation.created_at)

    def _latest_agent_evaluation(self) -> AgentEvaluation | None:
        return self.db.scalar(
            select(AgentEvaluation)
            .where(AgentEvaluation.organization_id == self.ctx.organization_id)
            .order_by(AgentEvaluation.created_at.desc())
            .limit(1)
        )

    def agent_quality(self) -> dict[str, Any]:
        row = self._latest_agent_evaluation()
        score = None if row is None else row.accuracy_pct
        target = domain.AGENT_QUALITY_TARGET_PCT
        return {
            "evaluation_id": None if row is None else row.id,
            "target_pct": target,
            "latest_score": score,
            "meets_target": domain.agent_quality_met(score, target),
        }

    # --- E2E tests ---

    def create_e2e_test(self, data: E2eTestCreate) -> E2eTest:
        domain.assert_e2e_result(data.result)
        code = data.code.strip()
        if self._org_by_code(E2eTest, code) is not None:
            raise ConflictError(f"E2E test code '{code}' already exists")
        row = E2eTest(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=code,
            suite_name=data.suite_name.strip(),
            result=data.result,
            evidence=data.evidence,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="ua_e2e_test_create",
            entity_type="ua_e2e_test",
            entity_id=row.id,
            payload={"code": row.code, "result": row.result},
        )
        self._enqueue(
            aggregate_type="ua_e2e_test",
            aggregate_id=row.id,
            event_type="uat.e2e_test.recorded",
            payload={"e2e_test_id": str(row.id), "result": row.result},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_e2e_tests(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[E2eTest], PageMeta]:
        stmt = select(E2eTest).where(E2eTest.organization_id == self.ctx.organization_id)
        return self._page(stmt, limit=limit, offset=offset, order_col=E2eTest.created_at)

    # --- Role UAT ---

    def create_role_uat(self, data: RoleUatCreate) -> RoleUat:
        domain.assert_role_uat_result(data.result)
        code = data.code.strip()
        if self._org_by_code(RoleUat, code) is not None:
            raise ConflictError(f"Role UAT code '{code}' already exists")
        row = RoleUat(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=code,
            role_code=data.role_code.strip(),
            scenario=data.scenario.strip(),
            result=data.result,
            tester_actor_id=data.tester_actor_id,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="ua_role_uat_create",
            entity_type="ua_role_uat",
            entity_id=row.id,
            payload={"code": row.code, "role_code": row.role_code, "result": row.result},
        )
        self._enqueue(
            aggregate_type="ua_role_uat",
            aggregate_id=row.id,
            event_type="uat.role_uat.recorded",
            payload={"role_uat_id": str(row.id), "result": row.result},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_role_uat(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[RoleUat], PageMeta]:
        stmt = select(RoleUat).where(RoleUat.organization_id == self.ctx.organization_id)
        return self._page(stmt, limit=limit, offset=offset, order_col=RoleUat.created_at)

    # --- Acceptance evidence / AC-003 ---

    def create_acceptance_evidence(self, data: AcceptanceEvidenceCreate) -> AcceptanceEvidence:
        domain.assert_evidence_status(data.status)
        code = data.code.strip()
        if self._org_by_code(AcceptanceEvidence, code) is not None:
            raise ConflictError(f"Acceptance evidence code '{code}' already exists")
        row = AcceptanceEvidence(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=code,
            title=data.title.strip(),
            evidence_ref=data.evidence_ref.strip(),
            status=data.status,
            submitted_by_actor_id=self.ctx.actor_id,
            accepted_by_actor_id=None,
            version=1,
        )
        self.uow.add(row)
        self._audit(
            action="ua_acceptance_evidence_create",
            entity_type="ua_acceptance_evidence",
            entity_id=row.id,
            payload={"code": row.code, "status": row.status},
        )
        self._enqueue(
            aggregate_type="ua_acceptance_evidence",
            aggregate_id=row.id,
            event_type="uat.acceptance_evidence.created",
            payload={"acceptance_evidence_id": str(row.id), "code": row.code},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_acceptance_evidence(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[AcceptanceEvidence], PageMeta]:
        stmt = select(AcceptanceEvidence).where(
            AcceptanceEvidence.organization_id == self.ctx.organization_id
        )
        return self._page(
            stmt, limit=limit, offset=offset, order_col=AcceptanceEvidence.created_at
        )

    def get_acceptance_evidence(self, evidence_id: UUID) -> AcceptanceEvidence:
        row = self.db.get(AcceptanceEvidence, evidence_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Acceptance evidence not found")
        return row

    def accept_evidence(
        self, evidence_id: UUID, data: AcceptanceEvidenceAccept
    ) -> AcceptanceEvidence:
        domain.assert_human_approval_only(self.ctx.actor_kind)
        row = self.get_acceptance_evidence(evidence_id)
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        domain.assert_evidence_acceptable(row.status)
        row.status = "accepted"
        row.accepted_by_actor_id = self.ctx.actor_id
        row.version += 1
        self._audit(
            action="ua_acceptance_evidence_accept",
            entity_type="ua_acceptance_evidence",
            entity_id=row.id,
            payload={"code": row.code, "version": row.version},
        )
        self._enqueue(
            aggregate_type="ua_acceptance_evidence",
            aggregate_id=row.id,
            event_type="uat.acceptance_evidence.accepted",
            payload={"acceptance_evidence_id": str(row.id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row
