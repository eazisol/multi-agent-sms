"""MOD-240 projects, requirements, versions, rules, ACs, assumptions, constraints, SRS.

Revision ID: 20260811_0013
Revises: 20260811_0012
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0013"
down_revision: str | None = "20260811_0012"
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
        "prj_projects",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("client_id", sa.Uuid(), nullable=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
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
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_prj_projects_code"),
    )
    op.create_index(
        op.f("ix_prj_projects_organization_id"), "prj_projects", ["organization_id"]
    )

    op.create_table(
        "prj_requirements",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("current_version_id", sa.Uuid(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "project_id", "requirement_code", name="uq_prj_requirements_code"
        ),
    )
    op.create_index(
        "ix_prj_requirements_project",
        "prj_requirements",
        ["organization_id", "project_id"],
    )
    op.create_index(
        op.f("ix_prj_requirements_organization_id"),
        "prj_requirements",
        ["organization_id"],
    )

    op.create_table(
        "prj_requirement_versions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_id", sa.Uuid(), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("statement", sa.Text(), nullable=False),
        sa.Column("priority", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("change_reason", sa.Text(), nullable=True),
        sa.Column("approved_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(["requirement_id"], ["prj_requirements.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "requirement_id", "version_number", name="uq_prj_requirement_versions"
        ),
    )
    op.create_index(
        op.f("ix_prj_requirement_versions_organization_id"),
        "prj_requirement_versions",
        ["organization_id"],
    )

    op.create_table(
        "prj_business_rules",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_version_id", sa.Uuid(), nullable=False),
        sa.Column("rule_code", sa.String(length=64), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(
            ["requirement_version_id"], ["prj_requirement_versions.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "requirement_version_id", "rule_code", name="uq_prj_business_rules_code"
        ),
    )
    op.create_index(
        op.f("ix_prj_business_rules_organization_id"),
        "prj_business_rules",
        ["organization_id"],
    )

    op.create_table(
        "prj_acceptance_criteria",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_version_id", sa.Uuid(), nullable=False),
        sa.Column("criterion_code", sa.String(length=64), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(
            ["requirement_version_id"], ["prj_requirement_versions.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "requirement_version_id",
            "criterion_code",
            name="uq_prj_acceptance_criteria_code",
        ),
    )
    op.create_index(
        op.f("ix_prj_acceptance_criteria_organization_id"),
        "prj_acceptance_criteria",
        ["organization_id"],
    )

    op.create_table(
        "prj_assumptions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_version_id", sa.Uuid(), nullable=True),
        sa.Column("assumption_code", sa.String(length=64), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(
            ["requirement_version_id"], ["prj_requirement_versions.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_prj_assumptions_project",
        "prj_assumptions",
        ["organization_id", "project_id"],
    )
    op.create_index(
        op.f("ix_prj_assumptions_organization_id"),
        "prj_assumptions",
        ["organization_id"],
    )

    op.create_table(
        "prj_constraints",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_version_id", sa.Uuid(), nullable=True),
        sa.Column("constraint_code", sa.String(length=64), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(
            ["requirement_version_id"], ["prj_requirement_versions.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_prj_constraints_project",
        "prj_constraints",
        ["organization_id", "project_id"],
    )
    op.create_index(
        op.f("ix_prj_constraints_organization_id"),
        "prj_constraints",
        ["organization_id"],
    )

    op.create_table(
        "prj_srs_baselines",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("requirement_version_ids", sa.JSON(), nullable=False),
        sa.Column("change_reason", sa.Text(), nullable=True),
        sa.Column("approved_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "project_id", "version_number", name="uq_prj_srs_baselines_version"
        ),
    )
    op.create_index(
        "ix_prj_srs_project",
        "prj_srs_baselines",
        ["organization_id", "project_id"],
    )
    op.create_index(
        op.f("ix_prj_srs_baselines_organization_id"),
        "prj_srs_baselines",
        ["organization_id"],
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "prj_projects",
            "prj_requirements",
            "prj_requirement_versions",
            "prj_business_rules",
            "prj_acceptance_criteria",
            "prj_assumptions",
            "prj_constraints",
            "prj_srs_baselines",
        ):
            _rls(table)


def downgrade() -> None:
    tables = (
        "prj_srs_baselines",
        "prj_constraints",
        "prj_assumptions",
        "prj_acceptance_criteria",
        "prj_business_rules",
        "prj_requirement_versions",
        "prj_requirements",
        "prj_projects",
    )
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
