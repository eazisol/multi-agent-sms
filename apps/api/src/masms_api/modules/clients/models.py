"""Client and contact persistence models (MOD-200)."""

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
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON, Uuid

from masms_api.db import Base


class Client(Base):
    __tablename__ = "crm_clients"
    __table_args__ = (
        UniqueConstraint("organization_id", "code", name="uq_crm_clients_org_code"),
        Index("ix_crm_clients_name", "organization_id", "legal_name"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    legal_name: Mapped[str] = mapped_column(String(255), nullable=False)
    trading_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    industry: Mapped[str | None] = mapped_column(String(128), nullable=True)
    website: Mapped[str | None] = mapped_column(String(320), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    updated_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class Contact(Base):
    __tablename__ = "crm_contacts"
    __table_args__ = (
        UniqueConstraint("organization_id", "client_id", "email", name="uq_crm_contacts_email"),
        Index("ix_crm_contacts_client", "organization_id", "client_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    client_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("crm_clients.id"), nullable=False
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    job_title: Mapped[str | None] = mapped_column(String(128), nullable=True)
    authority_level: Mapped[str] = mapped_column(String(64), nullable=False, default="general")
    # decision_maker | commercial | technical | general
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    updated_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ProjectContact(Base):
    __tablename__ = "crm_project_contacts"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "project_id",
            "contact_id",
            name="uq_crm_project_contacts",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    client_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("crm_clients.id"), nullable=False
    )
    project_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    contact_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("crm_contacts.id"), nullable=False
    )
    role_label: Mapped[str] = mapped_column(String(64), nullable=False, default="contact")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class CommunicationPreference(Base):
    __tablename__ = "crm_communication_preferences"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "contact_id",
            "channel",
            name="uq_crm_comm_pref_contact_channel",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    contact_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("crm_contacts.id"), nullable=False
    )
    channel: Mapped[str] = mapped_column(String(32), nullable=False)
    opted_in: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    quiet_hours_start: Mapped[str | None] = mapped_column(String(8), nullable=True)
    quiet_hours_end: Mapped[str | None] = mapped_column(String(8), nullable=True)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="UTC")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class DuplicateSuggestion(Base):
    __tablename__ = "crm_duplicate_suggestions"
    __table_args__ = (
        Index("ix_crm_dup_status", "organization_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    left_client_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("crm_clients.id"), nullable=False
    )
    right_client_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("crm_clients.id"), nullable=False
    )
    score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    # pending | merged | dismissed
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class MergeHistory(Base):
    __tablename__ = "crm_merge_history"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    surviving_client_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("crm_clients.id"), nullable=False
    )
    merged_client_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    duplicate_suggestion_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    merged_snapshot: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    merged_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
