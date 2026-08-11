"""MOD-360 agent runtime registry (definitions, prompts, runs, reviews).

Revision ID: 20260811_0022
Revises: 20260811_0021
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0022"
down_revision: str | None = "20260811_0021"
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
        "agr_agent_definitions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("department_code", sa.String(length=64), nullable=False),
        sa.Column("authority_level", sa.String(length=32), nullable=False),
        sa.Column("supervisor_actor_id", sa.Uuid(), nullable=True),
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
        sa.UniqueConstraint("organization_id", "code", name="uq_agr_definitions_org_code"),
    )
    op.create_index(
        op.f("ix_agr_agent_definitions_organization_id"),
        "agr_agent_definitions",
        ["organization_id"],
    )

    op.create_table(
        "agr_prompt_versions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("definition_id", sa.Uuid(), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("prompt_text", sa.Text(), nullable=False),
        sa.Column("model_name", sa.String(length=128), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False),
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
        sa.UniqueConstraint(
            "definition_id", "version_number", name="uq_agr_prompt_definition_number"
        ),
    )
    op.create_index(
        "ix_agr_prompt_definition",
        "agr_prompt_versions",
        ["organization_id", "definition_id"],
    )
    op.create_index(
        op.f("ix_agr_prompt_versions_organization_id"),
        "agr_prompt_versions",
        ["organization_id"],
    )

    op.create_table(
        "agr_tool_policies",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("definition_id", sa.Uuid(), nullable=False),
        sa.Column("policy_key", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("allowed_tools", sa.JSON(), nullable=False),
        sa.Column("denied_tools", sa.JSON(), nullable=False),
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
        sa.UniqueConstraint(
            "definition_id", "policy_key", name="uq_agr_tool_policy_definition_key"
        ),
    )
    op.create_index(
        "ix_agr_tool_policy_definition",
        "agr_tool_policies",
        ["organization_id", "definition_id"],
    )
    op.create_index(
        op.f("ix_agr_tool_policies_organization_id"),
        "agr_tool_policies",
        ["organization_id"],
    )

    op.create_table(
        "agr_context_profiles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("definition_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("min_sources", sa.Integer(), nullable=False),
        sa.Column("max_tokens", sa.Integer(), nullable=False),
        sa.Column("include_rules", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
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
        sa.UniqueConstraint(
            "definition_id", "code", name="uq_agr_context_definition_code"
        ),
    )
    op.create_index(
        "ix_agr_context_definition",
        "agr_context_profiles",
        ["organization_id", "definition_id"],
    )
    op.create_index(
        op.f("ix_agr_context_profiles_organization_id"),
        "agr_context_profiles",
        ["organization_id"],
    )

    op.create_table(
        "agr_agent_runs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("definition_id", sa.Uuid(), nullable=False),
        sa.Column("agent_code", sa.String(length=64), nullable=False),
        sa.Column("prompt_version_id", sa.Uuid(), nullable=False),
        sa.Column("tool_policy_id", sa.Uuid(), nullable=True),
        sa.Column("context_profile_id", sa.Uuid(), nullable=True),
        sa.Column("related_entity_type", sa.String(length=64), nullable=False),
        sa.Column("related_entity_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("langgraph_run_id", sa.String(length=128), nullable=True),
        sa.Column("model_name", sa.String(length=128), nullable=False),
        sa.Column("prompt_version_number", sa.Integer(), nullable=False),
        sa.Column("input_json", sa.JSON(), nullable=False),
        sa.Column("output_json", sa.JSON(), nullable=False),
        sa.Column("sources_json", sa.JSON(), nullable=False),
        sa.Column("tools_used_json", sa.JSON(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("cost_units", sa.Float(), nullable=True),
        sa.Column("review_required", sa.Boolean(), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("correlation_id", sa.Uuid(), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=True),
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
        sa.UniqueConstraint(
            "organization_id",
            "idempotency_key",
            name="uq_agr_runs_org_idempotency",
        ),
    )
    op.create_index(
        "ix_agr_runs_status",
        "agr_agent_runs",
        ["organization_id", "status"],
    )
    op.create_index(
        "ix_agr_runs_definition",
        "agr_agent_runs",
        ["organization_id", "definition_id"],
    )
    op.create_index(
        "ix_agr_runs_related",
        "agr_agent_runs",
        ["organization_id", "related_entity_type", "related_entity_id"],
    )
    op.create_index(
        op.f("ix_agr_agent_runs_organization_id"),
        "agr_agent_runs",
        ["organization_id"],
    )

    op.create_table(
        "agr_agent_reviews",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("run_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("reviewer_actor_id", sa.Uuid(), nullable=False),
        sa.Column("decision_reason", sa.Text(), nullable=True),
        sa.Column("outcome_json", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_agr_reviews_run",
        "agr_agent_reviews",
        ["organization_id", "run_id"],
    )
    op.create_index(
        op.f("ix_agr_agent_reviews_organization_id"),
        "agr_agent_reviews",
        ["organization_id"],
    )

    op.create_table(
        "agr_agent_evaluations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("run_id", sa.Uuid(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("rubric_code", sa.String(length=64), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("evaluator_actor_id", sa.Uuid(), nullable=False),
        sa.Column("metrics_json", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_agr_evaluations_run",
        "agr_agent_evaluations",
        ["organization_id", "run_id"],
    )
    op.create_index(
        op.f("ix_agr_agent_evaluations_organization_id"),
        "agr_agent_evaluations",
        ["organization_id"],
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "agr_agent_definitions",
            "agr_prompt_versions",
            "agr_tool_policies",
            "agr_context_profiles",
            "agr_agent_runs",
            "agr_agent_reviews",
            "agr_agent_evaluations",
        ):
            _rls(table)


def downgrade() -> None:
    bind = op.get_bind()
    tables = (
        "agr_agent_evaluations",
        "agr_agent_reviews",
        "agr_agent_runs",
        "agr_context_profiles",
        "agr_tool_policies",
        "agr_prompt_versions",
        "agr_agent_definitions",
    )
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
