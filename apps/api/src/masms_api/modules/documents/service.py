"""Documents application service (MOD-250)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from masms_api.errors import ForbiddenError, NotFoundError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.documents import domain
from masms_api.modules.documents.models import (
    Document,
    DocumentAttachment,
    DocumentPermission,
    DocumentTemplate,
    DocumentTemplateVersion,
    DocumentVersion,
    ScanResult,
)
from masms_api.modules.documents.schemas import (
    AccessCheckRequest,
    AttachmentCreate,
    DocumentCreate,
    DocumentVersionCreate,
    MarkAvailableRequest,
    PermissionCreate,
    ScanResultCreate,
    TemplateCreate,
    TemplateVersionCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class DocumentsService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_template(self, data: TemplateCreate) -> DocumentTemplate:
        row = DocumentTemplate(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code,
            title=data.title,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="template_create",
            entity_type="doc_template",
            entity_id=row.id,
            payload={"code": data.code},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_template_version(self, data: TemplateVersionCreate) -> DocumentTemplateVersion:
        template = self._get_template(data.template_id)
        next_version = (
            self.db.scalar(
                select(func.max(DocumentTemplateVersion.version_number)).where(
                    DocumentTemplateVersion.template_id == template.id
                )
            )
            or 0
        ) + 1
        row = DocumentTemplateVersion(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            template_id=template.id,
            version_number=next_version,
            status="draft",
            body_markdown=data.body_markdown,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def publish_template_version(self, version_id: UUID) -> DocumentTemplateVersion:
        row = self._get_template_version(version_id)
        domain.assert_can_publish_template(row.status)
        for prior in self.db.scalars(
            select(DocumentTemplateVersion).where(
                DocumentTemplateVersion.template_id == row.template_id,
                DocumentTemplateVersion.status == "published",
            )
        ):
            prior.status = "superseded"
            self.uow.add(prior)
        row.status = "published"
        row.published_at = datetime.now(UTC)
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_document(self, data: DocumentCreate) -> Document:
        client_id = data.client_id or self.ctx.tenant.client_id
        if self.ctx.tenant.client_id and client_id and client_id != self.ctx.tenant.client_id:
            raise ForbiddenError("Cross-client access denied")
        if data.template_id is not None:
            self._get_template(data.template_id)
        row = Document(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            client_id=client_id,
            project_id=data.project_id or self.ctx.tenant.project_id,
            title=data.title,
            classification=data.classification,
            status="draft",
            owner_actor_id=data.owner_actor_id or self.ctx.actor_id,
            template_id=data.template_id,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="document_create",
            entity_type="doc_document",
            entity_id=row.id,
            payload={"title": data.title, "classification": data.classification},
            project_id=row.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_document_version(self, data: DocumentVersionCreate) -> DocumentVersion:
        document = self._get_document(data.document_id)
        next_version = (
            self.db.scalar(
                select(func.max(DocumentVersion.version_number)).where(
                    DocumentVersion.document_id == document.id
                )
            )
            or 0
        ) + 1
        row = DocumentVersion(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            document_id=document.id,
            version_number=next_version,
            status="draft",
            owner_actor_id=document.owner_actor_id,
            storage_key=data.storage_key,
            filename=data.filename,
            content_type=data.content_type,
            size_bytes=data.size_bytes,
            checksum_sha256=data.checksum_sha256,
            indexing_allowed=False,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="document_version_create",
            entity_type="doc_document_version",
            entity_id=row.id,
            payload={"version_number": next_version, "filename": data.filename},
            project_id=document.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def add_attachment(self, data: AttachmentCreate) -> DocumentAttachment:
        version = self._get_document_version(data.document_version_id)
        if version.status in {domain.QUARANTINE, "retired"}:
            raise ForbiddenError("Cannot attach to quarantined or retired version")
        row = DocumentAttachment(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            document_version_id=version.id,
            storage_key=data.storage_key,
            filename=data.filename,
            content_type=data.content_type,
            size_bytes=data.size_bytes,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def grant_permission(self, data: PermissionCreate) -> DocumentPermission:
        document = self._get_document(data.document_id)
        existing = self.db.scalar(
            select(DocumentPermission).where(
                DocumentPermission.document_id == document.id,
                DocumentPermission.grantee_actor_id == data.grantee_actor_id,
            )
        )
        if existing is not None:
            existing.can_download = data.can_download
            existing.can_preview = data.can_preview
            existing.can_extract_text = data.can_extract_text
            existing.can_use_embeddings = data.can_use_embeddings
            row = existing
            self.uow.add(row)
        else:
            row = DocumentPermission(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                document_id=document.id,
                grantee_actor_id=data.grantee_actor_id,
                can_download=data.can_download,
                can_preview=data.can_preview,
                can_extract_text=data.can_extract_text,
                can_use_embeddings=data.can_use_embeddings,
                created_by_actor_id=self.ctx.actor_id,
            )
            self.uow.add(row)
        self.obs.write_audit(
            action="document_permission_grant",
            entity_type="doc_document_permission",
            entity_id=row.id,
            payload={"grantee": str(data.grantee_actor_id)},
            project_id=document.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def record_scan(self, data: ScanResultCreate) -> ScanResult:
        version = self._get_document_version(data.document_version_id)
        domain.assert_scan_verdict(data.verdict)
        next_status = domain.apply_scan_to_version_status(data.verdict)
        version.status = next_status
        if next_status == domain.QUARANTINE:
            version.indexing_allowed = False
        self.uow.add(version)
        row = ScanResult(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            document_version_id=version.id,
            engine=data.engine,
            verdict=data.verdict,
            detail=data.detail,
            metadata_json=data.metadata,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="doc_scan_result",
            aggregate_id=row.id,
            event_type="documents.scan.recorded",
            payload={"verdict": data.verdict, "document_version_id": str(version.id)},
            correlation_id=self.ctx.correlation_id,
        )
        self.obs.write_audit(
            action="document_scan_record",
            entity_type="doc_scan_result",
            entity_id=row.id,
            payload={"verdict": data.verdict},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def mark_available(
        self, version_id: UUID, data: MarkAvailableRequest
    ) -> DocumentVersion:
        version = self._get_document_version(version_id)
        document = self._get_document(version.document_id)
        latest = self._latest_scan(version.id)
        domain.assert_can_mark_available(
            status=version.status,
            latest_verdict=latest.verdict if latest else None,
            owner_actor_id=version.owner_actor_id,
            effective_at=data.effective_at,
        )
        version.status = domain.AVAILABLE
        version.effective_at = data.effective_at
        version.indexing_allowed = True
        document.status = "active"
        document.current_version_id = version.id
        self.uow.add(version)
        self.uow.add(document)
        self.obs.write_audit(
            action="document_version_available",
            entity_type="doc_document_version",
            entity_id=version.id,
            payload={
                "version_number": version.version_number,
                "effective_at": data.effective_at.isoformat(),
            },
            project_id=document.project_id,
        )
        self.uow.commit()
        self.uow.refresh(version)
        return version

    def check_access(self, data: AccessCheckRequest) -> dict[str, object]:
        version = self._get_document_version(data.document_version_id)
        document = self._get_document(version.document_id)
        perm = self.db.scalar(
            select(DocumentPermission).where(
                DocumentPermission.document_id == document.id,
                DocumentPermission.grantee_actor_id == data.actor_id,
            )
        )
        if perm is None:
            raise ForbiddenError("No document permission grant for actor")
        domain.assert_access_granted(
            action=data.action,
            version_status=version.status,
            can_download=perm.can_download,
            can_preview=perm.can_preview,
            can_extract_text=perm.can_extract_text,
            can_use_embeddings=perm.can_use_embeddings,
        )
        return {
            "allowed": True,
            "action": data.action,
            "document_version_id": version.id,
            "version_status": version.status,
        }

    def _latest_scan(self, version_id: UUID) -> ScanResult | None:
        return self.db.scalar(
            select(ScanResult)
            .where(ScanResult.document_version_id == version_id)
            .order_by(ScanResult.scanned_at.desc(), ScanResult.created_at.desc())
            .limit(1)
        )

    def _get_template(self, template_id: UUID) -> DocumentTemplate:
        row = self.db.scalar(select(DocumentTemplate).where(DocumentTemplate.id == template_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Template not found")
        return row

    def _get_template_version(self, version_id: UUID) -> DocumentTemplateVersion:
        row = self.db.scalar(
            select(DocumentTemplateVersion).where(DocumentTemplateVersion.id == version_id)
        )
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Template version not found")
        return row

    def _get_document(self, document_id: UUID) -> Document:
        row = self.db.scalar(select(Document).where(Document.id == document_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Document not found")
        ctx_client = self.ctx.tenant.client_id
        if ctx_client and row.client_id and row.client_id != ctx_client:
            raise ForbiddenError("Cross-client access denied")
        return row

    def _get_document_version(self, version_id: UUID) -> DocumentVersion:
        row = self.db.scalar(select(DocumentVersion).where(DocumentVersion.id == version_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Document version not found")
        self._get_document(row.document_id)
        return row
