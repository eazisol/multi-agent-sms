"""MOD-410 bug lifecycle (bugs, links, assignments, fixes, retests, known issues, SLA).

Revision ID: 20260811_0025
Revises: 20260811_0024
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0025"
down_revision: str | None = "20260811_0024"
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
        "bg_bugs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("severity", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("blocks_release", sa.Boolean(), nullable=False),
        sa.Column("rejection_reason", sa.Text(), nullable=True),
        sa.Column("rejection_evidence", sa.Text(), nullable=True),
        sa.Column("reopen_reason", sa.Text(), nullable=True),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("assignee_actor_id", sa.Uuid(), nullable=True),
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
        sa.UniqueConstraint("organization_id", "code", name="uq_bg_bugs_org_code"),
    )
    op.create_index("ix_bg_bugs_status", "bg_bugs", ["organization_id", "status"])
    op.create_index("ix_bg_bugs_project", "bg_bugs", ["organization_id", "project_id"])
    op.create_index("ix_bg_bugs_severity", "bg_bugs", ["organization_id", "severity"])
    op.create_index(op.f("ix_bg_bugs_organization_id"), "bg_bugs", ["organization_id"])

    op.create_table(
        "bg_links",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("bug_id", sa.Uuid(), nullable=False),
        sa.Column("link_type", sa.String(length=32), nullable=False),
        sa.Column("linked_entity_id", sa.Uuid(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
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
            "bug_id",
            "link_type",
            "linked_entity_id",
            name="uq_bg_links_bug_type_entity",
        ),
    )
    op.create_index("ix_bg_links_bug", "bg_links", ["organization_id", "bug_id"])
    op.create_index(op.f("ix_bg_links_organization_id"), "bg_links", ["organization_id"])

    op.create_table(
        "bg_assignments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("bug_id", sa.Uuid(), nullable=False),
        sa.Column("assignee_actor_id", sa.Uuid(), nullable=False),
        sa.Column("assigned_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column(
            "effective_from",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("effective_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_bg_assignments_bug", "bg_assignments", ["organization_id", "bug_id"])
    op.create_index(
        op.f("ix_bg_assignments_organization_id"), "bg_assignments", ["organization_id"]
    )

    op.create_table(
        "bg_fix_submissions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("bug_id", sa.Uuid(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("build_ref", sa.String(length=128), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("submitted_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_bg_fixes_bug", "bg_fix_submissions", ["organization_id", "bug_id"])
    op.create_index(
        op.f("ix_bg_fix_submissions_organization_id"),
        "bg_fix_submissions",
        ["organization_id"],
    )

    op.create_table(
        "bg_retests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("bug_id", sa.Uuid(), nullable=False),
        sa.Column("fix_submission_id", sa.Uuid(), nullable=True),
        sa.Column("result", sa.String(length=16), nullable=False),
        sa.Column("evidence_text", sa.Text(), nullable=True),
        sa.Column("environment_code", sa.String(length=64), nullable=False),
        sa.Column("build_ref", sa.String(length=128), nullable=True),
        sa.Column("tested_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_bg_retests_bug", "bg_retests", ["organization_id", "bug_id"])
    op.create_index(op.f("ix_bg_retests_organization_id"), "bg_retests", ["organization_id"])

    op.create_table(
        "bg_known_issue_approvals",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("bug_id", sa.Uuid(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("release_ref", sa.String(length=128), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("approved_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_bg_known_issue_bug", "bg_known_issue_approvals", ["organization_id", "bug_id"]
    )
    op.create_index(
        op.f("ix_bg_known_issue_approvals_organization_id"),
        "bg_known_issue_approvals",
        ["organization_id"],
    )

    op.create_table(
        "bg_severity_slas",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False),
        sa.Column("response_hours", sa.Integer(), nullable=False),
        sa.Column("resolve_hours", sa.Integer(), nullable=False),
        sa.Column("blocks_release", sa.Boolean(), nullable=False),
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
        sa.UniqueConstraint("organization_id", "severity", name="uq_bg_severity_slas_org_sev"),
    )
    op.create_index(
        op.f("ix_bg_severity_slas_organization_id"), "bg_severity_slas", ["organization_id"]
    )

    for table in (
        "bg_bugs",
        "bg_links",
        "bg_assignments",
        "bg_fix_submissions",
        "bg_retests",
        "bg_known_issue_approvals",
        "bg_severity_slas",
    ):
        _rls(table)


def downgrade() -> None:
    for table in (
        "bg_severity_slas",
        "bg_known_issue_approvals",
        "bg_retests",
        "bg_fix_submissions",
        "bg_assignments",
        "bg_links",
        "bg_bugs",
    ):
        op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
        op.drop_table(table)
