"""Testcases application service (MOD-400)."""

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
from masms_api.modules.testcases import domain
from masms_api.modules.testcases.models import (
    TestCase,
    TestCoverageLink,
    TestEvidence,
    TestPlan,
    TestRun,
    TestStep,
    TestSuite,
)
from masms_api.modules.testcases.schemas import (
    CaseCreate,
    CoverageCreate,
    CoverageSummary,
    PlanCreate,
    RunComplete,
    RunCreate,
    StepCreate,
    SuiteCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class TestcaseService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_case(self, data: CaseCreate) -> TestCase:
        domain.assert_case_type(data.case_type)
        domain.assert_case_priority(data.priority)
        existing = self.db.scalar(
            select(TestCase).where(
                TestCase.organization_id == self.ctx.organization_id,
                TestCase.code == data.code,
            )
        )
        if existing is not None:
            raise ConflictError(f"Test case code '{data.code}' already exists")
        row = TestCase(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            code=data.code.strip(),
            title=data.title.strip(),
            description=data.description,
            case_type=data.case_type,
            priority=data.priority,
            status="draft",
            preconditions=data.preconditions,
            expected_result=data.expected_result,
            owner_actor_id=data.owner_actor_id or self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        for step in data.steps:
            self.uow.add(
                TestStep(
                    id=uuid4(),
                    organization_id=self.ctx.organization_id,
                    case_id=row.id,
                    step_number=step.step_number,
                    action_text=step.action_text,
                    expected_text=step.expected_text,
                )
            )
        self.obs.write_audit(
            action="tc_case_create",
            entity_type="tc_case",
            entity_id=row.id,
            payload={"code": row.code, "case_type": row.case_type},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tc_case",
            aggregate_id=row.id,
            event_type="testcase.case.created",
            payload={"case_id": str(row.id), "code": row.code},
            correlation_id=self.ctx.correlation_id,
            project_id=data.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def approve_case(self, case_id: UUID, *, expected_version: int | None = None) -> TestCase:
        row = self.get_case(case_id)
        domain.assert_expected_version(current=row.version, expected=expected_version)
        if row.status not in {"draft", "approved"}:
            raise ValidationAppError(f"Cannot approve case in status {row.status}")
        row.status = "approved"
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        row.updated_at = datetime.now(UTC)
        self.obs.write_audit(
            action="tc_case_approve",
            entity_type="tc_case",
            entity_id=row.id,
            payload={"code": row.code},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def get_case(self, case_id: UUID) -> TestCase:
        row = self.db.get(TestCase, case_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Test case not found")
        return row

    def list_cases(
        self,
        *,
        status: str | None = None,
        case_type: str | None = None,
        project_id: UUID | None = None,
        q: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[TestCase], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(TestCase).where(TestCase.organization_id == self.ctx.organization_id)
        if status:
            stmt = stmt.where(TestCase.status == status)
        if case_type:
            stmt = stmt.where(TestCase.case_type == case_type)
        if project_id is not None:
            stmt = stmt.where(TestCase.project_id == project_id)
        if q:
            like = f"%{q.strip()}%"
            stmt = stmt.where(or_(TestCase.code.ilike(like), TestCase.title.ilike(like)))
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(stmt.order_by(TestCase.updated_at.desc()).limit(limit).offset(offset))
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def list_steps(self, case_id: UUID) -> list[TestStep]:
        self.get_case(case_id)
        return list(
            self.db.scalars(
                select(TestStep)
                .where(
                    TestStep.organization_id == self.ctx.organization_id,
                    TestStep.case_id == case_id,
                )
                .order_by(TestStep.step_number.asc())
            )
        )

    def add_steps(self, case_id: UUID, steps: list[StepCreate]) -> list[TestStep]:
        self.get_case(case_id)
        created: list[TestStep] = []
        for step in steps:
            row = TestStep(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                case_id=case_id,
                step_number=step.step_number,
                action_text=step.action_text,
                expected_text=step.expected_text,
            )
            self.uow.add(row)
            created.append(row)
        self.uow.commit()
        for row in created:
            self.db.refresh(row)
        return created

    def create_suite(self, data: SuiteCreate) -> TestSuite:
        existing = self.db.scalar(
            select(TestSuite).where(
                TestSuite.organization_id == self.ctx.organization_id,
                TestSuite.code == data.code,
            )
        )
        if existing is not None:
            raise ConflictError(f"Test suite code '{data.code}' already exists")
        for cid in data.case_ids:
            self.get_case(cid)
        row = TestSuite(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            code=data.code,
            title=data.title,
            status="active",
            case_ids=[str(c) for c in data.case_ids],
            owner_actor_id=self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="tc_suite_create",
            entity_type="tc_suite",
            entity_id=row.id,
            payload={"code": row.code, "case_count": len(data.case_ids)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_suites(self) -> list[TestSuite]:
        return list(
            self.db.scalars(
                select(TestSuite)
                .where(TestSuite.organization_id == self.ctx.organization_id)
                .order_by(TestSuite.created_at.desc())
            )
        )

    def create_plan(self, data: PlanCreate) -> TestPlan:
        existing = self.db.scalar(
            select(TestPlan).where(
                TestPlan.organization_id == self.ctx.organization_id,
                TestPlan.code == data.code,
            )
        )
        if existing is not None:
            raise ConflictError(f"Test plan code '{data.code}' already exists")
        row = TestPlan(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            code=data.code,
            title=data.title,
            status="active",
            environment_code=data.environment_code,
            build_ref=data.build_ref,
            suite_ids=[str(s) for s in data.suite_ids],
            owner_actor_id=self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="tc_plan_create",
            entity_type="tc_plan",
            entity_id=row.id,
            payload={
                "code": row.code,
                "environment_code": row.environment_code,
                "build_ref": row.build_ref,
            },
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_plans(self) -> list[TestPlan]:
        return list(
            self.db.scalars(
                select(TestPlan)
                .where(TestPlan.organization_id == self.ctx.organization_id)
                .order_by(TestPlan.created_at.desc())
            )
        )

    def start_run(self, data: RunCreate) -> TestRun:
        case = self.get_case(data.case_id)
        if case.status != "approved":
            raise ValidationAppError("Only approved test cases can be executed")
        plan = None
        if data.plan_id is not None:
            plan = self.db.get(TestPlan, data.plan_id)
            if plan is None or plan.organization_id != self.ctx.organization_id:
                raise NotFoundError("Test plan not found")
        now = datetime.now(UTC)
        row = TestRun(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id or case.project_id,
            case_id=case.id,
            plan_id=data.plan_id,
            status="running",
            environment_code=data.environment_code
            or (plan.environment_code if plan else "local"),
            build_ref=data.build_ref or (plan.build_ref if plan else None),
            executed_by_actor_id=self.ctx.actor_id,
            started_at=now,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="tc_run_start",
            entity_type="tc_run",
            entity_id=row.id,
            payload={"case_id": str(case.id), "environment_code": row.environment_code},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tc_run",
            aggregate_id=row.id,
            event_type="testcase.run.started",
            payload={"run_id": str(row.id), "case_id": str(case.id)},
            correlation_id=self.ctx.correlation_id,
            project_id=row.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def complete_run(self, run_id: UUID, data: RunComplete) -> TestRun:
        row = self.db.get(TestRun, run_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Test run not found")
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        if data.status not in {"passed", "failed", "blocked", "skipped"}:
            raise ValidationAppError(f"Invalid completion status '{data.status}'")
        domain.assert_run_transition(from_status=row.status, to_status=data.status)
        now = datetime.now(UTC)
        row.status = data.status
        row.result_summary = data.result_summary
        row.finished_at = now
        row.version += 1
        row.updated_at = now
        if data.evidence_title:
            self.uow.add(
                TestEvidence(
                    id=uuid4(),
                    organization_id=self.ctx.organization_id,
                    run_id=row.id,
                    evidence_type="result_note",
                    title=data.evidence_title,
                    body_text=data.evidence_body or data.result_summary,
                    environment_code=row.environment_code,
                    build_ref=row.build_ref,
                    created_by_actor_id=self.ctx.actor_id,
                )
            )
        self.obs.write_audit(
            action="tc_run_complete",
            entity_type="tc_run",
            entity_id=row.id,
            payload={
                "status": row.status,
                "environment_code": row.environment_code,
                "build_ref": row.build_ref,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tc_run",
            aggregate_id=row.id,
            event_type="testcase.run.completed",
            payload={"run_id": str(row.id), "status": row.status},
            correlation_id=self.ctx.correlation_id,
            project_id=row.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_runs(
        self,
        *,
        status: str | None = None,
        case_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[TestRun], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(TestRun).where(TestRun.organization_id == self.ctx.organization_id)
        if status:
            stmt = stmt.where(TestRun.status == status)
        if case_id is not None:
            stmt = stmt.where(TestRun.case_id == case_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(stmt.order_by(TestRun.created_at.desc()).limit(limit).offset(offset))
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def list_evidence(self, run_id: UUID) -> list[TestEvidence]:
        run = self.db.get(TestRun, run_id)
        if run is None or run.organization_id != self.ctx.organization_id:
            raise NotFoundError("Test run not found")
        return list(
            self.db.scalars(
                select(TestEvidence)
                .where(
                    TestEvidence.organization_id == self.ctx.organization_id,
                    TestEvidence.run_id == run_id,
                )
                .order_by(TestEvidence.created_at.desc())
            )
        )

    def link_coverage(self, case_id: UUID, data: CoverageCreate) -> TestCoverageLink:
        self.get_case(case_id)
        existing = self.db.scalar(
            select(TestCoverageLink).where(
                TestCoverageLink.organization_id == self.ctx.organization_id,
                TestCoverageLink.case_id == case_id,
                TestCoverageLink.requirement_id == data.requirement_id,
            )
        )
        if existing is not None:
            return existing
        row = TestCoverageLink(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            case_id=case_id,
            requirement_id=data.requirement_id,
            requirement_priority=data.requirement_priority,
            coverage_notes=data.coverage_notes,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="tc_coverage_link",
            entity_type="tc_coverage_link",
            entity_id=row.id,
            payload={
                "case_id": str(case_id),
                "requirement_id": str(data.requirement_id),
                "requirement_priority": data.requirement_priority,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tc_coverage_link",
            aggregate_id=row.id,
            event_type="testcase.coverage.linked",
            payload={
                "case_id": str(case_id),
                "requirement_id": str(data.requirement_id),
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_coverage(self, case_id: UUID | None = None) -> list[TestCoverageLink]:
        stmt = select(TestCoverageLink).where(
            TestCoverageLink.organization_id == self.ctx.organization_id
        )
        if case_id is not None:
            self.get_case(case_id)
            stmt = stmt.where(TestCoverageLink.case_id == case_id)
        return list(self.db.scalars(stmt))

    def coverage_summary(
        self,
        *,
        must_have_requirement_ids: list[UUID] | None = None,
    ) -> CoverageSummary:
        """AC-001 helper: given Must-Have requirement IDs, report coverage gaps.

        Also counts approved permission/negative cases (AC-002 signal).
        """
        must_ids = list(must_have_requirement_ids or [])
        links = self.list_coverage()
        covered = {link.requirement_id for link in links if link.requirement_id in set(must_ids)}
        if not must_ids:
            # Fall back to priorities recorded on links
            must_from_links = {
                link.requirement_id
                for link in links
                if link.requirement_priority.lower() in {"must-have", "must_have", "musthave"}
            }
            must_ids = list(must_from_links)
            covered = must_from_links
        permission_neg = (
            self.db.scalar(
                select(func.count())
                .select_from(TestCase)
                .where(
                    TestCase.organization_id == self.ctx.organization_id,
                    TestCase.status == "approved",
                    or_(
                        TestCase.case_type == "permission",
                        TestCase.case_type == "negative",
                    ),
                )
            )
            or 0
        )
        uncovered = [rid for rid in must_ids if rid not in covered]
        return CoverageSummary(
            must_have_total=len(must_ids),
            must_have_covered=len(must_ids) - len(uncovered),
            permission_negative_cases=int(permission_neg),
            uncovered_must_have_requirement_ids=uncovered,
        )
