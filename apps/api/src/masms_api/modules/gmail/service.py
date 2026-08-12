"""Gmail integration application service (MOD-510)."""

from __future__ import annotations

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
from masms_api.modules.gmail import domain
from masms_api.modules.gmail.models import (
    GmailApprovedSend,
    GmailAttachmentImport,
    GmailConnection,
    GmailDraftReview,
    GmailHistoryCursor,
    GmailMessageMapping,
    GmailThreadMapping,
)
from masms_api.modules.gmail.schemas import (
    AttachmentImportCreate,
    ConnectionCreate,
    DraftCreate,
    DraftReject,
    HistoryCursorUpsert,
    InboundProcess,
    PushReceive,
)
from masms_api.observability.writer import ObservabilityWriter


class GmailService:
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

    def _get_connection(self, connection_id: UUID) -> GmailConnection:
        row = self.db.get(GmailConnection, connection_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Gmail connection not found")
        return row

    def create_connection(self, data: ConnectionCreate) -> GmailConnection:
        domain.assert_no_raw_secrets(data.model_dump())
        credential_ref = data.credential_ref
        if not credential_ref:
            credential_ref = domain.default_credential_ref(
                organization_id=str(self.ctx.organization_id),
                code=data.code.strip(),
            )
        domain.assert_credential_ref(credential_ref)

        existing_code = self.db.scalar(
            select(GmailConnection).where(
                GmailConnection.organization_id == self.ctx.organization_id,
                GmailConnection.code == data.code.strip(),
            )
        )
        if existing_code is not None:
            raise ConflictError(f"Connection code '{data.code}' already exists")

        existing_email = self.db.scalar(
            select(GmailConnection).where(
                GmailConnection.organization_id == self.ctx.organization_id,
                GmailConnection.email_address == data.email_address.strip().lower(),
            )
        )
        if existing_email is not None:
            raise ConflictError(f"Email address '{data.email_address}' already connected")

        owner = data.owner_actor_id or self.ctx.actor_id
        row = GmailConnection(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code.strip(),
            email_address=data.email_address.strip().lower(),
            credential_ref=credential_ref,
            status="draft",
            scopes_json=data.scopes_json,
            owner_actor_id=owner,
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="gm_connection_create",
            entity_type="gm_connection",
            entity_id=row.id,
            payload={
                "code": row.code,
                "email_address": row.email_address,
                "credential_ref": row.credential_ref,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="gm_connection",
            aggregate_id=row.id,
            event_type="gmail.connection.created",
            payload={
                "connection_id": str(row.id),
                "code": row.code,
                "email_address": row.email_address,
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_connections(
        self,
        *,
        status: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[GmailConnection], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(GmailConnection).where(
            GmailConnection.organization_id == self.ctx.organization_id
        )
        if status:
            stmt = stmt.where(GmailConnection.status == status)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(GmailConnection.updated_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def get_connection(self, connection_id: UUID) -> GmailConnection:
        return self._get_connection(connection_id)

    def _transition_connection(
        self,
        connection_id: UUID,
        *,
        target_status: str,
        expected_version: int | None,
        action: str,
    ) -> GmailConnection:
        row = self._get_connection(connection_id)
        domain.assert_expected_version(current=row.version, expected=expected_version)
        domain.assert_connection_transition(row.status, target_status)
        row.status = target_status
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self._audit(
            action=action,
            entity_type="gm_connection",
            entity_id=row.id,
            payload={"status": target_status, "version": row.version},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="gm_connection",
            aggregate_id=row.id,
            event_type=f"gmail.connection.{target_status}",
            payload={"connection_id": str(row.id), "status": target_status},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def activate_connection(
        self, connection_id: UUID, *, expected_version: int | None = None
    ) -> GmailConnection:
        return self._transition_connection(
            connection_id,
            target_status="active",
            expected_version=expected_version,
            action="gm_connection_activate",
        )

    def pause_connection(
        self, connection_id: UUID, *, expected_version: int | None = None
    ) -> GmailConnection:
        return self._transition_connection(
            connection_id,
            target_status="paused",
            expected_version=expected_version,
            action="gm_connection_pause",
        )

    def upsert_history_cursor(self, data: HistoryCursorUpsert) -> GmailHistoryCursor:
        self._get_connection(data.connection_id)
        row = self.db.scalar(
            select(GmailHistoryCursor).where(
                GmailHistoryCursor.organization_id == self.ctx.organization_id,
                GmailHistoryCursor.connection_id == data.connection_id,
                GmailHistoryCursor.cursor_key == data.cursor_key,
            )
        )
        if row is None:
            row = GmailHistoryCursor(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                connection_id=data.connection_id,
                cursor_key=data.cursor_key,
                cursor_value=data.cursor_value,
            )
            self.uow.add(row)
            action = "gm_history_cursor_create"
        else:
            row.cursor_value = data.cursor_value
            action = "gm_history_cursor_update"
        self._audit(
            action=action,
            entity_type="gm_history_cursor",
            entity_id=row.id,
            payload={
                "connection_id": str(data.connection_id),
                "cursor_key": data.cursor_key,
            },
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def get_history_cursor(
        self, *, connection_id: UUID, cursor_key: str = domain.DEFAULT_CURSOR_KEY
    ) -> GmailHistoryCursor:
        self._get_connection(connection_id)
        row = self.db.scalar(
            select(GmailHistoryCursor).where(
                GmailHistoryCursor.organization_id == self.ctx.organization_id,
                GmailHistoryCursor.connection_id == connection_id,
                GmailHistoryCursor.cursor_key == cursor_key,
            )
        )
        if row is None:
            raise NotFoundError("History cursor not found")
        return row

    def _get_or_create_thread_mapping(
        self,
        *,
        connection_id: UUID,
        gmail_thread_id: str,
        query_id: UUID | None,
        client_id: UUID | None,
    ) -> GmailThreadMapping:
        row = self.db.scalar(
            select(GmailThreadMapping).where(
                GmailThreadMapping.organization_id == self.ctx.organization_id,
                GmailThreadMapping.connection_id == connection_id,
                GmailThreadMapping.gmail_thread_id == gmail_thread_id,
            )
        )
        if row is not None:
            if query_id is not None and row.query_id is None:
                row.query_id = query_id
            if client_id is not None and row.client_id is None:
                row.client_id = client_id
            return row

        resolved_query_id = query_id or uuid4()
        row = GmailThreadMapping(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            connection_id=connection_id,
            gmail_thread_id=gmail_thread_id,
            internal_thread_id=uuid4(),
            query_id=resolved_query_id,
            client_id=client_id,
        )
        self.uow.add(row)
        self._audit(
            action="gm_thread_mapping_create",
            entity_type="gm_thread_mapping",
            entity_id=row.id,
            payload={
                "gmail_thread_id": gmail_thread_id,
                "query_id": str(row.query_id),
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="gm_thread_mapping",
            aggregate_id=row.id,
            event_type="gmail.thread.mapped",
            payload={
                "thread_mapping_id": str(row.id),
                "gmail_thread_id": gmail_thread_id,
                "query_id": str(row.query_id),
            },
            correlation_id=self.ctx.correlation_id,
        )
        return row

    def process_inbound(self, data: InboundProcess) -> dict[str, Any]:
        self._get_connection(data.connection_id)
        domain.assert_no_raw_secrets(data.model_dump())

        existing_msg = self.db.scalar(
            select(GmailMessageMapping).where(
                GmailMessageMapping.organization_id == self.ctx.organization_id,
                GmailMessageMapping.connection_id == data.connection_id,
                GmailMessageMapping.gmail_message_id == data.gmail_message_id,
            )
        )
        if existing_msg is not None:
            thread = self.db.get(GmailThreadMapping, existing_msg.thread_mapping_id)
            if thread is None:
                raise NotFoundError("Thread mapping not found for existing message")
            return {
                "thread_mapping_id": thread.id,
                "message_mapping_id": existing_msg.id,
                "query_id": thread.query_id or uuid4(),
                "internal_thread_id": thread.internal_thread_id,
                "idempotent": True,
            }

        thread = self._get_or_create_thread_mapping(
            connection_id=data.connection_id,
            gmail_thread_id=data.gmail_thread_id,
            query_id=data.query_id,
            client_id=data.client_id,
        )

        msg = GmailMessageMapping(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            connection_id=data.connection_id,
            gmail_message_id=data.gmail_message_id,
            internal_message_id=uuid4(),
            thread_mapping_id=thread.id,
            direction="inbound",
            subject=data.subject,
            snippet=data.snippet,
            status="received",
        )
        self.uow.add(msg)
        self._audit(
            action="gm_message_inbound",
            entity_type="gm_message_mapping",
            entity_id=msg.id,
            payload={
                "gmail_message_id": data.gmail_message_id,
                "from_email": data.from_email,
                "subject": data.subject,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="gm_message_mapping",
            aggregate_id=msg.id,
            event_type="gmail.message.received",
            payload={
                "message_mapping_id": str(msg.id),
                "gmail_message_id": data.gmail_message_id,
                "query_id": str(thread.query_id),
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(thread)
        self.db.refresh(msg)
        return {
            "thread_mapping_id": thread.id,
            "message_mapping_id": msg.id,
            "query_id": thread.query_id,
            "internal_thread_id": thread.internal_thread_id,
            "idempotent": False,
        }

    def list_thread_mappings(
        self,
        *,
        connection_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[GmailThreadMapping], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(GmailThreadMapping).where(
            GmailThreadMapping.organization_id == self.ctx.organization_id
        )
        if connection_id is not None:
            stmt = stmt.where(GmailThreadMapping.connection_id == connection_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(GmailThreadMapping.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def list_message_mappings(
        self,
        *,
        connection_id: UUID | None = None,
        direction: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[GmailMessageMapping], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(GmailMessageMapping).where(
            GmailMessageMapping.organization_id == self.ctx.organization_id
        )
        if connection_id is not None:
            stmt = stmt.where(GmailMessageMapping.connection_id == connection_id)
        if direction:
            domain.assert_direction(direction)
            stmt = stmt.where(GmailMessageMapping.direction == direction)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(GmailMessageMapping.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def import_attachment(
        self, message_mapping_id: UUID, data: AttachmentImportCreate
    ) -> GmailAttachmentImport:
        msg = self.db.get(GmailMessageMapping, message_mapping_id)
        if msg is None or msg.organization_id != self.ctx.organization_id:
            raise NotFoundError("Message mapping not found")

        existing = self.db.scalar(
            select(GmailAttachmentImport).where(
                GmailAttachmentImport.message_mapping_id == message_mapping_id,
                GmailAttachmentImport.gmail_attachment_id == data.gmail_attachment_id,
            )
        )
        if existing is not None:
            return existing

        storage_ref = (
            f"local-stub/{self.ctx.organization_id}/{message_mapping_id}/"
            f"{data.gmail_attachment_id}/{data.file_name}"
        )
        row = GmailAttachmentImport(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            connection_id=msg.connection_id,
            message_mapping_id=message_mapping_id,
            gmail_attachment_id=data.gmail_attachment_id,
            file_name=data.file_name,
            mime_type=data.mime_type,
            storage_ref=storage_ref,
            status="imported",
        )
        self.uow.add(row)
        self._audit(
            action="gm_attachment_import",
            entity_type="gm_attachment_import",
            entity_id=row.id,
            payload={
                "message_mapping_id": str(message_mapping_id),
                "file_name": data.file_name,
                "storage_ref": storage_ref,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="gm_attachment_import",
            aggregate_id=row.id,
            event_type="gmail.attachment.imported",
            payload={
                "attachment_import_id": str(row.id),
                "storage_ref": storage_ref,
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def create_draft(self, data: DraftCreate) -> GmailDraftReview:
        self._get_connection(data.connection_id)
        if data.thread_mapping_id is not None:
            thread = self.db.get(GmailThreadMapping, data.thread_mapping_id)
            if thread is None or thread.organization_id != self.ctx.organization_id:
                raise NotFoundError("Thread mapping not found")

        row = GmailDraftReview(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            connection_id=data.connection_id,
            draft_id=uuid4(),
            thread_mapping_id=data.thread_mapping_id,
            to_addresses=data.to_addresses,
            subject=data.subject,
            body_preview=data.body_preview,
            status="draft",
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self._audit(
            action="gm_draft_create",
            entity_type="gm_draft_review",
            entity_id=row.id,
            payload={"subject": data.subject, "to_addresses": data.to_addresses},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_drafts(
        self,
        *,
        connection_id: UUID | None = None,
        status: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[GmailDraftReview], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(GmailDraftReview).where(
            GmailDraftReview.organization_id == self.ctx.organization_id
        )
        if connection_id is not None:
            stmt = stmt.where(GmailDraftReview.connection_id == connection_id)
        if status:
            domain.assert_draft_status(status)
            stmt = stmt.where(GmailDraftReview.status == status)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(GmailDraftReview.updated_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def submit_for_review(
        self, draft_review_id: UUID, *, expected_version: int | None = None
    ) -> GmailDraftReview:
        row = self._get_draft(draft_review_id)
        domain.assert_expected_version(current=row.version, expected=expected_version)
        domain.assert_draft_transition(row.status, "pending_review")
        row.status = "pending_review"
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self._audit(
            action="gm_draft_submit",
            entity_type="gm_draft_review",
            entity_id=row.id,
            payload={"status": row.status},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def approve_draft(
        self, draft_review_id: UUID, *, expected_version: int | None = None
    ) -> GmailDraftReview:
        row = self._get_draft(draft_review_id)
        domain.assert_expected_version(current=row.version, expected=expected_version)
        domain.assert_draft_transition(row.status, "approved")
        row.status = "approved"
        row.reviewer_actor_id = self.ctx.actor_id
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self._audit(
            action="gm_draft_approve",
            entity_type="gm_draft_review",
            entity_id=row.id,
            payload={"status": row.status},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def reject_draft(
        self, draft_review_id: UUID, data: DraftReject
    ) -> GmailDraftReview:
        row = self._get_draft(draft_review_id)
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        domain.assert_draft_transition(row.status, "rejected")
        row.status = "rejected"
        row.reviewer_actor_id = self.ctx.actor_id
        row.review_notes = data.review_notes
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        self._audit(
            action="gm_draft_reject",
            entity_type="gm_draft_review",
            entity_id=row.id,
            payload={"status": row.status, "review_notes": data.review_notes},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def send_approved(self, draft_review_id: UUID) -> dict[str, Any]:
        draft = self._get_draft(draft_review_id)
        if draft.status != "approved":
            raise ValidationAppError("Approved send requires draft status approved")

        existing_send = self.db.scalar(
            select(GmailApprovedSend).where(
                GmailApprovedSend.organization_id == self.ctx.organization_id,
                GmailApprovedSend.draft_review_id == draft_review_id,
            )
        )
        if existing_send is not None:
            msg = None
            if existing_send.message_mapping_id:
                msg = self.db.get(GmailMessageMapping, existing_send.message_mapping_id)
            if msg is None:
                raise ConflictError("Approved send exists but message mapping missing")
            return {"approved_send": existing_send, "message_mapping": msg, "idempotent": True}

        external_send_id = domain.simulate_external_send_id()
        gmail_message_id = f"outbound-{external_send_id}"

        thread_mapping_id = draft.thread_mapping_id
        if thread_mapping_id is None:
            thread = GmailThreadMapping(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                connection_id=draft.connection_id,
                gmail_thread_id=f"thread-{draft.draft_id}",
                internal_thread_id=uuid4(),
                query_id=None,
                client_id=None,
            )
            self.uow.add(thread)
            thread_mapping_id = thread.id
            draft.thread_mapping_id = thread_mapping_id

        outbound_msg = GmailMessageMapping(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            connection_id=draft.connection_id,
            gmail_message_id=gmail_message_id,
            internal_message_id=uuid4(),
            thread_mapping_id=thread_mapping_id,
            direction="outbound",
            subject=draft.subject,
            snippet=draft.body_preview,
            status="sent",
        )
        self.uow.add(outbound_msg)

        now = datetime.now(UTC)
        approved_send = GmailApprovedSend(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            connection_id=draft.connection_id,
            draft_review_id=draft.id,
            message_mapping_id=outbound_msg.id,
            external_send_id=external_send_id,
            status="sent",
            sent_at=now,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(approved_send)

        self._audit(
            action="gm_send_approved",
            entity_type="gm_approved_send",
            entity_id=approved_send.id,
            payload={
                "external_send_id": external_send_id,
                "draft_review_id": str(draft.id),
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="gm_approved_send",
            aggregate_id=approved_send.id,
            event_type="gmail.message.sent",
            payload={
                "approved_send_id": str(approved_send.id),
                "external_send_id": external_send_id,
                "message_mapping_id": str(outbound_msg.id),
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(approved_send)
        self.db.refresh(outbound_msg)
        return {
            "approved_send": approved_send,
            "message_mapping": outbound_msg,
            "idempotent": False,
        }

    def receive_push_notification(self, data: PushReceive) -> dict[str, Any]:
        self._get_connection(data.connection_id)
        domain.assert_no_raw_secrets(data.payload)

        push_key = domain.push_cursor_key(data.external_event_id)
        existing_cursor = self.db.scalar(
            select(GmailHistoryCursor).where(
                GmailHistoryCursor.organization_id == self.ctx.organization_id,
                GmailHistoryCursor.connection_id == data.connection_id,
                GmailHistoryCursor.cursor_key == push_key,
            )
        )
        if existing_cursor is not None:
            inbound_result = None
            if data.event_type == "message_received" and existing_cursor.cursor_value:
                inbound_result = {
                    "message_mapping_id": UUID(existing_cursor.cursor_value),
                    "idempotent": True,
                }
            return {
                "external_event_id": data.external_event_id,
                "event_type": data.event_type,
                "status": "processed",
                "inbound": inbound_result,
                "idempotent": True,
            }

        inbound_result: dict[str, Any] | None = None
        message_mapping_id: str | None = None

        if data.event_type == "message_received":
            payload = data.payload
            required = ("gmail_message_id", "gmail_thread_id", "from_email")
            if not all(payload.get(k) for k in required):
                raise ValidationAppError(
                    "message_received payload requires gmail_message_id, gmail_thread_id, from_email"
                )
            inbound = InboundProcess(
                connection_id=data.connection_id,
                gmail_message_id=str(payload["gmail_message_id"]),
                gmail_thread_id=str(payload["gmail_thread_id"]),
                subject=str(payload.get("subject", "")),
                from_email=str(payload["from_email"]),
                snippet=payload.get("snippet"),
                query_id=payload.get("query_id"),
                client_id=payload.get("client_id"),
            )
            inbound_result = self.process_inbound(inbound)
            message_mapping_id = str(inbound_result["message_mapping_id"])

        cursor = GmailHistoryCursor(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            connection_id=data.connection_id,
            cursor_key=push_key,
            cursor_value=message_mapping_id or "processed",
        )
        self.uow.add(cursor)
        self._audit(
            action="gm_push_receive",
            entity_type="gm_history_cursor",
            entity_id=cursor.id,
            payload={
                "external_event_id": data.external_event_id,
                "event_type": data.event_type,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="gm_history_cursor",
            aggregate_id=cursor.id,
            event_type="gmail.push.received",
            payload={
                "external_event_id": data.external_event_id,
                "event_type": data.event_type,
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        return {
            "external_event_id": data.external_event_id,
            "event_type": data.event_type,
            "status": "processed",
            "inbound": inbound_result,
            "idempotent": False,
        }

    def _get_draft(self, draft_review_id: UUID) -> GmailDraftReview:
        row = self.db.get(GmailDraftReview, draft_review_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Draft review not found")
        return row

    def _get_message_mapping(self, message_mapping_id: UUID) -> GmailMessageMapping:
        row = self.db.get(GmailMessageMapping, message_mapping_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Message mapping not found")
        return row
