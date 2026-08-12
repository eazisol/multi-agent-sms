"""Releases application service (MOD-430)."""

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
from masms_api.modules.releases import domain
from masms_api.modules.releases.models import (
    BackupConfirmation,
    CompletionReport,
    Deployment,
    DeploymentCheck,
    MigrationPlan,
    Release,
    ReleaseItem,
    Rollback,
)
from masms_api.modules.releases.schemas import (
    ApproveRelease,
    BackupCreate,
    CompletionReportCreate,
    DeploymentCheckCreate,
    DeploymentCreate,
    MigrationPlanCreate,
    ReleaseCreate,
    ReleaseItemCreate,
    RollbackCreate,
    SubmitApproval,
    TraceabilitySummary,
)
from masms_api.observability.writer import ObservabilityWriter

REQUIRED_TRACE_TYPES = frozenset(domain.ITEM_LINK_TYPES)


class ReleaseService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_release(self, data: ReleaseCreate) -> Release:
        existing = self.db.scalar(
            select(Release).where(
                Release.organization_id == self.ctx.organization_id,
                Release.code == data.code,
            )
        )
        if existing is not None:
            raise ConflictError(f"Release code '{data.code}' already exists")
        row = Release(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            code=data.code.strip(),
            title=data.title.strip(),
            description=data.description,
            status="draft",
            version_label=data.version_label,
            owner_actor_id=self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        for item in data.items:
            domain.assert_link_type(item.link_type)
            self.uow.add(
                ReleaseItem(
                    id=uuid4(),
                    organization_id=self.ctx.organization_id,
                    release_id=row.id,
                    link_type=item.link_type,
                    linked_entity_id=item.linked_entity_id,
                    notes=item.notes,
                    created_by_actor_id=self.ctx.actor_id,
                )
            )
        self.obs.write_audit(
            action="rl_release_create",
            entity_type="rl_release",
            entity_id=row.id,
            payload={"code": row.code, "version_label": row.version_label},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="rl_release",
            aggregate_id=row.id,
            event_type="release.created",
            payload={"release_id": str(row.id), "code": row.code},
            correlation_id=self.ctx.correlation_id,
            project_id=data.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def get_release(self, release_id: UUID) -> Release:
        row = self.db.get(Release, release_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Release not found")
        return row

    def list_releases(
        self,
        *,
        status: str | None = None,
        project_id: UUID | None = None,
        q: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Release], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(Release).where(Release.organization_id == self.ctx.organization_id)
        if status:
            stmt = stmt.where(Release.status == status)
        if project_id is not None:
            stmt = stmt.where(Release.project_id == project_id)
        if q:
            like = f"%{q.strip()}%"
            stmt = stmt.where(or_(Release.code.ilike(like), Release.title.ilike(like)))
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(stmt.order_by(Release.updated_at.desc()).limit(limit).offset(offset))
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def list_all_deployments(
        self,
        *,
        status: str | None = None,
        environment_code: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Deployment], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(Deployment).where(Deployment.organization_id == self.ctx.organization_id)
        if status:
            stmt = stmt.where(Deployment.status == status)
        if environment_code:
            stmt = stmt.where(Deployment.environment_code == environment_code)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(Deployment.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def add_item(self, release_id: UUID, data: ReleaseItemCreate) -> ReleaseItem:
        self.get_release(release_id)
        domain.assert_link_type(data.link_type)
        existing = self.db.scalar(
            select(ReleaseItem).where(
                ReleaseItem.organization_id == self.ctx.organization_id,
                ReleaseItem.release_id == release_id,
                ReleaseItem.link_type == data.link_type,
                ReleaseItem.linked_entity_id == data.linked_entity_id,
            )
        )
        if existing is not None:
            return existing
        row = ReleaseItem(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            release_id=release_id,
            link_type=data.link_type,
            linked_entity_id=data.linked_entity_id,
            notes=data.notes,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_items(self, release_id: UUID) -> list[ReleaseItem]:
        self.get_release(release_id)
        return list(
            self.db.scalars(
                select(ReleaseItem).where(
                    ReleaseItem.organization_id == self.ctx.organization_id,
                    ReleaseItem.release_id == release_id,
                )
            )
        )

    def traceability(self, release_id: UUID) -> TraceabilitySummary:
        items = self.list_items(release_id)
        present = sorted({i.link_type for i in items})
        missing = sorted(REQUIRED_TRACE_TYPES - set(present))
        return TraceabilitySummary(
            release_id=release_id,
            link_types_present=present,
            missing_link_types=missing,
            item_count=len(items),
        )

    def submit_for_approval(self, release_id: UUID, data: SubmitApproval) -> Release:
        row = self.get_release(release_id)
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        if not self.list_items(release_id):
            raise ValidationAppError("Release must include at least one traced item")
        domain.assert_release_transition(
            from_status=row.status, to_status="ready_for_approval"
        )
        row.status = "ready_for_approval"
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        row.updated_at = datetime.now(UTC)
        self.uow.commit()
        self.db.refresh(row)
        return row

    def approve(self, release_id: UUID, data: ApproveRelease) -> Release:
        row = self.get_release(release_id)
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        domain.assert_release_transition(
            from_status=row.status, to_status="approved_for_production"
        )
        now = datetime.now(UTC)
        row.status = "approved_for_production"
        row.approval_evidence = data.evidence
        row.approved_by_actor_id = self.ctx.actor_id
        row.approved_at = now
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        row.updated_at = now
        self.obs.write_audit(
            action="rl_release_approve",
            entity_type="rl_release",
            entity_id=row.id,
            payload={"evidence": data.evidence},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="rl_release",
            aggregate_id=row.id,
            event_type="release.approved",
            payload={"release_id": str(row.id)},
            correlation_id=self.ctx.correlation_id,
            project_id=row.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def add_backup(self, release_id: UUID, data: BackupCreate) -> BackupConfirmation:
        self.get_release(release_id)
        row = BackupConfirmation(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            release_id=release_id,
            backup_ref=data.backup_ref,
            confirmed=data.confirmed,
            notes=data.notes,
            confirmed_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_backups(self, release_id: UUID) -> list[BackupConfirmation]:
        self.get_release(release_id)
        return list(
            self.db.scalars(
                select(BackupConfirmation).where(
                    BackupConfirmation.organization_id == self.ctx.organization_id,
                    BackupConfirmation.release_id == release_id,
                )
            )
        )

    def add_migration_plan(self, release_id: UUID, data: MigrationPlanCreate) -> MigrationPlan:
        self.get_release(release_id)
        row = MigrationPlan(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            release_id=release_id,
            plan_text=data.plan_text,
            alembic_revision=data.alembic_revision,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_migration_plans(self, release_id: UUID) -> list[MigrationPlan]:
        self.get_release(release_id)
        return list(
            self.db.scalars(
                select(MigrationPlan).where(
                    MigrationPlan.organization_id == self.ctx.organization_id,
                    MigrationPlan.release_id == release_id,
                )
            )
        )

    def start_deployment(self, release_id: UUID, data: DeploymentCreate) -> Deployment:
        release = self.get_release(release_id)
        domain.assert_expected_version(current=release.version, expected=data.expected_version)
        domain.assert_environment(data.environment_code)
        now = datetime.now(UTC)
        if data.environment_code == "production":
            domain.assert_production_may_start(
                release_status=release.status,
                has_approval_evidence=bool(release.approval_evidence),
            )
            backups = [b for b in self.list_backups(release_id) if b.confirmed]
            if not backups:
                raise ValidationAppError(
                    "Production deployment requires a confirmed backup"
                )
            domain.assert_release_transition(from_status=release.status, to_status="deploying")
            release.status = "deploying"
            release.version += 1
            release.updated_by_actor_id = self.ctx.actor_id
            release.updated_at = now
        row = Deployment(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            release_id=release_id,
            environment_code=data.environment_code,
            status="in_progress",
            build_ref=data.build_ref,
            requested_by_actor_id=self.ctx.actor_id,
            started_at=now,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="rl_deploy_start",
            entity_type="rl_release",
            entity_id=release_id,
            payload={"environment_code": data.environment_code, "deployment_id": str(row.id)},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="rl_release",
            aggregate_id=release_id,
            event_type="release.deploy_started",
            payload={
                "release_id": str(release_id),
                "deployment_id": str(row.id),
                "environment_code": data.environment_code,
            },
            correlation_id=self.ctx.correlation_id,
            project_id=release.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_deployments(self, release_id: UUID) -> list[Deployment]:
        self.get_release(release_id)
        return list(
            self.db.scalars(
                select(Deployment)
                .where(
                    Deployment.organization_id == self.ctx.organization_id,
                    Deployment.release_id == release_id,
                )
                .order_by(Deployment.created_at.desc())
            )
        )

    def add_check(self, deployment_id: UUID, data: DeploymentCheckCreate) -> DeploymentCheck:
        deployment = self.db.get(Deployment, deployment_id)
        if deployment is None or deployment.organization_id != self.ctx.organization_id:
            raise NotFoundError("Deployment not found")
        if data.result not in domain.CHECK_RESULTS:
            raise ValidationAppError(f"Invalid check result '{data.result}'")
        row = DeploymentCheck(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            deployment_id=deployment_id,
            check_name=data.check_name,
            result=data.result,
            evidence=data.evidence,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        if data.result == "passed":
            deployment.status = "succeeded"
            deployment.finished_at = datetime.now(UTC)
            release = self.get_release(deployment.release_id)
            if (
                deployment.environment_code == "production"
                and release.status == "deploying"
            ):
                domain.assert_release_transition(from_status="deploying", to_status="deployed")
                release.status = "deployed"
                release.version += 1
                release.updated_by_actor_id = self.ctx.actor_id
                release.updated_at = datetime.now(UTC)
        elif data.result == "failed":
            deployment.status = "failed"
            deployment.finished_at = datetime.now(UTC)
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_checks(self, deployment_id: UUID) -> list[DeploymentCheck]:
        deployment = self.db.get(Deployment, deployment_id)
        if deployment is None or deployment.organization_id != self.ctx.organization_id:
            raise NotFoundError("Deployment not found")
        return list(
            self.db.scalars(
                select(DeploymentCheck).where(
                    DeploymentCheck.organization_id == self.ctx.organization_id,
                    DeploymentCheck.deployment_id == deployment_id,
                )
            )
        )

    def rollback(self, release_id: UUID, data: RollbackCreate) -> Rollback:
        release = self.get_release(release_id)
        domain.assert_expected_version(current=release.version, expected=data.expected_version)
        domain.assert_release_transition(from_status=release.status, to_status="rolled_back")
        release.status = "rolled_back"
        release.version += 1
        release.updated_by_actor_id = self.ctx.actor_id
        release.updated_at = datetime.now(UTC)
        row = Rollback(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            release_id=release_id,
            deployment_id=data.deployment_id,
            reason=data.reason,
            evidence=data.evidence,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="rl_rollback",
            entity_type="rl_release",
            entity_id=release_id,
            payload={"reason": data.reason},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="rl_release",
            aggregate_id=release_id,
            event_type="release.rolled_back",
            payload={"release_id": str(release_id)},
            correlation_id=self.ctx.correlation_id,
            project_id=release.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_rollbacks(self, release_id: UUID) -> list[Rollback]:
        self.get_release(release_id)
        return list(
            self.db.scalars(
                select(Rollback).where(
                    Rollback.organization_id == self.ctx.organization_id,
                    Rollback.release_id == release_id,
                )
            )
        )

    def upsert_completion(
        self, release_id: UUID, data: CompletionReportCreate
    ) -> CompletionReport:
        release = self.get_release(release_id)
        domain.assert_expected_version(current=release.version, expected=data.expected_version)
        row = self.db.scalar(
            select(CompletionReport).where(
                CompletionReport.organization_id == self.ctx.organization_id,
                CompletionReport.release_id == release_id,
            )
        )
        if row is None:
            row = CompletionReport(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                release_id=release_id,
                summary=data.summary,
                client_accepted=data.client_accepted,
                internal_accepted=data.internal_accepted,
                client_acceptance_notes=data.client_acceptance_notes,
                internal_acceptance_notes=data.internal_acceptance_notes,
                created_by_actor_id=self.ctx.actor_id,
            )
            self.uow.add(row)
        else:
            row.summary = data.summary
            row.client_accepted = data.client_accepted
            row.internal_accepted = data.internal_accepted
            row.client_acceptance_notes = data.client_acceptance_notes
            row.internal_acceptance_notes = data.internal_acceptance_notes
            row.updated_at = datetime.now(UTC)

        # AC-003: closure requires both acceptances
        if data.client_accepted and data.internal_accepted:
            if release.status not in {"deployed", "closed"}:
                raise ValidationAppError(
                    "Release must be deployed before closure with dual acceptance"
                )
            if release.status == "deployed":
                domain.assert_release_transition(from_status="deployed", to_status="closed")
                release.status = "closed"
                release.version += 1
                release.updated_by_actor_id = self.ctx.actor_id
                release.updated_at = datetime.now(UTC)
                enqueue_outbox(
                    self.db,
                    organization_id=self.ctx.organization_id,
                    aggregate_type="rl_release",
                    aggregate_id=release_id,
                    event_type="release.closed",
                    payload={"release_id": str(release_id)},
                    correlation_id=self.ctx.correlation_id,
                    project_id=release.project_id,
                )
        self.obs.write_audit(
            action="rl_completion",
            entity_type="rl_release",
            entity_id=release_id,
            payload={
                "client_accepted": data.client_accepted,
                "internal_accepted": data.internal_accepted,
            },
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def get_completion(self, release_id: UUID) -> CompletionReport | None:
        self.get_release(release_id)
        return self.db.scalar(
            select(CompletionReport).where(
                CompletionReport.organization_id == self.ctx.organization_id,
                CompletionReport.release_id == release_id,
            )
        )
