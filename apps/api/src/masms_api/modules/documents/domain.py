"""Document storage and scan domain rules (MOD-250)."""

from __future__ import annotations

from datetime import datetime

from masms_api.errors import ForbiddenError, InvalidTransitionError, ValidationAppError

CLEAN = "clean"
UNSAFE_VERDICTS = frozenset({"infected", "suspicious"})
AVAILABLE = "available"
QUARANTINE = "quarantine"
ACCESS_ACTIONS = frozenset({"download", "preview", "extract_text", "embeddings"})


def assert_can_publish_template(status: str) -> None:
    if status != "draft":
        raise InvalidTransitionError(
            f"Only draft template versions can be published; current='{status}'"
        )


def assert_scan_verdict(verdict: str) -> None:
    allowed = {"clean", "infected", "suspicious", "error"}
    if verdict not in allowed:
        raise ValidationAppError("verdict must be one of: " + ", ".join(sorted(allowed)))


def apply_scan_to_version_status(verdict: str) -> str:
    """Unsafe files go to quarantine and must not become available (AC-002)."""
    assert_scan_verdict(verdict)
    if verdict in UNSAFE_VERDICTS:
        return QUARANTINE
    if verdict == "error":
        return "scanning"
    return "scanning"


def assert_can_mark_available(
    *,
    status: str,
    latest_verdict: str | None,
    owner_actor_id: object | None,
    effective_at: datetime | None,
) -> None:
    """AC-001 + AC-002: authoritative docs need metadata; unsafe blocked."""
    if status == QUARANTINE:
        raise ForbiddenError("Quarantined files cannot become available")
    if latest_verdict is None:
        raise ValidationAppError("Scan result is required before making a version available")
    if latest_verdict != CLEAN:
        raise ForbiddenError(
            f"Unsafe or incomplete scan verdict '{latest_verdict}' cannot become available"
        )
    if owner_actor_id is None:
        raise ValidationAppError("Authoritative documents require an owner")
    if effective_at is None:
        raise ValidationAppError("Authoritative documents require an effective date")


def assert_indexing_allowed(*, status: str, latest_verdict: str | None) -> None:
    if status != AVAILABLE or latest_verdict != CLEAN:
        raise ForbiddenError("Only clean available versions may be indexed")


def assert_access_action(action: str) -> None:
    if action not in ACCESS_ACTIONS:
        raise ValidationAppError(
            "access action must be one of: " + ", ".join(sorted(ACCESS_ACTIONS))
        )


def permission_allows(
    *,
    action: str,
    can_download: bool,
    can_preview: bool,
    can_extract_text: bool,
    can_use_embeddings: bool,
) -> bool:
    assert_access_action(action)
    mapping = {
        "download": can_download,
        "preview": can_preview,
        "extract_text": can_extract_text,
        "embeddings": can_use_embeddings,
    }
    return bool(mapping[action])


def assert_access_granted(
    *,
    action: str,
    version_status: str,
    can_download: bool,
    can_preview: bool,
    can_extract_text: bool,
    can_use_embeddings: bool,
) -> None:
    """AC-003: access checks apply across file/preview/text/embeddings surfaces."""
    if version_status != AVAILABLE:
        raise ForbiddenError("Content is not available for access")
    if not permission_allows(
        action=action,
        can_download=can_download,
        can_preview=can_preview,
        can_extract_text=can_extract_text,
        can_use_embeddings=can_use_embeddings,
    ):
        raise ForbiddenError(f"Missing permission for action '{action}'")
