"""MOD-460 requirement traceability, audit reports, and evidence exports.

Revision ID: 20260811_0030
Revises: 20260811_0029
Create Date: 2026-08-11
"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260811_0030"
down_revision: str | None = "20260811_0029"
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
        "tr_requirement_ticket_links",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_id", sa.Uuid(), nullable=False),
        sa.Column("ticket_id", sa.Uuid(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "requirement_id",
            "ticket_id",
            name="uq_tr_req_ticket_links_org_req_ticket",
        ),
    )
    op.create_index(
        "ix_tr_req_ticket_links_org_req",
        "tr_requirement_ticket_links",
        ["organization_id", "requirement_id"],
    )
    op.create_index(
        op.f("ix_tr_requirement_ticket_links_organization_id"),
        "tr_requirement_ticket_links",
        ["organization_id"],
    )

    op.create_table(
        "tr_requirement_test_links",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_id", sa.Uuid(), nullable=False),
        sa.Column("test_case_id", sa.Uuid(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "requirement_id",
            "test_case_id",
            name="uq_tr_req_test_links_org_req_test",
        ),
    )
    op.create_index(
        "ix_tr_req_test_links_org_req",
        "tr_requirement_test_links",
        ["organization_id", "requirement_id"],
    )
    op.create_index(
        op.f("ix_tr_requirement_test_links_organization_id"),
        "tr_requirement_test_links",
        ["organization_id"],
    )

    op.create_table(
        "tr_requirement_release_links",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_id", sa.Uuid(), nullable=False),
        sa.Column("release_id", sa.Uuid(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "requirement_id",
            "release_id",
            name="uq_tr_req_release_links_org_req_release",
        ),
    )
    op.create_index(
        "ix_tr_req_release_links_org_req",
        "tr_requirement_release_links",
        ["organization_id", "requirement_id"],
    )
    op.create_index(
        op.f("ix_tr_requirement_release_links_organization_id"),
        "tr_requirement_release_links",
        ["organization_id"],
    )

    op.create_table(
        "tr_requirement_document_links",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_id", sa.Uuid(), nullable=False),
        sa.Column("document_id", sa.Uuid(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "requirement_id",
            "document_id",
            name="uq_tr_req_document_links_org_req_doc",
        ),
    )
    op.create_index(
        "ix_tr_req_document_links_org_req",
        "tr_requirement_document_links",
        ["organization_id", "requirement_id"],
    )
    op.create_index(
        op.f("ix_tr_requirement_document_links_organization_id"),
        "tr_requirement_document_links",
        ["organization_id"],
    )

    op.create_table(
        "tr_ticket_test_links",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("ticket_id", sa.Uuid(), nullable=False),
        sa.Column("test_case_id", sa.Uuid(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "ticket_id",
            "test_case_id",
            name="uq_tr_ticket_test_links_org_ticket_test",
        ),
    )
    op.create_index(
        "ix_tr_ticket_test_links_org_ticket",
        "tr_ticket_test_links",
        ["organization_id", "ticket_id"],
    )
    op.create_index(
        op.f("ix_tr_ticket_test_links_organization_id"),
        "tr_ticket_test_links",
        ["organization_id"],
    )

    op.create_table(
        "tr_evidence_manifests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("item_count", sa.Integer(), nullable=False),
        sa.Column("checksum", sa.String(length=128), nullable=True),
        sa.Column("sealed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("updated_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        _updated(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "code",
            name="uq_tr_evidence_manifests_org_code",
        ),
    )
    op.create_index(
        "ix_tr_evidence_manifests_org_status",
        "tr_evidence_manifests",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_tr_evidence_manifests_organization_id"),
        "tr_evidence_manifests",
        ["organization_id"],
    )

    # Supporting tables for AC (not checklist MPs)
    op.create_table(
        "tr_must_have_requirements",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("requirement_id", sa.Uuid(), nullable=False),
        sa.Column("requirement_code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("created_by_actor_id", sa.Uuid(), nullable=False),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "requirement_id",
            name="uq_tr_must_have_requirements_org_req",
        ),
    )
    op.create_index(
        "ix_tr_must_have_requirements_org_project",
        "tr_must_have_requirements",
        ["organization_id", "project_id"],
    )
    op.create_index(
        op.f("ix_tr_must_have_requirements_organization_id"),
        "tr_must_have_requirements",
        ["organization_id"],
    )

    op.create_table(
        "tr_evidence_manifest_items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("manifest_id", sa.Uuid(), nullable=False),
        sa.Column("item_type", sa.String(length=32), nullable=False),
        sa.Column("item_id", sa.Uuid(), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=True),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "organization_id",
            "manifest_id",
            "item_type",
            "item_id",
            name="uq_tr_evidence_manifest_items_org_manifest_item",
        ),
    )
    op.create_index(
        "ix_tr_evidence_manifest_items_manifest",
        "tr_evidence_manifest_items",
        ["organization_id", "manifest_id"],
    )
    op.create_index(
        op.f("ix_tr_evidence_manifest_items_organization_id"),
        "tr_evidence_manifest_items",
        ["organization_id"],
    )

    op.create_table(
        "tr_evidence_exports",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("manifest_id", sa.Uuid(), nullable=False),
        sa.Column("export_format", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("payload_preview", sa.Text(), nullable=True),
        sa.Column("reconciliation_hash", sa.String(length=128), nullable=True),
        sa.Column("requested_by_actor_id", sa.Uuid(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_tr_evidence_exports_org_status",
        "tr_evidence_exports",
        ["organization_id", "status"],
    )
    op.create_index(
        op.f("ix_tr_evidence_exports_organization_id"),
        "tr_evidence_exports",
        ["organization_id"],
    )

    op.create_table(
        "tr_action_audits",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("action", sa.String(length=96), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.Uuid(), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("correlation_id", sa.String(length=128), nullable=True),
        sa.Column("payload_json", sa.Text(), nullable=True),
        _ts(),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_tr_action_audits_org_action",
        "tr_action_audits",
        ["organization_id", "action"],
    )
    op.create_index(
        op.f("ix_tr_action_audits_organization_id"),
        "tr_action_audits",
        ["organization_id"],
    )

    for table in (
        "tr_requirement_ticket_links",
        "tr_requirement_test_links",
        "tr_requirement_release_links",
        "tr_requirement_document_links",
        "tr_ticket_test_links",
        "tr_evidence_manifests",
        "tr_must_have_requirements",
        "tr_evidence_manifest_items",
        "tr_evidence_exports",
        "tr_action_audits",
    ):
        _rls(table)


def downgrade() -> None:
    for table in (
        "tr_action_audits",
        "tr_evidence_exports",
        "tr_evidence_manifest_items",
        "tr_must_have_requirements",
        "tr_evidence_manifests",
        "tr_ticket_test_links",
        "tr_requirement_document_links",
        "tr_requirement_release_links",
        "tr_requirement_test_links",
        "tr_requirement_ticket_links",
    ):
        op.execute(f"DROP POLICY IF EXISTS {table}_org_isolation ON {table}")
        op.drop_table(table)
