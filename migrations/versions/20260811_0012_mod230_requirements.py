"""MOD-230 questionnaires, answers, clarifications, briefs, completeness.

Revision ID: 20260811_0012
Revises: 20260811_0011
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0012"
down_revision: str | None = "20260811_0011"
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
        "req_questionnaires",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "code", name="uq_req_questionnaires_code"),
    )
    op.create_index(
        op.f("ix_req_questionnaires_organization_id"),
        "req_questionnaires",
        ["organization_id"],
    )

    op.create_table(
        "req_questionnaire_versions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("questionnaire_id", sa.Uuid(), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("questions_json", sa.JSON(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["questionnaire_id"], ["req_questionnaires.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "questionnaire_id", "version_number", name="uq_req_questionnaire_versions"
        ),
    )
    op.create_index(
        op.f("ix_req_questionnaire_versions_organization_id"),
        "req_questionnaire_versions",
        ["organization_id"],
    )

    op.create_table(
        "req_answers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("questionnaire_version_id", sa.Uuid(), nullable=False),
        sa.Column("related_entity_type", sa.String(length=64), nullable=False),
        sa.Column("related_entity_id", sa.Uuid(), nullable=False),
        sa.Column("client_id", sa.Uuid(), nullable=True),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("question_key", sa.String(length=128), nullable=False),
        sa.Column("answer_text", sa.Text(), nullable=True),
        sa.Column("explicitly_unavailable", sa.Boolean(), nullable=False),
        sa.Column("answered_by_actor_id", sa.Uuid(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["questionnaire_version_id"], ["req_questionnaire_versions.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "questionnaire_version_id",
            "related_entity_type",
            "related_entity_id",
            "question_key",
            name="uq_req_answers_entity_question",
        ),
    )
    op.create_index(
        "ix_req_answers_entity",
        "req_answers",
        ["organization_id", "related_entity_type", "related_entity_id"],
    )
    op.create_index(op.f("ix_req_answers_organization_id"), "req_answers", ["organization_id"])

    op.create_table(
        "req_clarification_requests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("questionnaire_version_id", sa.Uuid(), nullable=False),
        sa.Column("related_entity_type", sa.String(length=64), nullable=False),
        sa.Column("related_entity_id", sa.Uuid(), nullable=False),
        sa.Column("question_key", sa.String(length=128), nullable=False),
        sa.Column("question_text", sa.String(length=512), nullable=False),
        sa.Column("owner_actor_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("response_text", sa.Text(), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["questionnaire_version_id"], ["req_questionnaire_versions.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_req_clarifications_entity",
        "req_clarification_requests",
        ["organization_id", "related_entity_type", "related_entity_id"],
    )
    op.create_index(
        op.f("ix_req_clarification_requests_organization_id"),
        "req_clarification_requests",
        ["organization_id"],
    )

    op.create_table(
        "req_completeness_scores",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("questionnaire_version_id", sa.Uuid(), nullable=False),
        sa.Column("related_entity_type", sa.String(length=64), nullable=False),
        sa.Column("related_entity_id", sa.Uuid(), nullable=False),
        sa.Column("mandatory_total", sa.Integer(), nullable=False),
        sa.Column("covered_count", sa.Integer(), nullable=False),
        sa.Column("percentage", sa.Numeric(5, 4), nullable=False),
        sa.Column("meets_threshold", sa.Boolean(), nullable=False),
        sa.Column("gap_question_keys", sa.JSON(), nullable=False),
        sa.Column("computed_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column(
            "computed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["questionnaire_version_id"], ["req_questionnaire_versions.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_req_completeness_entity",
        "req_completeness_scores",
        ["organization_id", "related_entity_type", "related_entity_id"],
    )
    op.create_index(
        op.f("ix_req_completeness_scores_organization_id"),
        "req_completeness_scores",
        ["organization_id"],
    )

    op.create_table(
        "req_requirement_briefs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("related_entity_type", sa.String(length=64), nullable=False),
        sa.Column("related_entity_id", sa.Uuid(), nullable=False),
        sa.Column("client_id", sa.Uuid(), nullable=True),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("questionnaire_version_id", sa.Uuid(), nullable=True),
        sa.Column("completeness_score_id", sa.Uuid(), nullable=True),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("approved_by_actor_id", sa.Uuid(), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["completeness_score_id"], ["req_completeness_scores.id"]
        ),
        sa.ForeignKeyConstraint(
            ["questionnaire_version_id"], ["req_questionnaire_versions.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "related_entity_type",
            "related_entity_id",
            "version_number",
            name="uq_req_briefs_entity_version",
        ),
    )
    op.create_index(
        "ix_req_briefs_entity",
        "req_requirement_briefs",
        ["organization_id", "related_entity_type", "related_entity_id"],
    )
    op.create_index(
        op.f("ix_req_requirement_briefs_organization_id"),
        "req_requirement_briefs",
        ["organization_id"],
    )

    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in (
            "req_questionnaires",
            "req_questionnaire_versions",
            "req_answers",
            "req_clarification_requests",
            "req_completeness_scores",
            "req_requirement_briefs",
        ):
            _rls(table)


def downgrade() -> None:
    tables = (
        "req_requirement_briefs",
        "req_completeness_scores",
        "req_clarification_requests",
        "req_answers",
        "req_questionnaire_versions",
        "req_questionnaires",
    )
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        for table in tables:
            op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
            op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
    for table in tables:
        op.drop_table(table)
