"""Bugs application service (MOD-410)."""

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
from masms_api.modules.bugs import domain
from masms_api.modules.bugs.models import (
    Bug,
    BugAssignment,
    BugFixSubmission,
    BugKnownIssueApproval,
    BugLink,
    BugRetest,
    BugSeveritySla,
)
from masms_api.modules.bugs.schemas import (
    AssignmentCreate,
    AssignmentRead,
    BugCreate,
    BugHistory,
    BugRead,
    BugReject,
    BugReopen,
    BugTransition,
    FixCreate,
    FixRead,
    KnownIssueCreate,
    KnownIssueDecide,
    KnownIssueRead,
    LinkCreate,
    LinkRead,
    ReleaseGateResult,
    RetestCreate,
    RetestRead,
    SeveritySlaUpsert,
)
from masms_api.observability.writer import ObservabilityWriter


class BugService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_bug(self, data: BugCreate) -> Bug:
        domain.assert_severity(data.severity)
        existing = self.db.scalar(
            select(Bug).where(
                Bug.organization_id == self.ctx.organization_id,
                Bug.code == data.code,
            )
        )
        if existing is not None:
            raise ConflictError(f"Bug code '{data.code}' already exists")
        blocks = (
            data.blocks_release
            if data.blocks_release is not None
            else data.severity in domain.BLOCKING_SEVERITIES
        )
        row = Bug(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            code=data.code.strip(),
            title=data.title.strip(),
            description=data.description,
            severity=data.severity,
            status="open",
            blocks_release=blocks,
            owner_actor_id=self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        for link in data.links:
            domain.assert_link_type(link.link_type)
            self.uow.add(
                BugLink(
                    id=uuid4(),
                    organization_id=self.ctx.organization_id,
                    bug_id=row.id,
                    link_type=link.link_type,
                    linked_entity_id=link.linked_entity_id,
                    notes=link.notes,
                    created_by_actor_id=self.ctx.actor_id,
                )
            )
        self.obs.write_audit(
            action="bg_bug_create",
            entity_type="bg_bug",
            entity_id=row.id,
            payload={"code": row.code, "severity": row.severity, "blocks_release": blocks},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="bg_bug",
            aggregate_id=row.id,
            event_type="bug.created",
            payload={"bug_id": str(row.id), "code": row.code, "severity": row.severity},
            correlation_id=self.ctx.correlation_id,
            project_id=data.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def get_bug(self, bug_id: UUID) -> Bug:
        row = self.db.get(Bug, bug_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Bug not found")
        return row

    def list_bugs(
        self,
        *,
        status: str | None = None,
        severity: str | None = None,
        project_id: UUID | None = None,
        q: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Bug], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(Bug).where(Bug.organization_id == self.ctx.organization_id)
        if status:
            stmt = stmt.where(Bug.status == status)
        if severity:
            stmt = stmt.where(Bug.severity == severity)
        if project_id is not None:
            stmt = stmt.where(Bug.project_id == project_id)
        if q:
            like = f"%{q.strip()}%"
            stmt = stmt.where(or_(Bug.code.ilike(like), Bug.title.ilike(like)))
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(stmt.order_by(Bug.updated_at.desc()).limit(limit).offset(offset))
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def reject_bug(self, bug_id: UUID, data: BugReject) -> Bug:
        row = self.get_bug(bug_id)
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        domain.assert_bug_transition(from_status=row.status, to_status="rejected")
        row.status = "rejected"
        row.rejection_reason = data.reason
        row.rejection_evidence = data.evidence
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        row.updated_at = datetime.now(UTC)
        self.obs.write_audit(
            action="bg_bug_reject",
            entity_type="bg_bug",
            entity_id=row.id,
            payload={"reason": data.reason},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="bg_bug",
            aggregate_id=row.id,
            event_type="bug.rejected",
            payload={"bug_id": str(row.id)},
            correlation_id=self.ctx.correlation_id,
            project_id=row.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def reopen_bug(self, bug_id: UUID, data: BugReopen) -> Bug:
        row = self.get_bug(bug_id)
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        domain.assert_bug_transition(from_status=row.status, to_status="open")
        row.status = "open"
        row.reopen_reason = data.reason
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        row.updated_at = datetime.now(UTC)
        self.obs.write_audit(
            action="bg_bug_reopen",
            entity_type="bg_bug",
            entity_id=row.id,
            payload={"reason": data.reason},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="bg_bug",
            aggregate_id=row.id,
            event_type="bug.reopened",
            payload={"bug_id": str(row.id)},
            correlation_id=self.ctx.correlation_id,
            project_id=row.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def transition_bug(self, bug_id: UUID, data: BugTransition) -> Bug:
        row = self.get_bug(bug_id)
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        domain.assert_bug_transition(from_status=row.status, to_status=data.status)
        row.status = data.status
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        row.updated_at = datetime.now(UTC)
        self.obs.write_audit(
            action="bg_bug_transition",
            entity_type="bg_bug",
            entity_id=row.id,
            payload={"status": data.status, "reason": data.reason},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def add_link(self, bug_id: UUID, data: LinkCreate) -> BugLink:
        self.get_bug(bug_id)
        domain.assert_link_type(data.link_type)
        existing = self.db.scalar(
            select(BugLink).where(
                BugLink.organization_id == self.ctx.organization_id,
                BugLink.bug_id == bug_id,
                BugLink.link_type == data.link_type,
                BugLink.linked_entity_id == data.linked_entity_id,
            )
        )
        if existing is not None:
            return existing
        row = BugLink(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            bug_id=bug_id,
            link_type=data.link_type,
            linked_entity_id=data.linked_entity_id,
            notes=data.notes,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_links(self, bug_id: UUID) -> list[BugLink]:
        self.get_bug(bug_id)
        return list(
            self.db.scalars(
                select(BugLink).where(
                    BugLink.organization_id == self.ctx.organization_id,
                    BugLink.bug_id == bug_id,
                )
            )
        )

    def assign(self, bug_id: UUID, data: AssignmentCreate) -> BugAssignment:
        bug = self.get_bug(bug_id)
        now = datetime.now(UTC)
        open_rows = list(
            self.db.scalars(
                select(BugAssignment).where(
                    BugAssignment.organization_id == self.ctx.organization_id,
                    BugAssignment.bug_id == bug_id,
                    BugAssignment.effective_to.is_(None),
                )
            )
        )
        for prev in open_rows:
            prev.effective_to = now
        row = BugAssignment(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            bug_id=bug_id,
            assignee_actor_id=data.assignee_actor_id,
            assigned_by_actor_id=self.ctx.actor_id,
            reason=data.reason,
            effective_from=now,
        )
        bug.assignee_actor_id = data.assignee_actor_id
        bug.updated_by_actor_id = self.ctx.actor_id
        bug.updated_at = now
        self.uow.add(row)
        self.obs.write_audit(
            action="bg_bug_assign",
            entity_type="bg_bug",
            entity_id=bug_id,
            payload={"assignee_actor_id": str(data.assignee_actor_id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_assignments(self, bug_id: UUID) -> list[BugAssignment]:
        self.get_bug(bug_id)
        return list(
            self.db.scalars(
                select(BugAssignment)
                .where(
                    BugAssignment.organization_id == self.ctx.organization_id,
                    BugAssignment.bug_id == bug_id,
                )
                .order_by(BugAssignment.effective_from.desc())
            )
        )

    def submit_fix(self, bug_id: UUID, data: FixCreate) -> BugFixSubmission:
        bug = self.get_bug(bug_id)
        domain.assert_expected_version(current=bug.version, expected=data.expected_version)
        if bug.status not in {"open", "in_fix", "rejected", "retesting"}:
            # allow moving into fixed from in_fix primarily
            pass
        if bug.status in {"open", "rejected"}:
            domain.assert_bug_transition(from_status=bug.status, to_status="in_fix")
            bug.status = "in_fix"
        domain.assert_bug_transition(from_status=bug.status, to_status="fixed")
        bug.status = "fixed"
        bug.version += 1
        bug.updated_by_actor_id = self.ctx.actor_id
        bug.updated_at = datetime.now(UTC)
        row = BugFixSubmission(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            bug_id=bug_id,
            summary=data.summary,
            build_ref=data.build_ref,
            status="submitted",
            submitted_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.add(
            BugLink(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                bug_id=bug_id,
                link_type="fix",
                linked_entity_id=row.id,
                notes=data.build_ref,
                created_by_actor_id=self.ctx.actor_id,
            )
        )
        self.obs.write_audit(
            action="bg_fix_submit",
            entity_type="bg_bug",
            entity_id=bug_id,
            payload={"fix_id": str(row.id), "build_ref": data.build_ref},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="bg_bug",
            aggregate_id=bug_id,
            event_type="bug.fix_submitted",
            payload={"bug_id": str(bug_id), "fix_id": str(row.id)},
            correlation_id=self.ctx.correlation_id,
            project_id=bug.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_fixes(self, bug_id: UUID) -> list[BugFixSubmission]:
        self.get_bug(bug_id)
        return list(
            self.db.scalars(
                select(BugFixSubmission)
                .where(
                    BugFixSubmission.organization_id == self.ctx.organization_id,
                    BugFixSubmission.bug_id == bug_id,
                )
                .order_by(BugFixSubmission.created_at.desc())
            )
        )

    def record_retest(self, bug_id: UUID, data: RetestCreate) -> BugRetest:
        bug = self.get_bug(bug_id)
        domain.assert_expected_version(current=bug.version, expected=data.expected_version)
        if data.result not in {"passed", "failed"}:
            raise ValidationAppError("Retest result must be passed or failed")
        # move fixed → retesting if needed
        if bug.status == "fixed":
            domain.assert_bug_transition(from_status="fixed", to_status="retesting")
            bug.status = "retesting"
        next_status = "verified" if data.result == "passed" else "in_fix"
        domain.assert_bug_transition(from_status=bug.status, to_status=next_status)
        bug.status = next_status
        bug.version += 1
        bug.updated_by_actor_id = self.ctx.actor_id
        bug.updated_at = datetime.now(UTC)
        row = BugRetest(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            bug_id=bug_id,
            fix_submission_id=data.fix_submission_id,
            result=data.result,
            evidence_text=data.evidence_text,
            environment_code=data.environment_code,
            build_ref=data.build_ref,
            tested_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.add(
            BugLink(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                bug_id=bug_id,
                link_type="retest",
                linked_entity_id=row.id,
                notes=data.result,
                created_by_actor_id=self.ctx.actor_id,
            )
        )
        self.obs.write_audit(
            action="bg_retest",
            entity_type="bg_bug",
            entity_id=bug_id,
            payload={"result": data.result, "environment_code": data.environment_code},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="bg_bug",
            aggregate_id=bug_id,
            event_type="bug.retested",
            payload={"bug_id": str(bug_id), "result": data.result},
            correlation_id=self.ctx.correlation_id,
            project_id=bug.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_retests(self, bug_id: UUID) -> list[BugRetest]:
        self.get_bug(bug_id)
        return list(
            self.db.scalars(
                select(BugRetest)
                .where(
                    BugRetest.organization_id == self.ctx.organization_id,
                    BugRetest.bug_id == bug_id,
                )
                .order_by(BugRetest.created_at.desc())
            )
        )

    def request_known_issue(self, bug_id: UUID, data: KnownIssueCreate) -> BugKnownIssueApproval:
        self.get_bug(bug_id)
        row = BugKnownIssueApproval(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            bug_id=bug_id,
            reason=data.reason,
            release_ref=data.release_ref,
            status="pending",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.db.refresh(row)
        return row

    def decide_known_issue(
        self, approval_id: UUID, data: KnownIssueDecide
    ) -> BugKnownIssueApproval:
        row = self.db.get(BugKnownIssueApproval, approval_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Known-issue approval not found")
        if data.status not in {"approved", "rejected"}:
            raise ValidationAppError("Decision status must be approved or rejected")
        bug = self.get_bug(row.bug_id)
        domain.assert_expected_version(
            current=bug.version, expected=data.expected_bug_version
        )
        now = datetime.now(UTC)
        row.status = data.status
        row.approved_by_actor_id = self.ctx.actor_id
        row.decided_at = now
        if data.status == "approved":
            domain.assert_bug_transition(from_status=bug.status, to_status="known_issue")
            bug.status = "known_issue"
            bug.version += 1
            bug.updated_by_actor_id = self.ctx.actor_id
            bug.updated_at = now
            if row.release_ref:
                self.uow.add(
                    BugLink(
                        id=uuid4(),
                        organization_id=self.ctx.organization_id,
                        bug_id=bug.id,
                        link_type="release",
                        linked_entity_id=uuid4(),
                        notes=row.release_ref,
                        created_by_actor_id=self.ctx.actor_id,
                    )
                )
            self.obs.write_audit(
                action="bg_known_issue_approve",
                entity_type="bg_bug",
                entity_id=bug.id,
                payload={"approval_id": str(row.id), "release_ref": row.release_ref},
            )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_known_issues(self, bug_id: UUID) -> list[BugKnownIssueApproval]:
        self.get_bug(bug_id)
        return list(
            self.db.scalars(
                select(BugKnownIssueApproval).where(
                    BugKnownIssueApproval.organization_id == self.ctx.organization_id,
                    BugKnownIssueApproval.bug_id == bug_id,
                )
            )
        )

    def upsert_severity_sla(self, data: SeveritySlaUpsert) -> BugSeveritySla:
        domain.assert_severity(data.severity)
        row = self.db.scalar(
            select(BugSeveritySla).where(
                BugSeveritySla.organization_id == self.ctx.organization_id,
                BugSeveritySla.severity == data.severity,
            )
        )
        if row is None:
            row = BugSeveritySla(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                severity=data.severity,
                response_hours=data.response_hours,
                resolve_hours=data.resolve_hours,
                blocks_release=data.blocks_release,
                created_by_actor_id=self.ctx.actor_id,
            )
            self.uow.add(row)
        else:
            row.response_hours = data.response_hours
            row.resolve_hours = data.resolve_hours
            row.blocks_release = data.blocks_release
            row.updated_at = datetime.now(UTC)
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_severity_slas(self) -> list[BugSeveritySla]:
        return list(
            self.db.scalars(
                select(BugSeveritySla)
                .where(BugSeveritySla.organization_id == self.ctx.organization_id)
                .order_by(BugSeveritySla.severity.asc())
            )
        )

    def _has_approved_known_issue(self, bug_id: UUID) -> bool:
        row = self.db.scalar(
            select(BugKnownIssueApproval).where(
                BugKnownIssueApproval.organization_id == self.ctx.organization_id,
                BugKnownIssueApproval.bug_id == bug_id,
                BugKnownIssueApproval.status == "approved",
            )
        )
        return row is not None

    def release_gate(self, *, project_id: UUID | None = None) -> ReleaseGateResult:
        stmt = select(Bug).where(Bug.organization_id == self.ctx.organization_id)
        if project_id is not None:
            stmt = stmt.where(Bug.project_id == project_id)
        bugs = list(self.db.scalars(stmt))
        blocking: list[Bug] = []
        for bug in bugs:
            if domain.is_actively_blocking(
                status=bug.status,
                severity=bug.severity,
                blocks_release_flag=bug.blocks_release,
                has_approved_known_issue=self._has_approved_known_issue(bug.id),
            ):
                blocking.append(bug)
        return ReleaseGateResult(
            project_id=project_id,
            release_allowed=len(blocking) == 0,
            blocking_bug_ids=[b.id for b in blocking],
            blocking_codes=[b.code for b in blocking],
        )

    def history(self, bug_id: UUID) -> BugHistory:
        bug = self.get_bug(bug_id)
        return BugHistory(
            bug=BugRead.model_validate(bug),
            links=[LinkRead.model_validate(r) for r in self.list_links(bug_id)],
            assignments=[
                AssignmentRead.model_validate(r) for r in self.list_assignments(bug_id)
            ],
            fixes=[FixRead.model_validate(r) for r in self.list_fixes(bug_id)],
            retests=[RetestRead.model_validate(r) for r in self.list_retests(bug_id)],
            known_issues=[
                KnownIssueRead.model_validate(r) for r in self.list_known_issues(bug_id)
            ],
        )
