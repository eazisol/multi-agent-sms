"""Add Auth0 subject link for human identities.

Revision ID: 20260817_0038
Revises: 20260811_0037
Create Date: 2026-08-17
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260817_0038"
down_revision: str | None = "20260811_0037"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "org_human_users",
        sa.Column("idp_subject", sa.String(length=255), nullable=True),
    )
    op.create_unique_constraint(
        "uq_org_human_users_idp_subject",
        "org_human_users",
        ["idp_subject"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_org_human_users_idp_subject",
        "org_human_users",
        type_="unique",
    )
    op.drop_column("org_human_users", "idp_subject")
