"""Unit tests for remaining MOD-020 kernel M1 pieces."""

from __future__ import annotations

from uuid import uuid4

import pytest
from masms_api.db import Base
from masms_api.kernel.concurrency import assert_expected_version
from masms_api.kernel.errors import ConflictError, ValidationAppError
from masms_api.kernel.outbox import OutboxMessage, enqueue_outbox
from masms_api.kernel.pagination import build_page_meta, normalize_paging
from masms_api.kernel.problem import PROBLEM_JSON_MEDIA_TYPE, problem_body
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


class _Row:
    version = 3


def test_normalize_paging_bounds() -> None:
    assert normalize_paging(20, 0) == (20, 0)
    with pytest.raises(ValidationAppError):
        normalize_paging(0, 0)
    with pytest.raises(ValidationAppError):
        normalize_paging(20, -1)


def test_build_page_meta_has_more() -> None:
    meta = build_page_meta(limit=10, offset=0, total=25)
    assert meta.has_more is True
    assert meta.total == 25


def test_assert_expected_version() -> None:
    assert_expected_version(_Row(), 3)
    with pytest.raises(ConflictError):
        assert_expected_version(_Row(), 2)


def test_problem_body_includes_rfc_and_message() -> None:
    body = problem_body(ConflictError("Stale version; refresh and retry"))
    assert body["status"] == 409
    assert body["detail"] == "Stale version; refresh and retry"
    assert body["message"] == "Stale version; refresh and retry"
    assert body["code"] == "conflict"
    assert PROBLEM_JSON_MEDIA_TYPE.endswith("problem+json")


def test_uow_and_outbox_same_transaction() -> None:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine, tables=[OutboxMessage.__table__])
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionLocal()
    uow = SqlAlchemyUnitOfWork(session)
    org = uuid4()
    corr = uuid4()
    agg = uuid4()
    enqueue_outbox(
        session,
        organization_id=org,
        aggregate_type="source_baseline",
        aggregate_id=agg,
        event_type="governance.baseline.created",
        payload={"ok": True},
        correlation_id=corr,
    )
    uow.commit()
    rows = list(session.scalars(select(OutboxMessage)))
    assert len(rows) == 1
    assert rows[0].status == "pending"
    session.close()
