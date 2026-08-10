"""MOD-120 RBAC, membership, approval authorities, access reviews.

Revision ID: 20260810_0006
Revises: 20260810_0005
Create Date: 2026-08-10
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260810_0006"
down_revision: str | None = "20260810_0005"
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
        "auth_permissions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=128), nullable=False),
        sa.Column("module_key", sa.String(length=64), nullable=False),
        sa.Column("action_key", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_auth_permissions_org_code"),
    )
    op.create_index("ix_auth_permissions_module", "auth_permissions", ["organization_id", "module_key"])
    op.create_index(op.f("ix_auth_permissions_organization_id"), "auth_permissions", ["organization_id"])

    op.create_table(
        "org_role_permissions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("role_id", sa.Uuid(), nullable=False),
        sa.Column("permission_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["permission_id"], ["auth_permissions.id"]),
        sa.ForeignKeyConstraint(["role_id"], ["org_roles.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("role_id", "permission_id", name="uq_org_role_permissions_pair"),
    )
    op.create_index("ix_org_role_permissions_org", "org_role_permissions", ["organization_id"])
    op.create_index(op.f("ix_org_role_permissions_organization_id"), "org_role_permissions", ["organization_id"])

    op.create_table(
        "org_project_members",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("client_id", sa.Uuid(), nullable=True),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("role_code", sa.String(length=64), nullable=False),
        sa.Column("access_level", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("assigned_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("effective_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "project_id",
            "actor_id",
            name="uq_org_project_members_actor",
        ),
    )
    op.create_index(
        "ix_org_project_members_project",
        "org_project_members",
        ["organization_id", "project_id"],
    )
    op.create_index(op.f("ix_org_project_members_organization_id"), "org_project_members", ["organization_id"])

    op.create_table(
        "org_module_access",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("module_key", sa.String(length=64), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("access_level", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("granted_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_org_module_access_scope",
        "org_module_access",
        ["organization_id", "actor_id", "module_key", "project_id"],
    )
    op.create_index(op.f("ix_org_module_access_organization_id"), "org_module_access", ["organization_id"])

    op.create_table(
        "org_document_access",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("document_ref", sa.String(length=255), nullable=False),
        sa.Column("classification", sa.String(length=32), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=True),
        sa.Column("role_code", sa.String(length=64), nullable=True),
        sa.Column("access_level", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("granted_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_org_document_access_target",
        "org_document_access",
        ["organization_id", "document_ref"],
    )
    op.create_index(op.f("ix_org_document_access_organization_id"), "org_document_access", ["organization_id"])

    op.create_table(
        "org_approval_authorities",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("action_code", sa.String(length=128), nullable=False),
        sa.Column("authority_actor_id", sa.Uuid(), nullable=True),
        sa.Column("authority_role_code", sa.String(length=64), nullable=True),
        sa.Column("client_id", sa.Uuid(), nullable=True),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("environment", sa.String(length=32), nullable=False),
        sa.Column("amount_threshold", sa.Numeric(14, 2), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("effective_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delegated_from_authority_id", sa.Uuid(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_org_approval_authorities_action",
        "org_approval_authorities",
        ["organization_id", "action_code"],
    )
    op.create_index(
        op.f("ix_org_approval_authorities_organization_id"),
        "org_approval_authorities",
        ["organization_id"],
    )

    op.create_table(
        "org_access_reviews",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("findings", sa.JSON(), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_org_access_reviews_status", "org_access_reviews", ["organization_id", "status"])
    op.create_index(op.f("ix_org_access_reviews_organization_id"), "org_access_reviews", ["organization_id"])

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "auth_permissions",
            "org_role_permissions",
            "org_project_members",
            "org_module_access",
            "org_document_access",
            "org_approval_authorities",
            "org_access_reviews",
        ):
            _rls(table)


def downgrade() -> None:
    tables = (
        "org_access_reviews",
        "org_approval_authorities",
        "org_document_access",
        "org_module_access",
        "org_project_members",
        "org_role_permissions",
        "auth_permissions",
    )
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
