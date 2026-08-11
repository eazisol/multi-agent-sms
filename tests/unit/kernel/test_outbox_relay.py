"""Unit tests for outbox relay stub (closes M1 publisher gap)."""

from __future__ import annotations

from uuid import uuid4

from masms_api.db import Base
from masms_api.kernel.outbox import OutboxMessage, enqueue_outbox, relay_pending_outbox
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


def _session() -> Session:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)()


def test_relay_marks_pending_published_idempotently() -> None:
    db = _session()
    org = uuid4()
    corr = uuid4()
    enqueue_outbox(
        db,
        organization_id=org,
        aggregate_type="demo",
        aggregate_id=uuid4(),
        event_type="demo.created",
        payload={"ok": True},
        correlation_id=corr,
    )
    enqueue_outbox(
        db,
        organization_id=org,
        aggregate_type="demo",
        aggregate_id=uuid4(),
        event_type="demo.updated",
        payload={"ok": True},
        correlation_id=corr,
    )
    db.commit()

    first = relay_pending_outbox(db, organization_id=org, limit=10)
    db.commit()
    assert len(first) == 2
    assert all(r.status == "published" for r in first)
    assert all(r.published_at is not None for r in first)
    assert all(r.attempt_count == 1 for r in first)

    second = relay_pending_outbox(db, organization_id=org, limit=10)
    db.commit()
    assert second == []

    rows = list(db.scalars(select(OutboxMessage).where(OutboxMessage.organization_id == org)))
    assert len(rows) == 2
    assert all(r.status == "published" for r in rows)
