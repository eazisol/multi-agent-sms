"""Communication thread models (MOD-220)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON, Uuid

from masms_api.db import Base


class Conversation(Base):
    __tablename__ = "com_conversations"
    __table_args__ = (
        Index(
            "ix_com_conversations_related",
            "organization_id",
            "related_entity_type",
            "related_entity_id",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    client_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    channel: Mapped[str] = mapped_column(String(32), nullable=False, default="email")
    direction: Mapped[str] = mapped_column(String(16), nullable=False, default="external")
    # internal | external
    related_entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    related_entity_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    classification: Mapped[str] = mapped_column(String(32), nullable=False, default="internal")
    # internal | confidential | restricted
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Message(Base):
    __tablename__ = "com_messages"
    __table_args__ = (Index("ix_com_messages_conversation", "organization_id", "conversation_id"),)

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    conversation_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("com_conversations.id"), nullable=False
    )
    sender_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    # draft | pending_approval | sent | failed
    classification: Mapped[str] = mapped_column(String(32), nullable=False, default="internal")
    requires_approval: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    approved_by_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revision_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class MessageRevision(Base):
    """Append-only body history for drafts; sent bodies are never rewritten."""

    __tablename__ = "com_message_revisions"
    __table_args__ = (
        UniqueConstraint("message_id", "revision_number", name="uq_com_message_revisions"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    message_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("com_messages.id"), nullable=False
    )
    revision_number: Mapped[int] = mapped_column(Integer, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    edited_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class MessageRecipient(Base):
    __tablename__ = "com_message_recipients"
    __table_args__ = (
        UniqueConstraint(
            "message_id", "address", "role", name="uq_com_message_recipients_addr_role"
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    message_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("com_messages.id"), nullable=False
    )
    role: Mapped[str] = mapped_column(String(16), nullable=False, default="to")
    # to | cc | bcc
    address: Mapped[str] = mapped_column(String(320), nullable=False)
    actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    contact_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class DeliveryReceipt(Base):
    __tablename__ = "com_delivery_receipts"
    __table_args__ = (Index("ix_com_delivery_message", "organization_id", "message_id"),)

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    message_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("com_messages.id"), nullable=False
    )
    recipient_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("com_message_recipients.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="queued")
    # queued | sent | delivered | bounced | failed
    provider_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class AttachmentLink(Base):
    """Logical attachment reference (file bytes live in MOD-250 storage)."""

    __tablename__ = "com_attachment_links"
    __table_args__ = (Index("ix_com_attachments_message", "organization_id", "message_id"),)

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    message_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("com_messages.id"), nullable=False
    )
    file_ref: Mapped[str] = mapped_column(String(512), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(
        String(128), nullable=False, default="application/octet-stream"
    )
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    classification: Mapped[str] = mapped_column(String(32), nullable=False, default="internal")
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
