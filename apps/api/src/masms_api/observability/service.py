"""Observability application service — append-only writes + tenant-scoped queries."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from masms_api.deps import RequestContext
from masms_api.errors import ForbiddenError, NotFoundError
from masms_api.kernel.outbox import OutboxMessage, relay_pending_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.observability.models import (
    ActivityEvent,
    AgentRun,
    AuditLog,
    StatusHistory,
)
from masms_api.observability.writer import ObservabilityWriter


class ObservabilityService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.writer = ObservabilityWriter(db, ctx)

    def list_audit_logs(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[AuditLog], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [AuditLog.organization_id == self.ctx.organization_id]
        total = self.db.scalar(select(func.count()).select_from(AuditLog).where(*filters)) or 0
        rows = self.db.scalars(
            select(AuditLog)
            .where(*filters)
            .order_by(AuditLog.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def list_activity(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[ActivityEvent], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [ActivityEvent.organization_id == self.ctx.organization_id]
        total = self.db.scalar(select(func.count()).select_from(ActivityEvent).where(*filters)) or 0
        rows = self.db.scalars(
            select(ActivityEvent)
            .where(*filters)
            .order_by(ActivityEvent.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def list_status_history(
        self,
        *,
        entity_type: str,
        entity_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[StatusHistory], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [
            StatusHistory.organization_id == self.ctx.organization_id,
            StatusHistory.entity_type == entity_type,
            StatusHistory.entity_id == entity_id,
        ]
        total = self.db.scalar(select(func.count()).select_from(StatusHistory).where(*filters)) or 0
        rows = self.db.scalars(
            select(StatusHistory)
            .where(*filters)
            .order_by(StatusHistory.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def start_agent_run(self, *, agent_name: str, input_summary: dict[str, object]) -> AgentRun:
        run = self.writer.start_agent_run(agent_name=agent_name, input_summary=input_summary)
        self.uow.flush()
        self.writer.write_audit(
            action="agent_run_start",
            entity_type="agent_run",
            entity_id=run.id,
            payload={"agent_name": agent_name, "api_token": "should-redact"},
        )
        self.writer.write_activity(
            activity_type="agent_run_started",
            summary=f"Agent '{agent_name}' started",
            entity_type="agent_run",
            entity_id=run.id,
        )
        self.uow.commit()
        self.uow.refresh(run)
        return run

    def finish_agent_run(
        self,
        run_id: UUID,
        *,
        status: str,
        output_summary: dict[str, object],
        error_summary: str | None,
    ) -> AgentRun:
        run = self.db.scalar(
            select(AgentRun).where(
                AgentRun.id == run_id,
                AgentRun.organization_id == self.ctx.organization_id,
            )
        )
        if run is None:
            raise NotFoundError("Agent run not found")
        self.writer.finish_agent_run(
            run,
            status=status,
            output_summary=output_summary,
            error_summary=error_summary,
        )
        self.writer.write_activity(
            activity_type="agent_run_finished",
            summary=f"Agent '{run.agent_name}' finished as {status}",
            entity_type="agent_run",
            entity_id=run.id,
        )
        self.uow.commit()
        self.uow.refresh(run)
        return run

    def refuse_audit_mutation(self) -> None:
        raise ForbiddenError("Audit logs are append-only for operational roles")

    def relay_outbox(self, *, limit: int = 100) -> list[OutboxMessage]:
        rows = relay_pending_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            limit=limit,
        )
        if rows:
            self.writer.write_audit(
                action="outbox_relay",
                entity_type="sys_outbox_messages",
                entity_id=rows[0].id,
                payload={"published_count": len(rows)},
            )
            self.uow.commit()
        return rows
