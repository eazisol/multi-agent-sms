"""Add pgvector storage for live knowledge embeddings.

Revision ID: 20260817_0039
Revises: 20260817_0038
Create Date: 2026-08-17
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

revision: str = "20260817_0039"
down_revision: str | None = "20260817_0038"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.add_column("kn_embeddings", sa.Column("embedding", Vector(1536), nullable=True))
    op.create_index(
        "ix_kn_embeddings_vector_cosine",
        "kn_embeddings",
        ["embedding"],
        postgresql_using="hnsw",
        postgresql_ops={"embedding": "vector_cosine_ops"},
    )


def downgrade() -> None:
    op.drop_index("ix_kn_embeddings_vector_cosine", table_name="kn_embeddings")
    op.drop_column("kn_embeddings", "embedding")
