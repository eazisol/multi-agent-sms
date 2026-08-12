"""MOD-630 controlled pilot, production release records, and final MVP sign-off.

Revision ID: 20260811_0037
Revises: 20260811_0036
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0037"
down_revision: str | None = "20260811_0036"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABLES = (
    "pl_pilot_plans",
    "pl_pilot_users",
    "pl_training_records",
    "pl_support_readiness",
    "pl_known_limitations",
    "pl_acceptance_tests",
    "pl_production_deployments",
    "pl_rollbacks",
    "pl_final_signoffs",
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
        "pl_pilot_plans",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        _updated_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_pl_pilot_plans_org_code"),
    )
    op.create_index(
        "ix_pl_pilot_plans_org_created",
        "pl_pilot_plans",
        ["organization_id", "created_at"],
    )
    op.create_index(
        op.f("ix_pl_pilot_plans_organization_id"),
        "pl_pilot_plans",
        ["organization_id"],
    )

    op.create_table(
        "pl_pilot_users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("plan_id", sa.Uuid(), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("role_label", sa.String(length=128), nullable=False),
        sa.Column("approved_production_use", sa.Boolean(), nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["pl_pilot_plans.id"],
            name="fk_pl_pilot_users_plan",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "plan_id",
            "actor_id",
            name="uq_pl_pilot_users_org_plan_actor",
        ),
    )
    op.create_index(
        "ix_pl_pilot_users_org_plan",
        "pl_pilot_users",
        ["organization_id", "plan_id"],
    )
    op.create_index(
        op.f("ix_pl_pilot_users_organization_id"),
        "pl_pilot_users",
        ["organization_id"],
    )

    op.create_table(
        "pl_training_records",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("plan_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("audience", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["pl_pilot_plans.id"],
            name="fk_pl_training_records_plan",
        ),
    )
    op.create_index(
        "ix_pl_training_records_org_plan",
        "pl_training_records",
        ["organization_id", "plan_id"],
    )
    op.create_index(
        op.f("ix_pl_training_records_organization_id"),
        "pl_training_records",
        ["organization_id"],
    )

    op.create_table(
        "pl_support_readiness",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("plan_id", sa.Uuid(), nullable=False),
        sa.Column("checklist_item", sa.String(length=255), nullable=False),
        sa.Column("ready", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["pl_pilot_plans.id"],
            name="fk_pl_support_readiness_plan",
        ),
    )
    op.create_index(
        "ix_pl_support_readiness_org_plan",
        "pl_support_readiness",
        ["organization_id", "plan_id"],
    )
    op.create_index(
        op.f("ix_pl_support_readiness_organization_id"),
        "pl_support_readiness",
        ["organization_id"],
    )

    op.create_table(
        "pl_known_limitations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("plan_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["pl_pilot_plans.id"],
            name="fk_pl_known_limitations_plan",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "plan_id",
            "code",
            name="uq_pl_known_limitations_org_plan_code",
        ),
    )
    op.create_index(
        "ix_pl_known_limitations_org_plan",
        "pl_known_limitations",
        ["organization_id", "plan_id"],
    )
    op.create_index(
        op.f("ix_pl_known_limitations_organization_id"),
        "pl_known_limitations",
        ["organization_id"],
    )

    op.create_table(
        "pl_acceptance_tests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("plan_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("result", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["pl_pilot_plans.id"],
            name="fk_pl_acceptance_tests_plan",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "plan_id",
            "code",
            name="uq_pl_acceptance_tests_org_plan_code",
        ),
    )
    op.create_index(
        "ix_pl_acceptance_tests_org_plan",
        "pl_acceptance_tests",
        ["organization_id", "plan_id"],
    )
    op.create_index(
        op.f("ix_pl_acceptance_tests_organization_id"),
        "pl_acceptance_tests",
        ["organization_id"],
    )

    op.create_table(
        "pl_production_deployments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("plan_id", sa.Uuid(), nullable=False),
        sa.Column("environment", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("human_approval_evidence", sa.Text(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["pl_pilot_plans.id"],
            name="fk_pl_production_deployments_plan",
        ),
    )
    op.create_index(
        "ix_pl_production_deployments_org_plan",
        "pl_production_deployments",
        ["organization_id", "plan_id"],
    )
    op.create_index(
        op.f("ix_pl_production_deployments_organization_id"),
        "pl_production_deployments",
        ["organization_id"],
    )

    op.create_table(
        "pl_rollbacks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("deployment_id", sa.Uuid(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["deployment_id"],
            ["pl_production_deployments.id"],
            name="fk_pl_rollbacks_deployment",
        ),
    )
    op.create_index(
        "ix_pl_rollbacks_org_deployment",
        "pl_rollbacks",
        ["organization_id", "deployment_id"],
    )
    op.create_index(
        op.f("ix_pl_rollbacks_organization_id"),
        "pl_rollbacks",
        ["organization_id"],
    )

    op.create_table(
        "pl_final_signoffs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("plan_id", sa.Uuid(), nullable=False),
        sa.Column("function_code", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("evidence", sa.Text(), nullable=False),
        sa.Column("signed_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("signed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["plan_id"],
            ["pl_pilot_plans.id"],
            name="fk_pl_final_signoffs_plan",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "plan_id",
            "function_code",
            name="uq_pl_final_signoffs_org_plan_function",
        ),
    )
    op.create_index(
        "ix_pl_final_signoffs_org_plan",
        "pl_final_signoffs",
        ["organization_id", "plan_id"],
    )
    op.create_index(
        op.f("ix_pl_final_signoffs_organization_id"),
        "pl_final_signoffs",
        ["organization_id"],
    )

    for table in _TABLES:
        _rls(table)


def downgrade() -> None:
    for table in reversed(_TABLES):
        op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
    op.drop_table("pl_final_signoffs")
    op.drop_table("pl_rollbacks")
    op.drop_table("pl_production_deployments")
    op.drop_table("pl_acceptance_tests")
    op.drop_table("pl_known_limitations")
    op.drop_table("pl_support_readiness")
    op.drop_table("pl_training_records")
    op.drop_table("pl_pilot_users")
    op.drop_table("pl_pilot_plans")
