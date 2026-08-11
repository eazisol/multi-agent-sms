"""MOD-310 assignments, recommendations, acknowledgments, and ownership history.

Revision ID: 20260811_0017
Revises: 20260811_0016
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0017"
down_revision: str | None = "20260811_0016"
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
        "asg_assignments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("ticket_id", sa.Uuid(), nullable=False),
        sa.Column("assignee_actor_id", sa.Uuid(), nullable=False),
        sa.Column("role_code", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("required_skill_code", sa.String(length=64), nullable=True),
        sa.Column("min_proficiency", sa.Integer(), nullable=False),
        sa.Column("override_reason", sa.Text(), nullable=True),
        sa.Column("is_override", sa.Boolean(), nullable=False),
        sa.Column("recommendation_id", sa.Uuid(), nullable=True),
        sa.Column("assigned_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(["ticket_id"], ["tkt_tickets.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_asg_assignments_ticket", "asg_assignments", ["organization_id", "ticket_id"]
    )
    op.create_index(
        "ix_asg_assignments_actor",
        "asg_assignments",
        ["organization_id", "assignee_actor_id"],
    )
    op.create_index(
        "ix_asg_assignments_status",
        "asg_assignments",
        ["organization_id", "ticket_id", "status"],
    )
    op.create_index(
        op.f("ix_asg_assignments_organization_id"), "asg_assignments", ["organization_id"]
    )

    op.create_table(
        "asg_assignment_recommendations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("ticket_id", sa.Uuid(), nullable=False),
        sa.Column("candidate_actor_id", sa.Uuid(), nullable=False),
        sa.Column("score", sa.Numeric(precision=8, scale=4), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("eligible", sa.Boolean(), nullable=False),
        sa.Column("reasons_json", sa.JSON(), nullable=False),
        sa.Column("remaining_capacity_pct", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
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
        "ix_asg_recommendations_ticket",
        "asg_assignment_recommendations",
        ["organization_id", "ticket_id"],
    )
    op.create_index(
        op.f("ix_asg_assignment_recommendations_organization_id"),
        "asg_assignment_recommendations",
        ["organization_id"],
    )

    op.create_table(
        "asg_allocation_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("ticket_id", sa.Uuid(), nullable=False),
        sa.Column("assignment_id", sa.Uuid(), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("allocation_pct", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("recorded_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "recorded_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["assignment_id"], ["asg_assignments.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(["ticket_id"], ["tkt_tickets.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_asg_alloc_hist_actor",
        "asg_allocation_history",
        ["organization_id", "actor_id"],
    )
    op.create_index(
        op.f("ix_asg_allocation_history_organization_id"),
        "asg_allocation_history",
        ["organization_id"],
    )

    op.create_table(
        "asg_acknowledgments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("assignment_id", sa.Uuid(), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column(
            "acknowledged_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["assignment_id"], ["asg_assignments.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_asg_ack_assignment",
        "asg_acknowledgments",
        ["organization_id", "assignment_id"],
    )
    op.create_index(
        op.f("ix_asg_acknowledgments_organization_id"),
        "asg_acknowledgments",
        ["organization_id"],
    )

    op.create_table(
        "asg_reassignment_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("ticket_id", sa.Uuid(), nullable=False),
        sa.Column("from_assignment_id", sa.Uuid(), nullable=True),
        sa.Column("to_assignment_id", sa.Uuid(), nullable=False),
        sa.Column("from_actor_id", sa.Uuid(), nullable=True),
        sa.Column("to_actor_id", sa.Uuid(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("is_override", sa.Boolean(), nullable=False),
        sa.Column("recorded_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "recorded_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["project_id"], ["prj_projects.id"]),
        sa.ForeignKeyConstraint(["ticket_id"], ["tkt_tickets.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_asg_reassign_ticket",
        "asg_reassignment_history",
        ["organization_id", "ticket_id"],
    )
    op.create_index(
        op.f("ix_asg_reassignment_history_organization_id"),
        "asg_reassignment_history",
        ["organization_id"],
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "asg_assignments",
            "asg_assignment_recommendations",
            "asg_allocation_history",
            "asg_acknowledgments",
            "asg_reassignment_history",
        ):
            _rls(table)


def downgrade() -> None:
    bind = op.get_bind()
    tables = (
        "asg_reassignment_history",
        "asg_acknowledgments",
        "asg_allocation_history",
        "asg_assignment_recommendations",
        "asg_assignments",
    )
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
