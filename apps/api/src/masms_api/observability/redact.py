"""Redact secrets and sensitive fields before logging or audit payloads (MOD-040)."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

SENSITIVE_KEY_FRAGMENTS = (
    "password",
    "secret",
    "token",
    "api_key",
    "apikey",
    "authorization",
    "credential",
    "private_key",
    "connection_string",
    "database_url",
)


def _is_sensitive_key(key: str) -> bool:
    lowered = key.lower().replace("-", "_")
    return any(fragment in lowered for fragment in SENSITIVE_KEY_FRAGMENTS)


def redact_mapping(payload: dict[str, Any] | None) -> dict[str, Any]:
    """Return a deep-copied mapping with sensitive values replaced."""
    if not payload:
        return {}
    data = deepcopy(payload)

    def walk(node: Any) -> Any:
        if isinstance(node, dict):
            return {
                key: ("[REDACTED]" if _is_sensitive_key(str(key)) else walk(value))
                for key, value in node.items()
            }
        if isinstance(node, list):
            return [walk(item) for item in node]
        return node

    result = walk(data)
    assert isinstance(result, dict)
    return result
