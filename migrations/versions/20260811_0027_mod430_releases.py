"""MOD-430 releases, items, deployments, checks, backups, migrations, rollbacks, completion.

Revision ID: 20260811_0027
Revises: 20260811_0026
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0027"
down_revision: str | None = "20260811_0026"
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


def _ts():
    return sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False)


def upgrade() -> None:
    op.create_table(
        "rl_releases",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("version_label", sa.String(length=64), nullable=False),
        sa.Column("approval_evidence", sa.Text(), nullable=True),
        sa.Column("approved_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_rl_releases_org_code"),
    )
    op.create_index("ix_rl_releases_status", "rl_releases", ["organization_id", "status"])
    op.create_index("ix_rl_releases_project", "rl_releases", ["organization_id", "project_id"])
    op.create_index(op.f("ix_rl_releases_organization_id"), "rl_releases", ["organization_id"])

    op.create_table(
        "rl_release_items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("release_id", sa.Uuid(), nullable=False),
        sa.Column("link_type", sa.String(length=32), nullable=False),
        sa.Column("linked_entity_id", sa.Uuid(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "release_id", "link_type", "linked_entity_id", name="uq_rl_items_release_link"),
    )
    op.create_index("ix_rl_items_release", "rl_release_items", ["organization_id", "release_id"])
    op.create_index(op.f("ix_rl_release_items_organization_id"), "rl_release_items", ["organization_id"])

    op.create_table(
        "rl_deployments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("release_id", sa.Uuid(), nullable=False),
        sa.Column("environment_code", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("build_ref", sa.String(length=128), nullable=True),
        sa.Column("requested_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_rl_deployments_release", "rl_deployments", ["organization_id", "release_id"])
    op.create_index(op.f("ix_rl_deployments_organization_id"), "rl_deployments", ["organization_id"])

    op.create_table(
        "rl_deployment_checks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("deployment_id", sa.Uuid(), nullable=False),
        sa.Column("check_name", sa.String(length=128), nullable=False),
        sa.Column("result", sa.String(length=16), nullable=False),
        sa.Column("evidence", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_rl_checks_deployment", "rl_deployment_checks", ["organization_id", "deployment_id"])
    op.create_index(op.f("ix_rl_deployment_checks_organization_id"), "rl_deployment_checks", ["organization_id"])

    op.create_table(
        "rl_backup_confirmations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("release_id", sa.Uuid(), nullable=False),
        sa.Column("backup_ref", sa.String(length=255), nullable=False),
        sa.Column("confirmed", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("confirmed_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_rl_backups_release", "rl_backup_confirmations", ["organization_id", "release_id"])
    op.create_index(op.f("ix_rl_backup_confirmations_organization_id"), "rl_backup_confirmations", ["organization_id"])

    op.create_table(
        "rl_migration_plans",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("release_id", sa.Uuid(), nullable=False),
        sa.Column("plan_text", sa.Text(), nullable=False),
        sa.Column("alembic_revision", sa.String(length=128), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_rl_migrations_release", "rl_migration_plans", ["organization_id", "release_id"])
    op.create_index(op.f("ix_rl_migration_plans_organization_id"), "rl_migration_plans", ["organization_id"])

    op.create_table(
        "rl_rollbacks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("release_id", sa.Uuid(), nullable=False),
        sa.Column("deployment_id", sa.Uuid(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("evidence", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_rl_rollbacks_release", "rl_rollbacks", ["organization_id", "release_id"])
    op.create_index(op.f("ix_rl_rollbacks_organization_id"), "rl_rollbacks", ["organization_id"])

    op.create_table(
        "rl_completion_reports",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("release_id", sa.Uuid(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("client_accepted", sa.Boolean(), nullable=False),
        sa.Column("internal_accepted", sa.Boolean(), nullable=False),
        sa.Column("client_acceptance_notes", sa.Text(), nullable=True),
        sa.Column("internal_acceptance_notes", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "release_id", name="uq_rl_completion_release"),
    )
    op.create_index(op.f("ix_rl_completion_reports_organization_id"), "rl_completion_reports", ["organization_id"])

    for table in (
        "rl_releases", "rl_release_items", "rl_deployments", "rl_deployment_checks",
        "rl_backup_confirmations", "rl_migration_plans", "rl_rollbacks", "rl_completion_reports",
    ):
        _rls(table)


def downgrade() -> None:
    for table in (
        "rl_completion_reports", "rl_rollbacks", "rl_migration_plans", "rl_backup_confirmations",
        "rl_deployment_checks", "rl_deployments", "rl_release_items", "rl_releases",
    ):
        op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
        op.drop_table(table)
