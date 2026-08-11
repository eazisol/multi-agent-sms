"""MOD-330 human approval gates, delegation, rejection, and override.

Revision ID: 20260811_0019
Revises: 20260811_0018
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0019"
down_revision: str | None = "20260811_0018"
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
        "apr_requests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("action_code", sa.String(length=128), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("target_entity_type", sa.String(length=64), nullable=False),
        sa.Column("target_entity_id", sa.Uuid(), nullable=False),
        sa.Column("target_version", sa.Integer(), nullable=False),
        sa.Column("workflow_code", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("current_step_order", sa.Integer(), nullable=False),
        sa.Column("submitted_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("submitted_by_actor_kind", sa.String(length=32), nullable=False),
        sa.Column("recommendation_source_actor_id", sa.Uuid(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("superseded_by_id", sa.Uuid(), nullable=True),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
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
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_apr_requests_target",
        "apr_requests",
        ["organization_id", "target_entity_type", "target_entity_id", "target_version"],
    )
    op.create_index("ix_apr_requests_status", "apr_requests", ["organization_id", "status"])
    op.create_index(op.f("ix_apr_requests_organization_id"), "apr_requests", ["organization_id"])

    op.create_table(
        "apr_workflows",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("approval_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("steps_json", sa.JSON(), nullable=False),
        sa.Column("configuration_version_id", sa.Uuid(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("approval_id", name="uq_apr_workflows_approval"),
    )
    op.create_index(op.f("ix_apr_workflows_organization_id"), "apr_workflows", ["organization_id"])

    op.create_table(
        "apr_steps",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("approval_id", sa.Uuid(), nullable=False),
        sa.Column("step_order", sa.Integer(), nullable=False),
        sa.Column("role_code", sa.String(length=64), nullable=False),
        sa.Column("required_authority_level", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("assignee_actor_id", sa.Uuid(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("approval_id", "step_order", name="uq_apr_steps_order"),
    )
    op.create_index("ix_apr_steps_approval", "apr_steps", ["organization_id", "approval_id"])
    op.create_index(op.f("ix_apr_steps_organization_id"), "apr_steps", ["organization_id"])

    op.create_table(
        "apr_decisions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("approval_id", sa.Uuid(), nullable=False),
        sa.Column("step_id", sa.Uuid(), nullable=False),
        sa.Column("decision", sa.String(length=32), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("actor_kind", sa.String(length=32), nullable=False),
        sa.Column("authority_mode", sa.String(length=32), nullable=False),
        sa.Column("delegation_id", sa.Uuid(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column(
            "decided_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_apr_decisions_approval", "apr_decisions", ["organization_id", "approval_id"]
    )
    op.create_index(op.f("ix_apr_decisions_organization_id"), "apr_decisions", ["organization_id"])

    op.create_table(
        "apr_delegations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("from_actor_id", sa.Uuid(), nullable=False),
        sa.Column("to_actor_id", sa.Uuid(), nullable=False),
        sa.Column("action_code", sa.String(length=128), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_by_actor_id", sa.Uuid(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_apr_delegations_delegate",
        "apr_delegations",
        ["organization_id", "to_actor_id", "status"],
    )
    op.create_index(
        op.f("ix_apr_delegations_organization_id"), "apr_delegations", ["organization_id"]
    )

    op.create_table(
        "apr_evidence",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("approval_id", sa.Uuid(), nullable=False),
        sa.Column("evidence_type", sa.String(length=64), nullable=False),
        sa.Column("evidence_ref", sa.String(length=512), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
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
        "ix_apr_evidence_approval", "apr_evidence", ["organization_id", "approval_id"]
    )
    op.create_index(op.f("ix_apr_evidence_organization_id"), "apr_evidence", ["organization_id"])

    op.create_table(
        "apr_overrides",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("approval_id", sa.Uuid(), nullable=True),
        sa.Column("action_code", sa.String(length=128), nullable=False),
        sa.Column("target_entity_type", sa.String(length=64), nullable=False),
        sa.Column("target_entity_id", sa.Uuid(), nullable=False),
        sa.Column("target_version", sa.Integer(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("authority_used", sa.String(length=128), nullable=False),
        sa.Column("retrospective_required", sa.Boolean(), nullable=False),
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
        "ix_apr_overrides_target",
        "apr_overrides",
        ["organization_id", "target_entity_type", "target_entity_id"],
    )
    op.create_index(op.f("ix_apr_overrides_organization_id"), "apr_overrides", ["organization_id"])

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "apr_requests",
            "apr_workflows",
            "apr_steps",
            "apr_decisions",
            "apr_delegations",
            "apr_evidence",
            "apr_overrides",
        ):
            _rls(table)


def downgrade() -> None:
    bind = op.get_bind()
    tables = (
        "apr_overrides",
        "apr_evidence",
        "apr_delegations",
        "apr_decisions",
        "apr_steps",
        "apr_workflows",
        "apr_requests",
    )
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
