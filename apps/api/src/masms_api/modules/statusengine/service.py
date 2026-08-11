"""Status / transition engine application service (MOD-320)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.configadmin import domain as config_domain
from masms_api.modules.configadmin.models import (
    ConfigurationVersion,
    StatusDefinition,
    TransitionRule,
    WorkflowDefinition,
)
from masms_api.modules.statusengine import domain
from masms_api.modules.statusengine.models import (
    AvailableActionsSnapshot,
    EntityState,
    HoldRecord,
    ReopenRecord,
    StatusHistory,
    WorkflowBinding,
)
from masms_api.modules.statusengine.schemas import (
    AvailableAction,
    AvailableActionsRead,
    EntityStateInit,
    HoldCreate,
    HoldRelease,
    ReopenApply,
    ResolveWorkflowRead,
    TransitionApply,
    WorkflowBindingCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class StatusEngineService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_binding(self, data: WorkflowBindingCreate) -> WorkflowBinding:
        row = WorkflowBinding(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            entity_type=data.entity_type.strip(),
            project_id=data.project_id,
            workflow_code=data.workflow_code.strip(),
            priority=data.priority,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="wfe_binding_create",
            entity_type="wfe_workflow_binding",
            entity_id=row.id,
            payload={
                "entity_type": row.entity_type,
                "workflow_code": row.workflow_code,
                "project_id": str(row.project_id) if row.project_id else None,
            },
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_bindings(self, *, entity_type: str | None = None) -> list[WorkflowBinding]:
        stmt = select(WorkflowBinding).where(
            WorkflowBinding.organization_id == self.ctx.organization_id,
            WorkflowBinding.status == "active",
        )
        if entity_type:
            stmt = stmt.where(WorkflowBinding.entity_type == entity_type)
        stmt = stmt.order_by(WorkflowBinding.priority.asc(), WorkflowBinding.created_at.asc())
        return list(self.db.scalars(stmt).all())

    def resolve_workflow(
        self, *, entity_type: str, project_id: UUID | None = None
    ) -> ResolveWorkflowRead:
        binding = self._resolve_binding(entity_type=entity_type, project_id=project_id)
        effective = self._get_effective_version(required=False)
        return ResolveWorkflowRead(
            entity_type=entity_type,
            project_id=project_id,
            workflow_code=binding.workflow_code,
            binding_id=binding.id,
            configuration_version_id=effective.id if effective else None,
        )

    def initialize_state(self, data: EntityStateInit) -> EntityState:
        existing = self._get_state_optional(data.entity_type, data.entity_id)
        if existing is not None:
            raise ConflictError("Entity already has a workflow state")

        if data.workflow_code:
            workflow_code = data.workflow_code.strip()
        else:
            binding = self._resolve_binding(
                entity_type=data.entity_type, project_id=data.project_id
            )
            workflow_code = binding.workflow_code

        effective = self._get_effective_version(required=True)
        assert effective is not None
        workflow = self._get_workflow(effective.id, workflow_code)
        status = self._get_status(effective.id, workflow.id, data.initial_status_code)

        row = EntityState(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            entity_type=data.entity_type.strip(),
            entity_id=data.entity_id,
            project_id=data.project_id,
            workflow_code=workflow.code,
            status_code=status.code,
            configuration_version_id=effective.id,
            version=1,
            on_hold=False,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)

        hist = StatusHistory(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            entity_type=row.entity_type,
            entity_id=row.entity_id,
            project_id=row.project_id,
            workflow_code=row.workflow_code,
            from_status_code="__none__",
            to_status_code=row.status_code,
            reason="initialize",
            evidence_ref=None,
            approval_id=None,
            actor_id=self.ctx.actor_id,
            actor_kind=self.ctx.actor_kind.value,
            rule_id=None,
            payload_json={},
        )
        self.uow.add(hist)
        self._refresh_actions(row, effective.id, workflow.id)
        self.obs.write_audit(
            action="wfe_state_initialize",
            entity_type=row.entity_type,
            entity_id=row.entity_id,
            payload={
                "workflow_code": row.workflow_code,
                "status_code": row.status_code,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="wfe_entity_state",
            aggregate_id=row.id,
            event_type="status.initialized",
            payload={
                "entity_type": row.entity_type,
                "entity_id": str(row.entity_id),
                "status_code": row.status_code,
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def get_state(self, entity_type: str, entity_id: UUID) -> EntityState:
        return self._get_state(entity_type, entity_id)

    def list_history(self, entity_type: str, entity_id: UUID) -> list[StatusHistory]:
        self._get_state(entity_type, entity_id)
        rows = self.db.scalars(
            select(StatusHistory)
            .where(
                StatusHistory.organization_id == self.ctx.organization_id,
                StatusHistory.entity_type == entity_type,
                StatusHistory.entity_id == entity_id,
            )
            .order_by(StatusHistory.recorded_at.asc())
        ).all()
        return list(rows)

    def available_actions(self, entity_type: str, entity_id: UUID) -> AvailableActionsRead:
        state = self._get_state(entity_type, entity_id)
        effective = self._get_effective_version(required=True)
        assert effective is not None
        workflow = self._get_workflow(effective.id, state.workflow_code)
        actions = self._compute_actions(effective.id, workflow.id, state.status_code)
        return AvailableActionsRead(
            entity_type=state.entity_type,
            entity_id=state.entity_id,
            workflow_code=state.workflow_code,
            status_code=state.status_code,
            on_hold=state.on_hold,
            actions=actions,
        )

    def apply_transition(self, data: TransitionApply) -> EntityState:
        state = self._get_state(data.entity_type, data.entity_id)
        if data.expected_version is not None and state.version != data.expected_version:
            raise ConflictError("Entity state version mismatch")

        domain.assert_not_on_hold(on_hold=state.on_hold)

        effective = self._get_effective_version(required=True)
        assert effective is not None
        workflow = self._get_workflow(effective.id, state.workflow_code)
        rule = self._get_transition_rule(
            effective.id, workflow.id, state.status_code, data.to_status_code
        )
        domain.assert_transition_exists(
            allowed=rule is not None,
            from_status=state.status_code,
            to_status=data.to_status_code,
        )
        assert rule is not None

        domain.assert_reason_if_required(requires_reason=rule.requires_reason, reason=data.reason)
        domain.assert_approval_gate(
            requires_approval=rule.requires_approval,
            approval_id=data.approval_id,
            actor_kind=self.ctx.actor_kind,
        )
        # Target status must exist in effective config (AC-001 string codes)
        self._get_status(effective.id, workflow.id, data.to_status_code)

        from_status = state.status_code
        state.status_code = data.to_status_code
        state.configuration_version_id = effective.id
        state.version += 1
        state.updated_by_actor_id = self.ctx.actor_id
        self.uow.add(state)

        hist = StatusHistory(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            entity_type=state.entity_type,
            entity_id=state.entity_id,
            project_id=state.project_id,
            workflow_code=state.workflow_code,
            from_status_code=from_status,
            to_status_code=state.status_code,
            reason=data.reason,
            evidence_ref=data.evidence_ref,
            approval_id=data.approval_id,
            actor_id=self.ctx.actor_id,
            actor_kind=self.ctx.actor_kind.value,
            rule_id=rule.id,
            payload_json=dict(data.fields or {}),
        )
        self.uow.add(hist)
        self._refresh_actions(state, effective.id, workflow.id)

        self.obs.write_audit(
            action="wfe_transition",
            entity_type=state.entity_type,
            entity_id=state.entity_id,
            payload={
                "from_status_code": from_status,
                "to_status_code": state.status_code,
                "reason": data.reason,
                "approval_id": str(data.approval_id) if data.approval_id else None,
                "rule_id": str(rule.id),
                "history_id": str(hist.id),
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="wfe_entity_state",
            aggregate_id=state.id,
            event_type="status.transitioned",
            payload={
                "entity_type": state.entity_type,
                "entity_id": str(state.entity_id),
                "from_status_code": from_status,
                "to_status_code": state.status_code,
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(state)
        return state

    def place_hold(self, data: HoldCreate) -> HoldRecord:
        state = self._get_state(data.entity_type, data.entity_id)
        domain.assert_hold_reason(data.reason)
        if state.on_hold:
            raise ConflictError("Entity is already on hold")

        open_hold = self.db.scalar(
            select(HoldRecord).where(
                HoldRecord.organization_id == self.ctx.organization_id,
                HoldRecord.entity_type == data.entity_type,
                HoldRecord.entity_id == data.entity_id,
                HoldRecord.status == "open",
            )
        )
        if open_hold is not None:
            raise ConflictError("Entity already has an open hold")

        row = HoldRecord(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            entity_type=state.entity_type,
            entity_id=state.entity_id,
            project_id=state.project_id,
            status_code_at_hold=state.status_code,
            reason=data.reason.strip(),
            responsible_actor_id=data.responsible_actor_id or self.ctx.actor_id,
            due_at=data.due_at,
            status="open",
            created_by_actor_id=self.ctx.actor_id,
        )
        state.on_hold = True
        state.version += 1
        state.updated_by_actor_id = self.ctx.actor_id
        self.uow.add(state)
        self.uow.add(row)
        self.obs.write_audit(
            action="wfe_hold_place",
            entity_type=state.entity_type,
            entity_id=state.entity_id,
            payload={"hold_id": str(row.id), "reason": row.reason},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="wfe_hold",
            aggregate_id=row.id,
            event_type="status.hold.placed",
            payload={
                "entity_type": state.entity_type,
                "entity_id": str(state.entity_id),
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def release_hold(
        self, entity_type: str, entity_id: UUID, data: HoldRelease
    ) -> HoldRecord:
        state = self._get_state(entity_type, entity_id)
        row = self.db.scalar(
            select(HoldRecord).where(
                HoldRecord.organization_id == self.ctx.organization_id,
                HoldRecord.entity_type == entity_type,
                HoldRecord.entity_id == entity_id,
                HoldRecord.status == "open",
            )
        )
        if row is None:
            raise NotFoundError("Open hold not found")

        row.status = "released"
        row.released_at = datetime.now(UTC)
        row.released_by_actor_id = self.ctx.actor_id
        state.on_hold = False
        state.version += 1
        state.updated_by_actor_id = self.ctx.actor_id
        self.uow.add(row)
        self.uow.add(state)
        self.obs.write_audit(
            action="wfe_hold_release",
            entity_type=state.entity_type,
            entity_id=state.entity_id,
            payload={"hold_id": str(row.id), "note": data.note},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="wfe_hold",
            aggregate_id=row.id,
            event_type="status.hold.released",
            payload={
                "entity_type": state.entity_type,
                "entity_id": str(state.entity_id),
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def reopen(self, data: ReopenApply) -> tuple[EntityState, ReopenRecord]:
        state = self._get_state(data.entity_type, data.entity_id)
        if data.expected_version is not None and state.version != data.expected_version:
            raise ConflictError("Entity state version mismatch")
        domain.assert_not_on_hold(on_hold=state.on_hold)

        effective = self._get_effective_version(required=True)
        assert effective is not None
        workflow = self._get_workflow(effective.id, state.workflow_code)
        current = self._get_status(effective.id, workflow.id, state.status_code)
        domain.assert_can_reopen(
            is_terminal=current.is_terminal,
            actor_kind=self.ctx.actor_kind,
            reason=data.reason,
        )
        target = self._get_status(effective.id, workflow.id, data.to_status_code)
        if target.is_terminal:
            raise ValidationAppError("Reopen target status cannot be terminal")

        from_status = state.status_code
        state.status_code = target.code
        state.configuration_version_id = effective.id
        state.version += 1
        state.updated_by_actor_id = self.ctx.actor_id
        self.uow.add(state)

        reopen = ReopenRecord(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            entity_type=state.entity_type,
            entity_id=state.entity_id,
            project_id=state.project_id,
            from_status_code=from_status,
            to_status_code=state.status_code,
            reason=data.reason.strip(),
            evidence_ref=data.evidence_ref,
            authorized_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(reopen)

        hist = StatusHistory(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            entity_type=state.entity_type,
            entity_id=state.entity_id,
            project_id=state.project_id,
            workflow_code=state.workflow_code,
            from_status_code=from_status,
            to_status_code=state.status_code,
            reason=data.reason,
            evidence_ref=data.evidence_ref,
            approval_id=None,
            actor_id=self.ctx.actor_id,
            actor_kind=self.ctx.actor_kind.value,
            rule_id=None,
            payload_json={"reopen_id": str(reopen.id)},
        )
        self.uow.add(hist)
        self._refresh_actions(state, effective.id, workflow.id)

        self.obs.write_audit(
            action="wfe_reopen",
            entity_type=state.entity_type,
            entity_id=state.entity_id,
            payload={
                "from_status_code": from_status,
                "to_status_code": state.status_code,
                "reopen_id": str(reopen.id),
                "history_id": str(hist.id),
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="wfe_entity_state",
            aggregate_id=state.id,
            event_type="status.reopened",
            payload={
                "entity_type": state.entity_type,
                "entity_id": str(state.entity_id),
                "from_status_code": from_status,
                "to_status_code": state.status_code,
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(state)
        self.uow.refresh(reopen)
        return state, reopen

    def _resolve_binding(
        self, *, entity_type: str, project_id: UUID | None
    ) -> WorkflowBinding:
        rows = list(
            self.db.scalars(
                select(WorkflowBinding)
                .where(
                    WorkflowBinding.organization_id == self.ctx.organization_id,
                    WorkflowBinding.entity_type == entity_type,
                    WorkflowBinding.status == "active",
                )
                .order_by(WorkflowBinding.priority.asc())
            ).all()
        )
        if not rows:
            raise NotFoundError(f"No workflow binding for entity_type '{entity_type}'")

        if project_id is not None:
            project_matches = [r for r in rows if r.project_id == project_id]
            if project_matches:
                return project_matches[0]

        org_defaults = [r for r in rows if r.project_id is None]
        if org_defaults:
            return org_defaults[0]
        raise NotFoundError(
            f"No workflow binding for entity_type '{entity_type}' "
            f"(project {project_id})"
        )

    def _get_effective_version(self, *, required: bool) -> ConfigurationVersion | None:
        row = self.db.scalar(
            select(ConfigurationVersion).where(
                ConfigurationVersion.organization_id == self.ctx.organization_id,
                ConfigurationVersion.status == config_domain.STATUS_EFFECTIVE,
            )
        )
        if row is None and required:
            raise NotFoundError("No effective configuration version")
        if row is not None:
            config_domain.assert_live_config(row.status)
        return row

    def _get_workflow(self, version_id: UUID, code: str) -> WorkflowDefinition:
        row = self.db.scalar(
            select(WorkflowDefinition).where(
                WorkflowDefinition.organization_id == self.ctx.organization_id,
                WorkflowDefinition.configuration_version_id == version_id,
                WorkflowDefinition.code == code,
                WorkflowDefinition.status == "active",
            )
        )
        if row is None:
            raise NotFoundError(f"Workflow '{code}' not found in effective config")
        return row

    def _get_status(
        self, version_id: UUID, workflow_id: UUID, code: str
    ) -> StatusDefinition:
        row = self.db.scalar(
            select(StatusDefinition).where(
                StatusDefinition.organization_id == self.ctx.organization_id,
                StatusDefinition.configuration_version_id == version_id,
                StatusDefinition.workflow_definition_id == workflow_id,
                StatusDefinition.code == code,
                StatusDefinition.status == "active",
            )
        )
        if row is None:
            raise NotFoundError(f"Status '{code}' not found in effective config")
        return row

    def _get_transition_rule(
        self,
        version_id: UUID,
        workflow_id: UUID,
        from_status: str,
        to_status: str,
    ) -> TransitionRule | None:
        return self.db.scalar(
            select(TransitionRule).where(
                TransitionRule.organization_id == self.ctx.organization_id,
                TransitionRule.configuration_version_id == version_id,
                TransitionRule.workflow_definition_id == workflow_id,
                TransitionRule.from_status_code == from_status,
                TransitionRule.to_status_code == to_status,
                TransitionRule.status == "active",
            )
        )

    def _compute_actions(
        self, version_id: UUID, workflow_id: UUID, from_status: str
    ) -> list[AvailableAction]:
        rules = self.db.scalars(
            select(TransitionRule).where(
                TransitionRule.organization_id == self.ctx.organization_id,
                TransitionRule.configuration_version_id == version_id,
                TransitionRule.workflow_definition_id == workflow_id,
                TransitionRule.from_status_code == from_status,
                TransitionRule.status == "active",
            )
        ).all()
        return [
            AvailableAction(
                to_status_code=r.to_status_code,
                requires_reason=r.requires_reason,
                requires_approval=r.requires_approval,
                rule_id=r.id,
            )
            for r in rules
        ]

    def _refresh_actions(
        self, state: EntityState, version_id: UUID, workflow_id: UUID
    ) -> None:
        actions = self._compute_actions(version_id, workflow_id, state.status_code)
        snap = self.db.scalar(
            select(AvailableActionsSnapshot).where(
                AvailableActionsSnapshot.organization_id == self.ctx.organization_id,
                AvailableActionsSnapshot.entity_type == state.entity_type,
                AvailableActionsSnapshot.entity_id == state.entity_id,
            )
        )
        payload = [a.model_dump(mode="json") for a in actions]
        if snap is None:
            snap = AvailableActionsSnapshot(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                entity_type=state.entity_type,
                entity_id=state.entity_id,
                workflow_code=state.workflow_code,
                status_code=state.status_code,
                actions_json=payload,
                computed_at=datetime.now(UTC),
            )
        else:
            snap.workflow_code = state.workflow_code
            snap.status_code = state.status_code
            snap.actions_json = payload
            snap.computed_at = datetime.now(UTC)
        self.uow.add(snap)

    def _get_state(self, entity_type: str, entity_id: UUID) -> EntityState:
        row = self._get_state_optional(entity_type, entity_id)
        if row is None:
            raise NotFoundError("Entity workflow state not found")
        return row

    def _get_state_optional(
        self, entity_type: str, entity_id: UUID
    ) -> EntityState | None:
        return self.db.scalar(
            select(EntityState).where(
                EntityState.organization_id == self.ctx.organization_id,
                EntityState.entity_type == entity_type,
                EntityState.entity_id == entity_id,
            )
        )
