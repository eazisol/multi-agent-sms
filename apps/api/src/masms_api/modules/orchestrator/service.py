"""Orchestrator application service (MOD-350)."""

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
from masms_api.modules.orchestrator import domain
from masms_api.modules.orchestrator.models import (
    WorkflowDefinition,
    WorkflowFailure,
    WorkflowInstance,
    WorkflowIntervention,
    WorkflowSignal,
    WorkflowVersion,
)
from masms_api.modules.orchestrator.schemas import (
    FailureCreate,
    InstanceCreate,
    InterventionCreate,
    InterventionResolve,
    SignalCreate,
    VersionCreate,
)
from masms_api.modules.orchestrator.temporal_adapter import TemporalAdapter, get_temporal_adapter
from masms_api.observability.writer import ObservabilityWriter


class OrchestratorService:
    def __init__(
        self,
        db: Session,
        ctx: RequestContext,
        temporal: TemporalAdapter | None = None,
    ) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        self.temporal = temporal or get_temporal_adapter()
        apply_tenant_rls(db, ctx.organization_id)

    # --- definitions / versions -------------------------------------------------

    def ensure_definitions(self) -> list[WorkflowDefinition]:
        """Seed the 12 approved catalog codes for the org when missing."""
        existing = list(
            self.db.scalars(
                select(WorkflowDefinition).where(
                    WorkflowDefinition.organization_id == self.ctx.organization_id
                )
            )
        )
        by_code = {row.code: row for row in existing}
        created = False
        for code in sorted(domain.ALLOWED_CODES):
            if code in by_code:
                continue
            row = WorkflowDefinition(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                code=code,
                title=domain.WORKFLOW_TITLES[code],
                description=f"Approved MASMS workflow: {domain.WORKFLOW_TITLES[code]}",
                status="active",
                created_by_actor_id=self.ctx.actor_id,
            )
            self.uow.add(row)
            by_code[code] = row
            created = True
        if created:
            self.obs.write_audit(
                action="orf_definitions_seeded",
                entity_type="orf_workflow_definition",
                entity_id=self.ctx.organization_id,
                payload={"codes": sorted(by_code.keys())},
            )
            self.uow.commit()
        return [by_code[c] for c in sorted(domain.ALLOWED_CODES)]

    def list_definitions(self) -> list[WorkflowDefinition]:
        return self.ensure_definitions()

    def create_version(self, code: str, data: VersionCreate) -> WorkflowVersion:
        domain.assert_allowed_workflow_code(code)
        definitions = {d.code: d for d in self.ensure_definitions()}
        definition = definitions[code]
        next_number = (
            self.db.scalar(
                select(func.coalesce(func.max(WorkflowVersion.version_number), 0)).where(
                    WorkflowVersion.definition_id == definition.id,
                    WorkflowVersion.organization_id == self.ctx.organization_id,
                )
            )
            or 0
        ) + 1
        temporal_type = data.temporal_workflow_type or f"masms.{code}"
        row = WorkflowVersion(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            definition_id=definition.id,
            version_number=next_number,
            status="draft",
            definition_json=data.definition_json or {},
            temporal_workflow_type=temporal_type,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="orf_version_create",
            entity_type="orf_workflow_version",
            entity_id=row.id,
            payload={"code": code, "version_number": next_number},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def activate_version(self, version_id: UUID) -> WorkflowVersion:
        version = self._get_version(version_id)
        if version.status == "retired":
            raise ConflictError("Retired workflow versions cannot be activated")
        actives = list(
            self.db.scalars(
                select(WorkflowVersion).where(
                    WorkflowVersion.organization_id == self.ctx.organization_id,
                    WorkflowVersion.definition_id == version.definition_id,
                    WorkflowVersion.status == "active",
                    WorkflowVersion.id != version.id,
                )
            )
        )
        for active in actives:
            active.status = "retired"
        version.status = "active"
        self.obs.write_audit(
            action="orf_version_activate",
            entity_type="orf_workflow_version",
            entity_id=version.id,
            payload={"definition_id": str(version.definition_id)},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="orf_workflow_version",
            aggregate_id=version.id,
            event_type="orchestrator.version.activated",
            payload={"version_number": version.version_number},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(version)
        return version

    def list_versions(self, definition_id: UUID | None = None) -> list[WorkflowVersion]:
        filters = [WorkflowVersion.organization_id == self.ctx.organization_id]
        if definition_id is not None:
            filters.append(WorkflowVersion.definition_id == definition_id)
        return list(
            self.db.scalars(
                select(WorkflowVersion)
                .where(*filters)
                .order_by(WorkflowVersion.created_at.desc())
            )
        )

    # --- instances --------------------------------------------------------------

    def start_instance(self, data: InstanceCreate) -> WorkflowInstance:
        domain.assert_allowed_workflow_code(data.workflow_code)
        self.ensure_definitions()
        version = self._resolve_start_version(data.workflow_code, data.workflow_version_id)

        instance_id = uuid4()
        temporal_workflow_id = f"{data.workflow_code}:{instance_id}"
        row = WorkflowInstance(
            id=instance_id,
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            workflow_code=data.workflow_code,
            workflow_version_id=version.id,
            related_entity_type=data.related_entity_type,
            related_entity_id=data.related_entity_id,
            status="pending",
            owner_actor_id=data.owner_actor_id or self.ctx.actor_id,
            correlation_id=self.ctx.correlation_id,
            input_json=data.input_json or {},
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.flush()

        run_id = self.temporal.start_workflow(
            workflow_type=version.temporal_workflow_type,
            workflow_id=temporal_workflow_id,
            input_payload=data.input_json or {},
        )
        domain.assert_instance_transition(from_status="pending", to_status="running")
        row.status = "running"
        row.temporal_run_id = run_id
        row.temporal_workflow_id = temporal_workflow_id
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id

        self.obs.write_audit(
            action="orf_instance_start",
            entity_type="orf_workflow_instance",
            entity_id=row.id,
            payload={
                "workflow_code": row.workflow_code,
                "temporal_run_id": run_id,
                "temporal_workflow_id": temporal_workflow_id,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="orf_workflow_instance",
            aggregate_id=row.id,
            event_type="orchestrator.workflow.started",
            payload={
                "workflow_code": row.workflow_code,
                "status": row.status,
                "temporal_run_id": run_id,
            },
            correlation_id=self.ctx.correlation_id,
            project_id=row.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def get_instance(self, instance_id: UUID) -> WorkflowInstance:
        return self._get_instance(instance_id)

    def list_instances(
        self,
        *,
        status: str | None = None,
        q: str | None = None,
        workflow_code: str | None = None,
        project_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[WorkflowInstance], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [WorkflowInstance.organization_id == self.ctx.organization_id]
        if status is not None and status != "all":
            filters.append(WorkflowInstance.status == status)
        if workflow_code:
            filters.append(WorkflowInstance.workflow_code == workflow_code)
        if project_id is not None:
            filters.append(WorkflowInstance.project_id == project_id)
        if q and q.strip():
            like = f"%{q.strip()}%"
            filters.append(
                or_(
                    WorkflowInstance.workflow_code.ilike(like),
                    WorkflowInstance.related_entity_type.ilike(like),
                    WorkflowInstance.status.ilike(like),
                )
            )
        total = (
            self.db.scalar(
                select(func.count()).select_from(WorkflowInstance).where(*filters)
            )
            or 0
        )
        rows = list(
            self.db.scalars(
                select(WorkflowInstance)
                .where(*filters)
                .order_by(WorkflowInstance.created_at.desc())
                .offset(offset)
                .limit(limit)
            )
        )
        return rows, build_page_meta(limit=limit, offset=offset, total=int(total))

    # --- signals / failures / interventions -------------------------------------

    def signal_instance(
        self, instance_id: UUID, data: SignalCreate
    ) -> tuple[WorkflowSignal, bool]:
        instance = self._get_instance(instance_id)

        existing = self.db.scalar(
            select(WorkflowSignal).where(
                WorkflowSignal.organization_id == self.ctx.organization_id,
                WorkflowSignal.instance_id == instance_id,
                WorkflowSignal.idempotency_key == data.idempotency_key,
            )
        )
        if existing is not None:
            if existing.status == "accepted":
                completed = self._reconcile_terminal_completion(
                    instance,
                    data.signal_name,
                    timeout_seconds=0.1,
                )
                if not completed:
                    self.temporal.signal_workflow(
                        workflow_id=instance.temporal_workflow_id or str(instance.id),
                        signal_name=data.signal_name,
                        payload=data.payload_json or {},
                        run_id=instance.temporal_run_id,
                    )
                    existing.status = "applied"
                    self._reconcile_terminal_completion(instance, data.signal_name)
                self.uow.commit()
                self.uow.refresh(existing)
            elif self._reconcile_terminal_completion(instance, data.signal_name):
                self.uow.commit()
                self.uow.refresh(existing)
            return existing, True

        domain.assert_instance_open(instance.status)

        row = WorkflowSignal(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            instance_id=instance_id,
            signal_name=data.signal_name,
            payload_json=data.payload_json or {},
            idempotency_key=data.idempotency_key,
            status="accepted",
            actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="orf_signal_accepted",
            entity_type="orf_workflow_instance",
            entity_id=instance_id,
            payload={
                "signal_name": data.signal_name,
                "idempotency_key": data.idempotency_key,
                "signal_id": str(row.id),
            },
        )
        self.uow.commit()
        self.temporal.signal_workflow(
            workflow_id=instance.temporal_workflow_id or str(instance.id),
            signal_name=data.signal_name,
            payload=data.payload_json or {},
            run_id=instance.temporal_run_id,
        )
        row.status = "applied"
        self._reconcile_terminal_completion(instance, data.signal_name)
        if instance.status == "waiting":
            domain.assert_instance_transition(from_status="waiting", to_status="running")
            instance.status = "running"
            instance.version += 1
            instance.updated_by_actor_id = self.ctx.actor_id

        self.obs.write_audit(
            action="orf_signal",
            entity_type="orf_workflow_instance",
            entity_id=instance_id,
            payload={
                "signal_name": data.signal_name,
                "idempotency_key": data.idempotency_key,
                "signal_id": str(row.id),
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="orf_workflow_instance",
            aggregate_id=instance_id,
            event_type="orchestrator.workflow.signaled",
            payload={"signal_name": data.signal_name, "signal_id": str(row.id)},
            correlation_id=self.ctx.correlation_id,
            project_id=instance.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row, False

    def _reconcile_terminal_completion(
        self,
        instance: WorkflowInstance,
        signal_name: str,
        *,
        timeout_seconds: float = 5.0,
    ) -> bool:
        if not domain.is_terminal_signal(
            workflow_code=instance.workflow_code,
            signal_name=signal_name,
        ):
            return False
        result = self.temporal.wait_for_workflow_result(
            workflow_id=instance.temporal_workflow_id or str(instance.id),
            run_id=instance.temporal_run_id,
            timeout_seconds=timeout_seconds,
        )
        if result is None or result.get("status") != "completed":
            return False
        if instance.status == "completed":
            return True

        domain.assert_instance_transition(from_status=instance.status, to_status="completed")
        now = datetime.now(UTC)
        instance.status = "completed"
        instance.closed_at = now
        instance.updated_at = now
        instance.updated_by_actor_id = self.ctx.actor_id
        instance.version += 1
        self.obs.write_audit(
            action="orf_instance_completed",
            entity_type="orf_workflow_instance",
            entity_id=instance.id,
            payload={"temporal_status": "completed", "signal_name": signal_name},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="orf_workflow_instance",
            aggregate_id=instance.id,
            event_type="orchestrator.workflow.completed",
            payload={"workflow_code": instance.workflow_code, "status": "completed"},
            correlation_id=instance.correlation_id,
            project_id=instance.project_id,
        )
        return True

    def list_signals(self, instance_id: UUID) -> list[WorkflowSignal]:
        self._get_instance(instance_id)
        return list(
            self.db.scalars(
                select(WorkflowSignal)
                .where(
                    WorkflowSignal.organization_id == self.ctx.organization_id,
                    WorkflowSignal.instance_id == instance_id,
                )
                .order_by(WorkflowSignal.created_at.asc())
            )
        )

    def record_failure(self, instance_id: UUID, data: FailureCreate) -> WorkflowFailure:
        instance = self._get_instance(instance_id)
        domain.assert_instance_open(instance.status)
        domain.assert_expected_version(
            current=instance.version, expected=data.expected_version
        )

        row = WorkflowFailure(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            instance_id=instance_id,
            failure_code=data.failure_code,
            message=data.message,
            retryable=data.retryable,
            attempt=data.attempt,
            details_json=data.details_json or {},
        )
        self.uow.add(row)

        if data.mark_instance_failed and instance.status in {"running", "waiting", "pending"}:
            # pending → failed is not in the transition chart; move via running if needed
            if instance.status == "pending":
                domain.assert_instance_transition(from_status="pending", to_status="running")
                instance.status = "running"
            domain.assert_instance_transition(
                from_status=instance.status, to_status="failed"
            )
            instance.status = "failed"
            instance.version += 1
            instance.updated_by_actor_id = self.ctx.actor_id

        self.obs.write_audit(
            action="orf_failure",
            entity_type="orf_workflow_instance",
            entity_id=instance_id,
            payload={
                "failure_code": data.failure_code,
                "failure_id": str(row.id),
                "retryable": data.retryable,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="orf_workflow_instance",
            aggregate_id=instance_id,
            event_type="orchestrator.workflow.failed",
            payload={"failure_code": data.failure_code, "failure_id": str(row.id)},
            correlation_id=self.ctx.correlation_id,
            project_id=instance.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_failures(self, instance_id: UUID) -> list[WorkflowFailure]:
        self._get_instance(instance_id)
        return list(
            self.db.scalars(
                select(WorkflowFailure)
                .where(
                    WorkflowFailure.organization_id == self.ctx.organization_id,
                    WorkflowFailure.instance_id == instance_id,
                )
                .order_by(WorkflowFailure.created_at.asc())
            )
        )

    def create_intervention(
        self, instance_id: UUID, data: InterventionCreate
    ) -> WorkflowIntervention:
        instance = self._get_instance(instance_id)
        domain.assert_instance_open(instance.status)
        domain.assert_intervention_action(data.action_code)
        if not (data.reason and data.reason.strip()):
            raise ValidationAppError("Intervention requires a reason")

        row = WorkflowIntervention(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            instance_id=instance_id,
            reason=data.reason.strip(),
            action_code=data.action_code,
            notes=data.notes,
            status="open",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="orf_intervention_create",
            entity_type="orf_workflow_instance",
            entity_id=instance_id,
            payload={"intervention_id": str(row.id), "action_code": data.action_code},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def resolve_intervention(
        self, intervention_id: UUID, data: InterventionResolve | None = None
    ) -> WorkflowIntervention:
        data = data or InterventionResolve()
        intervention = self._get_intervention(intervention_id)
        if intervention.status != "open":
            raise ConflictError("Intervention is already resolved")

        instance = self._get_instance(intervention.instance_id)
        domain.assert_instance_open(instance.status)
        domain.assert_expected_version(
            current=instance.version, expected=data.expected_version
        )

        target = domain.next_status_for_intervention(
            action_code=intervention.action_code,
            current_status=instance.status,
        )

        if intervention.action_code == "cancel":
            self.temporal.cancel_workflow(
                workflow_id=instance.temporal_workflow_id or str(instance.id),
                run_id=instance.temporal_run_id,
                reason=intervention.reason,
            )
        elif intervention.action_code in {"retry", "resume"}:
            # Re-signal / re-start is stub-only; business status is updated in Postgres.
            if not instance.temporal_run_id:
                run_id = self.temporal.start_workflow(
                    workflow_type=f"masms.{instance.workflow_code}",
                    workflow_id=instance.temporal_workflow_id or str(instance.id),
                    input_payload=instance.input_json or {},
                )
                instance.temporal_run_id = run_id

        now = datetime.now(UTC)
        instance.status = target
        instance.version += 1
        instance.updated_by_actor_id = self.ctx.actor_id
        if target in domain.TERMINAL_INSTANCE_STATUSES:
            instance.closed_at = now

        intervention.status = "resolved"
        intervention.decided_by_actor_id = self.ctx.actor_id
        intervention.resolved_at = now
        if data.notes:
            intervention.notes = data.notes

        self.obs.write_audit(
            action="orf_intervention_resolve",
            entity_type="orf_workflow_instance",
            entity_id=instance.id,
            payload={
                "intervention_id": str(intervention.id),
                "action_code": intervention.action_code,
                "new_status": target,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="orf_workflow_instance",
            aggregate_id=instance.id,
            event_type=f"orchestrator.workflow.{target}",
            payload={
                "intervention_id": str(intervention.id),
                "action_code": intervention.action_code,
                "status": target,
            },
            correlation_id=self.ctx.correlation_id,
            project_id=instance.project_id,
        )
        self.uow.commit()
        self.uow.refresh(intervention)
        return intervention

    def list_interventions(self, instance_id: UUID) -> list[WorkflowIntervention]:
        self._get_instance(instance_id)
        return list(
            self.db.scalars(
                select(WorkflowIntervention)
                .where(
                    WorkflowIntervention.organization_id == self.ctx.organization_id,
                    WorkflowIntervention.instance_id == instance_id,
                )
                .order_by(WorkflowIntervention.created_at.asc())
            )
        )

    # --- helpers ----------------------------------------------------------------

    def _resolve_start_version(
        self, workflow_code: str, workflow_version_id: UUID | None
    ) -> WorkflowVersion:
        if workflow_version_id is not None:
            version = self._get_version(workflow_version_id)
            definition = self.db.scalar(
                select(WorkflowDefinition).where(
                    WorkflowDefinition.id == version.definition_id,
                    WorkflowDefinition.organization_id == self.ctx.organization_id,
                )
            )
            if definition is None or definition.code != workflow_code:
                raise ValidationAppError(
                    "workflow_version_id does not belong to the requested workflow_code"
                )
            if version.status != "active":
                raise ConflictError("Workflow version must be active to start an instance")
            return version

        definition = self.db.scalar(
            select(WorkflowDefinition).where(
                WorkflowDefinition.organization_id == self.ctx.organization_id,
                WorkflowDefinition.code == workflow_code,
            )
        )
        if definition is None:
            raise NotFoundError(f"Workflow definition '{workflow_code}' not found")
        active = self.db.scalar(
            select(WorkflowVersion)
            .where(
                WorkflowVersion.organization_id == self.ctx.organization_id,
                WorkflowVersion.definition_id == definition.id,
                WorkflowVersion.status == "active",
            )
            .order_by(WorkflowVersion.version_number.desc())
        )
        if active is None:
            raise ConflictError(
                f"No active version for workflow_code '{workflow_code}'. "
                "Create and activate a version first."
            )
        return active

    def _get_instance(self, instance_id: UUID) -> WorkflowInstance:
        row = self.db.scalar(
            select(WorkflowInstance).where(
                WorkflowInstance.id == instance_id,
                WorkflowInstance.organization_id == self.ctx.organization_id,
            )
        )
        if row is None:
            raise NotFoundError("Workflow instance not found")
        return row

    def _get_version(self, version_id: UUID) -> WorkflowVersion:
        row = self.db.scalar(
            select(WorkflowVersion).where(
                WorkflowVersion.id == version_id,
                WorkflowVersion.organization_id == self.ctx.organization_id,
            )
        )
        if row is None:
            raise NotFoundError("Workflow version not found")
        return row

    def _get_intervention(self, intervention_id: UUID) -> WorkflowIntervention:
        row = self.db.scalar(
            select(WorkflowIntervention).where(
                WorkflowIntervention.id == intervention_id,
                WorkflowIntervention.organization_id == self.ctx.organization_id,
            )
        )
        if row is None:
            raise NotFoundError("Workflow intervention not found")
        return row
