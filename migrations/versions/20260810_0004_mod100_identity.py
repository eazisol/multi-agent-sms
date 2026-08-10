"""MOD-100 identity and organization tables.

Revision ID: 20260810_0004
Revises: 20260810_0003
Create Date: 2026-08-10
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260810_0004"
down_revision: str | None = "20260810_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _rls(table: str, *, id_column: str = "organization_id") -> None:
    op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
    op.execute(
        f"""
        CREATE POLICY {table}_org_isolation ON {table}
        USING ({id_column}::text = current_setting('app.current_organization_id', true))
        WITH CHECK ({id_column}::text = current_setting('app.current_organization_id', true))
        """
    )


def upgrade() -> None:
    op.create_table(
        "org_organizations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug", name="uq_org_organizations_slug"),
    )

    op.create_table(
        "org_actors",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("actor_kind", sa.String(length=32), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["organization_id"], ["org_organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id", "display_name", "actor_kind", name="uq_org_actors_org_name_kind"
        ),
    )
    op.create_index("ix_org_actors_org_kind", "org_actors", ["organization_id", "actor_kind"])
    op.create_index(op.f("ix_org_actors_organization_id"), "org_actors", ["organization_id"])

    op.create_table(
        "org_human_users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("primary_role_code", sa.String(length=64), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["actor_id"], ["org_actors.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["org_organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("actor_id", name="uq_org_human_users_actor"),
        sa.UniqueConstraint("organization_id", "email", name="uq_org_human_users_org_email"),
    )
    op.create_index(op.f("ix_org_human_users_organization_id"), "org_human_users", ["organization_id"])

    op.create_table(
        "org_agents",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("agent_key", sa.String(length=64), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("supervisor_human_user_id", sa.Uuid(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["actor_id"], ["org_actors.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["org_organizations.id"]),
        sa.ForeignKeyConstraint(["supervisor_human_user_id"], ["org_human_users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("actor_id", name="uq_org_agents_actor"),
        sa.UniqueConstraint("organization_id", "agent_key", name="uq_org_agents_org_key"),
    )
    op.create_index("ix_org_agents_supervisor", "org_agents", ["organization_id", "supervisor_human_user_id"])
    op.create_index(op.f("ix_org_agents_organization_id"), "org_agents", ["organization_id"])

    op.create_table(
        "org_roles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["organization_id"], ["org_organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_org_roles_org_code"),
    )
    op.create_index(op.f("ix_org_roles_organization_id"), "org_roles", ["organization_id"])

    op.create_table(
        "org_departments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["organization_id"], ["org_organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_org_departments_org_code"),
    )
    op.create_index(op.f("ix_org_departments_organization_id"), "org_departments", ["organization_id"])

    op.create_table(
        "org_teams",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("department_id", sa.Uuid(), nullable=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["department_id"], ["org_departments.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["org_organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_org_teams_org_code"),
    )
    op.create_index(op.f("ix_org_teams_organization_id"), "org_teams", ["organization_id"])

    op.create_table(
        "org_team_members",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("team_id", sa.Uuid(), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("membership_role", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["actor_id"], ["org_actors.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["org_organizations.id"]),
        sa.ForeignKeyConstraint(["team_id"], ["org_teams.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("team_id", "actor_id", name="uq_org_team_members_team_actor"),
    )
    op.create_index(op.f("ix_org_team_members_organization_id"), "org_team_members", ["organization_id"])

    op.create_table(
        "org_reporting_lines",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("subordinate_actor_id", sa.Uuid(), nullable=False),
        sa.Column("manager_actor_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("effective_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["manager_actor_id"], ["org_actors.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["org_organizations.id"]),
        sa.ForeignKeyConstraint(["subordinate_actor_id"], ["org_actors.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "subordinate_actor_id",
            "manager_actor_id",
            "effective_from",
            name="uq_org_reporting_lines_edge",
        ),
    )
    op.create_index(
        "ix_org_reporting_lines_subordinate",
        "org_reporting_lines",
        ["organization_id", "subordinate_actor_id"],
    )
    op.create_index(op.f("ix_org_reporting_lines_organization_id"), "org_reporting_lines", ["organization_id"])

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        _rls("org_organizations", id_column="id")
        for table in (
            "org_actors",
            "org_human_users",
            "org_agents",
            "org_roles",
            "org_departments",
            "org_teams",
            "org_team_members",
            "org_reporting_lines",
        ):
            _rls(table)


def downgrade() -> None:
    tables = (
        "org_reporting_lines",
        "org_team_members",
        "org_teams",
        "org_departments",
        "org_roles",
        "org_agents",
        "org_human_users",
        "org_actors",
        "org_organizations",
    )
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
