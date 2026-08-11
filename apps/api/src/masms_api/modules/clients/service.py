"""Clients application service (MOD-200)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, ForbiddenError, NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.clients import domain
from masms_api.modules.clients.models import (
    Client,
    CommunicationPreference,
    Contact,
    DuplicateSuggestion,
    MergeHistory,
    ProjectContact,
)
from masms_api.modules.clients.schemas import (
    ClientCreate,
    CommunicationPreferenceCreate,
    ContactCreate,
    DuplicateSuggestionCreate,
    MergeClientsRequest,
    ProjectContactCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class ClientsService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_client(self, data: ClientCreate) -> Client:
        if self.db.scalar(
            select(Client).where(
                Client.organization_id == self.ctx.organization_id,
                Client.code == data.code,
                Client.deleted_at.is_(None),
            )
        ):
            raise ConflictError(f"Client code '{data.code}' already exists")
        row = Client(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code,
            legal_name=data.legal_name,
            trading_name=data.trading_name,
            status="active",
            owner_actor_id=data.owner_actor_id or self.ctx.actor_id,
            industry=data.industry,
            website=data.website,
            notes=data.notes,
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="client_create",
            entity_type="crm_client",
            entity_id=row.id,
            payload={"code": data.code, "legal_name": data.legal_name},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="crm_client",
            aggregate_id=row.id,
            event_type="clients.client.created",
            payload={"code": data.code},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_clients(
        self,
        *,
        q: str | None = None,
        status: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Client], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [
            Client.organization_id == self.ctx.organization_id,
            Client.deleted_at.is_(None),
        ]
        if self.ctx.tenant.client_id is not None:
            filters.append(Client.id == self.ctx.tenant.client_id)
        if status:
            filters.append(Client.status == status)
        if q and q.strip():
            like = f"%{q.strip()}%"
            filters.append(
                or_(
                    Client.legal_name.ilike(like),
                    Client.code.ilike(like),
                    Client.trading_name.ilike(like),
                    Client.industry.ilike(like),
                )
            )
        total = self.db.scalar(select(func.count()).select_from(Client).where(*filters)) or 0
        rows = list(
            self.db.scalars(
                select(Client)
                .where(*filters)
                .order_by(Client.legal_name)
                .offset(offset)
                .limit(limit)
            )
        )
        return rows, build_page_meta(limit=limit, offset=offset, total=int(total))

    def create_contact(self, data: ContactCreate) -> Contact:
        client = self._get_client(data.client_id)
        domain.assert_authority_level(data.authority_level)
        email = domain.normalize_email(data.email)
        if self.db.scalar(
            select(Contact).where(
                Contact.organization_id == self.ctx.organization_id,
                Contact.client_id == client.id,
                Contact.email == email,
                Contact.deleted_at.is_(None),
            )
        ):
            raise ConflictError("Contact email already exists for this client")
        if data.is_primary:
            self._clear_primary(client.id)
        row = Contact(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            client_id=client.id,
            full_name=data.full_name,
            email=email,
            phone=data.phone,
            job_title=data.job_title,
            authority_level=data.authority_level,
            is_primary=data.is_primary,
            status="active",
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="contact_create",
            entity_type="crm_contact",
            entity_id=row.id,
            payload={
                "client_id": str(client.id),
                "authority_level": data.authority_level,
                "is_primary": data.is_primary,
            },
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_contacts(self, *, client_id: UUID) -> list[Contact]:
        self._get_client(client_id)
        rows = self.db.scalars(
            select(Contact).where(
                Contact.organization_id == self.ctx.organization_id,
                Contact.client_id == client_id,
                Contact.deleted_at.is_(None),
            )
        )
        return list(rows)

    def create_project_contact(self, data: ProjectContactCreate) -> ProjectContact:
        client = self._get_client(data.client_id)
        contact = self._get_contact(data.contact_id)
        if contact.client_id != client.id:
            raise ValidationAppError("Contact does not belong to the specified client")
        row = ProjectContact(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            client_id=client.id,
            project_id=data.project_id,
            contact_id=contact.id,
            role_label=data.role_label,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_preference(self, data: CommunicationPreferenceCreate) -> CommunicationPreference:
        contact = self._get_contact(data.contact_id)
        row = CommunicationPreference(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            contact_id=contact.id,
            channel=data.channel,
            opted_in=data.opted_in,
            quiet_hours_start=data.quiet_hours_start,
            quiet_hours_end=data.quiet_hours_end,
            timezone=data.timezone,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_duplicate(self, data: DuplicateSuggestionCreate) -> DuplicateSuggestion:
        domain.assert_distinct_clients(data.left_client_id, data.right_client_id)
        self._get_client(data.left_client_id)
        self._get_client(data.right_client_id)
        row = DuplicateSuggestion(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            left_client_id=data.left_client_id,
            right_client_id=data.right_client_id,
            score=data.score,
            reason=data.reason,
            status="pending",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def merge_clients(self, data: MergeClientsRequest) -> MergeHistory:
        domain.assert_distinct_clients(data.surviving_client_id, data.merged_client_id)
        survivor = self._get_client(data.surviving_client_id)
        merged = self._get_client(data.merged_client_id)
        snapshot = {
            "id": str(merged.id),
            "code": merged.code,
            "legal_name": merged.legal_name,
            "trading_name": merged.trading_name,
            "status": merged.status,
            "version": merged.version,
        }
        # Reassign contacts to survivor
        contacts = list(
            self.db.scalars(
                select(Contact).where(
                    Contact.organization_id == self.ctx.organization_id,
                    Contact.client_id == merged.id,
                    Contact.deleted_at.is_(None),
                )
            )
        )
        for contact in contacts:
            # Avoid unique email collision: prefix relocated emails if needed
            existing = self.db.scalar(
                select(Contact).where(
                    Contact.organization_id == self.ctx.organization_id,
                    Contact.client_id == survivor.id,
                    Contact.email == contact.email,
                    Contact.deleted_at.is_(None),
                )
            )
            if existing is not None:
                contact.status = "merged_duplicate"
                contact.deleted_at = datetime.now(UTC)
            else:
                contact.client_id = survivor.id
                contact.updated_by_actor_id = self.ctx.actor_id
                contact.version += 1
            self.uow.add(contact)

        merged.status = "merged"
        merged.deleted_at = datetime.now(UTC)
        merged.updated_by_actor_id = self.ctx.actor_id
        merged.version += 1
        self.uow.add(merged)

        if data.duplicate_suggestion_id is not None:
            dup = self.db.scalar(
                select(DuplicateSuggestion).where(
                    DuplicateSuggestion.id == data.duplicate_suggestion_id
                )
            )
            if dup is None or dup.organization_id != self.ctx.organization_id:
                raise NotFoundError("Duplicate suggestion not found")
            dup.status = "merged"
            dup.resolved_at = datetime.now(UTC)
            self.uow.add(dup)

        history = MergeHistory(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            surviving_client_id=survivor.id,
            merged_client_id=merged.id,
            duplicate_suggestion_id=data.duplicate_suggestion_id,
            merged_snapshot=snapshot,
            reason=data.reason,
            merged_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(history)
        self.obs.write_audit(
            action="client_merge",
            entity_type="crm_client",
            entity_id=survivor.id,
            payload={
                "surviving_client_id": str(survivor.id),
                "merged_client_id": str(merged.id),
                "reason": data.reason,
            },
        )
        self.uow.commit()
        self.uow.refresh(history)
        return history

    def _get_client(self, client_id: UUID) -> Client:
        row = self.db.scalar(select(Client).where(Client.id == client_id))
        if row is None or row.organization_id != self.ctx.organization_id or row.deleted_at:
            raise NotFoundError("Client not found")
        if self.ctx.tenant.client_id is not None and row.id != self.ctx.tenant.client_id:
            raise ForbiddenError("Cross-client access denied")
        return row

    def _get_contact(self, contact_id: UUID) -> Contact:
        row = self.db.scalar(select(Contact).where(Contact.id == contact_id))
        if row is None or row.organization_id != self.ctx.organization_id or row.deleted_at:
            raise NotFoundError("Contact not found")
        self._get_client(row.client_id)
        return row

    def _clear_primary(self, client_id: UUID) -> None:
        for contact in self.db.scalars(
            select(Contact).where(
                Contact.organization_id == self.ctx.organization_id,
                Contact.client_id == client_id,
                Contact.is_primary.is_(True),
                Contact.deleted_at.is_(None),
            )
        ):
            contact.is_primary = False
            contact.updated_by_actor_id = self.ctx.actor_id
            self.uow.add(contact)
