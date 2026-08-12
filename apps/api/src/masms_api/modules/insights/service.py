"""Insights application service (MOD-450)."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.insights import domain
from masms_api.modules.insights.models import (
    ActivityEvent,
    DashboardSnapshot,
    ExportJob,
    ProjectHealth,
    Report,
    SavedFilter,
    SearchDocument,
)
from masms_api.modules.insights.schemas import (
    ActivityCreate,
    DashboardRefresh,
    DashboardSnapshotRead,
    ExportCreate,
    ProjectHealthUpsert,
    ReportCreate,
    SavedFilterCreate,
    SearchIndexCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class InsightsService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def _count_model(self, model: type[Any], *, open_statuses: frozenset[str] | None = None) -> int:
        try:
            stmt = select(func.count()).select_from(model).where(
                model.organization_id == self.ctx.organization_id  # type: ignore[attr-defined]
            )
            if open_statuses is not None and hasattr(model, "status"):
                stmt = stmt.where(model.status.in_(open_statuses))  # type: ignore[attr-defined]
            return int(self.db.scalar(stmt) or 0)
        except Exception:
            return 0

    def _collect_source_metrics(self, project_id: UUID | None = None) -> dict[str, Any]:
        metrics: dict[str, Any] = {
            "projects_total": 0,
            "tickets_open": 0,
            "bugs_open": 0,
            "followups_open": 0,
            "approvals_pending": 0,
            "queries_open": 0,
            "reconciled": True,
        }
        try:
            from masms_api.modules.projects.models import Project

            stmt = select(func.count()).select_from(Project).where(
                Project.organization_id == self.ctx.organization_id
            )
            if project_id is not None:
                stmt = stmt.where(Project.id == project_id)
            metrics["projects_total"] = int(self.db.scalar(stmt) or 0)
        except Exception:
            metrics["projects_total"] = 0

        try:
            from masms_api.modules.tickets.models import Ticket

            open_ticket = frozenset(
                {"backlog", "todo", "in_progress", "blocked", "in_review", "open"}
            )
            stmt = select(func.count()).select_from(Ticket).where(
                Ticket.organization_id == self.ctx.organization_id,
                Ticket.status.in_(open_ticket),
            )
            if project_id is not None:
                stmt = stmt.where(Ticket.project_id == project_id)
            metrics["tickets_open"] = int(self.db.scalar(stmt) or 0)
        except Exception:
            metrics["tickets_open"] = 0

        try:
            from masms_api.modules.bugs.models import Bug

            open_bug = frozenset({"open", "triaged", "in_progress", "reopened"})
            stmt = select(func.count()).select_from(Bug).where(
                Bug.organization_id == self.ctx.organization_id,
                Bug.status.in_(open_bug),
            )
            if project_id is not None:
                stmt = stmt.where(Bug.project_id == project_id)
            metrics["bugs_open"] = int(self.db.scalar(stmt) or 0)
        except Exception:
            metrics["bugs_open"] = 0

        try:
            from masms_api.modules.followups.models import FollowUp

            open_fu = frozenset({"open", "waiting", "overdue"})
            stmt = select(func.count()).select_from(FollowUp).where(
                FollowUp.organization_id == self.ctx.organization_id,
                FollowUp.status.in_(open_fu),
            )
            if project_id is not None:
                stmt = stmt.where(FollowUp.project_id == project_id)
            metrics["followups_open"] = int(self.db.scalar(stmt) or 0)
        except Exception:
            metrics["followups_open"] = 0

        try:
            from masms_api.modules.approvalgates.models import ApprovalRequest

            stmt = select(func.count()).select_from(ApprovalRequest).where(
                ApprovalRequest.organization_id == self.ctx.organization_id,
                ApprovalRequest.status == "pending",
            )
            if project_id is not None and hasattr(ApprovalRequest, "project_id"):
                stmt = stmt.where(ApprovalRequest.project_id == project_id)
            metrics["approvals_pending"] = int(self.db.scalar(stmt) or 0)
        except Exception:
            metrics["approvals_pending"] = 0

        try:
            from masms_api.modules.queries.models import ClientQuery

            open_q = frozenset(
                {"received", "triaged", "in_progress", "waiting", "open", "active"}
            )
            stmt = select(func.count()).select_from(ClientQuery).where(
                ClientQuery.organization_id == self.ctx.organization_id,
                ClientQuery.status.in_(open_q),
            )
            metrics["queries_open"] = int(self.db.scalar(stmt) or 0)
        except Exception:
            metrics["queries_open"] = 0

        return metrics

    def _to_dashboard_read(self, row: DashboardSnapshot) -> DashboardSnapshotRead:
        try:
            metrics = json.loads(row.metric_json)
            if not isinstance(metrics, dict):
                metrics = {"raw": row.metric_json}
        except json.JSONDecodeError:
            metrics = {"raw": row.metric_json}
        return DashboardSnapshotRead(
            id=row.id,
            organization_id=row.organization_id,
            scope_key=row.scope_key,
            project_id=row.project_id,
            metrics=metrics,
            source_hash=row.source_hash,
            computed_at=row.computed_at,
            refreshed_at=row.refreshed_at,
            is_fresh=domain.is_snapshot_fresh(row.computed_at),
            version=row.version,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def refresh_dashboard(self, data: DashboardRefresh | None = None) -> DashboardSnapshotRead:
        payload = data or DashboardRefresh()
        now = datetime.now(UTC)
        metrics = self._collect_source_metrics(payload.project_id)
        metric_json = json.dumps(metrics, sort_keys=True)
        source_hash = hashlib.sha256(metric_json.encode("utf-8")).hexdigest()
        scope_key = domain.scope_key_for_project(payload.project_id)

        row = self.db.scalar(
            select(DashboardSnapshot).where(
                DashboardSnapshot.organization_id == self.ctx.organization_id,
                DashboardSnapshot.scope_key == scope_key,
            )
        )
        if row is None:
            row = DashboardSnapshot(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                scope_key=scope_key,
                project_id=payload.project_id,
                metric_json=metric_json,
                source_hash=source_hash,
                computed_at=now,
                refreshed_at=now,
                created_by_actor_id=self.ctx.actor_id,
                updated_by_actor_id=self.ctx.actor_id,
            )
            self.uow.add(row)
        else:
            row.metric_json = metric_json
            row.source_hash = source_hash
            row.computed_at = now
            row.refreshed_at = now
            row.project_id = payload.project_id
            row.version += 1
            row.updated_by_actor_id = self.ctx.actor_id
            row.updated_at = now

        self.obs.write_audit(
            action="rp_dashboard_refresh",
            entity_type="rp_dashboard_snapshot",
            entity_id=row.id,
            payload={"scope_key": scope_key, "metrics": metrics},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="rp_dashboard_snapshot",
            aggregate_id=row.id,
            event_type="insights.dashboard.refreshed",
            payload={"scope_key": scope_key, "projects_total": metrics.get("projects_total")},
            correlation_id=self.ctx.correlation_id,
            project_id=payload.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return self._to_dashboard_read(row)

    def get_dashboard(self, project_id: UUID | None = None) -> DashboardSnapshotRead:
        scope_key = domain.scope_key_for_project(project_id)
        row = self.db.scalar(
            select(DashboardSnapshot).where(
                DashboardSnapshot.organization_id == self.ctx.organization_id,
                DashboardSnapshot.scope_key == scope_key,
            )
        )
        if row is None:
            raise NotFoundError("Dashboard snapshot not found; refresh first")
        return self._to_dashboard_read(row)

    def upsert_project_health(self, data: ProjectHealthUpsert) -> ProjectHealth:
        domain.assert_health_status(data.health_status)
        domain.assert_score(data.score)
        now = datetime.now(UTC)
        row = self.db.scalar(
            select(ProjectHealth).where(
                ProjectHealth.organization_id == self.ctx.organization_id,
                ProjectHealth.project_id == data.project_id,
            )
        )
        if row is None:
            row = ProjectHealth(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                project_id=data.project_id,
                health_status=data.health_status,
                score=data.score,
                blockers_count=data.blockers_count,
                open_tickets=data.open_tickets,
                open_bugs=data.open_bugs,
                overdue_followups=data.overdue_followups,
                notes=data.notes,
                computed_at=now,
                created_by_actor_id=self.ctx.actor_id,
                updated_by_actor_id=self.ctx.actor_id,
            )
            self.uow.add(row)
        else:
            domain.assert_expected_version(current=row.version, expected=data.expected_version)
            row.health_status = data.health_status
            row.score = data.score
            row.blockers_count = data.blockers_count
            row.open_tickets = data.open_tickets
            row.open_bugs = data.open_bugs
            row.overdue_followups = data.overdue_followups
            row.notes = data.notes
            row.computed_at = now
            row.version += 1
            row.updated_by_actor_id = self.ctx.actor_id
            row.updated_at = now

        self.obs.write_audit(
            action="rp_project_health_upsert",
            entity_type="rp_project_health",
            entity_id=row.id,
            payload={"project_id": str(data.project_id), "health_status": data.health_status},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="rp_project_health",
            aggregate_id=row.id,
            event_type="insights.project_health.upserted",
            payload={"project_id": str(data.project_id), "score": data.score},
            correlation_id=self.ctx.correlation_id,
            project_id=data.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_project_health(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[ProjectHealth], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(ProjectHealth).where(
            ProjectHealth.organization_id == self.ctx.organization_id
        )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(ProjectHealth.updated_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def get_project_health(self, project_id: UUID) -> ProjectHealth:
        row = self.db.scalar(
            select(ProjectHealth).where(
                ProjectHealth.organization_id == self.ctx.organization_id,
                ProjectHealth.project_id == project_id,
            )
        )
        if row is None:
            raise NotFoundError("Project health not found")
        return row

    def create_saved_filter(self, data: SavedFilterCreate) -> SavedFilter:
        existing = self.db.scalar(
            select(SavedFilter).where(
                SavedFilter.organization_id == self.ctx.organization_id,
                SavedFilter.owner_actor_id == self.ctx.actor_id,
                SavedFilter.name == data.name.strip(),
            )
        )
        if existing is not None:
            raise ConflictError(f"Saved filter named '{data.name}' already exists")
        row = SavedFilter(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            owner_actor_id=self.ctx.actor_id,
            name=data.name.strip(),
            module_key=data.module_key.strip(),
            filter_json=data.filter_json,
            is_shared=data.is_shared,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="rp_saved_filter_create",
            entity_type="rp_saved_filter",
            entity_id=row.id,
            payload={"name": row.name, "module_key": row.module_key},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="rp_saved_filter",
            aggregate_id=row.id,
            event_type="insights.saved_filter.created",
            payload={"name": row.name},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_saved_filters(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[SavedFilter], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(SavedFilter).where(
            SavedFilter.organization_id == self.ctx.organization_id,
            or_(
                SavedFilter.owner_actor_id == self.ctx.actor_id,
                SavedFilter.is_shared.is_(True),
            ),
        )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(SavedFilter.updated_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def delete_saved_filter(self, filter_id: UUID) -> None:
        row = self.db.get(SavedFilter, filter_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Saved filter not found")
        if row.owner_actor_id != self.ctx.actor_id:
            raise ValidationAppError("Only the owner can delete a saved filter")
        self.obs.write_audit(
            action="rp_saved_filter_delete",
            entity_type="rp_saved_filter",
            entity_id=row.id,
            payload={"name": row.name},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="rp_saved_filter",
            aggregate_id=row.id,
            event_type="insights.saved_filter.deleted",
            payload={"name": row.name},
            correlation_id=self.ctx.correlation_id,
        )
        self.db.delete(row)
        self.uow.commit()

    def index_search_document(self, data: SearchIndexCreate) -> SearchDocument:
        domain.assert_entity_type(data.entity_type)
        domain.assert_classification(data.classification)
        now = datetime.now(UTC)
        row = self.db.scalar(
            select(SearchDocument).where(
                SearchDocument.organization_id == self.ctx.organization_id,
                SearchDocument.entity_type == data.entity_type,
                SearchDocument.entity_id == data.entity_id,
            )
        )
        if row is None:
            row = SearchDocument(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                project_id=data.project_id,
                entity_type=data.entity_type,
                entity_id=data.entity_id,
                title=data.title.strip(),
                body_preview=data.body_preview,
                classification=data.classification,
                indexed_at=now,
                created_by_actor_id=self.ctx.actor_id,
            )
            self.uow.add(row)
        else:
            row.title = data.title.strip()
            row.body_preview = data.body_preview
            row.project_id = data.project_id
            row.classification = data.classification
            row.indexed_at = now

        self.obs.write_audit(
            action="rp_search_index",
            entity_type="rp_search_document",
            entity_id=row.id,
            payload={"entity_type": data.entity_type, "entity_id": str(data.entity_id)},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="rp_search_document",
            aggregate_id=row.id,
            event_type="insights.search.indexed",
            payload={"entity_type": data.entity_type, "entity_id": str(data.entity_id)},
            correlation_id=self.ctx.correlation_id,
            project_id=data.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def global_search(
        self, *, q: str, limit: int = 20, offset: int = 0
    ) -> tuple[list[SearchDocument], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        term = q.strip()
        if not term:
            raise ValidationAppError("Search query q is required")
        like = f"%{term}%"
        stmt = select(SearchDocument).where(
            SearchDocument.organization_id == self.ctx.organization_id,
            or_(
                SearchDocument.title.ilike(like),
                SearchDocument.body_preview.ilike(like),
            ),
        )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(SearchDocument.indexed_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def record_activity(self, data: ActivityCreate) -> ActivityEvent:
        now = datetime.now(UTC)
        row = ActivityEvent(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            actor_id=self.ctx.actor_id,
            event_type=data.event_type.strip(),
            entity_type=data.entity_type.strip(),
            entity_id=data.entity_id,
            summary=data.summary.strip(),
            occurred_at=data.occurred_at or now,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="rp_activity_record",
            entity_type="rp_activity_event",
            entity_id=row.id,
            payload={"event_type": row.event_type, "entity_type": row.entity_type},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="rp_activity_event",
            aggregate_id=row.id,
            event_type="insights.activity.recorded",
            payload={"event_type": row.event_type},
            correlation_id=self.ctx.correlation_id,
            project_id=data.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_activity(
        self,
        *,
        project_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[ActivityEvent], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(ActivityEvent).where(
            ActivityEvent.organization_id == self.ctx.organization_id
        )
        if project_id is not None:
            stmt = stmt.where(ActivityEvent.project_id == project_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(ActivityEvent.occurred_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def create_report(self, data: ReportCreate) -> Report:
        domain.assert_report_status(data.status)
        existing = self.db.scalar(
            select(Report).where(
                Report.organization_id == self.ctx.organization_id,
                Report.code == data.code.strip(),
            )
        )
        if existing is not None:
            raise ConflictError(f"Report code '{data.code}' already exists")
        row = Report(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code.strip(),
            title=data.title.strip(),
            report_type=data.report_type.strip(),
            definition_json=data.definition_json,
            status=data.status,
            owner_actor_id=self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="rp_report_create",
            entity_type="rp_report",
            entity_id=row.id,
            payload={"code": row.code, "status": row.status},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="rp_report",
            aggregate_id=row.id,
            event_type="insights.report.created",
            payload={"code": row.code},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_reports(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[Report], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(Report).where(Report.organization_id == self.ctx.organization_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(stmt.order_by(Report.updated_at.desc()).limit(limit).offset(offset))
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def get_report(self, report_id: UUID) -> Report:
        row = self.db.get(Report, report_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Report not found")
        return row

    def create_export(self, data: ExportCreate) -> ExportJob:
        domain.assert_export_format(data.export_format)
        now = datetime.now(UTC)
        report: Report | None = None
        if data.report_id is not None:
            report = self.get_report(data.report_id)

        payload: dict[str, Any] = {
            "organization_id": str(self.ctx.organization_id),
            "export_format": data.export_format,
        }
        row_count = 0
        if data.include_dashboard_metrics:
            metrics = self._collect_source_metrics()
            payload["metrics"] = metrics
            row_count = 1
        if report is not None:
            payload["report"] = {
                "id": str(report.id),
                "code": report.code,
                "title": report.title,
                "report_type": report.report_type,
                "status": report.status,
            }
            row_count += 1

        # AC-003: payload must only include this org's data (organization_id baked in).
        preview = json.dumps(payload, sort_keys=True)[:4000]
        row = ExportJob(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            report_id=data.report_id,
            export_format=data.export_format,
            status="ready",
            payload_preview=preview,
            row_count=row_count,
            requested_by_actor_id=self.ctx.actor_id,
            completed_at=now,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="rp_export_create",
            entity_type="rp_export",
            entity_id=row.id,
            payload={"export_format": data.export_format, "row_count": row_count},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="rp_export",
            aggregate_id=row.id,
            event_type="insights.export.ready",
            payload={"export_format": data.export_format, "status": "ready"},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_exports(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[ExportJob], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(ExportJob).where(ExportJob.organization_id == self.ctx.organization_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(ExportJob.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def get_export(self, export_id: UUID) -> ExportJob:
        row = self.db.get(ExportJob, export_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Export not found")
        return row
