"""MOD-500 integration framework: connections, webhooks, sync, mappings, outbox, inbox, health.

Revision ID: 20260811_0031
Revises: 20260811_0030
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0031"
down_revision: str | None = "20260811_0030"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABLES = (
    "ig_connections",
    "ig_webhook_events",
    "ig_sync_cursors",
    "ig_external_mappings",
    "ig_outbox_events",
    "ig_inbox_events",
    "ig_connection_health",
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
        "ig_connections",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("provider", sa.String(length=32), nullable=False),
        sa.Column("auth_type", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("credential_ref", sa.String(length=255), nullable=True),
        sa.Column("scopes_json", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.Text(), nullable=True),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        _updated(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_ig_connections_org_code"),
    )
    op.create_index(
        "ix_ig_connections_org_status",
        "ig_connections",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_ig_connections_organization_id"),
        "ig_connections",
        ["organization_id"],
    )

    op.create_table(
        "ig_webhook_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("connection_id", sa.Uuid(), nullable=False),
        sa.Column("external_event_id", sa.String(length=128), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        sa.Column(
            "received_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "connection_id",
            "external_event_id",
            name="uq_ig_webhook_events_org_conn_ext",
        ),
    )
    op.create_index(
        "ix_ig_webhook_events_org_conn",
        "ig_webhook_events",
        ["organization_id", "connection_id"],
    )
    op.create_index(
        op.f("ix_ig_webhook_events_organization_id"),
        "ig_webhook_events",
        ["organization_id"],
    )

    op.create_table(
        "ig_sync_cursors",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("connection_id", sa.Uuid(), nullable=False),
        sa.Column("stream_key", sa.String(length=128), nullable=False),
        sa.Column("cursor_value", sa.Text(), nullable=False),
        _updated(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "connection_id",
            "stream_key",
            name="uq_ig_sync_cursors_org_conn_stream",
        ),
    )
    op.create_index(
        op.f("ix_ig_sync_cursors_organization_id"),
        "ig_sync_cursors",
        ["organization_id"],
    )

    op.create_table(
        "ig_external_mappings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("connection_id", sa.Uuid(), nullable=False),
        sa.Column("internal_entity_type", sa.String(length=64), nullable=False),
        sa.Column("internal_entity_id", sa.String(length=128), nullable=False),
        sa.Column("external_entity_type", sa.String(length=64), nullable=False),
        sa.Column("external_entity_id", sa.String(length=128), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "connection_id",
            "internal_entity_type",
            "internal_entity_id",
            name="uq_ig_ext_map_org_conn_internal",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "connection_id",
            "external_entity_type",
            "external_entity_id",
            name="uq_ig_ext_map_org_conn_external",
        ),
    )
    op.create_index(
        "ix_ig_ext_map_org_conn",
        "ig_external_mappings",
        ["organization_id", "connection_id"],
    )
    op.create_index(
        op.f("ix_ig_external_mappings_organization_id"),
        "ig_external_mappings",
        ["organization_id"],
    )

    op.create_table(
        "ig_outbox_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("connection_id", sa.Uuid(), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.Column("last_error", sa.Text(), nullable=True),
        _ts(),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ig_outbox_events_org_status",
        "ig_outbox_events",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_ig_outbox_events_organization_id"),
        "ig_outbox_events",
        ["organization_id"],
    )

    op.create_table(
        "ig_inbox_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("connection_id", sa.Uuid(), nullable=False),
        sa.Column("external_event_id", sa.String(length=128), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        _ts(),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "connection_id",
            "external_event_id",
            name="uq_ig_inbox_events_org_conn_ext",
        ),
    )
    op.create_index(
        "ix_ig_inbox_events_org_status",
        "ig_inbox_events",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_ig_inbox_events_organization_id"),
        "ig_inbox_events",
        ["organization_id"],
    )

    op.create_table(
        "ig_connection_health",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("connection_id", sa.Uuid(), nullable=False),
        sa.Column("health_status", sa.String(length=32), nullable=False),
        sa.Column("last_success_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_failure_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failure_count", sa.Integer(), nullable=False),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column(
            "checked_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        _updated(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "connection_id",
            name="uq_ig_connection_health_org_conn",
        ),
    )
    op.create_index(
        op.f("ix_ig_connection_health_organization_id"),
        "ig_connection_health",
        ["organization_id"],
    )

    for table in _TABLES:
        _rls(table)


def downgrade() -> None:
    for table in reversed(_TABLES):
        op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
    op.drop_table("ig_connection_health")
    op.drop_table("ig_inbox_events")
    op.drop_table("ig_outbox_events")
    op.drop_table("ig_external_mappings")
    op.drop_table("ig_sync_cursors")
    op.drop_table("ig_webhook_events")
    op.drop_table("ig_connections")
