"""MOD-320 configurable status and transition engine tables.

Revision ID: 20260811_0018
Revises: 20260811_0017
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0018"
down_revision: str | None = "20260811_0017"
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
        "wfe_workflow_bindings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("workflow_code", sa.String(length=64), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "entity_type",
            "project_id",
            "workflow_code",
            name="uq_wfe_workflow_bindings",
        ),
    )
    op.create_index(
        "ix_wfe_bindings_entity",
        "wfe_workflow_bindings",
        ["organization_id", "entity_type"],
    )
    op.create_index(
        op.f("ix_wfe_workflow_bindings_organization_id"),
        "wfe_workflow_bindings",
        ["organization_id"],
    )

    op.create_table(
        "wfe_entity_states",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("workflow_code", sa.String(length=64), nullable=False),
        sa.Column("status_code", sa.String(length=64), nullable=False),
        sa.Column("configuration_version_id", sa.Uuid(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("on_hold", sa.Boolean(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "updated_at",
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
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "entity_type",
            "entity_id",
            name="uq_wfe_entity_states",
        ),
    )
    op.create_index(
        "ix_wfe_entity_states_lookup",
        "wfe_entity_states",
        ["organization_id", "entity_type", "status_code"],
    )
    op.create_index(
        op.f("ix_wfe_entity_states_organization_id"),
        "wfe_entity_states",
        ["organization_id"],
    )

    op.create_table(
        "wfe_status_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("workflow_code", sa.String(length=64), nullable=False),
        sa.Column("from_status_code", sa.String(length=64), nullable=False),
        sa.Column("to_status_code", sa.String(length=64), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("evidence_ref", sa.String(length=512), nullable=True),
        sa.Column("approval_id", sa.Uuid(), nullable=True),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("actor_kind", sa.String(length=32), nullable=False),
        sa.Column("rule_id", sa.Uuid(), nullable=True),
        sa.Column("payload_json", sa.JSON(), nullable=False),
        sa.Column(
            "recorded_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_wfe_status_history_entity",
        "wfe_status_history",
        ["organization_id", "entity_type", "entity_id"],
    )
    op.create_index(
        op.f("ix_wfe_status_history_organization_id"),
        "wfe_status_history",
        ["organization_id"],
    )

    op.create_table(
        "wfe_holds",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("status_code_at_hold", sa.String(length=64), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("responsible_actor_id", sa.Uuid(), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("released_by_actor_id", sa.Uuid(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_wfe_holds_entity",
        "wfe_holds",
        ["organization_id", "entity_type", "entity_id"],
    )
    op.create_index(
        op.f("ix_wfe_holds_organization_id"),
        "wfe_holds",
        ["organization_id"],
    )

    op.create_table(
        "wfe_reopens",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("from_status_code", sa.String(length=64), nullable=False),
        sa.Column("to_status_code", sa.String(length=64), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("evidence_ref", sa.String(length=512), nullable=True),
        sa.Column("authorized_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_wfe_reopens_entity",
        "wfe_reopens",
        ["organization_id", "entity_type", "entity_id"],
    )
    op.create_index(
        op.f("ix_wfe_reopens_organization_id"),
        "wfe_reopens",
        ["organization_id"],
    )

    op.create_table(
        "wfe_available_actions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.Uuid(), nullable=False),
        sa.Column("workflow_code", sa.String(length=64), nullable=False),
        sa.Column("status_code", sa.String(length=64), nullable=False),
        sa.Column("actions_json", sa.JSON(), nullable=False),
        sa.Column(
            "computed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "entity_type",
            "entity_id",
            name="uq_wfe_available_actions",
        ),
    )
    op.create_index(
        op.f("ix_wfe_available_actions_organization_id"),
        "wfe_available_actions",
        ["organization_id"],
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "wfe_workflow_bindings",
            "wfe_entity_states",
            "wfe_status_history",
            "wfe_holds",
            "wfe_reopens",
            "wfe_available_actions",
        ):
            _rls(table)


def downgrade() -> None:
    bind = op.get_bind()
    tables = (
        "wfe_available_actions",
        "wfe_reopens",
        "wfe_holds",
        "wfe_status_history",
        "wfe_entity_states",
        "wfe_workflow_bindings",
    )
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
