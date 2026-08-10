"""Optimistic concurrency helpers (MOD-020-MP-009)."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from masms_api.kernel.errors import ConflictError


class Versioned(Protocol):
    version: int


def assert_expected_version(
    row: Versioned,
    expected_version: int,
    *,
    correlation_id: UUID | None = None,
    message: str = "Stale version; refresh and retry",
) -> None:
    if row.version != expected_version:
        raise ConflictError(message, correlation_id=correlation_id)
