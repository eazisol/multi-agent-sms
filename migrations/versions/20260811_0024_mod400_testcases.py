"""MOD-400 test cases, steps, suites, plans, runs, evidence, coverage.

Revision ID: 20260811_0024
Revises: 20260811_0023
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0024"
down_revision: str | None = "20260811_0023"
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
        "tc_cases",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("case_type", sa.String(length=32), nullable=False),
        sa.Column("priority", sa.String(length=8), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("preconditions", sa.Text(), nullable=True),
        sa.Column("expected_result", sa.Text(), nullable=True),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
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
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_tc_cases_org_code"),
    )
    op.create_index("ix_tc_cases_status", "tc_cases", ["organization_id", "status"])
    op.create_index("ix_tc_cases_project", "tc_cases", ["organization_id", "project_id"])
    op.create_index(op.f("ix_tc_cases_organization_id"), "tc_cases", ["organization_id"])

    op.create_table(
        "tc_steps",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("case_id", sa.Uuid(), nullable=False),
        sa.Column("step_number", sa.Integer(), nullable=False),
        sa.Column("action_text", sa.Text(), nullable=False),
        sa.Column("expected_text", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("case_id", "step_number", name="uq_tc_steps_case_number"),
    )
    op.create_index("ix_tc_steps_case", "tc_steps", ["organization_id", "case_id"])
    op.create_index(op.f("ix_tc_steps_organization_id"), "tc_steps", ["organization_id"])

    op.create_table(
        "tc_suites",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("case_ids", sa.JSON(), nullable=False),
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
        sa.UniqueConstraint("organization_id", "code", name="uq_tc_suites_org_code"),
    )
    op.create_index(op.f("ix_tc_suites_organization_id"), "tc_suites", ["organization_id"])

    op.create_table(
        "tc_plans",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("environment_code", sa.String(length=64), nullable=False),
        sa.Column("build_ref", sa.String(length=128), nullable=True),
        sa.Column("suite_ids", sa.JSON(), nullable=False),
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
        sa.UniqueConstraint("organization_id", "code", name="uq_tc_plans_org_code"),
    )
    op.create_index("ix_tc_plans_status", "tc_plans", ["organization_id", "status"])
    op.create_index(op.f("ix_tc_plans_organization_id"), "tc_plans", ["organization_id"])

    op.create_table(
        "tc_runs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("case_id", sa.Uuid(), nullable=False),
        sa.Column("plan_id", sa.Uuid(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("environment_code", sa.String(length=64), nullable=False),
        sa.Column("build_ref", sa.String(length=128), nullable=True),
        sa.Column("result_summary", sa.Text(), nullable=True),
        sa.Column("executed_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
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
    )
    op.create_index("ix_tc_runs_status", "tc_runs", ["organization_id", "status"])
    op.create_index("ix_tc_runs_case", "tc_runs", ["organization_id", "case_id"])
    op.create_index(op.f("ix_tc_runs_organization_id"), "tc_runs", ["organization_id"])

    op.create_table(
        "tc_evidence",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("run_id", sa.Uuid(), nullable=False),
        sa.Column("evidence_type", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("body_text", sa.Text(), nullable=True),
        sa.Column("uri", sa.String(length=1024), nullable=True),
        sa.Column("environment_code", sa.String(length=64), nullable=False),
        sa.Column("build_ref", sa.String(length=128), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_tc_evidence_run", "tc_evidence", ["organization_id", "run_id"])
    op.create_index(op.f("ix_tc_evidence_organization_id"), "tc_evidence", ["organization_id"])

    op.create_table(
        "tc_coverage_links",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("case_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_priority", sa.String(length=32), nullable=False),
        sa.Column("coverage_notes", sa.Text(), nullable=True),
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
            "case_id",
            "requirement_id",
            name="uq_tc_coverage_case_requirement",
        ),
    )
    op.create_index("ix_tc_coverage_case", "tc_coverage_links", ["organization_id", "case_id"])
    op.create_index(
        "ix_tc_coverage_requirement",
        "tc_coverage_links",
        ["organization_id", "requirement_id"],
    )
    op.create_index(
        op.f("ix_tc_coverage_links_organization_id"),
        "tc_coverage_links",
        ["organization_id"],
    )

    for table in (
        "tc_cases",
        "tc_steps",
        "tc_suites",
        "tc_plans",
        "tc_runs",
        "tc_evidence",
        "tc_coverage_links",
    ):
        _rls(table)


def downgrade() -> None:
    for table in (
        "tc_coverage_links",
        "tc_evidence",
        "tc_runs",
        "tc_plans",
        "tc_suites",
        "tc_steps",
        "tc_cases",
    ):
        op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
        op.drop_table(table)
