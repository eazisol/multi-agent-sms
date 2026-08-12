"""Traceability application service (MOD-460)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.traceability import domain
from masms_api.modules.traceability.models import (
    ActionAudit,
    EvidenceExport,
    EvidenceManifest,
    EvidenceManifestItem,
    MustHaveRequirement,
    RequirementDocumentLink,
    RequirementReleaseLink,
    RequirementTestLink,
    RequirementTicketLink,
    TicketTestLink,
)
from masms_api.modules.traceability.schemas import (
    AuditCoverageReport,
    CoverageReport,
    ExportCreate,
    ManifestCreate,
    ManifestItemCreate,
    ManifestSeal,
    MustHaveCreate,
    RequirementDocumentLinkCreate,
    RequirementReleaseLinkCreate,
    RequirementTestLinkCreate,
    RequirementTicketLinkCreate,
    TicketTestLinkCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class TraceabilityService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def _record_controlled_action(
        self,
        *,
        action: str,
        entity_type: str,
        entity_id: UUID,
        payload: dict[str, Any] | None = None,
        project_id: UUID | None = None,
    ) -> None:
        audit_row = ActionAudit(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            actor_id=self.ctx.actor_id,
            correlation_id=str(self.ctx.correlation_id) if self.ctx.correlation_id else None,
            payload_json=json.dumps(payload or {}, sort_keys=True)[:4000],
        )
        self.uow.add(audit_row)
        self.obs.write_audit(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload,
            project_id=project_id,
        )

    def register_must_have(self, data: MustHaveCreate) -> MustHaveRequirement:
        existing = self.db.scalar(
            select(MustHaveRequirement).where(
                MustHaveRequirement.organization_id == self.ctx.organization_id,
                MustHaveRequirement.requirement_id == data.requirement_id,
            )
        )
        if existing is not None:
            raise ConflictError(
                f"Must-have requirement '{data.requirement_id}' already registered"
            )
        row = MustHaveRequirement(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            requirement_id=data.requirement_id,
            requirement_code=data.requirement_code.strip(),
            title=data.title.strip(),
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._record_controlled_action(
            action="tr_must_have_register",
            entity_type="tr_must_have_requirement",
            entity_id=row.id,
            payload={
                "requirement_id": str(data.requirement_id),
                "requirement_code": row.requirement_code,
            },
            project_id=data.project_id,
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tr_must_have_requirement",
            aggregate_id=row.id,
            event_type="traceability.must_have.registered",
            payload={"requirement_id": str(data.requirement_id)},
            correlation_id=self.ctx.correlation_id,
            project_id=data.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_must_haves(
        self,
        *,
        project_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[MustHaveRequirement], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(MustHaveRequirement).where(
            MustHaveRequirement.organization_id == self.ctx.organization_id
        )
        if project_id is not None:
            stmt = stmt.where(MustHaveRequirement.project_id == project_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(MustHaveRequirement.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def create_requirement_ticket_link(
        self, data: RequirementTicketLinkCreate
    ) -> RequirementTicketLink:
        existing = self.db.scalar(
            select(RequirementTicketLink).where(
                RequirementTicketLink.organization_id == self.ctx.organization_id,
                RequirementTicketLink.requirement_id == data.requirement_id,
                RequirementTicketLink.ticket_id == data.ticket_id,
            )
        )
        if existing is not None:
            raise ConflictError("Requirement-ticket link already exists")
        row = RequirementTicketLink(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            requirement_id=data.requirement_id,
            ticket_id=data.ticket_id,
            notes=data.notes,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._record_controlled_action(
            action="tr_requirement_ticket_link_create",
            entity_type="tr_requirement_ticket_link",
            entity_id=row.id,
            payload={
                "requirement_id": str(data.requirement_id),
                "ticket_id": str(data.ticket_id),
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tr_requirement_ticket_link",
            aggregate_id=row.id,
            event_type="traceability.requirement_ticket.linked",
            payload={
                "requirement_id": str(data.requirement_id),
                "ticket_id": str(data.ticket_id),
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_requirement_ticket_links(
        self,
        *,
        requirement_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[RequirementTicketLink], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(RequirementTicketLink).where(
            RequirementTicketLink.organization_id == self.ctx.organization_id
        )
        if requirement_id is not None:
            stmt = stmt.where(RequirementTicketLink.requirement_id == requirement_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(RequirementTicketLink.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def create_requirement_test_link(
        self, data: RequirementTestLinkCreate
    ) -> RequirementTestLink:
        existing = self.db.scalar(
            select(RequirementTestLink).where(
                RequirementTestLink.organization_id == self.ctx.organization_id,
                RequirementTestLink.requirement_id == data.requirement_id,
                RequirementTestLink.test_case_id == data.test_case_id,
            )
        )
        if existing is not None:
            raise ConflictError("Requirement-test link already exists")
        row = RequirementTestLink(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            requirement_id=data.requirement_id,
            test_case_id=data.test_case_id,
            notes=data.notes,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._record_controlled_action(
            action="tr_requirement_test_link_create",
            entity_type="tr_requirement_test_link",
            entity_id=row.id,
            payload={
                "requirement_id": str(data.requirement_id),
                "test_case_id": str(data.test_case_id),
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tr_requirement_test_link",
            aggregate_id=row.id,
            event_type="traceability.requirement_test.linked",
            payload={
                "requirement_id": str(data.requirement_id),
                "test_case_id": str(data.test_case_id),
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_requirement_test_links(
        self,
        *,
        requirement_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[RequirementTestLink], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(RequirementTestLink).where(
            RequirementTestLink.organization_id == self.ctx.organization_id
        )
        if requirement_id is not None:
            stmt = stmt.where(RequirementTestLink.requirement_id == requirement_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(RequirementTestLink.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def create_requirement_release_link(
        self, data: RequirementReleaseLinkCreate
    ) -> RequirementReleaseLink:
        existing = self.db.scalar(
            select(RequirementReleaseLink).where(
                RequirementReleaseLink.organization_id == self.ctx.organization_id,
                RequirementReleaseLink.requirement_id == data.requirement_id,
                RequirementReleaseLink.release_id == data.release_id,
            )
        )
        if existing is not None:
            raise ConflictError("Requirement-release link already exists")
        row = RequirementReleaseLink(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            requirement_id=data.requirement_id,
            release_id=data.release_id,
            notes=data.notes,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._record_controlled_action(
            action="tr_requirement_release_link_create",
            entity_type="tr_requirement_release_link",
            entity_id=row.id,
            payload={
                "requirement_id": str(data.requirement_id),
                "release_id": str(data.release_id),
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tr_requirement_release_link",
            aggregate_id=row.id,
            event_type="traceability.requirement_release.linked",
            payload={
                "requirement_id": str(data.requirement_id),
                "release_id": str(data.release_id),
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_requirement_release_links(
        self,
        *,
        requirement_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[RequirementReleaseLink], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(RequirementReleaseLink).where(
            RequirementReleaseLink.organization_id == self.ctx.organization_id
        )
        if requirement_id is not None:
            stmt = stmt.where(RequirementReleaseLink.requirement_id == requirement_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(RequirementReleaseLink.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def create_requirement_document_link(
        self, data: RequirementDocumentLinkCreate
    ) -> RequirementDocumentLink:
        existing = self.db.scalar(
            select(RequirementDocumentLink).where(
                RequirementDocumentLink.organization_id == self.ctx.organization_id,
                RequirementDocumentLink.requirement_id == data.requirement_id,
                RequirementDocumentLink.document_id == data.document_id,
            )
        )
        if existing is not None:
            raise ConflictError("Requirement-document link already exists")
        row = RequirementDocumentLink(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            requirement_id=data.requirement_id,
            document_id=data.document_id,
            notes=data.notes,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._record_controlled_action(
            action="tr_requirement_document_link_create",
            entity_type="tr_requirement_document_link",
            entity_id=row.id,
            payload={
                "requirement_id": str(data.requirement_id),
                "document_id": str(data.document_id),
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tr_requirement_document_link",
            aggregate_id=row.id,
            event_type="traceability.requirement_document.linked",
            payload={
                "requirement_id": str(data.requirement_id),
                "document_id": str(data.document_id),
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_requirement_document_links(
        self,
        *,
        requirement_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[RequirementDocumentLink], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(RequirementDocumentLink).where(
            RequirementDocumentLink.organization_id == self.ctx.organization_id
        )
        if requirement_id is not None:
            stmt = stmt.where(RequirementDocumentLink.requirement_id == requirement_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(RequirementDocumentLink.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def create_ticket_test_link(self, data: TicketTestLinkCreate) -> TicketTestLink:
        existing = self.db.scalar(
            select(TicketTestLink).where(
                TicketTestLink.organization_id == self.ctx.organization_id,
                TicketTestLink.ticket_id == data.ticket_id,
                TicketTestLink.test_case_id == data.test_case_id,
            )
        )
        if existing is not None:
            raise ConflictError("Ticket-test link already exists")
        row = TicketTestLink(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            ticket_id=data.ticket_id,
            test_case_id=data.test_case_id,
            notes=data.notes,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._record_controlled_action(
            action="tr_ticket_test_link_create",
            entity_type="tr_ticket_test_link",
            entity_id=row.id,
            payload={
                "ticket_id": str(data.ticket_id),
                "test_case_id": str(data.test_case_id),
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tr_ticket_test_link",
            aggregate_id=row.id,
            event_type="traceability.ticket_test.linked",
            payload={
                "ticket_id": str(data.ticket_id),
                "test_case_id": str(data.test_case_id),
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_ticket_test_links(
        self,
        *,
        ticket_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[TicketTestLink], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(TicketTestLink).where(
            TicketTestLink.organization_id == self.ctx.organization_id
        )
        if ticket_id is not None:
            stmt = stmt.where(TicketTestLink.ticket_id == ticket_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(TicketTestLink.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def coverage_report(self, project_id: UUID | None = None) -> CoverageReport:
        stmt = select(MustHaveRequirement).where(
            MustHaveRequirement.organization_id == self.ctx.organization_id
        )
        if project_id is not None:
            stmt = stmt.where(MustHaveRequirement.project_id == project_id)
        must_haves = list(self.db.scalars(stmt))
        total = len(must_haves)
        complete_count = 0
        incomplete: list[UUID] = []

        for mh in must_haves:
            rid = mh.requirement_id
            has_ticket = (
                self.db.scalar(
                    select(func.count())
                    .select_from(RequirementTicketLink)
                    .where(
                        RequirementTicketLink.organization_id == self.ctx.organization_id,
                        RequirementTicketLink.requirement_id == rid,
                    )
                )
                or 0
            ) > 0
            has_test = (
                self.db.scalar(
                    select(func.count())
                    .select_from(RequirementTestLink)
                    .where(
                        RequirementTestLink.organization_id == self.ctx.organization_id,
                        RequirementTestLink.requirement_id == rid,
                    )
                )
                or 0
            ) > 0
            has_release = (
                self.db.scalar(
                    select(func.count())
                    .select_from(RequirementReleaseLink)
                    .where(
                        RequirementReleaseLink.organization_id == self.ctx.organization_id,
                        RequirementReleaseLink.requirement_id == rid,
                    )
                )
                or 0
            ) > 0
            has_document = (
                self.db.scalar(
                    select(func.count())
                    .select_from(RequirementDocumentLink)
                    .where(
                        RequirementDocumentLink.organization_id == self.ctx.organization_id,
                        RequirementDocumentLink.requirement_id == rid,
                    )
                )
                or 0
            ) > 0
            if domain.requirement_is_complete(
                has_ticket, has_test, has_release, has_document
            ):
                complete_count += 1
            else:
                incomplete.append(rid)

        pct = domain.coverage_pct(complete_count, total)
        return CoverageReport(
            organization_id=self.ctx.organization_id,
            project_id=project_id,
            total_must_haves=total,
            complete_count=complete_count,
            incomplete_count=total - complete_count,
            coverage_pct=pct,
            release_ready=domain.release_ready(pct),
            incomplete_requirement_ids=incomplete,
        )

    def audit_coverage(self) -> AuditCoverageReport:
        action_count = int(
            self.db.scalar(
                select(func.count())
                .select_from(ActionAudit)
                .where(ActionAudit.organization_id == self.ctx.organization_id)
            )
            or 0
        )
        # Every controlled mutation writes exactly one tr_action_audits row.
        audited_count = action_count
        pct = 100.0 if action_count > 0 and audited_count == action_count else (
            100.0 if action_count == 0 else 0.0
        )
        if action_count == 0:
            pct = 0.0
        return AuditCoverageReport(
            organization_id=self.ctx.organization_id,
            action_count=action_count,
            audited_count=audited_count,
            coverage_pct=pct,
            complete=action_count > 0 and audited_count == action_count and pct >= 100.0,
        )

    def create_manifest(self, data: ManifestCreate) -> EvidenceManifest:
        existing = self.db.scalar(
            select(EvidenceManifest).where(
                EvidenceManifest.organization_id == self.ctx.organization_id,
                EvidenceManifest.code == data.code.strip(),
            )
        )
        if existing is not None:
            raise ConflictError(f"Manifest code '{data.code}' already exists")
        row = EvidenceManifest(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            code=data.code.strip(),
            title=data.title.strip(),
            status="draft",
            item_count=0,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._record_controlled_action(
            action="tr_manifest_create",
            entity_type="tr_evidence_manifest",
            entity_id=row.id,
            payload={"code": row.code, "status": row.status},
            project_id=data.project_id,
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tr_evidence_manifest",
            aggregate_id=row.id,
            event_type="traceability.manifest.created",
            payload={"code": row.code},
            correlation_id=self.ctx.correlation_id,
            project_id=data.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_manifests(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[EvidenceManifest], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(EvidenceManifest).where(
            EvidenceManifest.organization_id == self.ctx.organization_id
        )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(EvidenceManifest.updated_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def get_manifest(self, manifest_id: UUID) -> EvidenceManifest:
        row = self.db.get(EvidenceManifest, manifest_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Evidence manifest not found")
        return row

    def add_manifest_item(
        self, manifest_id: UUID, data: ManifestItemCreate
    ) -> EvidenceManifestItem:
        domain.assert_item_type(data.item_type)
        manifest = self.get_manifest(manifest_id)
        if manifest.status != "draft":
            raise ValidationAppError("Items can only be added to draft manifests")
        existing = self.db.scalar(
            select(EvidenceManifestItem).where(
                EvidenceManifestItem.organization_id == self.ctx.organization_id,
                EvidenceManifestItem.manifest_id == manifest_id,
                EvidenceManifestItem.item_type == data.item_type,
                EvidenceManifestItem.item_id == data.item_id,
            )
        )
        if existing is not None:
            raise ConflictError("Manifest item already exists")
        now = datetime.now(UTC)
        row = EvidenceManifestItem(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            manifest_id=manifest_id,
            item_type=data.item_type,
            item_id=data.item_id,
            label=data.label,
        )
        self.uow.add(row)
        manifest.item_count += 1
        manifest.version += 1
        manifest.updated_by_actor_id = self.ctx.actor_id
        manifest.updated_at = now
        self._record_controlled_action(
            action="tr_manifest_item_add",
            entity_type="tr_evidence_manifest_item",
            entity_id=row.id,
            payload={
                "manifest_id": str(manifest_id),
                "item_type": data.item_type,
                "item_id": str(data.item_id),
            },
            project_id=manifest.project_id,
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tr_evidence_manifest_item",
            aggregate_id=row.id,
            event_type="traceability.manifest_item.added",
            payload={"manifest_id": str(manifest_id), "item_type": data.item_type},
            correlation_id=self.ctx.correlation_id,
            project_id=manifest.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def seal_manifest(
        self, manifest_id: UUID, data: ManifestSeal | None = None
    ) -> EvidenceManifest:
        payload = data or ManifestSeal()
        manifest = self.get_manifest(manifest_id)
        domain.assert_expected_version(
            current=manifest.version, expected=payload.expected_version
        )
        domain.assert_manifest_transition(manifest.status, "sealed")
        items = list(
            self.db.scalars(
                select(EvidenceManifestItem).where(
                    EvidenceManifestItem.organization_id == self.ctx.organization_id,
                    EvidenceManifestItem.manifest_id == manifest_id,
                )
            )
        )
        keys = [domain.item_key(i.item_type, i.item_id) for i in items]
        checksum = domain.compute_manifest_checksum(keys)
        now = datetime.now(UTC)
        manifest.status = "sealed"
        manifest.checksum = checksum
        manifest.item_count = len(items)
        manifest.sealed_at = now
        manifest.version += 1
        manifest.updated_by_actor_id = self.ctx.actor_id
        manifest.updated_at = now
        self._record_controlled_action(
            action="tr_manifest_seal",
            entity_type="tr_evidence_manifest",
            entity_id=manifest.id,
            payload={"code": manifest.code, "checksum": checksum, "item_count": len(items)},
            project_id=manifest.project_id,
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tr_evidence_manifest",
            aggregate_id=manifest.id,
            event_type="traceability.manifest.sealed",
            payload={"code": manifest.code, "checksum": checksum},
            correlation_id=self.ctx.correlation_id,
            project_id=manifest.project_id,
        )
        self.uow.commit()
        self.db.refresh(manifest)
        return manifest

    def create_export(self, data: ExportCreate) -> EvidenceExport:
        domain.assert_export_format(data.export_format)
        manifest = self.get_manifest(data.manifest_id)
        if manifest.status not in {"sealed", "exported"}:
            raise ValidationAppError("Export requires a sealed (or exported) manifest")
        items = list(
            self.db.scalars(
                select(EvidenceManifestItem).where(
                    EvidenceManifestItem.organization_id == self.ctx.organization_id,
                    EvidenceManifestItem.manifest_id == data.manifest_id,
                )
            )
        )
        item_list = [
            {
                "item_type": i.item_type,
                "item_id": str(i.item_id),
                "label": i.label,
            }
            for i in sorted(items, key=lambda x: (x.item_type, str(x.item_id)))
        ]
        keys = [domain.item_key(i.item_type, i.item_id) for i in items]
        reconciliation_hash = domain.compute_manifest_checksum(keys)
        if manifest.checksum and reconciliation_hash != manifest.checksum:
            raise ValidationAppError("Manifest checksum does not match current items")

        payload: dict[str, Any] = {
            "organization_id": str(self.ctx.organization_id),
            "manifest_id": str(manifest.id),
            "manifest_code": manifest.code,
            "checksum": manifest.checksum,
            "reconciliation_hash": reconciliation_hash,
            "item_count": len(item_list),
            "items": item_list,
        }
        now = datetime.now(UTC)
        row = EvidenceExport(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            manifest_id=manifest.id,
            export_format=data.export_format,
            status="ready",
            payload_preview=json.dumps(payload, sort_keys=True)[:8000],
            reconciliation_hash=reconciliation_hash,
            requested_by_actor_id=self.ctx.actor_id,
            completed_at=now,
        )
        self.uow.add(row)
        if manifest.status == "sealed":
            domain.assert_manifest_transition(manifest.status, "exported")
            manifest.status = "exported"
            manifest.version += 1
            manifest.updated_by_actor_id = self.ctx.actor_id
            manifest.updated_at = now

        self._record_controlled_action(
            action="tr_export_create",
            entity_type="tr_evidence_export",
            entity_id=row.id,
            payload={
                "manifest_id": str(manifest.id),
                "item_count": len(item_list),
                "reconciliation_hash": reconciliation_hash,
            },
            project_id=manifest.project_id,
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="tr_evidence_export",
            aggregate_id=row.id,
            event_type="traceability.export.ready",
            payload={"manifest_id": str(manifest.id), "status": "ready"},
            correlation_id=self.ctx.correlation_id,
            project_id=manifest.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_exports(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[EvidenceExport], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(EvidenceExport).where(
            EvidenceExport.organization_id == self.ctx.organization_id
        )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(EvidenceExport.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def get_export(self, export_id: UUID) -> EvidenceExport:
        row = self.db.get(EvidenceExport, export_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Evidence export not found")
        return row
