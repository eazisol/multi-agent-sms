"""Traceability domain rules (MOD-460)."""

from __future__ import annotations

import hashlib

from masms_api.errors import ConflictError, InvalidTransitionError, ValidationAppError

COMPLETE_TRACE_LINK_TYPES = frozenset({"ticket", "test", "release", "document"})
MANIFEST_STATUSES = frozenset({"draft", "sealed", "exported"})
MANIFEST_TRANSITIONS: dict[str, frozenset[str]] = {
    "draft": frozenset({"sealed"}),
    "sealed": frozenset({"exported"}),
    "exported": frozenset(),
}
EXPORT_FORMATS = frozenset({"json"})
EXPORT_STATUSES = frozenset({"pending", "ready", "failed"})
MANIFEST_ITEM_TYPES = frozenset(
    {"requirement", "ticket", "test_case", "release", "document", "link"}
)
RELEASE_READY_THRESHOLD = 95.0


def requirement_is_complete(
    has_ticket: bool,
    has_test: bool,
    has_release: bool,
    has_document: bool,
) -> bool:
    return bool(has_ticket and has_test and has_release and has_document)


def coverage_pct(complete: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((complete / total) * 100.0, 4)


def release_ready(pct: float) -> bool:
    return pct >= RELEASE_READY_THRESHOLD


def assert_expected_version(*, current: int, expected: int | None) -> None:
    if expected is not None and current != expected:
        raise ConflictError(
            f"Optimistic concurrency conflict: expected version {expected}, got {current}"
        )


def assert_manifest_status(value: str) -> None:
    if value not in MANIFEST_STATUSES:
        raise ValidationAppError(f"Invalid manifest status '{value}'")


def assert_manifest_transition(current: str, nxt: str) -> None:
    assert_manifest_status(current)
    assert_manifest_status(nxt)
    allowed = MANIFEST_TRANSITIONS.get(current, frozenset())
    if nxt not in allowed:
        raise InvalidTransitionError(
            f"Invalid manifest transition from '{current}' to '{nxt}'"
        )


def assert_export_format(value: str) -> None:
    if value not in EXPORT_FORMATS:
        raise ValidationAppError(f"Invalid export_format '{value}'")


def assert_item_type(value: str) -> None:
    if value not in MANIFEST_ITEM_TYPES:
        raise ValidationAppError(f"Invalid item_type '{value}'")


def item_key(item_type: str, item_id: object) -> str:
    return f"{item_type}:{item_id}"


def compute_manifest_checksum(item_keys: list[str]) -> str:
    """SHA-256 over sorted canonical item keys (type:id)."""
    canonical = "\n".join(sorted(item_keys))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
