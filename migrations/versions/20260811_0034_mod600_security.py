"""MOD-600 security hardening tables.

Revision ID: 20260811_0034
Revises: 20260811_0033
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0034"
down_revision: str | None = "20260811_0033"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABLES = (
    "sh_threat_models",
    "sh_pii_inventory",
    "sh_retention_policies",
    "sh_legal_holds",
    "sh_deletion_jobs",
    "sh_backup_records",
    "sh_restore_tests",
    "sh_security_incidents",
    "sh_training_policies",
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
        "sh_threat_models",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("scope_summary", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        _updated_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id", "code", name="uq_sh_threat_models_org_code"
        ),
    )
    op.create_index(
        "ix_sh_threat_models_org_status",
        "sh_threat_models",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_sh_threat_models_organization_id"),
        "sh_threat_models",
        ["organization_id"],
    )

    op.create_table(
        "sh_pii_inventory",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("data_category", sa.String(length=128), nullable=False),
        sa.Column("field_path", sa.String(length=255), nullable=False),
        sa.Column("classification", sa.String(length=32), nullable=False),
        sa.Column("purpose", sa.Text(), nullable=False),
        sa.Column("retention_days", sa.Integer(), nullable=True),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "data_category",
            "field_path",
            name="uq_sh_pii_inventory_org_cat_path",
        ),
    )
    op.create_index(
        "ix_sh_pii_inventory_org_class",
        "sh_pii_inventory",
        ["organization_id", "classification"],
    )
    op.create_index(
        op.f("ix_sh_pii_inventory_organization_id"),
        "sh_pii_inventory",
        ["organization_id"],
    )

    op.create_table(
        "sh_retention_policies",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("retain_days", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        _updated_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id", "code", name="uq_sh_retention_policies_org_code"
        ),
    )
    op.create_index(
        "ix_sh_retention_policies_org_status",
        "sh_retention_policies",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_sh_retention_policies_organization_id"),
        "sh_retention_policies",
        ["organization_id"],
    )

    op.create_table(
        "sh_legal_holds",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("scope_json", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("held_entity_type", sa.String(length=64), nullable=True),
        sa.Column("held_entity_id", sa.Uuid(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("released_by_actor_id", sa.Uuid(), nullable=True),
        _created_at(),
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id", "code", name="uq_sh_legal_holds_org_code"
        ),
    )
    op.create_index(
        "ix_sh_legal_holds_org_status",
        "sh_legal_holds",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_sh_legal_holds_organization_id"),
        "sh_legal_holds",
        ["organization_id"],
    )

    op.create_table(
        "sh_deletion_jobs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("retention_policy_id", sa.Uuid(), nullable=True),
        sa.Column("target_entity_type", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("blocked_reason", sa.Text(), nullable=True),
        sa.Column("rows_affected", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_sh_deletion_jobs_org_status",
        "sh_deletion_jobs",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_sh_deletion_jobs_organization_id"),
        "sh_deletion_jobs",
        ["organization_id"],
    )

    op.create_table(
        "sh_backup_records",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("backup_ref", sa.String(length=255), nullable=False),
        sa.Column("environment", sa.String(length=32), nullable=False),
        sa.Column("rpo_minutes", sa.Integer(), nullable=False),
        sa.Column("rto_minutes", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id", "backup_ref", name="uq_sh_backup_records_org_ref"
        ),
    )
    op.create_index(
        "ix_sh_backup_records_org_env",
        "sh_backup_records",
        ["organization_id", "environment"],
    )
    op.create_index(
        op.f("ix_sh_backup_records_organization_id"),
        "sh_backup_records",
        ["organization_id"],
    )

    op.create_table(
        "sh_restore_tests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("backup_record_id", sa.Uuid(), nullable=False),
        sa.Column("measured_rpo_minutes", sa.Integer(), nullable=False),
        sa.Column("measured_rto_minutes", sa.Integer(), nullable=False),
        sa.Column("result", sa.String(length=32), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("tested_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_sh_restore_tests_org_created",
        "sh_restore_tests",
        ["organization_id", "created_at"],
    )
    op.create_index(
        op.f("ix_sh_restore_tests_organization_id"),
        "sh_restore_tests",
        ["organization_id"],
    )

    op.create_table(
        "sh_security_incidents",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        _updated_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id", "code", name="uq_sh_security_incidents_org_code"
        ),
    )
    op.create_index(
        "ix_sh_security_incidents_org_sev",
        "sh_security_incidents",
        ["organization_id", "severity", "status"],
    )
    op.create_index(
        op.f("ix_sh_security_incidents_organization_id"),
        "sh_security_incidents",
        ["organization_id"],
    )

    op.create_table(
        "sh_training_policies",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("allow_model_training", sa.Boolean(), nullable=False),
        sa.Column("approval_evidence", sa.Text(), nullable=True),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        _updated_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", name="uq_sh_training_policies_org"),
    )
    op.create_index(
        op.f("ix_sh_training_policies_organization_id"),
        "sh_training_policies",
        ["organization_id"],
    )

    for table in _TABLES:
        _rls(table)


def downgrade() -> None:
    for table in reversed(_TABLES):
        op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
    op.drop_table("sh_training_policies")
    op.drop_table("sh_security_incidents")
    op.drop_table("sh_restore_tests")
    op.drop_table("sh_backup_records")
    op.drop_table("sh_deletion_jobs")
    op.drop_table("sh_legal_holds")
    op.drop_table("sh_retention_policies")
    op.drop_table("sh_pii_inventory")
    op.drop_table("sh_threat_models")
