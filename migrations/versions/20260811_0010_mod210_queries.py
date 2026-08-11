"""MOD-210 client queries, opportunities, qualification, SLA.

Revision ID: 20260811_0010
Revises: 20260811_0009
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0010"
down_revision: str | None = "20260811_0009"
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
        "crm_query_sources",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("channel", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_crm_query_sources_code"),
    )
    op.create_index(op.f("ix_crm_query_sources_organization_id"), "crm_query_sources", ["organization_id"])

    op.create_table(
        "crm_queries",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("client_id", sa.Uuid(), nullable=True),
        sa.Column("contact_id", sa.Uuid(), nullable=True),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("source_id", sa.Uuid(), nullable=True),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("original_message", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("classification", sa.String(length=64), nullable=True),
        sa.Column("rejection_reason", sa.Text(), nullable=True),
        sa.Column("sla_due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("first_responded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sla_status", sa.String(length=32), nullable=False),
        sa.Column("opportunity_id", sa.Uuid(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["source_id"], ["crm_query_sources.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_crm_queries_status", "crm_queries", ["organization_id", "status"])
    op.create_index("ix_crm_queries_client", "crm_queries", ["organization_id", "client_id"])
    op.create_index(op.f("ix_crm_queries_organization_id"), "crm_queries", ["organization_id"])

    op.create_table(
        "crm_opportunities",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("query_id", sa.Uuid(), nullable=False),
        sa.Column("client_id", sa.Uuid(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("estimated_value", sa.Numeric(14, 2), nullable=True),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("conversion_notes", sa.Text(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["query_id"], ["crm_queries.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_crm_opportunities_query", "crm_opportunities", ["organization_id", "query_id"])
    op.create_index(op.f("ix_crm_opportunities_organization_id"), "crm_opportunities", ["organization_id"])

    op.create_table(
        "crm_qualification_answers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("query_id", sa.Uuid(), nullable=False),
        sa.Column("question_key", sa.String(length=128), nullable=False),
        sa.Column("question_text", sa.String(length=512), nullable=False),
        sa.Column("answer_text", sa.Text(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=True),
        sa.Column("answered_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["query_id"], ["crm_queries.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("query_id", "question_key", name="uq_crm_qualification_query_question"),
    )
    op.create_index(
        op.f("ix_crm_qualification_answers_organization_id"),
        "crm_qualification_answers",
        ["organization_id"],
    )

    op.create_table(
        "crm_query_status_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("query_id", sa.Uuid(), nullable=False),
        sa.Column("previous_status", sa.String(length=32), nullable=False),
        sa.Column("next_status", sa.String(length=32), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("rule_code", sa.String(length=64), nullable=True),
        sa.Column("evidence", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["query_id"], ["crm_queries.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_crm_query_history_query",
        "crm_query_status_history",
        ["organization_id", "query_id"],
    )
    op.create_index(
        op.f("ix_crm_query_status_history_organization_id"),
        "crm_query_status_history",
        ["organization_id"],
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "crm_query_sources",
            "crm_queries",
            "crm_opportunities",
            "crm_qualification_answers",
            "crm_query_status_history",
        ):
            _rls(table)


def downgrade() -> None:
    tables = (
        "crm_query_status_history",
        "crm_qualification_answers",
        "crm_opportunities",
        "crm_queries",
        "crm_query_sources",
    )
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
