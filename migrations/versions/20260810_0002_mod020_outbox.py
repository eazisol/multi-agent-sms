"""MOD-020 transactional outbox table.

Revision ID: 20260810_0002
Revises: 20260810_0001
Create Date: 2026-08-10
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260810_0002"
down_revision: str | None = "20260810_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "sys_outbox_messages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("aggregate_type", sa.String(length=64), nullable=False),
        sa.Column("aggregate_id", sa.Uuid(), nullable=False),
        sa.Column("event_type", sa.String(length=128), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("correlation_id", sa.Uuid(), nullable=False),
        sa.Column("causation_id", sa.Uuid(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "available_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_sys_outbox_status_available",
        "sys_outbox_messages",
        ["status", "available_at"],
    )
    op.create_index(
        "ix_sys_outbox_org_created",
        "sys_outbox_messages",
        ["organization_id", "created_at"],
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("ALTER TABLE sys_outbox_messages ENABLE ROW LEVEL SECURITY")
        op.execute(
            """
            CREATE POLICY sys_outbox_messages_org_isolation ON sys_outbox_messages
            USING (organization_id::text = current_setting('app.current_organization_id', true))
            WITH CHECK (organization_id::text = current_setting('app.current_organization_id', true))
            """
        )


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("DROP POLICY IF EXISTS sys_outbox_messages_org_isolation ON sys_outbox_messages")
        op.execute("ALTER TABLE sys_outbox_messages DISABLE ROW LEVEL SECURITY")
    op.drop_index("ix_sys_outbox_org_created", table_name="sys_outbox_messages")
    op.drop_index("ix_sys_outbox_status_available", table_name="sys_outbox_messages")
    op.drop_table("sys_outbox_messages")
