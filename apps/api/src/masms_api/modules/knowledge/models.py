"""Knowledge entities (MOD-370).

PostgreSQL is the source of truth. Embeddings are stub vectors in M1 (no live
embedding model / pgvector required).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
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


class KnowledgeItem(Base):
    __tablename__ = "kn_items"
    __table_args__ = (
        UniqueConstraint("organization_id", "code", name="uq_kn_items_org_code"),
        Index("ix_kn_items_scope", "organization_id", "project_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    classification: Mapped[str] = mapped_column(String(32), nullable=False, default="internal")
    owner_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
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


class KnowledgeVersion(Base):
    __tablename__ = "kn_versions"
    __table_args__ = (
        UniqueConstraint("item_id", "version_number", name="uq_kn_versions_item_number"),
        Index("ix_kn_versions_item", "organization_id", "item_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    item_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    body_text: Mapped[str] = mapped_column(Text, nullable=False)
    change_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    effective_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    approved_by_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class KnowledgeChunk(Base):
    __tablename__ = "kn_chunks"
    __table_args__ = (
        UniqueConstraint("version_id", "chunk_index", name="uq_kn_chunks_version_index"),
        Index("ix_kn_chunks_version", "organization_id", "version_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    item_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    version_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    token_estimate: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class KnowledgeEmbedding(Base):
    __tablename__ = "kn_embeddings"
    __table_args__ = (
        UniqueConstraint("chunk_id", "model_name", name="uq_kn_embeddings_chunk_model"),
        Index("ix_kn_embeddings_chunk", "organization_id", "chunk_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    chunk_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    model_name: Mapped[str] = mapped_column(String(128), nullable=False, default="stub-embed-v1")
    dims: Mapped[int] = mapped_column(Integer, nullable=False, default=8)
    # Stub vector stored as JSON list[float]; live pgvector deferred.
    vector_stub: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class KnowledgePermission(Base):
    __tablename__ = "kn_permissions"
    __table_args__ = (
        Index("ix_kn_permissions_item", "organization_id", "item_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    item_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    effect: Mapped[str] = mapped_column(String(16), nullable=False, default="allow")
    principal_type: Mapped[str] = mapped_column(String(32), nullable=False, default="organization")
    principal_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    can_retrieve: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    can_manage: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class KnowledgeUsageLog(Base):
    __tablename__ = "kn_usage_logs"
    __table_args__ = (
        Index("ix_kn_usage_item", "organization_id", "item_id"),
        Index("ix_kn_usage_created", "organization_id", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    item_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    version_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    chunk_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    query_text: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    correlation_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class KnowledgeConflict(Base):
    __tablename__ = "kn_conflicts"
    __table_args__ = (
        Index("ix_kn_conflicts_status", "organization_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    project_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    item_id_a: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    version_id_a: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    item_id_b: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    version_id_b: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    resolution_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by_actor_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    resolved_by_actor_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
