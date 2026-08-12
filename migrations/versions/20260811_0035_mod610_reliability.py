"""MOD-610 reliability, SLO, replay, and DR tables.

Revision ID: 20260811_0035
Revises: 20260811_0034
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0035"
down_revision: str | None = "20260811_0034"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABLES = (
    "rlb_performance_tests",
    "rlb_resilience_tests",
    "rlb_index_reviews",
    "rlb_slo_dashboards",
    "rlb_workflow_replays",
    "rlb_integration_failure_tests",
    "rlb_dr_runbooks",
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
        "rlb_performance_tests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("suite_name", sa.String(length=255), nullable=False),
        sa.Column("p95_ms", sa.Integer(), nullable=False),
        sa.Column("sample_count", sa.Integer(), nullable=False),
        sa.Column("samples_json", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id", "code", name="uq_rlb_performance_tests_org_code"
        ),
    )
    op.create_index(
        "ix_rlb_performance_tests_org_created",
        "rlb_performance_tests",
        ["organization_id", "created_at"],
    )
    op.create_index(
        op.f("ix_rlb_performance_tests_organization_id"),
        "rlb_performance_tests",
        ["organization_id"],
    )

    op.create_table(
        "rlb_resilience_tests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("scenario", sa.String(length=255), nullable=False),
        sa.Column("result", sa.String(length=32), nullable=False),
        sa.Column("evidence", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id", "code", name="uq_rlb_resilience_tests_org_code"
        ),
    )
    op.create_index(
        "ix_rlb_resilience_tests_org_created",
        "rlb_resilience_tests",
        ["organization_id", "created_at"],
    )
    op.create_index(
        op.f("ix_rlb_resilience_tests_organization_id"),
        "rlb_resilience_tests",
        ["organization_id"],
    )

    op.create_table(
        "rlb_index_reviews",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("table_name", sa.String(length=128), nullable=False),
        sa.Column("index_name", sa.String(length=128), nullable=False),
        sa.Column("recommendation", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_rlb_index_reviews_org_status",
        "rlb_index_reviews",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_rlb_index_reviews_organization_id"),
        "rlb_index_reviews",
        ["organization_id"],
    )

    op.create_table(
        "rlb_slo_dashboards",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("dashboard_p95_ms", sa.Integer(), nullable=False),
        sa.Column("api_p95_ms", sa.Integer(), nullable=True),
        sa.Column("samples_json", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        _updated_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id", "name", name="uq_rlb_slo_dashboards_org_name"
        ),
    )
    op.create_index(
        "ix_rlb_slo_dashboards_org_status",
        "rlb_slo_dashboards",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_rlb_slo_dashboards_organization_id"),
        "rlb_slo_dashboards",
        ["organization_id"],
    )

    op.create_table(
        "rlb_workflow_replays",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("workflow_name", sa.String(length=128), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        _updated_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "idempotency_key",
            name="uq_rlb_workflow_replays_org_idempotency",
        ),
    )
    op.create_index(
        "ix_rlb_workflow_replays_org_status",
        "rlb_workflow_replays",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_rlb_workflow_replays_organization_id"),
        "rlb_workflow_replays",
        ["organization_id"],
    )

    op.create_table(
        "rlb_integration_failure_tests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("result", sa.String(length=32), nullable=False),
        sa.Column("failure_mode", sa.String(length=128), nullable=False),
        sa.Column("recovered", sa.Boolean(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "code",
            name="uq_rlb_integration_failure_tests_org_code",
        ),
    )
    op.create_index(
        "ix_rlb_integration_failure_tests_org_created",
        "rlb_integration_failure_tests",
        ["organization_id", "created_at"],
    )
    op.create_index(
        op.f("ix_rlb_integration_failure_tests_organization_id"),
        "rlb_integration_failure_tests",
        ["organization_id"],
    )

    op.create_table(
        "rlb_dr_runbooks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("rto_minutes", sa.Integer(), nullable=False),
        sa.Column("rpo_minutes", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("body_preview", sa.Text(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _created_at(),
        _updated_at(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_rlb_dr_runbooks_org_code"),
    )
    op.create_index(
        "ix_rlb_dr_runbooks_org_status",
        "rlb_dr_runbooks",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_rlb_dr_runbooks_organization_id"),
        "rlb_dr_runbooks",
        ["organization_id"],
    )

    for table in _TABLES:
        _rls(table)


def downgrade() -> None:
    for table in reversed(_TABLES):
        op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
    op.drop_table("rlb_dr_runbooks")
    op.drop_table("rlb_integration_failure_tests")
    op.drop_table("rlb_workflow_replays")
    op.drop_table("rlb_slo_dashboards")
    op.drop_table("rlb_index_reviews")
    op.drop_table("rlb_resilience_tests")
    op.drop_table("rlb_performance_tests")
