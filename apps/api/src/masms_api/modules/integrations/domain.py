"""Integration framework domain rules (MOD-500)."""

from __future__ import annotations

import json
import re
from typing import Any

from masms_api.errors import ConflictError, InvalidTransitionError, ValidationAppError
from masms_api.kernel.redact import redact_mapping

PROVIDERS = frozenset({"github", "jira", "slack", "custom"})
AUTH_TYPES = frozenset({"oauth2", "api_key", "none"})
CONNECTION_STATUSES = frozenset({"draft", "active", "paused", "error", "revoked"})
HEALTH_STATUSES = frozenset({"healthy", "degraded", "down"})
WEBHOOK_STATUSES = frozenset({"received", "processed", "failed", "ignored"})
INBOX_STATUSES = frozenset({"pending", "processed", "failed"})
OUTBOX_STATUSES = frozenset({"pending", "sent", "failed", "dead"})

CONNECTION_TRANSITIONS: dict[str, frozenset[str]] = {
    "draft": frozenset({"active", "revoked"}),
    "active": frozenset({"paused", "error", "revoked"}),
    "paused": frozenset({"active", "revoked"}),
    "error": frozenset({"active", "paused", "revoked"}),
    "revoked": frozenset(),
}

SECRET_FIELD_NAMES = frozenset(
    {
        "client_secret",
        "access_token",
        "refresh_token",
        "api_key",
        "apikey",
        "password",
        "secret",
        "token",
        "credential",
        "private_key",
        "authorization",
    }
)

_RAW_TOKEN_PATTERN = re.compile(r"^[A-Za-z0-9_\-./+=]{20,}$")


ALLOWED_REFERENCE_FIELDS = frozenset({"credential_ref"})


def _normalize_key(key: str) -> str:
    return key.lower().replace("-", "_")


def _is_forbidden_secret_key(key: str) -> bool:
    normalized = _normalize_key(key)
    if normalized in ALLOWED_REFERENCE_FIELDS:
        return False
    if normalized in SECRET_FIELD_NAMES:
        return True
    return any(
        fragment in normalized for fragment in ("secret", "token", "password", "credential")
    ) and normalized not in ALLOWED_REFERENCE_FIELDS


def assert_no_raw_secrets(payload: dict[str, Any]) -> None:
    """Reject request bodies that include raw secret/token fields."""
    for key in payload:
        if _is_forbidden_secret_key(str(key)):
            raise ValidationAppError(
                f"Field '{key}' is not allowed; use credential_ref for secret-manager references"
            )
        value = payload[key]
        if isinstance(value, dict):
            assert_no_raw_secrets(value)


def redact_payload(payload: dict[str, Any] | str | None) -> str:
    """Return JSON string with sensitive keys redacted."""
    if payload is None:
        return "{}"
    if isinstance(payload, str):
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError:
            return payload
        if isinstance(parsed, dict):
            return json.dumps(redact_mapping(parsed), sort_keys=True)
        return payload
    return json.dumps(redact_mapping(payload), sort_keys=True)


def assert_credential_ref(auth_type: str, credential_ref: str | None) -> None:
    if auth_type not in AUTH_TYPES:
        raise ValidationAppError(f"Invalid auth_type '{auth_type}'")
    if auth_type == "none":
        return
    if not credential_ref or not credential_ref.strip():
        raise ValidationAppError("credential_ref is required when auth_type is not none")
    ref = credential_ref.strip()
    if not (ref.startswith("secrets/") or ref.startswith("sm:")):
        raise ValidationAppError(
            "credential_ref must be an opaque secret-manager reference (secrets/ or sm: prefix)"
        )
    if _RAW_TOKEN_PATTERN.match(ref) and not ref.startswith("secrets/"):
        raise ValidationAppError("credential_ref must not look like a raw token")


def assert_provider(value: str) -> None:
    if value not in PROVIDERS:
        raise ValidationAppError(f"Invalid provider '{value}'")


def assert_connection_status(value: str) -> None:
    if value not in CONNECTION_STATUSES:
        raise ValidationAppError(f"Invalid connection status '{value}'")


def assert_connection_transition(current: str, nxt: str) -> None:
    assert_connection_status(current)
    assert_connection_status(nxt)
    allowed = CONNECTION_TRANSITIONS.get(current, frozenset())
    if nxt not in allowed:
        raise InvalidTransitionError(
            f"Invalid connection transition from '{current}' to '{nxt}'"
        )


def assert_expected_version(*, current: int, expected: int | None) -> None:
    if expected is not None and current != expected:
        raise ConflictError(
            f"Optimistic concurrency conflict: expected version {expected}, got {current}"
        )


def default_credential_ref(*, organization_id: str, code: str) -> str:
    return f"secrets/oauth/{organization_id}/{code}"


def mapping_fields_present(payload: dict[str, Any]) -> bool:
    required = (
        "internal_entity_type",
        "internal_entity_id",
        "external_entity_type",
        "external_entity_id",
    )
    return all(key in payload and payload[key] for key in required)
