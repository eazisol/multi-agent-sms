"""Tenant RLS session binding helpers (MOD-120)."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session


def apply_tenant_rls(session: Session, organization_id: UUID) -> None:
    """Bind PostgreSQL RLS GUC for the current transaction.

    SQLite and other dialects no-op (RLS policies are Postgres-only in migrations).
    """
    bind = session.get_bind()
    if bind is None or bind.dialect.name != "postgresql":
        return
    session.execute(
        text("SELECT set_config('app.current_organization_id', :oid, true)"),
        {"oid": str(organization_id)},
    )
