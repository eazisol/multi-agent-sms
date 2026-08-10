"""Unit tests for MOD-040 observability helpers."""

from __future__ import annotations

from uuid import uuid4

from masms_api.db import Base
from masms_api.kernel.actor import ActorKind
from masms_api.kernel.context import RequestContext
from masms_api.observability.models import (
    ActivityEvent,
    AgentRun,
    AuditLog,
    IntegrationEvent,
    StatusHistory,
)
from masms_api.observability.otel import TracingStub
from masms_api.observability.redact import redact_mapping
from masms_api.observability.writer import ObservabilityWriter
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


def _session():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(
        bind=engine,
        tables=[
            AuditLog.__table__,
            ActivityEvent.__table__,
            StatusHistory.__table__,
            AgentRun.__table__,
            IntegrationEvent.__table__,
        ],
    )
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)()


def test_redact_mapping_hides_secrets() -> None:
    redacted = redact_mapping({"title": "ok", "api_token": "secret", "nested": {"password": "x"}})
    assert redacted["title"] == "ok"
    assert redacted["api_token"] == "[REDACTED]"
    assert redacted["nested"]["password"] == "[REDACTED]"


def test_writer_append_only_and_redacts() -> None:
    session = _session()
    ctx = RequestContext.from_parts(
        organization_id=uuid4(),
        actor_id=uuid4(),
        actor_kind=ActorKind.HUMAN,
        correlation_id=uuid4(),
        display_name="tester",
    )
    writer = ObservabilityWriter(session, ctx)
    entity_id = uuid4()
    audit = writer.write_audit(
        action="update",
        entity_type="source_baseline",
        entity_id=entity_id,
        payload={"database_url": "postgres://user:pass@host/db"},
    )
    writer.write_status_history(
        entity_type="source_baseline",
        entity_id=entity_id,
        previous_status="draft",
        next_status="submitted",
        rule="BASELINE_TRANSITIONS",
    )
    writer.write_integration_event(
        provider="github",
        direction="inbound",
        event_type="pull_request.opened",
        payload={"authorization": "Bearer xyz"},
    )
    session.commit()
    assert audit.payload_redacted["database_url"] == "[REDACTED]"
    events = list(session.scalars(select(IntegrationEvent)))
    assert events[0].payload_redacted["authorization"] == "[REDACTED]"
    session.close()


def test_tracing_stub_records_spans() -> None:
    tracer = TracingStub()
    with tracer.span("demo", attributes={"token": "abc", "ok": True}) as span:
        assert span.name == "demo"
    assert tracer.spans[-1].attributes["token"] == "[REDACTED]"
    assert tracer.spans[-1].status == "ok"
