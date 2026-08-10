"""MOD-040 observability tables.

Revision ID: 20260810_0003
Revises: 20260810_0002
Create Date: 2026-08-10
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260810_0003"
down_revision: str | None = "20260810_0002"
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
        "ops_audit_logs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("actor_kind", sa.String(length=32), nullable=False),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.Uuid(), nullable=False),
        sa.Column("entity_version", sa.Integer(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("source", sa.String(length=64), nullable=False, server_default="api"),
        sa.Column("correlation_id", sa.Uuid(), nullable=False),
        sa.Column("payload_redacted", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ops_audit_logs_org_created", "ops_audit_logs", ["organization_id", "created_at"])
    op.create_index(
        "ix_ops_audit_logs_entity",
        "ops_audit_logs",
        ["organization_id", "entity_type", "entity_id"],
    )

    op.create_table(
        "ops_activity_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("actor_kind", sa.String(length=32), nullable=False),
        sa.Column("activity_type", sa.String(length=64), nullable=False),
        sa.Column("summary", sa.String(length=512), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=True),
        sa.Column("entity_id", sa.Uuid(), nullable=True),
        sa.Column("correlation_id", sa.Uuid(), nullable=False),
        sa.Column("payload_redacted", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ops_activity_org_created", "ops_activity_events", ["organization_id", "created_at"]
    )

    op.create_table(
        "ops_status_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.Uuid(), nullable=False),
        sa.Column("previous_status", sa.String(length=64), nullable=True),
        sa.Column("next_status", sa.String(length=64), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("actor_kind", sa.String(length=32), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("rule", sa.String(length=128), nullable=True),
        sa.Column("correlation_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ops_status_history_entity",
        "ops_status_history",
        ["organization_id", "entity_type", "entity_id", "created_at"],
    )

    op.create_table(
        "ops_agent_runs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("agent_name", sa.String(length=128), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="started"),
        sa.Column("correlation_id", sa.Uuid(), nullable=False),
        sa.Column("input_summary_redacted", sa.JSON(), nullable=False),
        sa.Column("output_summary_redacted", sa.JSON(), nullable=False),
        sa.Column("error_summary", sa.Text(), nullable=True),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ops_agent_runs_org_started", "ops_agent_runs", ["organization_id", "started_at"]
    )

    op.create_table(
        "ops_integration_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("direction", sa.String(length=16), nullable=False),
        sa.Column("event_type", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="received"),
        sa.Column("correlation_id", sa.Uuid(), nullable=False),
        sa.Column("payload_redacted", sa.JSON(), nullable=False),
        sa.Column("error_summary", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ops_integration_org_created",
        "ops_integration_events",
        ["organization_id", "created_at"],
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "ops_audit_logs",
            "ops_activity_events",
            "ops_status_history",
            "ops_agent_runs",
            "ops_integration_events",
        ):
            _rls(table)


def downgrade() -> None:
    bind = op.get_bind()
    tables = (
        "ops_integration_events",
        "ops_agent_runs",
        "ops_status_history",
        "ops_activity_events",
        "ops_audit_logs",
    )
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
