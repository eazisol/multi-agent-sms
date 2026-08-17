"""Application service for MOD-520 Jira integration."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, ForbiddenError, NotFoundError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.jira import domain
from masms_api.modules.jira.client import JiraClient, get_jira_client
from masms_api.modules.jira.models import JiraCommentSync, JiraIssuePush, JiraStatusConflict
from masms_api.modules.jira.schemas import (
    JiraCommentSyncCreate,
    JiraIssuePushCreate,
    JiraStatusWebhookIn,
)


class JiraService:
    def __init__(
        self,
        db: Session,
        ctx: RequestContext,
        jira_client: JiraClient | None = None,
    ) -> None:
        self.db = db
        self.ctx = ctx
        self.jira_client = jira_client or get_jira_client()
        self.uow = SqlAlchemyUnitOfWork(db)
        apply_tenant_rls(db, ctx.organization_id)

    def _get_issue_push(self, issue_push_id: UUID) -> JiraIssuePush:
        row = self.db.get(JiraIssuePush, issue_push_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Jira issue push not found")
        return row

    def push_issue(self, data: JiraIssuePushCreate) -> JiraIssuePush:
        domain.assert_approved_for_push(data.approval_status)
        existing = self.db.scalar(
            select(JiraIssuePush).where(
                JiraIssuePush.organization_id == self.ctx.organization_id,
                JiraIssuePush.internal_ticket_id == data.internal_ticket_id,
            )
        )
        if existing is not None:
            return existing
        issue_key = self.jira_client.create_issue(
            internal_ticket_id=data.internal_ticket_id,
            summary=data.summary,
            simulated_key=data.simulated_jira_key,
        )
        row = JiraIssuePush(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            internal_ticket_id=data.internal_ticket_id,
            jira_issue_key=issue_key,
            summary=data.summary,
            approval_status=data.approval_status,
            push_status="pushed",
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_issue_pushes(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[JiraIssuePush], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(JiraIssuePush).where(
            JiraIssuePush.organization_id == self.ctx.organization_id
        )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(JiraIssuePush.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def receive_status_webhook(
        self,
        data: JiraStatusWebhookIn,
        *,
        raw_body: bytes = b"",
        signature: str | None = None,
    ) -> JiraStatusConflict:
        try:
            self.jira_client.verify_webhook(body=raw_body, signature=signature)
        except PermissionError as exc:
            raise ForbiddenError(str(exc)) from exc
        self._get_issue_push(data.issue_push_id)
        conflict = JiraStatusConflict(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            issue_push_id=data.issue_push_id,
            external_status=data.external_status,
            attempted_internal_status=data.attempted_internal_status,
            conflict_reason="Inbound Jira status cannot mutate internal workflow status",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(conflict)
        self.uow.commit()
        self.db.refresh(conflict)
        return conflict

    def create_comment_sync(self, data: JiraCommentSyncCreate) -> JiraCommentSync:
        issue = self._get_issue_push(data.issue_push_id)
        now = datetime.now(UTC)
        failed = data.force_fail
        if not failed:
            try:
                self.jira_client.add_comment(
                    issue_key=issue.jira_issue_key,
                    comment_text=data.comment_text,
                )
            except RuntimeError:
                failed = True
        row = JiraCommentSync(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            issue_push_id=data.issue_push_id,
            comment_text=data.comment_text,
            sync_status="failed" if failed else "synced",
            retry_count=1,
            failure_reason="Jira comment sync failed" if failed else None,
            last_attempt_at=now,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_comment_syncs(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[JiraCommentSync], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(JiraCommentSync).where(
            JiraCommentSync.organization_id == self.ctx.organization_id
        )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(JiraCommentSync.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def retry_comment_sync(self, sync_id: UUID) -> JiraCommentSync:
        row = self.db.get(JiraCommentSync, sync_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Jira comment sync not found")
        if row.sync_status != "failed":
            raise ConflictError("Only failed comment sync records can be retried")
        issue = self._get_issue_push(row.issue_push_id)
        row.retry_count += 1
        row.last_attempt_at = datetime.now(UTC)
        row.updated_by_actor_id = self.ctx.actor_id
        try:
            self.jira_client.add_comment(
                issue_key=issue.jira_issue_key,
                comment_text=row.comment_text,
            )
            row.sync_status = "synced"
            row.failure_reason = None
        except RuntimeError:
            row.failure_reason = "Jira comment sync failed"
        self.uow.commit()
        self.db.refresh(row)
        return row
