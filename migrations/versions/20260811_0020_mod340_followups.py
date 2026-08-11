"""MOD-340 follow-ups, reminders, escalations, SLA pauses.

Revision ID: 20260811_0020
Revises: 20260811_0019
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0020"
down_revision: str | None = "20260811_0019"
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
        "flu_followups",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("direction", sa.String(length=32), nullable=False),
        sa.Column("source_entity_type", sa.String(length=64), nullable=False),
        sa.Column("source_entity_id", sa.Uuid(), nullable=False),
        sa.Column("source_actor_id", sa.Uuid(), nullable=False),
        sa.Column("recipient_actor_id", sa.Uuid(), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("required_response", sa.String(length=255), nullable=False),
        sa.Column("closure_condition", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("rule_version_id", sa.Uuid(), nullable=True),
        sa.Column("reminder_rule_code", sa.String(length=64), nullable=True),
        sa.Column("escalation_rule_code", sa.String(length=64), nullable=True),
        sa.Column("reminder_offset_hours", sa.Integer(), nullable=False),
        sa.Column("escalation_after_hours", sa.Integer(), nullable=False),
        sa.Column("escalate_to_role_code", sa.String(length=64), nullable=True),
        sa.Column("parent_followup_id", sa.Uuid(), nullable=True),
        sa.Column("return_to_followup_id", sa.Uuid(), nullable=True),
        sa.Column("sla_paused", sa.Boolean(), nullable=False),
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
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_flu_followups_status", "flu_followups", ["organization_id", "status"])
    op.create_index("ix_flu_followups_due", "flu_followups", ["organization_id", "due_at"])
    op.create_index(
        "ix_flu_followups_source",
        "flu_followups",
        ["organization_id", "source_entity_type", "source_entity_id"],
    )
    op.create_index(op.f("ix_flu_followups_organization_id"), "flu_followups", ["organization_id"])

    op.create_table(
        "flu_parent_child_links",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("parent_followup_id", sa.Uuid(), nullable=False),
        sa.Column("child_followup_id", sa.Uuid(), nullable=False),
        sa.Column("link_type", sa.String(length=32), nullable=False),
        sa.Column("mandatory", sa.Boolean(), nullable=False),
        sa.Column("return_route", sa.String(length=64), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("parent_followup_id", "child_followup_id", name="uq_flu_parent_child"),
    )
    op.create_index(
        "ix_flu_links_parent",
        "flu_parent_child_links",
        ["organization_id", "parent_followup_id"],
    )
    op.create_index(
        op.f("ix_flu_parent_child_links_organization_id"),
        "flu_parent_child_links",
        ["organization_id"],
    )

    op.create_table(
        "flu_reminders",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("followup_id", sa.Uuid(), nullable=False),
        sa.Column("scheduled_for", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("channel", sa.String(length=32), nullable=False),
        sa.Column("triggered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_flu_reminders_followup", "flu_reminders", ["organization_id", "followup_id"]
    )
    op.create_index(op.f("ix_flu_reminders_organization_id"), "flu_reminders", ["organization_id"])

    op.create_table(
        "flu_escalations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("followup_id", sa.Uuid(), nullable=False),
        sa.Column("escalate_to_role_code", sa.String(length=64), nullable=False),
        sa.Column("escalate_to_actor_id", sa.Uuid(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column(
            "triggered_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_flu_escalations_followup",
        "flu_escalations",
        ["organization_id", "followup_id"],
    )
    op.create_index(
        op.f("ix_flu_escalations_organization_id"), "flu_escalations", ["organization_id"]
    )

    op.create_table(
        "flu_sla_pauses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("followup_id", sa.Uuid(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("responsible_actor_id", sa.Uuid(), nullable=False),
        sa.Column("next_action", sa.String(length=255), nullable=False),
        sa.Column("review_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column(
            "paused_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("resumed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resumed_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_flu_sla_pauses_followup", "flu_sla_pauses", ["organization_id", "followup_id"]
    )
    op.create_index(
        op.f("ix_flu_sla_pauses_organization_id"), "flu_sla_pauses", ["organization_id"]
    )

    op.create_table(
        "flu_business_deadlines",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("followup_id", sa.Uuid(), nullable=False),
        sa.Column("calendar_code", sa.String(length=64), nullable=False),
        sa.Column("due_offset_hours", sa.Integer(), nullable=False),
        sa.Column("wall_clock_due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("business_due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "computed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("followup_id", name="uq_flu_business_deadlines_followup"),
    )
    op.create_index(
        op.f("ix_flu_business_deadlines_organization_id"),
        "flu_business_deadlines",
        ["organization_id"],
    )

    op.create_table(
        "flu_closure_evidence",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("followup_id", sa.Uuid(), nullable=False),
        sa.Column("evidence_ref", sa.String(length=512), nullable=False),
        sa.Column("evidence_type", sa.String(length=64), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_flu_closure_followup",
        "flu_closure_evidence",
        ["organization_id", "followup_id"],
    )
    op.create_index(
        op.f("ix_flu_closure_evidence_organization_id"),
        "flu_closure_evidence",
        ["organization_id"],
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "flu_followups",
            "flu_parent_child_links",
            "flu_reminders",
            "flu_escalations",
            "flu_sla_pauses",
            "flu_business_deadlines",
            "flu_closure_evidence",
        ):
            _rls(table)


def downgrade() -> None:
    bind = op.get_bind()
    tables = (
        "flu_closure_evidence",
        "flu_business_deadlines",
        "flu_sla_pauses",
        "flu_escalations",
        "flu_reminders",
        "flu_parent_child_links",
        "flu_followups",
    )
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
