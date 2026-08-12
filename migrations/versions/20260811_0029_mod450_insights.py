"""MOD-450 insights dashboard, search, health, activity, reports, exports.

Revision ID: 20260811_0029
Revises: 20260811_0028
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0029"
down_revision: str | None = "20260811_0028"
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


def _ts():
    return sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        nullable=False,
    )


def _updated():
    return sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        nullable=False,
    )


def upgrade() -> None:
    op.create_table(
        "rp_dashboard_snapshots",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("scope_key", sa.String(length=96), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("metric_json", sa.Text(), nullable=False),
        sa.Column("source_hash", sa.String(length=128), nullable=True),
        sa.Column("computed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("refreshed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        _updated(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "scope_key",
            name="uq_rp_dashboard_snapshots_org_scope",
        ),
    )
    op.create_index(
        "ix_rp_dashboard_snapshots_org", "rp_dashboard_snapshots", ["organization_id"]
    )
    op.create_index(
        op.f("ix_rp_dashboard_snapshots_organization_id"),
        "rp_dashboard_snapshots",
        ["organization_id"],
    )

    op.create_table(
        "rp_project_health",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("health_status", sa.String(length=32), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("blockers_count", sa.Integer(), nullable=False),
        sa.Column("open_tickets", sa.Integer(), nullable=False),
        sa.Column("open_bugs", sa.Integer(), nullable=False),
        sa.Column("overdue_followups", sa.Integer(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("computed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        _updated(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "project_id",
            name="uq_rp_project_health_org_project",
        ),
    )
    op.create_index(
        op.f("ix_rp_project_health_organization_id"),
        "rp_project_health",
        ["organization_id"],
    )

    op.create_table(
        "rp_saved_filters",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("module_key", sa.String(length=64), nullable=False),
        sa.Column("filter_json", sa.Text(), nullable=False),
        sa.Column("is_shared", sa.Boolean(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        _ts(),
        _updated(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "owner_actor_id",
            "name",
            name="uq_rp_saved_filters_org_owner_name",
        ),
    )
    op.create_index(
        op.f("ix_rp_saved_filters_organization_id"),
        "rp_saved_filters",
        ["organization_id"],
    )

    op.create_table(
        "rp_search_documents",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("body_preview", sa.Text(), nullable=False),
        sa.Column("classification", sa.String(length=32), nullable=False),
        sa.Column("indexed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "entity_type",
            "entity_id",
            name="uq_rp_search_documents_org_entity",
        ),
    )
    op.create_index(
        "ix_rp_search_documents_org_type",
        "rp_search_documents",
        ["organization_id", "entity_type"],
    )
    op.create_index(
        op.f("ix_rp_search_documents_organization_id"),
        "rp_search_documents",
        ["organization_id"],
    )

    op.create_table(
        "rp_activity_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.Uuid(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_rp_activity_events_org_occurred",
        "rp_activity_events",
        ["organization_id", "occurred_at"],
    )
    op.create_index(
        op.f("ix_rp_activity_events_organization_id"),
        "rp_activity_events",
        ["organization_id"],
    )

    op.create_table(
        "rp_reports",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("report_type", sa.String(length=64), nullable=False),
        sa.Column("definition_json", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        _updated(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_rp_reports_org_code"),
    )
    op.create_index(
        op.f("ix_rp_reports_organization_id"), "rp_reports", ["organization_id"]
    )

    op.create_table(
        "rp_exports",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("report_id", sa.Uuid(), nullable=True),
        sa.Column("export_format", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("payload_preview", sa.Text(), nullable=True),
        sa.Column("row_count", sa.Integer(), nullable=False),
        sa.Column("requested_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        _ts(),
        _updated(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_rp_exports_org_status", "rp_exports", ["organization_id", "status"]
    )
    op.create_index(
        op.f("ix_rp_exports_organization_id"), "rp_exports", ["organization_id"]
    )

    for table in (
        "rp_dashboard_snapshots",
        "rp_project_health",
        "rp_saved_filters",
        "rp_search_documents",
        "rp_activity_events",
        "rp_reports",
        "rp_exports",
    ):
        _rls(table)


def downgrade() -> None:
    for table in (
        "rp_exports",
        "rp_reports",
        "rp_activity_events",
        "rp_search_documents",
        "rp_saved_filters",
        "rp_project_health",
        "rp_dashboard_snapshots",
    ):
        op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
        op.drop_table(table)
