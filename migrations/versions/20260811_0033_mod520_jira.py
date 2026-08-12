"""MOD-520 Jira integration tables.

Revision ID: 20260811_0033
Revises: 20260811_0032
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0033"
down_revision: str | None = "20260811_0032"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABLES = (
    "jr_issue_pushes",
    "jr_status_conflicts",
    "jr_comment_syncs",
)


def _rls(table: str) -> None:
    op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY {table}_org_isolation ON {table}
        USING (organization_id::text = current_setting('app.current_organization_id', true))
        WITH CHECK (organization_id::text = current_setting('app.current_organization_id', true))
        """
    )


def _created_at() -> sa.Column[sa.DateTime]:
    return sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        nullable=False,
    )


def _updated_at() -> sa.Column[sa.DateTime]:
    return sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        nullable=False,
    )


def upgrade() -> None:
    op.create_table(
        "jr_issue_pushes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("internal_ticket_id", sa.Uuid(), nullable=False),
        sa.Column("jira_issue_key", sa.String(length=64), nullable=False),
        sa.Column("summary", sa.String(length=512), nullable=False),
        sa.Column("approval_status", sa.String(length=32), nullable=False),
        sa.Column("push_status", sa.String(length=32), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        _updated_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "internal_ticket_id",
            name="uq_jr_issue_pushes_org_ticket",
        ),
    )
    op.create_index(
        "ix_jr_issue_pushes_org_status",
        "jr_issue_pushes",
        ["organization_id", "push_status"],
    )
    op.create_index(
        op.f("ix_jr_issue_pushes_organization_id"),
        "jr_issue_pushes",
        ["organization_id"],
    )

    op.create_table(
        "jr_status_conflicts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("issue_push_id", sa.Uuid(), nullable=False),
        sa.Column("external_status", sa.String(length=64), nullable=False),
        sa.Column("attempted_internal_status", sa.String(length=64), nullable=True),
        sa.Column("conflict_reason", sa.String(length=255), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_jr_status_conflicts_org_created",
        "jr_status_conflicts",
        ["organization_id", "created_at"],
    )
    op.create_index(
        op.f("ix_jr_status_conflicts_organization_id"),
        "jr_status_conflicts",
        ["organization_id"],
    )

    op.create_table(
        "jr_comment_syncs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("issue_push_id", sa.Uuid(), nullable=False),
        sa.Column("comment_text", sa.Text(), nullable=False),
        sa.Column("sync_status", sa.String(length=32), nullable=False),
        sa.Column("retry_count", sa.Integer(), nullable=False),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        sa.Column("last_attempt_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        _updated_at(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_jr_comment_syncs_org_status",
        "jr_comment_syncs",
        ["organization_id", "sync_status"],
    )
    op.create_index(
        op.f("ix_jr_comment_syncs_organization_id"),
        "jr_comment_syncs",
        ["organization_id"],
    )

    for table in _TABLES:
        _rls(table)


def downgrade() -> None:
    for table in reversed(_TABLES):
        op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
    op.drop_table("jr_comment_syncs")
    op.drop_table("jr_status_conflicts")
    op.drop_table("jr_issue_pushes")
