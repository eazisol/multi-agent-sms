"""Append-only observability writers (MOD-040). No update/delete APIs for ops roles."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from masms_api.kernel.context import RequestContext
from masms_api.observability.models import (
    ActivityEvent,
    AgentRun,
    AuditLog,
    IntegrationEvent,
    StatusHistory,
)
from masms_api.observability.redact import redact_mapping


class ObservabilityWriter:
    """Insert-only helpers used by application services."""

    def __init__(self, session: Session, ctx: RequestContext) -> None:
        self.session = session
        self.ctx = ctx

    def write_audit(
        self,
        *,
        action: str,
        entity_type: str,
        entity_id: UUID,
        entity_version: int | None = None,
        reason: str | None = None,
        source: str = "api",
        payload: dict[str, Any] | None = None,
        project_id: UUID | None = None,
    ) -> AuditLog:
        row = AuditLog(
            organization_id=self.ctx.organization_id,
            project_id=project_id or self.ctx.tenant.project_id,
            actor_id=self.ctx.actor_id,
            actor_kind=self.ctx.actor_kind.value,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_version=entity_version,
            reason=reason,
            source=source,
            correlation_id=self.ctx.correlation_id,
            payload_redacted=redact_mapping(payload),
        )
        self.session.add(row)
        return row

    def write_activity(
        self,
        *,
        activity_type: str,
        summary: str,
        entity_type: str | None = None,
        entity_id: UUID | None = None,
        payload: dict[str, Any] | None = None,
        project_id: UUID | None = None,
    ) -> ActivityEvent:
        row = ActivityEvent(
            organization_id=self.ctx.organization_id,
            project_id=project_id or self.ctx.tenant.project_id,
            actor_id=self.ctx.actor_id,
            actor_kind=self.ctx.actor_kind.value,
            activity_type=activity_type,
            summary=summary,
            entity_type=entity_type,
            entity_id=entity_id,
            correlation_id=self.ctx.correlation_id,
            payload_redacted=redact_mapping(payload),
        )
        self.session.add(row)
        return row

    def write_status_history(
        self,
        *,
        entity_type: str,
        entity_id: UUID,
        previous_status: str | None,
        next_status: str,
        reason: str | None = None,
        rule: str | None = None,
        project_id: UUID | None = None,
    ) -> StatusHistory:
        row = StatusHistory(
            organization_id=self.ctx.organization_id,
            project_id=project_id or self.ctx.tenant.project_id,
            entity_type=entity_type,
            entity_id=entity_id,
            previous_status=previous_status,
            next_status=next_status,
            actor_id=self.ctx.actor_id,
            actor_kind=self.ctx.actor_kind.value,
            reason=reason,
            rule=rule,
            correlation_id=self.ctx.correlation_id,
        )
        self.session.add(row)
        return row

    def start_agent_run(
        self,
        *,
        agent_name: str,
        input_summary: dict[str, Any] | None = None,
        project_id: UUID | None = None,
    ) -> AgentRun:
        row = AgentRun(
            organization_id=self.ctx.organization_id,
            project_id=project_id or self.ctx.tenant.project_id,
            agent_name=agent_name,
            actor_id=self.ctx.actor_id,
            status="started",
            correlation_id=self.ctx.correlation_id,
            input_summary_redacted=redact_mapping(input_summary),
        )
        self.session.add(row)
        return row

    def finish_agent_run(
        self,
        run: AgentRun,
        *,
        status: str,
        output_summary: dict[str, Any] | None = None,
        error_summary: str | None = None,
    ) -> AgentRun:
        if run.organization_id != self.ctx.organization_id:
            raise PermissionError("Agent run outside tenant scope")
        run.status = status
        run.output_summary_redacted = redact_mapping(output_summary)
        run.error_summary = error_summary
        run.finished_at = datetime.now(UTC)
        self.session.add(run)
        return run

    def write_integration_event(
        self,
        *,
        provider: str,
        direction: str,
        event_type: str,
        status: str = "received",
        payload: dict[str, Any] | None = None,
        error_summary: str | None = None,
        project_id: UUID | None = None,
    ) -> IntegrationEvent:
        row = IntegrationEvent(
            organization_id=self.ctx.organization_id,
            project_id=project_id or self.ctx.tenant.project_id,
            provider=provider,
            direction=direction,
            event_type=event_type,
            status=status,
            correlation_id=self.ctx.correlation_id,
            payload_redacted=redact_mapping(payload),
            error_summary=error_summary,
        )
        self.session.add(row)
        return row
