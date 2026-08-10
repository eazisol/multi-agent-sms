"""Governance application service."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from masms_api.deps import RequestContext
from masms_api.errors import NotFoundError, ValidationAppError
from masms_api.kernel.concurrency import assert_expected_version
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.governance import domain
from masms_api.modules.governance.models import (
    ArchitectureDecision,
    GovernanceApprovalRecord,
    GovernanceAuditEvent,
    GovernanceChangeRequest,
    RequirementMapping,
    SourceBaseline,
)
from masms_api.modules.governance.schemas import (
    AdrCreate,
    AdrTransition,
    ApprovalCreate,
    BaselineCreate,
    BaselineTransition,
    BaselineUpdate,
    ChangeRequestCreate,
    ChangeRequestTransition,
    RequirementMappingCreate,
)

BASELINE_SORT_FIELDS = {
    "baseline_key": SourceBaseline.baseline_key,
    "updated_at": SourceBaseline.updated_at,
    "approval_status": SourceBaseline.approval_status,
    "version": SourceBaseline.version,
}


class GovernanceService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)

    def _audit(
        self,
        *,
        action: str,
        entity_type: str,
        entity_id: UUID,
        entity_version: int | None = None,
        reason: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        self.db.add(
            GovernanceAuditEvent(
                organization_id=self.ctx.organization_id,
                actor_id=self.ctx.actor_id,
                actor_kind=self.ctx.actor_kind.value,
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
                entity_version=entity_version,
                reason=reason,
                source="api",
                correlation_id=self.ctx.correlation_id,
                payload_redacted=payload or {},
            )
        )

    def create_baseline(self, data: BaselineCreate) -> SourceBaseline:
        row = SourceBaseline(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            baseline_key=data.baseline_key,
            title=data.title,
            artifact_path=data.artifact_path,
            document_version=data.document_version,
            classification=data.classification,
            approval_status="draft",
            version=1,
            content_sha256=data.content_sha256,
            owner_actor_id=self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
            metadata_json=data.metadata,
        )
        self.uow.add(row)
        self.uow.flush()
        self._audit(
            action="create",
            entity_type="source_baseline",
            entity_id=row.id,
            entity_version=row.version,
            payload={"baseline_key": row.baseline_key},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="source_baseline",
            aggregate_id=row.id,
            event_type="governance.baseline.created",
            payload={"baseline_key": row.baseline_key, "version": row.version},
            correlation_id=self.ctx.correlation_id,
            project_id=row.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def get_baseline(self, baseline_id: UUID) -> SourceBaseline:
        row = self.db.scalar(
            select(SourceBaseline).where(
                SourceBaseline.id == baseline_id,
                SourceBaseline.organization_id == self.ctx.organization_id,
                SourceBaseline.deleted_at.is_(None),
            )
        )
        if row is None:
            raise NotFoundError("Source baseline not found")
        return row

    def list_baselines(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        status: str | None = None,
        q: str | None = None,
        sort: str = "baseline_key",
    ) -> tuple[list[SourceBaseline], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        if sort not in BASELINE_SORT_FIELDS:
            raise ValidationAppError(
                f"Unsupported sort field '{sort}'. Allowed: {sorted(BASELINE_SORT_FIELDS)}"
            )
        filters = [
            SourceBaseline.organization_id == self.ctx.organization_id,
            SourceBaseline.deleted_at.is_(None),
        ]
        if status:
            filters.append(SourceBaseline.approval_status == status)
        if q:
            pattern = f"%{q}%"
            filters.append(
                or_(
                    SourceBaseline.baseline_key.ilike(pattern),
                    SourceBaseline.title.ilike(pattern),
                )
            )
        total = (
            self.db.scalar(select(func.count()).select_from(SourceBaseline).where(*filters)) or 0
        )
        rows = self.db.scalars(
            select(SourceBaseline)
            .where(*filters)
            .order_by(BASELINE_SORT_FIELDS[sort], SourceBaseline.id)
            .offset(offset)
            .limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def list_baseline_history(
        self,
        baseline_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[GovernanceAuditEvent], PageMeta]:
        self.get_baseline(baseline_id)
        limit, offset = normalize_paging(limit, offset)
        filters = [
            GovernanceAuditEvent.organization_id == self.ctx.organization_id,
            GovernanceAuditEvent.entity_type == "source_baseline",
            GovernanceAuditEvent.entity_id == baseline_id,
        ]
        total = (
            self.db.scalar(select(func.count()).select_from(GovernanceAuditEvent).where(*filters))
            or 0
        )
        rows = self.db.scalars(
            select(GovernanceAuditEvent)
            .where(*filters)
            .order_by(GovernanceAuditEvent.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def update_baseline(self, baseline_id: UUID, data: BaselineUpdate) -> SourceBaseline:
        row = self.get_baseline(baseline_id)
        domain.assert_mutable(row.approval_status)
        assert_expected_version(row, data.expected_version, correlation_id=self.ctx.correlation_id)
        if data.title is not None:
            row.title = data.title
        if data.artifact_path is not None:
            row.artifact_path = data.artifact_path
        if data.document_version is not None:
            row.document_version = data.document_version
        if data.classification is not None:
            row.classification = data.classification
        if data.metadata is not None:
            row.metadata_json = data.metadata
        row.version = domain.next_version(row.version)
        row.updated_by_actor_id = self.ctx.actor_id
        self._audit(
            action="update",
            entity_type="source_baseline",
            entity_id=row.id,
            entity_version=row.version,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def transition_baseline(self, baseline_id: UUID, data: BaselineTransition) -> SourceBaseline:
        row = self.get_baseline(baseline_id)
        assert_expected_version(row, data.expected_version, correlation_id=self.ctx.correlation_id)
        if data.target_status in domain.APPROVED_STATUSES:
            domain.assert_human_approver(self.ctx.actor_kind)
        domain.assert_transition(
            row.approval_status, data.target_status, domain.BASELINE_TRANSITIONS
        )
        if data.target_status in {"rejected", "withdrawn"}:
            domain.assert_reason_when_required(data.target_status, data.reason)
        row.approval_status = data.target_status
        row.version = domain.next_version(row.version)
        row.updated_by_actor_id = self.ctx.actor_id
        if data.target_status == "approved":
            row.effective_from = datetime.now(UTC)
        self._audit(
            action="transition",
            entity_type="source_baseline",
            entity_id=row.id,
            entity_version=row.version,
            reason=data.reason,
            payload={"status": data.target_status},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_requirement_mapping(self, data: RequirementMappingCreate) -> RequirementMapping:
        row = RequirementMapping(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            requirement_id=data.requirement_id,
            requirement_title=data.requirement_title,
            module_id=data.module_id,
            mapping_role=data.mapping_role,
            notes=data.notes,
            status="active",
            version=1,
            owner_actor_id=self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.db.add(row)
        self.uow.flush()
        self._audit(
            action="create",
            entity_type="requirement_mapping",
            entity_id=row.id,
            entity_version=row.version,
            payload={"requirement_id": row.requirement_id, "module_id": row.module_id},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_requirement_mappings(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        q: str | None = None,
    ) -> tuple[list[RequirementMapping], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [
            RequirementMapping.organization_id == self.ctx.organization_id,
            RequirementMapping.deleted_at.is_(None),
        ]
        if q:
            pattern = f"%{q}%"
            filters.append(
                or_(
                    RequirementMapping.requirement_id.ilike(pattern),
                    RequirementMapping.module_id.ilike(pattern),
                    RequirementMapping.requirement_title.ilike(pattern),
                )
            )
        total = (
            self.db.scalar(select(func.count()).select_from(RequirementMapping).where(*filters))
            or 0
        )
        rows = self.db.scalars(
            select(RequirementMapping)
            .where(*filters)
            .order_by(RequirementMapping.requirement_id, RequirementMapping.module_id)
            .offset(offset)
            .limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def create_adr(self, data: AdrCreate) -> ArchitectureDecision:
        row = ArchitectureDecision(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            adr_key=data.adr_key,
            title=data.title,
            status="proposed",
            version=1,
            context=data.context,
            decision=data.decision,
            consequences=data.consequences,
            security_notes=data.security_notes,
            document_path=data.document_path,
            owner_actor_id=self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.db.add(row)
        self.uow.flush()
        self._audit(
            action="create",
            entity_type="architecture_decision",
            entity_id=row.id,
            entity_version=row.version,
            payload={"adr_key": row.adr_key},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_adrs(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        status: str | None = None,
    ) -> tuple[list[ArchitectureDecision], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [
            ArchitectureDecision.organization_id == self.ctx.organization_id,
            ArchitectureDecision.deleted_at.is_(None),
        ]
        if status:
            filters.append(ArchitectureDecision.status == status)
        total = (
            self.db.scalar(select(func.count()).select_from(ArchitectureDecision).where(*filters))
            or 0
        )
        rows = self.db.scalars(
            select(ArchitectureDecision)
            .where(*filters)
            .order_by(ArchitectureDecision.adr_key, ArchitectureDecision.version)
            .offset(offset)
            .limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def get_adr(self, adr_id: UUID) -> ArchitectureDecision:
        row = self.db.scalar(
            select(ArchitectureDecision).where(
                ArchitectureDecision.id == adr_id,
                ArchitectureDecision.organization_id == self.ctx.organization_id,
                ArchitectureDecision.deleted_at.is_(None),
            )
        )
        if row is None:
            raise NotFoundError("Architecture decision not found")
        return row

    def transition_adr(self, adr_id: UUID, data: AdrTransition) -> ArchitectureDecision:
        row = self.get_adr(adr_id)
        assert_expected_version(row, data.expected_version, correlation_id=self.ctx.correlation_id)
        if data.target_status == "accepted":
            domain.assert_human_approver(self.ctx.actor_kind)
        domain.assert_transition(row.status, data.target_status, domain.ADR_TRANSITIONS)
        row.status = data.target_status
        row.version = domain.next_version(row.version)
        row.updated_by_actor_id = self.ctx.actor_id
        self._audit(
            action="transition",
            entity_type="architecture_decision",
            entity_id=row.id,
            entity_version=row.version,
            reason=data.reason,
            payload={"status": data.target_status},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_change_request(self, data: ChangeRequestCreate) -> GovernanceChangeRequest:
        if data.idempotency_key:
            existing = self.db.scalar(
                select(GovernanceChangeRequest).where(
                    GovernanceChangeRequest.organization_id == self.ctx.organization_id,
                    GovernanceChangeRequest.idempotency_key == data.idempotency_key,
                    GovernanceChangeRequest.deleted_at.is_(None),
                )
            )
            if existing is not None:
                return existing

        row = GovernanceChangeRequest(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            change_request_key=data.change_request_key,
            title=data.title,
            summary=data.summary,
            rationale=data.rationale,
            impact=data.impact,
            target_entity_type=data.target_entity_type,
            target_entity_id=data.target_entity_id,
            target_version=data.target_version,
            proposed_version=data.proposed_version,
            priority=data.priority,
            status="draft",
            version=1,
            idempotency_key=data.idempotency_key,
            owner_actor_id=self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.db.add(row)
        self.uow.flush()
        self._audit(
            action="create",
            entity_type="governance_change_request",
            entity_id=row.id,
            entity_version=row.version,
            payload={"change_request_key": row.change_request_key},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_change_requests(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        status: str | None = None,
    ) -> tuple[list[GovernanceChangeRequest], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [
            GovernanceChangeRequest.organization_id == self.ctx.organization_id,
            GovernanceChangeRequest.deleted_at.is_(None),
        ]
        if status:
            filters.append(GovernanceChangeRequest.status == status)
        total = (
            self.db.scalar(
                select(func.count()).select_from(GovernanceChangeRequest).where(*filters)
            )
            or 0
        )
        rows = self.db.scalars(
            select(GovernanceChangeRequest)
            .where(*filters)
            .order_by(GovernanceChangeRequest.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def get_change_request(self, change_request_id: UUID) -> GovernanceChangeRequest:
        row = self.db.scalar(
            select(GovernanceChangeRequest).where(
                GovernanceChangeRequest.id == change_request_id,
                GovernanceChangeRequest.organization_id == self.ctx.organization_id,
                GovernanceChangeRequest.deleted_at.is_(None),
            )
        )
        if row is None:
            raise NotFoundError("Change request not found")
        return row

    def transition_change_request(
        self, change_request_id: UUID, data: ChangeRequestTransition
    ) -> GovernanceChangeRequest:
        row = self.get_change_request(change_request_id)
        assert_expected_version(row, data.expected_version, correlation_id=self.ctx.correlation_id)
        if data.target_status == "approved":
            domain.assert_human_approver(self.ctx.actor_kind)
        domain.assert_transition(row.status, data.target_status, domain.CR_TRANSITIONS)
        if data.target_status in {"rejected", "withdrawn"}:
            domain.assert_reason_when_required(data.target_status, data.reason)
        row.status = data.target_status
        row.version = domain.next_version(row.version)
        row.updated_by_actor_id = self.ctx.actor_id
        self._audit(
            action="transition",
            entity_type="governance_change_request",
            entity_id=row.id,
            entity_version=row.version,
            reason=data.reason,
            payload={"status": data.target_status},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_approval(self, data: ApprovalCreate) -> GovernanceApprovalRecord:
        domain.assert_human_approver(self.ctx.actor_kind)
        domain.assert_reason_when_required(data.decision, data.reason)
        row = GovernanceApprovalRecord(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            target_entity_type=data.target_entity_type,
            target_entity_id=data.target_entity_id,
            target_version=data.target_version,
            decision=data.decision,
            status="decided",
            version=1,
            approver_actor_id=self.ctx.actor_id,
            authority_level=data.authority_level,
            reason=data.reason,
            decided_at=datetime.now(UTC),
            correlation_id=self.ctx.correlation_id,
            owner_actor_id=self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.db.add(row)
        self.uow.flush()
        self._audit(
            action="approval_decision",
            entity_type=data.target_entity_type,
            entity_id=data.target_entity_id,
            entity_version=data.target_version,
            reason=data.reason,
            payload={"decision": data.decision, "authority_level": data.authority_level},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_approvals(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[GovernanceApprovalRecord], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [
            GovernanceApprovalRecord.organization_id == self.ctx.organization_id,
            GovernanceApprovalRecord.deleted_at.is_(None),
        ]
        total = (
            self.db.scalar(
                select(func.count()).select_from(GovernanceApprovalRecord).where(*filters)
            )
            or 0
        )
        rows = self.db.scalars(
            select(GovernanceApprovalRecord)
            .where(*filters)
            .order_by(GovernanceApprovalRecord.decided_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def list_audit_events(self) -> list[GovernanceAuditEvent]:
        rows = self.db.scalars(
            select(GovernanceAuditEvent)
            .where(GovernanceAuditEvent.organization_id == self.ctx.organization_id)
            .order_by(GovernanceAuditEvent.created_at.desc())
        )
        return list(rows)
