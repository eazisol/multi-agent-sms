"""Governance application service."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from masms_api.deps import RequestContext
from masms_api.errors import ConflictError, NotFoundError
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


class GovernanceService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx

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
        self.db.add(row)
        self.db.flush()
        self._audit(
            action="create",
            entity_type="source_baseline",
            entity_id=row.id,
            entity_version=row.version,
            payload={"baseline_key": row.baseline_key},
        )
        self.db.commit()
        self.db.refresh(row)
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

    def list_baselines(self) -> list[SourceBaseline]:
        rows = self.db.scalars(
            select(SourceBaseline)
            .where(
                SourceBaseline.organization_id == self.ctx.organization_id,
                SourceBaseline.deleted_at.is_(None),
            )
            .order_by(SourceBaseline.baseline_key, SourceBaseline.version)
        )
        return list(rows)

    def update_baseline(self, baseline_id: UUID, data: BaselineUpdate) -> SourceBaseline:
        row = self.get_baseline(baseline_id)
        domain.assert_mutable(row.approval_status)
        if row.version != data.expected_version:
            raise ConflictError("Stale version; refresh and retry")
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
        self.db.commit()
        self.db.refresh(row)
        return row

    def transition_baseline(self, baseline_id: UUID, data: BaselineTransition) -> SourceBaseline:
        row = self.get_baseline(baseline_id)
        if row.version != data.expected_version:
            raise ConflictError("Stale version; refresh and retry")
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
        self.db.commit()
        self.db.refresh(row)
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
        self.db.flush()
        self._audit(
            action="create",
            entity_type="requirement_mapping",
            entity_id=row.id,
            entity_version=row.version,
            payload={"requirement_id": row.requirement_id, "module_id": row.module_id},
        )
        self.db.commit()
        self.db.refresh(row)
        return row

    def list_requirement_mappings(self) -> list[RequirementMapping]:
        rows = self.db.scalars(
            select(RequirementMapping)
            .where(
                RequirementMapping.organization_id == self.ctx.organization_id,
                RequirementMapping.deleted_at.is_(None),
            )
            .order_by(RequirementMapping.requirement_id, RequirementMapping.module_id)
        )
        return list(rows)

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
        self.db.flush()
        self._audit(
            action="create",
            entity_type="architecture_decision",
            entity_id=row.id,
            entity_version=row.version,
            payload={"adr_key": row.adr_key},
        )
        self.db.commit()
        self.db.refresh(row)
        return row

    def list_adrs(self) -> list[ArchitectureDecision]:
        rows = self.db.scalars(
            select(ArchitectureDecision)
            .where(
                ArchitectureDecision.organization_id == self.ctx.organization_id,
                ArchitectureDecision.deleted_at.is_(None),
            )
            .order_by(ArchitectureDecision.adr_key, ArchitectureDecision.version)
        )
        return list(rows)

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
        if row.version != data.expected_version:
            raise ConflictError("Stale version; refresh and retry")
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
        self.db.commit()
        self.db.refresh(row)
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
        self.db.flush()
        self._audit(
            action="create",
            entity_type="governance_change_request",
            entity_id=row.id,
            entity_version=row.version,
            payload={"change_request_key": row.change_request_key},
        )
        self.db.commit()
        self.db.refresh(row)
        return row

    def list_change_requests(self) -> list[GovernanceChangeRequest]:
        rows = self.db.scalars(
            select(GovernanceChangeRequest)
            .where(
                GovernanceChangeRequest.organization_id == self.ctx.organization_id,
                GovernanceChangeRequest.deleted_at.is_(None),
            )
            .order_by(GovernanceChangeRequest.created_at.desc())
        )
        return list(rows)

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
        if row.version != data.expected_version:
            raise ConflictError("Stale version; refresh and retry")
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
        self.db.commit()
        self.db.refresh(row)
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
        self.db.flush()
        self._audit(
            action="approval_decision",
            entity_type=data.target_entity_type,
            entity_id=data.target_entity_id,
            entity_version=data.target_version,
            reason=data.reason,
            payload={"decision": data.decision, "authority_level": data.authority_level},
        )
        self.db.commit()
        self.db.refresh(row)
        return row

    def list_approvals(self) -> list[GovernanceApprovalRecord]:
        rows = self.db.scalars(
            select(GovernanceApprovalRecord)
            .where(
                GovernanceApprovalRecord.organization_id == self.ctx.organization_id,
                GovernanceApprovalRecord.deleted_at.is_(None),
            )
            .order_by(GovernanceApprovalRecord.decided_at.desc())
        )
        return list(rows)

    def list_audit_events(self) -> list[GovernanceAuditEvent]:
        rows = self.db.scalars(
            select(GovernanceAuditEvent)
            .where(GovernanceAuditEvent.organization_id == self.ctx.organization_id)
            .order_by(GovernanceAuditEvent.created_at.desc())
        )
        return list(rows)
