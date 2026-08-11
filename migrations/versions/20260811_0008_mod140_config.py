"""MOD-140 configuration versions and operational rules.

Revision ID: 20260811_0008
Revises: 20260810_0007
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0008"
down_revision: str | None = "20260810_0007"
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
        "cfg_configuration_versions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("based_on_version_id", sa.Uuid(), nullable=True),
        sa.Column("change_reason", sa.Text(), nullable=True),
        sa.Column("approved_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("effective_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("superseded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rolled_back_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "version_number", name="uq_cfg_versions_org_num"),
    )
    op.create_index("ix_cfg_versions_status", "cfg_configuration_versions", ["organization_id", "status"])
    op.create_index(
        op.f("ix_cfg_configuration_versions_organization_id"),
        "cfg_configuration_versions",
        ["organization_id"],
    )

    op.create_table(
        "cfg_workflow_definitions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("configuration_version_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["configuration_version_id"], ["cfg_configuration_versions.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "configuration_version_id", "code", name="uq_cfg_workflows_version_code"
        ),
    )
    op.create_index(
        op.f("ix_cfg_workflow_definitions_organization_id"),
        "cfg_workflow_definitions",
        ["organization_id"],
    )

    op.create_table(
        "cfg_status_definitions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("configuration_version_id", sa.Uuid(), nullable=False),
        sa.Column("workflow_definition_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("is_terminal", sa.Boolean(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["configuration_version_id"], ["cfg_configuration_versions.id"]),
        sa.ForeignKeyConstraint(["workflow_definition_id"], ["cfg_workflow_definitions.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "workflow_definition_id", "code", name="uq_cfg_statuses_workflow_code"
        ),
    )
    op.create_index(
        op.f("ix_cfg_status_definitions_organization_id"),
        "cfg_status_definitions",
        ["organization_id"],
    )

    op.create_table(
        "cfg_transition_rules",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("configuration_version_id", sa.Uuid(), nullable=False),
        sa.Column("workflow_definition_id", sa.Uuid(), nullable=False),
        sa.Column("from_status_code", sa.String(length=64), nullable=False),
        sa.Column("to_status_code", sa.String(length=64), nullable=False),
        sa.Column("requires_reason", sa.Boolean(), nullable=False),
        sa.Column("requires_approval", sa.Boolean(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["configuration_version_id"], ["cfg_configuration_versions.id"]),
        sa.ForeignKeyConstraint(["workflow_definition_id"], ["cfg_workflow_definitions.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "workflow_definition_id",
            "from_status_code",
            "to_status_code",
            name="uq_cfg_transitions_edge",
        ),
    )
    op.create_index(
        op.f("ix_cfg_transition_rules_organization_id"),
        "cfg_transition_rules",
        ["organization_id"],
    )

    op.create_table(
        "cfg_followup_rules",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("configuration_version_id", sa.Uuid(), nullable=False),
        sa.Column("workflow_code", sa.String(length=64), nullable=False),
        sa.Column("trigger_status_code", sa.String(length=64), nullable=False),
        sa.Column("due_offset_hours", sa.Integer(), nullable=False),
        sa.Column("required_response", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["configuration_version_id"], ["cfg_configuration_versions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_cfg_followup_version",
        "cfg_followup_rules",
        ["configuration_version_id", "workflow_code"],
    )
    op.create_index(
        op.f("ix_cfg_followup_rules_organization_id"),
        "cfg_followup_rules",
        ["organization_id"],
    )

    op.create_table(
        "cfg_reminder_rules",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("configuration_version_id", sa.Uuid(), nullable=False),
        sa.Column("workflow_code", sa.String(length=64), nullable=False),
        sa.Column("offset_hours_before_due", sa.Integer(), nullable=False),
        sa.Column("channel", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["configuration_version_id"], ["cfg_configuration_versions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_cfg_reminder_rules_organization_id"),
        "cfg_reminder_rules",
        ["organization_id"],
    )

    op.create_table(
        "cfg_escalation_rules",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("configuration_version_id", sa.Uuid(), nullable=False),
        sa.Column("workflow_code", sa.String(length=64), nullable=False),
        sa.Column("after_hours_overdue", sa.Integer(), nullable=False),
        sa.Column("escalate_to_role_code", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["configuration_version_id"], ["cfg_configuration_versions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_cfg_escalation_rules_organization_id"),
        "cfg_escalation_rules",
        ["organization_id"],
    )

    op.create_table(
        "cfg_approval_workflows",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("configuration_version_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("action_code", sa.String(length=128), nullable=False),
        sa.Column("steps", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["configuration_version_id"], ["cfg_configuration_versions.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "configuration_version_id", "code", name="uq_cfg_approval_wf_version_code"
        ),
    )
    op.create_index(
        op.f("ix_cfg_approval_workflows_organization_id"),
        "cfg_approval_workflows",
        ["organization_id"],
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "cfg_configuration_versions",
            "cfg_workflow_definitions",
            "cfg_status_definitions",
            "cfg_transition_rules",
            "cfg_followup_rules",
            "cfg_reminder_rules",
            "cfg_escalation_rules",
            "cfg_approval_workflows",
        ):
            _rls(table)


def downgrade() -> None:
    tables = (
        "cfg_approval_workflows",
        "cfg_escalation_rules",
        "cfg_reminder_rules",
        "cfg_followup_rules",
        "cfg_transition_rules",
        "cfg_status_definitions",
        "cfg_workflow_definitions",
        "cfg_configuration_versions",
    )
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
