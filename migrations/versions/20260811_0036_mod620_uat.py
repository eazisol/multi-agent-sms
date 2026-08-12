"""MOD-620 synthetic sample projects, agent evaluation, E2E, and UAT tables.

Revision ID: 20260811_0036
Revises: 20260811_0035
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0036"
down_revision: str | None = "20260811_0035"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABLES = (
    "ua_sample_projects",
    "ua_seed_scripts",
    "ua_expected_decisions",
    "ua_agent_evaluations",
    "ua_e2e_tests",
    "ua_role_uat",
    "ua_acceptance_evidence",
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
        "ua_sample_projects",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("workflow_status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_ua_sample_projects_org_code"),
    )
    op.create_index(
        "ix_ua_sample_projects_org_created",
        "ua_sample_projects",
        ["organization_id", "created_at"],
    )
    op.create_index(
        op.f("ix_ua_sample_projects_organization_id"),
        "ua_sample_projects",
        ["organization_id"],
    )

    op.create_table(
        "ua_seed_scripts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("sample_project_code", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("checksum", sa.String(length=128), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        _updated_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_ua_seed_scripts_org_code"),
    )
    op.create_index(
        "ix_ua_seed_scripts_org_created",
        "ua_seed_scripts",
        ["organization_id", "created_at"],
    )
    op.create_index(
        op.f("ix_ua_seed_scripts_organization_id"),
        "ua_seed_scripts",
        ["organization_id"],
    )

    op.create_table(
        "ua_expected_decisions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("seed_script_id", sa.Uuid(), nullable=True),
        sa.Column("decision_key", sa.String(length=128), nullable=False),
        sa.Column("expected_outcome", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["seed_script_id"],
            ["ua_seed_scripts.id"],
            name="fk_ua_expected_decisions_seed_script",
        ),
        sa.UniqueConstraint(
            "organization_id", "decision_key", name="uq_ua_expected_decisions_org_key"
        ),
    )
    op.create_index(
        "ix_ua_expected_decisions_org_created",
        "ua_expected_decisions",
        ["organization_id", "created_at"],
    )
    op.create_index(
        op.f("ix_ua_expected_decisions_organization_id"),
        "ua_expected_decisions",
        ["organization_id"],
    )

    op.create_table(
        "ua_agent_evaluations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("agent_code", sa.String(length=64), nullable=False),
        sa.Column("accuracy_pct", sa.Integer(), nullable=False),
        sa.Column("sample_count", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id", "code", name="uq_ua_agent_evaluations_org_code"
        ),
    )
    op.create_index(
        "ix_ua_agent_evaluations_org_created",
        "ua_agent_evaluations",
        ["organization_id", "created_at"],
    )
    op.create_index(
        op.f("ix_ua_agent_evaluations_organization_id"),
        "ua_agent_evaluations",
        ["organization_id"],
    )

    op.create_table(
        "ua_e2e_tests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("suite_name", sa.String(length=255), nullable=False),
        sa.Column("result", sa.String(length=32), nullable=False),
        sa.Column("evidence", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_ua_e2e_tests_org_code"),
    )
    op.create_index(
        "ix_ua_e2e_tests_org_created",
        "ua_e2e_tests",
        ["organization_id", "created_at"],
    )
    op.create_index(
        op.f("ix_ua_e2e_tests_organization_id"),
        "ua_e2e_tests",
        ["organization_id"],
    )

    op.create_table(
        "ua_role_uat",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("role_code", sa.String(length=64), nullable=False),
        sa.Column("scenario", sa.String(length=255), nullable=False),
        sa.Column("result", sa.String(length=32), nullable=False),
        sa.Column("tester_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_ua_role_uat_org_code"),
    )
    op.create_index(
        "ix_ua_role_uat_org_created",
        "ua_role_uat",
        ["organization_id", "created_at"],
    )
    op.create_index(
        op.f("ix_ua_role_uat_organization_id"),
        "ua_role_uat",
        ["organization_id"],
    )

    op.create_table(
        "ua_acceptance_evidence",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("evidence_ref", sa.String(length=512), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("submitted_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("accepted_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        _created_at(),
        _updated_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id", "code", name="uq_ua_acceptance_evidence_org_code"
        ),
    )
    op.create_index(
        "ix_ua_acceptance_evidence_org_status",
        "ua_acceptance_evidence",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_ua_acceptance_evidence_organization_id"),
        "ua_acceptance_evidence",
        ["organization_id"],
    )

    for table in _TABLES:
        _rls(table)


def downgrade() -> None:
    for table in reversed(_TABLES):
        op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
    op.drop_table("ua_acceptance_evidence")
    op.drop_table("ua_role_uat")
    op.drop_table("ua_e2e_tests")
    op.drop_table("ua_agent_evaluations")
    op.drop_table("ua_expected_decisions")
    op.drop_table("ua_seed_scripts")
    op.drop_table("ua_sample_projects")
