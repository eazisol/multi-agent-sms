"""Integration framework persistence models (MOD-500)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from masms_api.db import Base


class IntegrationConnection(Base):
    __tablename__ = "ig_connections"
    __table_args__ = (
        UniqueConstraint("organization_id", "code", name="uq_ig_connections_org_code"),
        Index("ix_ig_connections_org_status", "organization_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    provider: Mapped[str] = mapped_column(String(32), nullable=False)
    auth_type: Mapped[str] = mapped_column(String(16), nullable=False, default="oauth2")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    credential_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    scopes_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
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


class WebhookEvent(Base):
    __tablename__ = "ig_webhook_events"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "connection_id",
            "external_event_id",
            name="uq_ig_webhook_events_org_conn_ext",
        ),
        Index("ix_ig_webhook_events_org_conn", "organization_id", "connection_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    connection_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    external_event_id: Mapped[str] = mapped_column(String(128), nullable=False)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    payload_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="received")
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class SyncCursor(Base):
    __tablename__ = "ig_sync_cursors"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "connection_id",
            "stream_key",
            name="uq_ig_sync_cursors_org_conn_stream",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    connection_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    stream_key: Mapped[str] = mapped_column(String(128), nullable=False)
    cursor_value: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class ExternalMapping(Base):
    __tablename__ = "ig_external_mappings"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "connection_id",
            "internal_entity_type",
            "internal_entity_id",
            name="uq_ig_ext_map_org_conn_internal",
        ),
        UniqueConstraint(
            "organization_id",
            "connection_id",
            "external_entity_type",
            "external_entity_id",
            name="uq_ig_ext_map_org_conn_external",
        ),
        Index("ix_ig_ext_map_org_conn", "organization_id", "connection_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    connection_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    internal_entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    internal_entity_id: Mapped[str] = mapped_column(String(128), nullable=False)
    external_entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    external_entity_id: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class IntegrationOutboxEvent(Base):
    """Outbound integration relay queue — distinct from kernel sys_outbox_messages."""

    __tablename__ = "ig_outbox_events"
    __table_args__ = (
        Index("ix_ig_outbox_events_org_status", "organization_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    connection_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    payload_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class InboxEvent(Base):
    __tablename__ = "ig_inbox_events"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "connection_id",
            "external_event_id",
            name="uq_ig_inbox_events_org_conn_ext",
        ),
        Index("ix_ig_inbox_events_org_status", "organization_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    connection_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    external_event_id: Mapped[str] = mapped_column(String(128), nullable=False)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    payload_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ConnectionHealth(Base):
    __tablename__ = "ig_connection_health"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "connection_id",
            name="uq_ig_connection_health_org_conn",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    connection_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    health_status: Mapped[str] = mapped_column(String(32), nullable=False, default="healthy")
    last_success_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_failure_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failure_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
