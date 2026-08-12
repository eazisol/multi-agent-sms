"""MOD-510 Gmail integration: connections, history, threads, messages, attachments, drafts, sends.

Revision ID: 20260811_0032
Revises: 20260811_0031
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0032"
down_revision: str | None = "20260811_0031"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABLES = (
    "gm_connections",
    "gm_history_cursors",
    "gm_thread_mappings",
    "gm_message_mappings",
    "gm_attachment_imports",
    "gm_draft_reviews",
    "gm_approved_sends",
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


def _ts():
    return sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        nullable=False,
    )


def _updated():
    return sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        nullable=False,
    )


def upgrade() -> None:
    op.create_table(
        "gm_connections",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("email_address", sa.String(length=255), nullable=False),
        sa.Column("credential_ref", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("scopes_json", sa.Text(), nullable=True),
        sa.Column("history_id", sa.String(length=128), nullable=True),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        _updated(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_gm_connections_org_code"),
        sa.UniqueConstraint(
            "organization_id", "email_address", name="uq_gm_connections_org_email"
        ),
    )
    op.create_index(
        "ix_gm_connections_org_status",
        "gm_connections",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_gm_connections_organization_id"),
        "gm_connections",
        ["organization_id"],
    )

    op.create_table(
        "gm_history_cursors",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("connection_id", sa.Uuid(), nullable=False),
        sa.Column("cursor_key", sa.String(length=128), nullable=False),
        sa.Column("cursor_value", sa.Text(), nullable=False),
        _updated(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "connection_id",
            "cursor_key",
            name="uq_gm_history_cursors_org_conn_key",
        ),
    )
    op.create_index(
        op.f("ix_gm_history_cursors_organization_id"),
        "gm_history_cursors",
        ["organization_id"],
    )

    op.create_table(
        "gm_thread_mappings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("connection_id", sa.Uuid(), nullable=False),
        sa.Column("gmail_thread_id", sa.String(length=128), nullable=False),
        sa.Column("internal_thread_id", sa.Uuid(), nullable=False),
        sa.Column("query_id", sa.Uuid(), nullable=True),
        sa.Column("client_id", sa.Uuid(), nullable=True),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "connection_id",
            "gmail_thread_id",
            name="uq_gm_thread_mappings_org_conn_thread",
        ),
    )
    op.create_index(
        "ix_gm_thread_mappings_org_conn",
        "gm_thread_mappings",
        ["organization_id", "connection_id"],
    )
    op.create_index(
        op.f("ix_gm_thread_mappings_organization_id"),
        "gm_thread_mappings",
        ["organization_id"],
    )

    op.create_table(
        "gm_message_mappings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("connection_id", sa.Uuid(), nullable=False),
        sa.Column("gmail_message_id", sa.String(length=128), nullable=False),
        sa.Column("internal_message_id", sa.Uuid(), nullable=True),
        sa.Column("thread_mapping_id", sa.Uuid(), nullable=False),
        sa.Column("direction", sa.String(length=16), nullable=False),
        sa.Column("subject", sa.String(length=512), nullable=True),
        sa.Column("snippet", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "connection_id",
            "gmail_message_id",
            name="uq_gm_message_mappings_org_conn_msg",
        ),
    )
    op.create_index(
        "ix_gm_message_mappings_org_conn",
        "gm_message_mappings",
        ["organization_id", "connection_id"],
    )
    op.create_index(
        op.f("ix_gm_message_mappings_organization_id"),
        "gm_message_mappings",
        ["organization_id"],
    )

    op.create_table(
        "gm_attachment_imports",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("connection_id", sa.Uuid(), nullable=False),
        sa.Column("message_mapping_id", sa.Uuid(), nullable=False),
        sa.Column("gmail_attachment_id", sa.String(length=128), nullable=False),
        sa.Column("file_name", sa.String(length=512), nullable=False),
        sa.Column("mime_type", sa.String(length=128), nullable=True),
        sa.Column("storage_ref", sa.String(length=512), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "message_mapping_id",
            "gmail_attachment_id",
            name="uq_gm_attachment_imports_org_msg_att",
        ),
    )
    op.create_index(
        op.f("ix_gm_attachment_imports_organization_id"),
        "gm_attachment_imports",
        ["organization_id"],
    )

    op.create_table(
        "gm_draft_reviews",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("connection_id", sa.Uuid(), nullable=False),
        sa.Column("draft_id", sa.Uuid(), nullable=False),
        sa.Column("thread_mapping_id", sa.Uuid(), nullable=True),
        sa.Column("to_addresses", sa.Text(), nullable=False),
        sa.Column("subject", sa.String(length=512), nullable=False),
        sa.Column("body_preview", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("reviewer_actor_id", sa.Uuid(), nullable=True),
        sa.Column("review_notes", sa.Text(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        _updated(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_gm_draft_reviews_org_status",
        "gm_draft_reviews",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_gm_draft_reviews_organization_id"),
        "gm_draft_reviews",
        ["organization_id"],
    )

    op.create_table(
        "gm_approved_sends",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("connection_id", sa.Uuid(), nullable=False),
        sa.Column("draft_review_id", sa.Uuid(), nullable=False),
        sa.Column("message_mapping_id", sa.Uuid(), nullable=True),
        sa.Column("external_send_id", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id", "draft_review_id", name="uq_gm_approved_sends_org_draft"
        ),
    )
    op.create_index(
        op.f("ix_gm_approved_sends_organization_id"),
        "gm_approved_sends",
        ["organization_id"],
    )

    for table in _TABLES:
        _rls(table)


def downgrade() -> None:
    for table in reversed(_TABLES):
        op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
    op.drop_table("gm_approved_sends")
    op.drop_table("gm_draft_reviews")
    op.drop_table("gm_attachment_imports")
    op.drop_table("gm_message_mappings")
    op.drop_table("gm_thread_mappings")
    op.drop_table("gm_history_cursors")
    op.drop_table("gm_connections")
