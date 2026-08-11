"""MOD-300 tickets, subtasks, dependencies, evidence, readiness and done checks.

Revision ID: 20260811_0016
Revises: 20260811_0015
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0016"
down_revision: str | None = "20260811_0015"
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
        "tkt_tickets",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("phase_id", sa.Uuid(), nullable=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("ticket_type", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("priority", sa.String(length=32), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=True),
        sa.Column("queue_code", sa.String(length=64), nullable=True),
        sa.Column("estimate_points", sa.Numeric(precision=8, scale=2), nullable=True),
        sa.Column("acceptance_criteria", sa.Text(), nullable=True),
        sa.Column("definition_of_done", sa.Text(), nullable=True),
        sa.Column("blocked_reason", sa.Text(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reopen_reason", sa.Text(), nullable=True),
        sa.Column("reopen_evidence_id", sa.Uuid(), nullable=True),
        sa.Column("reopened_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("reopened_at", sa.DateTime(timezone=True), nullable=True),
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
        sa.ForeignKeyConstraint(["phase_id"], ["pm_phases.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id", "code", name="uq_tkt_tickets_code"),
    )
    op.create_index(
        "ix_tkt_tickets_project", "tkt_tickets", ["organization_id", "project_id"]
    )
    op.create_index(
        "ix_tkt_tickets_status", "tkt_tickets", ["organization_id", "status"]
    )
    op.create_index(
        op.f("ix_tkt_tickets_organization_id"), "tkt_tickets", ["organization_id"]
    )

    op.create_table(
        "tkt_subtasks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("ticket_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=True),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(["ticket_id"], ["tkt_tickets.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ticket_id", "code", name="uq_tkt_subtasks_code"),
    )
    op.create_index(
        "ix_tkt_subtasks_ticket", "tkt_subtasks", ["organization_id", "ticket_id"]
    )
    op.create_index(
        op.f("ix_tkt_subtasks_organization_id"), "tkt_subtasks", ["organization_id"]
    )

    op.create_table(
        "tkt_ticket_dependencies",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("predecessor_ticket_id", sa.Uuid(), nullable=False),
        sa.Column("successor_ticket_id", sa.Uuid(), nullable=False),
        sa.Column("dependency_type", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["predecessor_ticket_id"], ["tkt_tickets.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(["successor_ticket_id"], ["tkt_tickets.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "predecessor_ticket_id",
            "successor_ticket_id",
            name="uq_tkt_ticket_dependencies",
        ),
    )
    op.create_index(
        op.f("ix_tkt_ticket_dependencies_organization_id"),
        "tkt_ticket_dependencies",
        ["organization_id"],
    )

    op.create_table(
        "tkt_requirement_links",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("ticket_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_version_id", sa.Uuid(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(["requirement_id"], ["prj_requirements.id"]),
        sa.ForeignKeyConstraint(["ticket_id"], ["tkt_tickets.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "ticket_id", "requirement_id", name="uq_tkt_requirement_links"
        ),
    )
    op.create_index(
        op.f("ix_tkt_requirement_links_organization_id"),
        "tkt_requirement_links",
        ["organization_id"],
    )

    op.create_table(
        "tkt_ticket_evidence",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("ticket_id", sa.Uuid(), nullable=False),
        sa.Column("evidence_type", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("uri_or_ref", sa.String(length=1024), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(["ticket_id"], ["tkt_tickets.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_tkt_evidence_ticket",
        "tkt_ticket_evidence",
        ["organization_id", "ticket_id"],
    )
    op.create_index(
        op.f("ix_tkt_ticket_evidence_organization_id"),
        "tkt_ticket_evidence",
        ["organization_id"],
    )

    op.create_table(
        "tkt_readiness_checks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("ticket_id", sa.Uuid(), nullable=False),
        sa.Column("check_code", sa.String(length=64), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.Column("is_required", sa.Boolean(), nullable=False),
        sa.Column("is_satisfied", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("satisfied_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("satisfied_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(["ticket_id"], ["tkt_tickets.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "ticket_id", "check_code", name="uq_tkt_readiness_checks"
        ),
    )
    op.create_index(
        op.f("ix_tkt_readiness_checks_organization_id"),
        "tkt_readiness_checks",
        ["organization_id"],
    )

    op.create_table(
        "tkt_done_checks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("ticket_id", sa.Uuid(), nullable=False),
        sa.Column("check_code", sa.String(length=64), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.Column("is_required", sa.Boolean(), nullable=False),
        sa.Column("is_satisfied", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("satisfied_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("satisfied_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(["ticket_id"], ["tkt_tickets.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ticket_id", "check_code", name="uq_tkt_done_checks"),
    )
    op.create_index(
        op.f("ix_tkt_done_checks_organization_id"),
        "tkt_done_checks",
        ["organization_id"],
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "tkt_tickets",
            "tkt_subtasks",
            "tkt_ticket_dependencies",
            "tkt_requirement_links",
            "tkt_ticket_evidence",
            "tkt_readiness_checks",
            "tkt_done_checks",
        ):
            _rls(table)


def downgrade() -> None:
    bind = op.get_bind()
    tables = (
        "tkt_done_checks",
        "tkt_readiness_checks",
        "tkt_ticket_evidence",
        "tkt_requirement_links",
        "tkt_ticket_dependencies",
        "tkt_subtasks",
        "tkt_tickets",
    )
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
