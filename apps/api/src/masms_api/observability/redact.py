"""Redact secrets and sensitive fields before logging or audit payloads (MOD-040).

Canonical implementation lives in ``masms_api.kernel.redact`` (MOD-020-SEC-003).
"""

from __future__ import annotations

from masms_api.kernel.redact import SENSITIVE_KEY_FRAGMENTS, redact_mapping

__all__ = ["SENSITIVE_KEY_FRAGMENTS", "redact_mapping"]
