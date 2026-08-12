"""Gmail integration persistence models (MOD-510)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from masms_api.db import Base


class GmailConnection(Base):
    __tablename__ = "gm_connections"
    __table_args__ = (
        UniqueConstraint("organization_id", "code", name="uq_gm_connections_org_code"),
        UniqueConstraint(
            "organization_id", "email_address", name="uq_gm_connections_org_email"
        ),
        Index("ix_gm_connections_org_status", "organization_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    email_address: Mapped[str] = mapped_column(String(255), nullable=False)
    credential_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    scopes_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    history_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    updated_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class GmailHistoryCursor(Base):
    __tablename__ = "gm_history_cursors"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "connection_id",
            "cursor_key",
            name="uq_gm_history_cursors_org_conn_key",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    connection_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    cursor_key: Mapped[str] = mapped_column(String(128), nullable=False, default="history")
    cursor_value: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class GmailThreadMapping(Base):
    __tablename__ = "gm_thread_mappings"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "connection_id",
            "gmail_thread_id",
            name="uq_gm_thread_mappings_org_conn_thread",
        ),
        Index("ix_gm_thread_mappings_org_conn", "organization_id", "connection_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    connection_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    gmail_thread_id: Mapped[str] = mapped_column(String(128), nullable=False)
    internal_thread_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    query_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    client_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class GmailMessageMapping(Base):
    __tablename__ = "gm_message_mappings"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "connection_id",
            "gmail_message_id",
            name="uq_gm_message_mappings_org_conn_msg",
        ),
        Index("ix_gm_message_mappings_org_conn", "organization_id", "connection_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    connection_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    gmail_message_id: Mapped[str] = mapped_column(String(128), nullable=False)
    internal_message_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    thread_mapping_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    direction: Mapped[str] = mapped_column(String(16), nullable=False)
    subject: Mapped[str | None] = mapped_column(String(512), nullable=True)
    snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="received")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class GmailAttachmentImport(Base):
    __tablename__ = "gm_attachment_imports"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "message_mapping_id",
            "gmail_attachment_id",
            name="uq_gm_attachment_imports_org_msg_att",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    connection_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    message_mapping_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    gmail_attachment_id: Mapped[str] = mapped_column(String(128), nullable=False)
    file_name: Mapped[str] = mapped_column(String(512), nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(128), nullable=True)
    storage_ref: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class GmailDraftReview(Base):
    __tablename__ = "gm_draft_reviews"
    __table_args__ = (
        Index("ix_gm_draft_reviews_org_status", "organization_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    connection_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    draft_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    thread_mapping_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    to_addresses: Mapped[str] = mapped_column(Text, nullable=False)
    subject: Mapped[str] = mapped_column(String(512), nullable=False)
    body_preview: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    reviewer_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    review_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    updated_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class GmailApprovedSend(Base):
    __tablename__ = "gm_approved_sends"
    __table_args__ = (
        UniqueConstraint(
            "organization_id", "draft_review_id", name="uq_gm_approved_sends_org_draft"
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    connection_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    draft_review_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    message_mapping_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    external_send_id: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="queued")
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
