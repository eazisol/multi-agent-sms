"""MOD-200 clients, contacts, preferences, duplicates, merge history.

Revision ID: 20260811_0009
Revises: 20260811_0008
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0009"
down_revision: str | None = "20260811_0008"
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
        "crm_clients",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("legal_name", sa.String(length=255), nullable=False),
        sa.Column("trading_name", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("industry", sa.String(length=128), nullable=True),
        sa.Column("website", sa.String(length=320), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_crm_clients_org_code"),
    )
    op.create_index("ix_crm_clients_name", "crm_clients", ["organization_id", "legal_name"])
    op.create_index(op.f("ix_crm_clients_organization_id"), "crm_clients", ["organization_id"])

    op.create_table(
        "crm_contacts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("client_id", sa.Uuid(), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("phone", sa.String(length=64), nullable=True),
        sa.Column("job_title", sa.String(length=128), nullable=True),
        sa.Column("authority_level", sa.String(length=64), nullable=False),
        sa.Column("is_primary", sa.Boolean(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["client_id"], ["crm_clients.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "client_id", "email", name="uq_crm_contacts_email"),
    )
    op.create_index("ix_crm_contacts_client", "crm_contacts", ["organization_id", "client_id"])
    op.create_index(op.f("ix_crm_contacts_organization_id"), "crm_contacts", ["organization_id"])

    op.create_table(
        "crm_project_contacts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("client_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("contact_id", sa.Uuid(), nullable=False),
        sa.Column("role_label", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["client_id"], ["crm_clients.id"]),
        sa.ForeignKeyConstraint(["contact_id"], ["crm_contacts.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id", "project_id", "contact_id", name="uq_crm_project_contacts"
        ),
    )
    op.create_index(
        op.f("ix_crm_project_contacts_organization_id"),
        "crm_project_contacts",
        ["organization_id"],
    )

    op.create_table(
        "crm_communication_preferences",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("contact_id", sa.Uuid(), nullable=False),
        sa.Column("channel", sa.String(length=32), nullable=False),
        sa.Column("opted_in", sa.Boolean(), nullable=False),
        sa.Column("quiet_hours_start", sa.String(length=8), nullable=True),
        sa.Column("quiet_hours_end", sa.String(length=8), nullable=True),
        sa.Column("timezone", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["contact_id"], ["crm_contacts.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "contact_id",
            "channel",
            name="uq_crm_comm_pref_contact_channel",
        ),
    )
    op.create_index(
        op.f("ix_crm_communication_preferences_organization_id"),
        "crm_communication_preferences",
        ["organization_id"],
    )

    op.create_table(
        "crm_duplicate_suggestions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("left_client_id", sa.Uuid(), nullable=False),
        sa.Column("right_client_id", sa.Uuid(), nullable=False),
        sa.Column("score", sa.Numeric(5, 2), nullable=False),
        sa.Column("reason", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["left_client_id"], ["crm_clients.id"]),
        sa.ForeignKeyConstraint(["right_client_id"], ["crm_clients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_crm_dup_status", "crm_duplicate_suggestions", ["organization_id", "status"])
    op.create_index(
        op.f("ix_crm_duplicate_suggestions_organization_id"),
        "crm_duplicate_suggestions",
        ["organization_id"],
    )

    op.create_table(
        "crm_merge_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("surviving_client_id", sa.Uuid(), nullable=False),
        sa.Column("merged_client_id", sa.Uuid(), nullable=False),
        sa.Column("duplicate_suggestion_id", sa.Uuid(), nullable=True),
        sa.Column("merged_snapshot", sa.JSON(), nullable=False),
        sa.Column("reason", sa.String(length=255), nullable=False),
        sa.Column("merged_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["surviving_client_id"], ["crm_clients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_crm_merge_history_organization_id"),
        "crm_merge_history",
        ["organization_id"],
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "crm_clients",
            "crm_contacts",
            "crm_project_contacts",
            "crm_communication_preferences",
            "crm_duplicate_suggestions",
            "crm_merge_history",
        ):
            _rls(table)


def downgrade() -> None:
    tables = (
        "crm_merge_history",
        "crm_duplicate_suggestions",
        "crm_communication_preferences",
        "crm_project_contacts",
        "crm_contacts",
        "crm_clients",
    )
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
