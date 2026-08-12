"""Application service for MOD-600 security hardening."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, NotFoundError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.securityhardening import domain
from masms_api.modules.securityhardening.models import (
    BackupRecord,
    DeletionJob,
    LegalHold,
    PiiInventoryItem,
    RetentionPolicy,
    RestoreTest,
    SecurityIncident,
    ThreatModel,
    TrainingPolicy,
)
from masms_api.modules.securityhardening.schemas import (
    BackupRecordCreate,
    DeletionJobCreate,
    LegalHoldCreate,
    PiiInventoryCreate,
    RetentionPolicyCreate,
    RestoreTestCreate,
    SecurityIncidentClose,
    SecurityIncidentCreate,
    ThreatModelCreate,
    TrainingPolicyUpdate,
)
from masms_api.observability.writer import ObservabilityWriter


class SecurityHardeningService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def _audit(
        self,
        *,
        action: str,
        entity_type: str,
        entity_id: UUID,
        payload: dict[str, Any] | None = None,
    ) -> None:
        self.obs.write_audit(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload,
        )

    def _enqueue(
        self,
        *,
        aggregate_type: str,
        aggregate_id: UUID,
        event_type: str,
        payload: dict[str, Any],
    ) -> None:
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=event_type,
            payload=payload,
            correlation_id=self.ctx.correlation_id,
        )

    # --- Threat models ---

    def create_threat_model(self, data: ThreatModelCreate) -> ThreatModel:
        domain.assert_threat_model_status(data.status)
        existing = self.db.scalar(
            select(ThreatModel).where(
                ThreatModel.organization_id == self.ctx.organization_id,
                ThreatModel.code == data.code.strip(),
            )
        )
        if existing is not None:
            raise ConflictError(f"Threat model code '{data.code}' already exists")
        owner = data.owner_actor_id or self.ctx.actor_id
        row = ThreatModel(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code.strip(),
            title=data.title.strip(),
            scope_summary=data.scope_summary.strip(),
            status=data.status,
            version=1,
            owner_actor_id=owner,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="sh_threat_model_create",
            entity_type="sh_threat_model",
            entity_id=row.id,
            payload={"code": row.code, "status": row.status},
        )
        self._enqueue(
            aggregate_type="sh_threat_model",
            aggregate_id=row.id,
            event_type="security.threat_model.created",
            payload={"threat_model_id": str(row.id), "code": row.code},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_threat_models(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[ThreatModel], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(ThreatModel).where(
            ThreatModel.organization_id == self.ctx.organization_id
        )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(ThreatModel.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    # --- PII inventory ---

    def create_pii_inventory(self, data: PiiInventoryCreate) -> PiiInventoryItem:
        domain.assert_pii_classification(data.classification)
        existing = self.db.scalar(
            select(PiiInventoryItem).where(
                PiiInventoryItem.organization_id == self.ctx.organization_id,
                PiiInventoryItem.data_category == data.data_category.strip(),
                PiiInventoryItem.field_path == data.field_path.strip(),
            )
        )
        if existing is not None:
            raise ConflictError("PII inventory entry already exists for category/field")
        row = PiiInventoryItem(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            data_category=data.data_category.strip(),
            field_path=data.field_path.strip(),
            classification=data.classification,
            purpose=data.purpose.strip(),
            retention_days=data.retention_days,
        )
        self.uow.add(row)
        self._audit(
            action="sh_pii_inventory_create",
            entity_type="sh_pii_inventory",
            entity_id=row.id,
            payload={
                "data_category": row.data_category,
                "field_path": row.field_path,
                "classification": row.classification,
            },
        )
        self._enqueue(
            aggregate_type="sh_pii_inventory",
            aggregate_id=row.id,
            event_type="security.pii_inventory.created",
            payload={"pii_inventory_id": str(row.id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_pii_inventory(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[PiiInventoryItem], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(PiiInventoryItem).where(
            PiiInventoryItem.organization_id == self.ctx.organization_id
        )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(PiiInventoryItem.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    # --- Retention policies ---

    def create_retention_policy(self, data: RetentionPolicyCreate) -> RetentionPolicy:
        domain.assert_retention_action(data.action)
        domain.assert_retention_status(data.status)
        existing = self.db.scalar(
            select(RetentionPolicy).where(
                RetentionPolicy.organization_id == self.ctx.organization_id,
                RetentionPolicy.code == data.code.strip(),
            )
        )
        if existing is not None:
            raise ConflictError(f"Retention policy code '{data.code}' already exists")
        row = RetentionPolicy(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code.strip(),
            entity_type=data.entity_type.strip(),
            retain_days=data.retain_days,
            action=data.action,
            status=data.status,
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="sh_retention_policy_create",
            entity_type="sh_retention_policy",
            entity_id=row.id,
            payload={"code": row.code, "action": row.action},
        )
        self._enqueue(
            aggregate_type="sh_retention_policy",
            aggregate_id=row.id,
            event_type="security.retention_policy.created",
            payload={"retention_policy_id": str(row.id), "code": row.code},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_retention_policies(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[RetentionPolicy], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(RetentionPolicy).where(
            RetentionPolicy.organization_id == self.ctx.organization_id
        )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(RetentionPolicy.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    # --- Legal holds ---

    def create_legal_hold(self, data: LegalHoldCreate) -> LegalHold:
        existing = self.db.scalar(
            select(LegalHold).where(
                LegalHold.organization_id == self.ctx.organization_id,
                LegalHold.code == data.code.strip(),
            )
        )
        if existing is not None:
            raise ConflictError(f"Legal hold code '{data.code}' already exists")
        row = LegalHold(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code.strip(),
            reason=data.reason.strip(),
            scope_json=data.scope_json,
            status="active",
            held_entity_type=data.held_entity_type,
            held_entity_id=data.held_entity_id,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="sh_legal_hold_create",
            entity_type="sh_legal_hold",
            entity_id=row.id,
            payload={"code": row.code, "held_entity_type": row.held_entity_type},
        )
        self._enqueue(
            aggregate_type="sh_legal_hold",
            aggregate_id=row.id,
            event_type="security.legal_hold.created",
            payload={"legal_hold_id": str(row.id), "code": row.code},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_legal_holds(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[LegalHold], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(LegalHold).where(LegalHold.organization_id == self.ctx.organization_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(LegalHold.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def release_legal_hold(self, hold_id: UUID) -> LegalHold:
        row = self.db.get(LegalHold, hold_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Legal hold not found")
        if row.status != "active":
            raise ConflictError("Only active legal holds can be released")
        row.status = "released"
        row.released_by_actor_id = self.ctx.actor_id
        row.released_at = datetime.now(UTC)
        self._audit(
            action="sh_legal_hold_release",
            entity_type="sh_legal_hold",
            entity_id=row.id,
            payload={"code": row.code},
        )
        self._enqueue(
            aggregate_type="sh_legal_hold",
            aggregate_id=row.id,
            event_type="security.legal_hold.released",
            payload={"legal_hold_id": str(row.id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    # --- Deletion jobs ---

    def create_deletion_job(self, data: DeletionJobCreate) -> DeletionJob:
        if data.retention_policy_id is not None:
            policy = self.db.get(RetentionPolicy, data.retention_policy_id)
            if policy is None or policy.organization_id != self.ctx.organization_id:
                raise NotFoundError("Retention policy not found")

        holds = list(
            self.db.scalars(
                select(LegalHold).where(
                    LegalHold.organization_id == self.ctx.organization_id,
                    LegalHold.status == "active",
                )
            )
        )
        blocked = domain.active_hold_blocks_deletion(
            holds=holds,
            entity_type=data.target_entity_type.strip(),
            entity_id=str(data.target_entity_id) if data.target_entity_id else None,
        )
        now = datetime.now(UTC)
        if blocked:
            status = "blocked"
            rows_affected = 0
            completed_at = now
            blocked_reason = blocked
        else:
            status = "completed"
            rows_affected = data.simulated_rows
            completed_at = now
            blocked_reason = None

        row = DeletionJob(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            retention_policy_id=data.retention_policy_id,
            target_entity_type=data.target_entity_type.strip(),
            status=status,
            blocked_reason=blocked_reason,
            rows_affected=rows_affected,
            created_by_actor_id=self.ctx.actor_id,
            completed_at=completed_at,
        )
        self.uow.add(row)
        self._audit(
            action="sh_deletion_job_create",
            entity_type="sh_deletion_job",
            entity_id=row.id,
            payload={
                "status": row.status,
                "target_entity_type": row.target_entity_type,
                "rows_affected": row.rows_affected,
            },
        )
        self._enqueue(
            aggregate_type="sh_deletion_job",
            aggregate_id=row.id,
            event_type=f"security.deletion_job.{status}",
            payload={"deletion_job_id": str(row.id), "status": status},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_deletion_jobs(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[DeletionJob], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(DeletionJob).where(
            DeletionJob.organization_id == self.ctx.organization_id
        )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(DeletionJob.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    # --- Backups ---

    def create_backup_record(self, data: BackupRecordCreate) -> BackupRecord:
        domain.assert_backup_environment(data.environment)
        domain.assert_backup_status(data.status)
        existing = self.db.scalar(
            select(BackupRecord).where(
                BackupRecord.organization_id == self.ctx.organization_id,
                BackupRecord.backup_ref == data.backup_ref.strip(),
            )
        )
        if existing is not None:
            raise ConflictError(f"Backup ref '{data.backup_ref}' already exists")
        row = BackupRecord(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            backup_ref=data.backup_ref.strip(),
            environment=data.environment,
            rpo_minutes=data.rpo_minutes,
            rto_minutes=data.rto_minutes,
            status=data.status,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="sh_backup_record_create",
            entity_type="sh_backup_record",
            entity_id=row.id,
            payload={
                "backup_ref": row.backup_ref,
                "rpo_minutes": row.rpo_minutes,
                "rto_minutes": row.rto_minutes,
            },
        )
        self._enqueue(
            aggregate_type="sh_backup_record",
            aggregate_id=row.id,
            event_type="security.backup.recorded",
            payload={"backup_record_id": str(row.id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_backup_records(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[BackupRecord], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(BackupRecord).where(
            BackupRecord.organization_id == self.ctx.organization_id
        )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(BackupRecord.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def _get_backup(self, backup_id: UUID) -> BackupRecord:
        row = self.db.get(BackupRecord, backup_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Backup record not found")
        return row

    # --- Restore tests ---

    def create_restore_test(self, data: RestoreTestCreate) -> RestoreTest:
        backup = self._get_backup(data.backup_record_id)
        rpo_met, rto_met, validated = domain.assert_rpo_rto_met(
            target_rpo=backup.rpo_minutes,
            target_rto=backup.rto_minutes,
            measured_rpo=data.measured_rpo_minutes,
            measured_rto=data.measured_rto_minutes,
        )
        result = "passed" if validated else "failed"
        domain.assert_restore_result(result)
        row = RestoreTest(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            backup_record_id=backup.id,
            measured_rpo_minutes=data.measured_rpo_minutes,
            measured_rto_minutes=data.measured_rto_minutes,
            result=result,
            notes=data.notes,
            tested_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="sh_restore_test_create",
            entity_type="sh_restore_test",
            entity_id=row.id,
            payload={
                "result": row.result,
                "rpo_met": rpo_met,
                "rto_met": rto_met,
            },
        )
        self._enqueue(
            aggregate_type="sh_restore_test",
            aggregate_id=row.id,
            event_type="security.restore_test.recorded",
            payload={"restore_test_id": str(row.id), "result": result},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_restore_tests(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[RestoreTest], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(RestoreTest).where(
            RestoreTest.organization_id == self.ctx.organization_id
        )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(RestoreTest.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def recovery_validation(self) -> dict[str, Any]:
        backup = self.db.scalar(
            select(BackupRecord)
            .where(BackupRecord.organization_id == self.ctx.organization_id)
            .order_by(BackupRecord.created_at.desc())
            .limit(1)
        )
        restore = self.db.scalar(
            select(RestoreTest)
            .where(RestoreTest.organization_id == self.ctx.organization_id)
            .order_by(RestoreTest.created_at.desc())
            .limit(1)
        )
        if backup is None or restore is None:
            return {
                "backup_record_id": backup.id if backup else None,
                "restore_test_id": restore.id if restore else None,
                "target_rpo_minutes": backup.rpo_minutes if backup else None,
                "target_rto_minutes": backup.rto_minutes if backup else None,
                "measured_rpo_minutes": restore.measured_rpo_minutes if restore else None,
                "measured_rto_minutes": restore.measured_rto_minutes if restore else None,
                "rpo_met": False,
                "rto_met": False,
                "validated": False,
            }
        # Prefer restore linked to latest backup when available
        linked = self.db.scalar(
            select(RestoreTest)
            .where(
                RestoreTest.organization_id == self.ctx.organization_id,
                RestoreTest.backup_record_id == backup.id,
            )
            .order_by(RestoreTest.created_at.desc())
            .limit(1)
        )
        use_restore = linked or restore
        use_backup = backup
        if linked is None and restore.backup_record_id != backup.id:
            use_backup = self._get_backup(restore.backup_record_id)
            use_restore = restore
        rpo_met, rto_met, validated = domain.assert_rpo_rto_met(
            target_rpo=use_backup.rpo_minutes,
            target_rto=use_backup.rto_minutes,
            measured_rpo=use_restore.measured_rpo_minutes,
            measured_rto=use_restore.measured_rto_minutes,
        )
        return {
            "backup_record_id": use_backup.id,
            "restore_test_id": use_restore.id,
            "target_rpo_minutes": use_backup.rpo_minutes,
            "target_rto_minutes": use_backup.rto_minutes,
            "measured_rpo_minutes": use_restore.measured_rpo_minutes,
            "measured_rto_minutes": use_restore.measured_rto_minutes,
            "rpo_met": rpo_met,
            "rto_met": rto_met,
            "validated": validated,
        }

    # --- Incidents ---

    def create_incident(self, data: SecurityIncidentCreate) -> SecurityIncident:
        domain.assert_incident_severity(data.severity)
        domain.assert_incident_status(data.status)
        existing = self.db.scalar(
            select(SecurityIncident).where(
                SecurityIncident.organization_id == self.ctx.organization_id,
                SecurityIncident.code == data.code.strip(),
            )
        )
        if existing is not None:
            raise ConflictError(f"Incident code '{data.code}' already exists")
        row = SecurityIncident(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code.strip(),
            title=data.title.strip(),
            severity=data.severity,
            status=data.status,
            summary=data.summary.strip(),
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="sh_incident_create",
            entity_type="sh_security_incident",
            entity_id=row.id,
            payload={"code": row.code, "severity": row.severity, "status": row.status},
        )
        self._enqueue(
            aggregate_type="sh_security_incident",
            aggregate_id=row.id,
            event_type="security.incident.created",
            payload={
                "incident_id": str(row.id),
                "severity": row.severity,
                "status": row.status,
            },
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_incidents(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[SecurityIncident], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(SecurityIncident).where(
            SecurityIncident.organization_id == self.ctx.organization_id
        )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(SecurityIncident.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def _get_incident(self, incident_id: UUID) -> SecurityIncident:
        row = self.db.get(SecurityIncident, incident_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Security incident not found")
        return row

    def close_incident(
        self, incident_id: UUID, data: SecurityIncidentClose
    ) -> SecurityIncident:
        row = self._get_incident(incident_id)
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        if row.status == "closed":
            raise ConflictError("Incident is already closed")
        row.status = "closed"
        if data.summary:
            row.summary = data.summary.strip()
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self._audit(
            action="sh_incident_close",
            entity_type="sh_security_incident",
            entity_id=row.id,
            payload={"code": row.code, "version": row.version},
        )
        self._enqueue(
            aggregate_type="sh_security_incident",
            aggregate_id=row.id,
            event_type="security.incident.closed",
            payload={"incident_id": str(row.id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def security_gate(self) -> dict[str, Any]:
        incidents = list(
            self.db.scalars(
                select(SecurityIncident).where(
                    SecurityIncident.organization_id == self.ctx.organization_id
                )
            )
        )
        critical_open_count, gate_passed = domain.assert_no_critical_open(incidents)
        return {
            "critical_open_count": critical_open_count,
            "gate_passed": gate_passed,
        }

    # --- Training policy ---

    def get_or_create_training_policy(self) -> TrainingPolicy:
        row = self.db.scalar(
            select(TrainingPolicy).where(
                TrainingPolicy.organization_id == self.ctx.organization_id
            )
        )
        if row is not None:
            return row
        row = TrainingPolicy(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            allow_model_training=False,
            approval_evidence=None,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="sh_training_policy_create",
            entity_type="sh_training_policy",
            entity_id=row.id,
            payload={"allow_model_training": False},
        )
        self._enqueue(
            aggregate_type="sh_training_policy",
            aggregate_id=row.id,
            event_type="security.training_policy.created",
            payload={"training_policy_id": str(row.id)},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def update_training_policy(self, data: TrainingPolicyUpdate) -> TrainingPolicy:
        domain.assert_training_opt_in_allowed(
            allow=data.allow_model_training,
            evidence=data.human_approval_evidence,
        )
        row = self.get_or_create_training_policy()
        row.allow_model_training = data.allow_model_training
        if data.allow_model_training:
            row.approval_evidence = (
                data.human_approval_evidence.strip()
                if data.human_approval_evidence
                else None
            )
        else:
            row.approval_evidence = None
        row.updated_by_actor_id = self.ctx.actor_id
        self._audit(
            action="sh_training_policy_update",
            entity_type="sh_training_policy",
            entity_id=row.id,
            payload={
                "allow_model_training": row.allow_model_training,
                "has_evidence": bool(row.approval_evidence),
            },
        )
        self._enqueue(
            aggregate_type="sh_training_policy",
            aggregate_id=row.id,
            event_type="security.training_policy.updated",
            payload={
                "training_policy_id": str(row.id),
                "allow_model_training": row.allow_model_training,
            },
        )
        self.uow.commit()
        self.db.refresh(row)
        return row
