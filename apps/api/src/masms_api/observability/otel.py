"""OpenTelemetry-compatible stub without requiring OTEL packages (MOD-040-MP-006).

Real OpenTelemetry SDK wiring is deferred until PRE observability stack approval.
This stub emits structured span dictionaries safe for logs (secrets redacted).
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from masms_api.observability.redact import redact_mapping


@dataclass
class SpanRecord:
    name: str
    trace_id: str
    span_id: str
    attributes: dict[str, Any] = field(default_factory=dict)
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    ended_at: datetime | None = None
    status: str = "ok"
    error: str | None = None


class TracingStub:
    def __init__(self) -> None:
        self.spans: list[SpanRecord] = []

    @contextmanager
    def span(self, name: str, *, attributes: dict[str, Any] | None = None) -> Iterator[SpanRecord]:
        record = SpanRecord(
            name=name,
            trace_id=uuid4().hex,
            span_id=uuid4().hex[:16],
            attributes=redact_mapping(attributes or {}),
        )
        self.spans.append(record)
        try:
            yield record
            record.status = "ok"
        except Exception as exc:  # noqa: BLE001 - capture for span status then re-raise
            record.status = "error"
            record.error = exc.__class__.__name__
            raise
        finally:
            record.ended_at = datetime.now(UTC)


_default_tracer = TracingStub()


def get_tracer() -> TracingStub:
    return _default_tracer
