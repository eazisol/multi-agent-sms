"""Standard audit action codes for MASMS modules (MOD-020-SEC-004).

Emission remains in MOD-040 (`ObservabilityWriter`) / governance writers.
Modules should reuse these codes for consistent audit catalogs.
"""

from __future__ import annotations

from typing import Final

AUDIT_ACTION_CREATE: Final = "create"
AUDIT_ACTION_READ_SENSITIVE: Final = "read_sensitive"
AUDIT_ACTION_UPDATE: Final = "update"
AUDIT_ACTION_DELETE: Final = "delete"
AUDIT_ACTION_ASSIGNMENT: Final = "assignment"
AUDIT_ACTION_TRANSITION: Final = "transition"
AUDIT_ACTION_APPROVAL: Final = "approval"
AUDIT_ACTION_REJECTION: Final = "rejection"
AUDIT_ACTION_OVERRIDE: Final = "override"
AUDIT_ACTION_EXPORT: Final = "export"
AUDIT_ACTION_INTEGRATION: Final = "integration"
AUDIT_ACTION_AGENT_ACTION: Final = "agent_action"

STANDARD_AUDIT_ACTIONS: frozenset[str] = frozenset(
    {
        AUDIT_ACTION_CREATE,
        AUDIT_ACTION_READ_SENSITIVE,
        AUDIT_ACTION_UPDATE,
        AUDIT_ACTION_DELETE,
        AUDIT_ACTION_ASSIGNMENT,
        AUDIT_ACTION_TRANSITION,
        AUDIT_ACTION_APPROVAL,
        AUDIT_ACTION_REJECTION,
        AUDIT_ACTION_OVERRIDE,
        AUDIT_ACTION_EXPORT,
        AUDIT_ACTION_INTEGRATION,
        AUDIT_ACTION_AGENT_ACTION,
    }
)
