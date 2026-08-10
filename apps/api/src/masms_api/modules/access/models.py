"""Access-control persistence models (MOD-120)."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
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


class Permission(Base):
    __tablename__ = "auth_permissions"
    __table_args__ = (
        UniqueConstraint("organization_id", "code", name="uq_auth_permissions_org_code"),
        Index("ix_auth_permissions_module", "organization_id", "module_key"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(128), nullable=False)
    module_key: Mapped[str] = mapped_column(String(64), nullable=False)
    action_key: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class RolePermission(Base):
    __tablename__ = "org_role_permissions"
    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uq_org_role_permissions_pair"),
        Index("ix_org_role_permissions_org", "organization_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    role_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("org_roles.id"), nullable=False
    )
    permission_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("auth_permissions.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ProjectMember(Base):
    __tablename__ = "org_project_members"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "project_id",
            "actor_id",
            name="uq_org_project_members_actor",
        ),
        Index("ix_org_project_members_project", "organization_id", "project_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    client_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    project_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    role_code: Mapped[str] = mapped_column(String(64), nullable=False, default="member")
    access_level: Mapped[str] = mapped_column(String(32), nullable=False, default="standard")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    assigned_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ModuleAccess(Base):
    __tablename__ = "org_module_access"
    __table_args__ = (
        Index(
            "ix_org_module_access_scope",
            "organization_id",
            "actor_id",
            "module_key",
            "project_id",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    module_key: Mapped[str] = mapped_column(String(64), nullable=False)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    access_level: Mapped[str] = mapped_column(String(32), nullable=False, default="read")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    granted_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class DocumentAccess(Base):
    __tablename__ = "org_document_access"
    __table_args__ = (
        Index("ix_org_document_access_target", "organization_id", "document_ref"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    document_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    classification: Mapped[str] = mapped_column(String(32), nullable=False, default="internal")
    actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    role_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    access_level: Mapped[str] = mapped_column(String(32), nullable=False, default="read")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    granted_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ApprovalAuthority(Base):
    __tablename__ = "org_approval_authorities"
    __table_args__ = (
        Index("ix_org_approval_authorities_action", "organization_id", "action_code"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    action_code: Mapped[str] = mapped_column(String(128), nullable=False)
    authority_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    authority_role_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    client_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    environment: Mapped[str] = mapped_column(String(32), nullable=False, default="all")
    amount_threshold: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    delegated_from_authority_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), nullable=True
    )
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class AccessReview(Base):
    __tablename__ = "org_access_reviews"
    __table_args__ = (Index("ix_org_access_reviews_status", "organization_id", "status"),)

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    findings_json: Mapped[dict[str, Any]] = mapped_column("findings", JSON, default=dict)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
