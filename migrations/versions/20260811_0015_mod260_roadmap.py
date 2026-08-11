"""MOD-260 phases, milestones, deliverables, dependencies, baselines, forecasts.

Revision ID: 20260811_0015
Revises: 20260811_0014
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0015"
down_revision: str | None = "20260811_0014"
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
        "pm_phases",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("planned_start", sa.Date(), nullable=True),
        sa.Column("planned_end", sa.Date(), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id", "code", name="uq_pm_phases_code"),
    )
    op.create_index("ix_pm_phases_project", "pm_phases", ["organization_id", "project_id"])
    op.create_index(op.f("ix_pm_phases_organization_id"), "pm_phases", ["organization_id"])

    op.create_table(
        "pm_milestones",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("phase_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("target_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("requires_approval", sa.Boolean(), nullable=False),
        sa.Column("approved_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["phase_id"], ["pm_phases.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("phase_id", "code", name="uq_pm_milestones_code"),
    )
    op.create_index(
        "ix_pm_milestones_phase", "pm_milestones", ["organization_id", "phase_id"]
    )
    op.create_index(
        op.f("ix_pm_milestones_organization_id"), "pm_milestones", ["organization_id"]
    )

    op.create_table(
        "pm_deliverables",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("phase_id", sa.Uuid(), nullable=False),
        sa.Column("milestone_id", sa.Uuid(), nullable=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["milestone_id"], ["pm_milestones.id"]),
        sa.ForeignKeyConstraint(["phase_id"], ["pm_phases.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("phase_id", "code", name="uq_pm_deliverables_code"),
    )
    op.create_index(
        op.f("ix_pm_deliverables_organization_id"),
        "pm_deliverables",
        ["organization_id"],
    )

    op.create_table(
        "pm_phase_dependencies",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("predecessor_phase_id", sa.Uuid(), nullable=False),
        sa.Column("successor_phase_id", sa.Uuid(), nullable=False),
        sa.Column("dependency_type", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["predecessor_phase_id"], ["pm_phases.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(["successor_phase_id"], ["pm_phases.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "predecessor_phase_id",
            "successor_phase_id",
            name="uq_pm_phase_dependencies",
        ),
    )
    op.create_index(
        op.f("ix_pm_phase_dependencies_organization_id"),
        "pm_phase_dependencies",
        ["organization_id"],
    )

    op.create_table(
        "pm_requirement_phase_maps",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_id", sa.Uuid(), nullable=False),
        sa.Column("phase_id", sa.Uuid(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["phase_id"], ["pm_phases.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(["requirement_id"], ["prj_requirements.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "requirement_id", "phase_id", name="uq_pm_requirement_phase_maps"
        ),
    )
    op.create_index(
        op.f("ix_pm_requirement_phase_maps_organization_id"),
        "pm_requirement_phase_maps",
        ["organization_id"],
    )

    op.create_table(
        "pm_project_baselines",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("snapshot_json", sa.JSON(), nullable=False),
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
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "project_id", "version_number", name="uq_pm_project_baselines"
        ),
    )
    op.create_index(
        "ix_pm_baselines_project",
        "pm_project_baselines",
        ["organization_id", "project_id"],
    )
    op.create_index(
        op.f("ix_pm_project_baselines_organization_id"),
        "pm_project_baselines",
        ["organization_id"],
    )

    op.create_table(
        "pm_forecasts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("phase_id", sa.Uuid(), nullable=True),
        sa.Column("forecast_type", sa.String(length=32), nullable=False),
        sa.Column("predicted_date", sa.Date(), nullable=True),
        sa.Column("predicted_value", sa.Numeric(14, 2), nullable=True),
        sa.Column("confidence", sa.Numeric(5, 4), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["phase_id"], ["pm_phases.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_pm_forecasts_project",
        "pm_forecasts",
        ["organization_id", "project_id"],
    )
    op.create_index(
        op.f("ix_pm_forecasts_organization_id"), "pm_forecasts", ["organization_id"]
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "pm_phases",
            "pm_milestones",
            "pm_deliverables",
            "pm_phase_dependencies",
            "pm_requirement_phase_maps",
            "pm_project_baselines",
            "pm_forecasts",
        ):
            _rls(table)


def downgrade() -> None:
    tables = (
        "pm_forecasts",
        "pm_project_baselines",
        "pm_requirement_phase_maps",
        "pm_phase_dependencies",
        "pm_deliverables",
        "pm_milestones",
        "pm_phases",
    )
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
