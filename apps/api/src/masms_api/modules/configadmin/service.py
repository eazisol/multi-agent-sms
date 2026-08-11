"""Configuration application service (MOD-140)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from masms_api.errors import NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.configadmin import domain
from masms_api.modules.configadmin.models import (
    ApprovalWorkflowConfig,
    ConfigurationVersion,
    EscalationRule,
    FollowUpRule,
    ReminderRule,
    StatusDefinition,
    TransitionRule,
    WorkflowDefinition,
)
from masms_api.modules.configadmin.schemas import (
    ApprovalWorkflowCreate,
    ConfigurationVersionCreate,
    EscalationRuleCreate,
    FollowUpRuleCreate,
    LiveTransitionCheckResponse,
    ReminderRuleCreate,
    StatusCreate,
    TransitionCreate,
    WorkflowCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class ConfigAdminService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_version(self, data: ConfigurationVersionCreate) -> ConfigurationVersion:
        max_num = self.db.scalar(
            select(func.max(ConfigurationVersion.version_number)).where(
                ConfigurationVersion.organization_id == self.ctx.organization_id
            )
        )
        next_num = int(max_num or 0) + 1
        if data.based_on_version_id is not None:
            base = self._get_version(data.based_on_version_id)
            _ = base
        row = ConfigurationVersion(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            version_number=next_num,
            title=data.title,
            status=domain.STATUS_DRAFT,
            based_on_version_id=data.based_on_version_id,
            change_reason=data.change_reason,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="config_version_create",
            entity_type="cfg_configuration_version",
            entity_id=row.id,
            payload={"version_number": next_num, "title": data.title},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def approve_version(self, version_id: UUID) -> ConfigurationVersion:
        row = self._get_version(version_id)
        domain.assert_can_approve(row.status)
        row.status = domain.STATUS_APPROVED
        row.approved_by_actor_id = self.ctx.actor_id
        row.approved_at = datetime.now(UTC)
        self.uow.add(row)
        self.obs.write_audit(
            action="config_version_approve",
            entity_type="cfg_configuration_version",
            entity_id=row.id,
            payload={"version_number": row.version_number},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def activate_version(self, version_id: UUID) -> ConfigurationVersion:
        row = self._get_version(version_id)
        domain.assert_can_activate(row.status)
        current = self.db.scalar(
            select(ConfigurationVersion).where(
                ConfigurationVersion.organization_id == self.ctx.organization_id,
                ConfigurationVersion.status == domain.STATUS_EFFECTIVE,
            )
        )
        now = datetime.now(UTC)
        if current is not None:
            current.status = domain.STATUS_SUPERSEDED
            current.superseded_at = now
            self.uow.add(current)
        row.status = domain.STATUS_EFFECTIVE
        row.effective_at = now
        self.uow.add(row)
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            event_type="config.version.activated",
            aggregate_type="cfg_configuration_version",
            aggregate_id=row.id,
            payload={"version_number": row.version_number},
            correlation_id=self.ctx.correlation_id,
        )
        self.obs.write_audit(
            action="config_version_activate",
            entity_type="cfg_configuration_version",
            entity_id=row.id,
            payload={"version_number": row.version_number},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def rollback_effective(self, *, restore_version_id: UUID | None = None) -> ConfigurationVersion:
        current = self.db.scalar(
            select(ConfigurationVersion).where(
                ConfigurationVersion.organization_id == self.ctx.organization_id,
                ConfigurationVersion.status == domain.STATUS_EFFECTIVE,
            )
        )
        if current is None:
            raise NotFoundError("No effective configuration to roll back")
        domain.assert_can_rollback(current.status)
        now = datetime.now(UTC)
        current.status = domain.STATUS_ROLLED_BACK
        current.rolled_back_at = now
        self.uow.add(current)

        restored: ConfigurationVersion | None = None
        if restore_version_id is not None:
            restored = self._get_version(restore_version_id)
            if restored.status not in {
                domain.STATUS_SUPERSEDED,
                domain.STATUS_APPROVED,
                domain.STATUS_ROLLED_BACK,
            }:
                raise ValidationAppError(
                    "Restore target must be a prior approved/superseded version"
                )
            restored.status = domain.STATUS_EFFECTIVE
            restored.effective_at = now
            restored.rolled_back_at = None
            self.uow.add(restored)

        self.obs.write_audit(
            action="config_version_rollback",
            entity_type="cfg_configuration_version",
            entity_id=current.id,
            payload={
                "rolled_back_version": current.version_number,
                "restored_version_id": str(restore_version_id) if restore_version_id else None,
            },
        )
        self.uow.commit()
        self.uow.refresh(current)
        return restored or current

    def create_workflow(self, data: WorkflowCreate) -> WorkflowDefinition:
        version = self._get_version(data.configuration_version_id)
        domain.assert_draft_editable(version.status)
        row = WorkflowDefinition(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            configuration_version_id=version.id,
            code=data.code,
            title=data.title,
            entity_type=data.entity_type,
            description=data.description,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="config_workflow_create",
            entity_type="cfg_workflow_definition",
            entity_id=row.id,
            payload={"code": data.code, "version_id": str(version.id)},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_status(self, data: StatusCreate) -> StatusDefinition:
        version = self._get_version(data.configuration_version_id)
        domain.assert_draft_editable(version.status)
        workflow = self._get_workflow(data.workflow_definition_id, version.id)
        row = StatusDefinition(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            configuration_version_id=version.id,
            workflow_definition_id=workflow.id,
            code=data.code,
            title=data.title,
            is_terminal=data.is_terminal,
            sort_order=data.sort_order,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_transition(self, data: TransitionCreate) -> TransitionRule:
        version = self._get_version(data.configuration_version_id)
        domain.assert_draft_editable(version.status)
        workflow = self._get_workflow(data.workflow_definition_id, version.id)
        row = TransitionRule(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            configuration_version_id=version.id,
            workflow_definition_id=workflow.id,
            from_status_code=data.from_status_code,
            to_status_code=data.to_status_code,
            requires_reason=data.requires_reason,
            requires_approval=data.requires_approval,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_followup(self, data: FollowUpRuleCreate) -> FollowUpRule:
        version = self._get_version(data.configuration_version_id)
        domain.assert_draft_editable(version.status)
        domain.assert_positive_hours(data.due_offset_hours, field="due_offset_hours")
        row = FollowUpRule(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            configuration_version_id=version.id,
            workflow_code=data.workflow_code,
            trigger_status_code=data.trigger_status_code,
            due_offset_hours=data.due_offset_hours,
            required_response=data.required_response,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_reminder(self, data: ReminderRuleCreate) -> ReminderRule:
        version = self._get_version(data.configuration_version_id)
        domain.assert_draft_editable(version.status)
        row = ReminderRule(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            configuration_version_id=version.id,
            workflow_code=data.workflow_code,
            offset_hours_before_due=data.offset_hours_before_due,
            channel=data.channel,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_escalation(self, data: EscalationRuleCreate) -> EscalationRule:
        version = self._get_version(data.configuration_version_id)
        domain.assert_draft_editable(version.status)
        row = EscalationRule(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            configuration_version_id=version.id,
            workflow_code=data.workflow_code,
            after_hours_overdue=data.after_hours_overdue,
            escalate_to_role_code=data.escalate_to_role_code,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_approval_workflow(self, data: ApprovalWorkflowCreate) -> ApprovalWorkflowConfig:
        version = self._get_version(data.configuration_version_id)
        domain.assert_draft_editable(version.status)
        row = ApprovalWorkflowConfig(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            configuration_version_id=version.id,
            code=data.code,
            title=data.title,
            action_code=data.action_code,
            steps_json=data.steps,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def check_live_transition(
        self,
        *,
        workflow_code: str,
        from_status_code: str,
        to_status_code: str,
    ) -> LiveTransitionCheckResponse:
        effective = self.db.scalar(
            select(ConfigurationVersion).where(
                ConfigurationVersion.organization_id == self.ctx.organization_id,
                ConfigurationVersion.status == domain.STATUS_EFFECTIVE,
            )
        )
        if effective is None:
            return LiveTransitionCheckResponse(
                allowed=False,
                configuration_version_id=None,
                configuration_status=None,
                reason="No effective configuration version",
            )
        domain.assert_live_config(effective.status)
        workflow = self.db.scalar(
            select(WorkflowDefinition).where(
                WorkflowDefinition.organization_id == self.ctx.organization_id,
                WorkflowDefinition.configuration_version_id == effective.id,
                WorkflowDefinition.code == workflow_code,
                WorkflowDefinition.status == "active",
            )
        )
        if workflow is None:
            return LiveTransitionCheckResponse(
                allowed=False,
                configuration_version_id=effective.id,
                configuration_status=effective.status,
                reason=f"Workflow '{workflow_code}' not found in effective config",
            )
        rule = self.db.scalar(
            select(TransitionRule).where(
                TransitionRule.organization_id == self.ctx.organization_id,
                TransitionRule.configuration_version_id == effective.id,
                TransitionRule.workflow_definition_id == workflow.id,
                TransitionRule.from_status_code == from_status_code,
                TransitionRule.to_status_code == to_status_code,
                TransitionRule.status == "active",
            )
        )
        if rule is None:
            return LiveTransitionCheckResponse(
                allowed=False,
                configuration_version_id=effective.id,
                configuration_status=effective.status,
                reason="Transition not defined in effective configuration",
            )
        return LiveTransitionCheckResponse(
            allowed=True,
            configuration_version_id=effective.id,
            configuration_status=effective.status,
            reason="allowed by effective configuration",
        )

    def _get_version(self, version_id: UUID) -> ConfigurationVersion:
        row = self.db.scalar(
            select(ConfigurationVersion).where(ConfigurationVersion.id == version_id)
        )
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Configuration version not found")
        return row

    def _get_workflow(self, workflow_id: UUID, version_id: UUID) -> WorkflowDefinition:
        row = self.db.scalar(
            select(WorkflowDefinition).where(WorkflowDefinition.id == workflow_id)
        )
        if (
            row is None
            or row.organization_id != self.ctx.organization_id
            or row.configuration_version_id != version_id
        ):
            raise NotFoundError("Workflow definition not found in this configuration version")
        return row
