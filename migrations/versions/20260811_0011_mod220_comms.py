"""MOD-220 conversations, messages, recipients, receipts, attachments.

Revision ID: 20260811_0011
Revises: 20260811_0010
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0011"
down_revision: str | None = "20260811_0010"
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
        "com_conversations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("client_id", sa.Uuid(), nullable=True),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("channel", sa.String(length=32), nullable=False),
        sa.Column("direction", sa.String(length=16), nullable=False),
        sa.Column("related_entity_type", sa.String(length=64), nullable=False),
        sa.Column("related_entity_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("classification", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_com_conversations_related",
        "com_conversations",
        ["organization_id", "related_entity_type", "related_entity_id"],
    )
    op.create_index(
        op.f("ix_com_conversations_organization_id"),
        "com_conversations",
        ["organization_id"],
    )

    op.create_table(
        "com_messages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("conversation_id", sa.Uuid(), nullable=False),
        sa.Column("sender_actor_id", sa.Uuid(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("classification", sa.String(length=32), nullable=False),
        sa.Column("requires_approval", sa.Boolean(), nullable=False),
        sa.Column("approved_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revision_number", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["conversation_id"], ["com_conversations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_com_messages_conversation",
        "com_messages",
        ["organization_id", "conversation_id"],
    )
    op.create_index(op.f("ix_com_messages_organization_id"), "com_messages", ["organization_id"])

    op.create_table(
        "com_message_revisions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("message_id", sa.Uuid(), nullable=False),
        sa.Column("revision_number", sa.Integer(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("edited_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["message_id"], ["com_messages.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("message_id", "revision_number", name="uq_com_message_revisions"),
    )
    op.create_index(
        op.f("ix_com_message_revisions_organization_id"),
        "com_message_revisions",
        ["organization_id"],
    )

    op.create_table(
        "com_message_recipients",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("message_id", sa.Uuid(), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column("address", sa.String(length=320), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=True),
        sa.Column("contact_id", sa.Uuid(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["message_id"], ["com_messages.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "message_id", "address", "role", name="uq_com_message_recipients_addr_role"
        ),
    )
    op.create_index(
        op.f("ix_com_message_recipients_organization_id"),
        "com_message_recipients",
        ["organization_id"],
    )

    op.create_table(
        "com_delivery_receipts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("message_id", sa.Uuid(), nullable=False),
        sa.Column("recipient_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("provider_ref", sa.String(length=255), nullable=True),
        sa.Column("detail", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["message_id"], ["com_messages.id"]),
        sa.ForeignKeyConstraint(["recipient_id"], ["com_message_recipients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_com_delivery_message",
        "com_delivery_receipts",
        ["organization_id", "message_id"],
    )
    op.create_index(
        op.f("ix_com_delivery_receipts_organization_id"),
        "com_delivery_receipts",
        ["organization_id"],
    )

    op.create_table(
        "com_attachment_links",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("message_id", sa.Uuid(), nullable=False),
        sa.Column("file_ref", sa.String(length=512), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("content_type", sa.String(length=128), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("classification", sa.String(length=32), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["message_id"], ["com_messages.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_com_attachments_message",
        "com_attachment_links",
        ["organization_id", "message_id"],
    )
    op.create_index(
        op.f("ix_com_attachment_links_organization_id"),
        "com_attachment_links",
        ["organization_id"],
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "com_conversations",
            "com_messages",
            "com_message_revisions",
            "com_message_recipients",
            "com_delivery_receipts",
            "com_attachment_links",
        ):
            _rls(table)


def downgrade() -> None:
    tables = (
        "com_attachment_links",
        "com_delivery_receipts",
        "com_message_recipients",
        "com_message_revisions",
        "com_messages",
        "com_conversations",
    )
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
