"""Token hashing helpers (no third-party JWT dependency in scaffold)."""

from __future__ import annotations

import hashlib
import hmac
import secrets


def hash_secret(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def generate_opaque_token(*, prefix: str = "masms") -> str:
    return f"{prefix}_{secrets.token_urlsafe(32)}"


def constant_time_equals(left: str, right: str) -> bool:
    return hmac.compare_digest(left, right)
