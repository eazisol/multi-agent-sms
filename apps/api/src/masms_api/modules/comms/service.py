"""Communications application service (MOD-220)."""

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
from masms_api.modules.comms import domain
from masms_api.modules.comms.models import (
    AttachmentLink,
    Conversation,
    DeliveryReceipt,
    Message,
    MessageRecipient,
    MessageRevision,
)
from masms_api.modules.comms.schemas import (
    AttachmentLinkCreate,
    ConversationCreate,
    DeliveryReceiptCreate,
    MessageCreate,
    MessageUpdateBody,
    RecipientCreate,
)
from masms_api.observability.writer import ObservabilityWriter


class CommsService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_conversation(self, data: ConversationCreate) -> Conversation:
        client_id = data.client_id or self.ctx.tenant.client_id
        if self.ctx.tenant.client_id and client_id and client_id != self.ctx.tenant.client_id:
            raise ForbiddenError("Cross-client access denied")
        row = Conversation(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            client_id=client_id,
            project_id=data.project_id or self.ctx.tenant.project_id,
            subject=data.subject,
            channel=data.channel,
            direction=data.direction,
            related_entity_type=data.related_entity_type,
            related_entity_id=data.related_entity_id,
            status="open",
            classification=data.classification,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="conversation_create",
            entity_type="com_conversation",
            entity_id=row.id,
            payload={
                "related_entity_type": data.related_entity_type,
                "related_entity_id": str(data.related_entity_id),
                "channel": data.channel,
            },
            project_id=row.project_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_message(self, data: MessageCreate) -> Message:
        conversation = self._get_conversation(data.conversation_id)
        classification = data.classification or conversation.classification
        requires_approval = domain.requires_approval_for_classification(classification)
        row = Message(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            conversation_id=conversation.id,
            sender_actor_id=self.ctx.actor_id,
            body=data.body,
            status="pending_approval" if requires_approval else "draft",
            classification=classification,
            requires_approval=requires_approval,
            revision_number=1,
        )
        self.uow.add(row)
        self.uow.flush()
        self.uow.add(
            MessageRevision(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                message_id=row.id,
                revision_number=1,
                body=data.body,
                edited_by_actor_id=self.ctx.actor_id,
            )
        )
        self.obs.write_audit(
            action="message_create",
            entity_type="com_message",
            entity_id=row.id,
            payload={
                "conversation_id": str(conversation.id),
                "classification": classification,
                "requires_approval": requires_approval,
            },
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def update_draft_body(self, message_id: UUID, data: MessageUpdateBody) -> Message:
        row = self._get_message(message_id)
        domain.assert_sent_immutable(row.status)
        domain.assert_message_editable(row.status)
        row.body = data.body
        row.revision_number += 1
        self.uow.add(row)
        self.uow.add(
            MessageRevision(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                message_id=row.id,
                revision_number=row.revision_number,
                body=data.body,
                edited_by_actor_id=self.ctx.actor_id,
            )
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def approve_message(self, message_id: UUID) -> Message:
        row = self._get_message(message_id)
        domain.assert_sent_immutable(row.status)
        if not row.requires_approval:
            raise ForbiddenError("Message does not require approval")
        if row.status not in {"draft", "pending_approval"}:
            raise ForbiddenError(f"Cannot approve message in status '{row.status}'")
        row.status = "pending_approval"
        row.approved_by_actor_id = self.ctx.actor_id
        row.approved_at = datetime.now(UTC)
        self.uow.add(row)
        self.obs.write_audit(
            action="message_approve",
            entity_type="com_message",
            entity_id=row.id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def add_recipient(self, data: RecipientCreate) -> MessageRecipient:
        message = self._get_message(data.message_id)
        domain.assert_sent_immutable(message.status)
        domain.assert_message_editable(message.status)
        domain.assert_recipient_role(data.role)
        row = MessageRecipient(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            message_id=message.id,
            role=data.role,
            address=data.address.strip().lower(),
            actor_id=data.actor_id,
            contact_id=data.contact_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def send_message(self, message_id: UUID) -> Message:
        row = self._get_message(message_id)
        approved = row.approved_by_actor_id is not None
        domain.assert_can_send(
            status=row.status,
            requires_approval=row.requires_approval,
            approved=approved,
        )
        count = self.db.scalar(
            select(func.count()).select_from(MessageRecipient).where(
                MessageRecipient.message_id == row.id
            )
        ) or 0
        domain.assert_has_recipients(int(count))
        now = datetime.now(UTC)
        row.status = "sent"
        row.sent_at = now
        self.uow.add(row)
        recipients = list(
            self.db.scalars(
                select(MessageRecipient).where(MessageRecipient.message_id == row.id)
            )
        )
        for recipient in recipients:
            self.uow.add(
                DeliveryReceipt(
                    id=uuid4(),
                    organization_id=self.ctx.organization_id,
                    message_id=row.id,
                    recipient_id=recipient.id,
                    status="sent",
                    provider_ref=None,
                    detail="recorded at send",
                )
            )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="com_message",
            aggregate_id=row.id,
            event_type="comms.message.sent",
            payload={"conversation_id": str(row.conversation_id)},
            correlation_id=self.ctx.correlation_id,
        )
        self.obs.write_audit(
            action="message_send",
            entity_type="com_message",
            entity_id=row.id,
            payload={"recipient_count": int(count)},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def add_attachment(self, data: AttachmentLinkCreate) -> AttachmentLink:
        message = self._get_message(data.message_id)
        domain.assert_sent_immutable(message.status)
        domain.assert_message_editable(message.status)
        row = AttachmentLink(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            message_id=message.id,
            file_ref=data.file_ref,
            filename=data.filename,
            content_type=data.content_type,
            size_bytes=data.size_bytes,
            classification=data.classification or message.classification,
            metadata_json=data.metadata,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def record_delivery(self, data: DeliveryReceiptCreate) -> DeliveryReceipt:
        message = self._get_message(data.message_id)
        if message.status != "sent":
            raise ForbiddenError("Delivery receipts require a sent message")
        recipient = self.db.scalar(
            select(MessageRecipient).where(MessageRecipient.id == data.recipient_id)
        )
        if recipient is None or recipient.message_id != message.id:
            raise NotFoundError("Recipient not found for message")
        row = DeliveryReceipt(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            message_id=message.id,
            recipient_id=recipient.id,
            status=data.status,
            provider_ref=data.provider_ref,
            detail=data.detail,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_revisions(self, message_id: UUID) -> list[MessageRevision]:
        self._get_message(message_id)
        rows = self.db.scalars(
            select(MessageRevision)
            .where(
                MessageRevision.organization_id == self.ctx.organization_id,
                MessageRevision.message_id == message_id,
            )
            .order_by(MessageRevision.revision_number)
        )
        return list(rows)

    def list_messages(self, conversation_id: UUID) -> list[Message]:
        self._get_conversation(conversation_id)
        rows = self.db.scalars(
            select(Message)
            .where(
                Message.organization_id == self.ctx.organization_id,
                Message.conversation_id == conversation_id,
            )
            .order_by(Message.created_at)
        )
        return list(rows)

    def _get_conversation(self, conversation_id: UUID) -> Conversation:
        row = self.db.scalar(select(Conversation).where(Conversation.id == conversation_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Conversation not found")
        ctx_client = self.ctx.tenant.client_id
        if ctx_client and row.client_id and row.client_id != ctx_client:
            raise ForbiddenError("Cross-client access denied")
        return row

    def _get_message(self, message_id: UUID) -> Message:
        row = self.db.scalar(select(Message).where(Message.id == message_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Message not found")
        self._get_conversation(row.conversation_id)
        return row
