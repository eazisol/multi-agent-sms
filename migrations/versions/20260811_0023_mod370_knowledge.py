"""MOD-370 knowledge base registry (items, versions, chunks, embeddings).

Revision ID: 20260811_0023
Revises: 20260811_0022
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0023"
down_revision: str | None = "20260811_0022"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _rls(table: str) -> None:
    op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY {table}_org_isolation ON {table}
        USING (organization_id::text = current_setting('app.current_organization_id', true))
        WITH CHECK (organization_id::text = current_setting('app.current_organization_id', true))
        """
    )


def upgrade() -> None:
    op.create_table(
        "kn_items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("classification", sa.String(length=32), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_kn_items_org_code"),
    )
    op.create_index("ix_kn_items_scope", "kn_items", ["organization_id", "project_id", "status"])
    op.create_index(op.f("ix_kn_items_organization_id"), "kn_items", ["organization_id"])

    op.create_table(
        "kn_versions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("body_text", sa.Text(), nullable=False),
        sa.Column("change_summary", sa.Text(), nullable=True),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("effective_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("approved_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("item_id", "version_number", name="uq_kn_versions_item_number"),
    )
    op.create_index("ix_kn_versions_item", "kn_versions", ["organization_id", "item_id", "status"])
    op.create_index(op.f("ix_kn_versions_organization_id"), "kn_versions", ["organization_id"])

    op.create_table(
        "kn_chunks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("version_id", sa.Uuid(), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("content_text", sa.Text(), nullable=False),
        sa.Column("token_estimate", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("version_id", "chunk_index", name="uq_kn_chunks_version_index"),
    )
    op.create_index("ix_kn_chunks_version", "kn_chunks", ["organization_id", "version_id"])
    op.create_index(op.f("ix_kn_chunks_organization_id"), "kn_chunks", ["organization_id"])

    op.create_table(
        "kn_embeddings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("chunk_id", sa.Uuid(), nullable=False),
        sa.Column("model_name", sa.String(length=128), nullable=False),
        sa.Column("dims", sa.Integer(), nullable=False),
        sa.Column("vector_stub", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("chunk_id", "model_name", name="uq_kn_embeddings_chunk_model"),
    )
    op.create_index("ix_kn_embeddings_chunk", "kn_embeddings", ["organization_id", "chunk_id"])
    op.create_index(op.f("ix_kn_embeddings_organization_id"), "kn_embeddings", ["organization_id"])

    op.create_table(
        "kn_permissions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("effect", sa.String(length=16), nullable=False),
        sa.Column("principal_type", sa.String(length=32), nullable=False),
        sa.Column("principal_id", sa.Uuid(), nullable=True),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("can_retrieve", sa.Boolean(), nullable=False),
        sa.Column("can_manage", sa.Boolean(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_kn_permissions_item", "kn_permissions", ["organization_id", "item_id"])
    op.create_index(op.f("ix_kn_permissions_organization_id"), "kn_permissions", ["organization_id"])

    op.create_table(
        "kn_usage_logs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("version_id", sa.Uuid(), nullable=False),
        sa.Column("chunk_id", sa.Uuid(), nullable=True),
        sa.Column("query_text", sa.Text(), nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("correlation_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_kn_usage_item", "kn_usage_logs", ["organization_id", "item_id"])
    op.create_index("ix_kn_usage_created", "kn_usage_logs", ["organization_id", "created_at"])
    op.create_index(op.f("ix_kn_usage_logs_organization_id"), "kn_usage_logs", ["organization_id"])

    op.create_table(
        "kn_conflicts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("item_id_a", sa.Uuid(), nullable=False),
        sa.Column("version_id_a", sa.Uuid(), nullable=False),
        sa.Column("item_id_b", sa.Uuid(), nullable=False),
        sa.Column("version_id_b", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("resolution_notes", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("resolved_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_kn_conflicts_status", "kn_conflicts", ["organization_id", "status"])
    op.create_index(op.f("ix_kn_conflicts_organization_id"), "kn_conflicts", ["organization_id"])

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "kn_items",
            "kn_versions",
            "kn_chunks",
            "kn_embeddings",
            "kn_permissions",
            "kn_usage_logs",
            "kn_conflicts",
        ):
            _rls(table)


def downgrade() -> None:
    bind = op.get_bind()
    tables = (
        "kn_conflicts",
        "kn_usage_logs",
        "kn_permissions",
        "kn_embeddings",
        "kn_chunks",
        "kn_versions",
        "kn_items",
    )
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
