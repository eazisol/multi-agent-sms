"""Domain rules for MOD-600 security hardening."""

from __future__ import annotations

import json
from typing import Any

from masms_api.errors import ConflictError, ValidationAppError
from masms_api.kernel.redact import redact_mapping

THREAT_MODEL_STATUSES = frozenset({"draft", "active", "archived"})
PII_CLASSIFICATIONS = frozenset({"pii", "sensitive", "public"})
RETENTION_ACTIONS = frozenset({"delete", "anonymize", "archive"})
RETENTION_STATUSES = frozenset({"draft", "active", "suspended"})
LEGAL_HOLD_STATUSES = frozenset({"active", "released"})
DELETION_JOB_STATUSES = frozenset({"pending", "blocked", "completed", "failed"})
BACKUP_ENVIRONMENTS = frozenset({"local", "staging", "production"})
BACKUP_STATUSES = frozenset({"recorded", "verified", "failed"})
RESTORE_RESULTS = frozenset({"passed", "failed"})
INCIDENT_SEVERITIES = frozenset({"low", "medium", "high", "critical"})
INCIDENT_STATUSES = frozenset({"open", "mitigated", "closed"})


def assert_threat_model_status(value: str) -> None:
    if value not in THREAT_MODEL_STATUSES:
        raise ValidationAppError(f"Invalid threat model status '{value}'")


def assert_pii_classification(value: str) -> None:
    if value not in PII_CLASSIFICATIONS:
        raise ValidationAppError(f"Invalid PII classification '{value}'")


def assert_retention_action(value: str) -> None:
    if value not in RETENTION_ACTIONS:
        raise ValidationAppError(f"Invalid retention action '{value}'")


def assert_retention_status(value: str) -> None:
    if value not in RETENTION_STATUSES:
        raise ValidationAppError(f"Invalid retention status '{value}'")


def assert_legal_hold_status(value: str) -> None:
    if value not in LEGAL_HOLD_STATUSES:
        raise ValidationAppError(f"Invalid legal hold status '{value}'")


def assert_deletion_job_status(value: str) -> None:
    if value not in DELETION_JOB_STATUSES:
        raise ValidationAppError(f"Invalid deletion job status '{value}'")


def assert_backup_environment(value: str) -> None:
    if value not in BACKUP_ENVIRONMENTS:
        raise ValidationAppError(f"Invalid backup environment '{value}'")


def assert_backup_status(value: str) -> None:
    if value not in BACKUP_STATUSES:
        raise ValidationAppError(f"Invalid backup status '{value}'")


def assert_restore_result(value: str) -> None:
    if value not in RESTORE_RESULTS:
        raise ValidationAppError(f"Invalid restore result '{value}'")


def assert_incident_severity(value: str) -> None:
    if value not in INCIDENT_SEVERITIES:
        raise ValidationAppError(f"Invalid incident severity '{value}'")


def assert_incident_status(value: str) -> None:
    if value not in INCIDENT_STATUSES:
        raise ValidationAppError(f"Invalid incident status '{value}'")


def assert_expected_version(*, current: int, expected: int | None) -> None:
    if expected is not None and current != expected:
        raise ConflictError(
            f"Optimistic concurrency conflict: expected version {expected}, got {current}"
        )


def assert_no_critical_open(incidents: list[Any]) -> tuple[int, bool]:
    """Return (critical_open_count, gate_passed) for AC-001."""
    critical_open = [
        item
        for item in incidents
        if getattr(item, "severity", None) == "critical"
        and getattr(item, "status", None) == "open"
    ]
    count = len(critical_open)
    return count, count == 0


def security_gate_passed(*, critical_open_count: int) -> bool:
    return critical_open_count == 0


def assert_rpo_rto_met(
    *,
    target_rpo: int,
    target_rto: int,
    measured_rpo: int,
    measured_rto: int,
) -> tuple[bool, bool, bool]:
    """Return (rpo_met, rto_met, validated) for AC-002."""
    rpo_met = measured_rpo <= target_rpo
    rto_met = measured_rto <= target_rto
    return rpo_met, rto_met, rpo_met and rto_met


def assert_training_opt_in_allowed(*, allow: bool, evidence: str | None) -> None:
    """AC-003: enabling model training requires non-empty human approval evidence."""
    if allow and (evidence is None or not str(evidence).strip()):
        raise ValidationAppError(
            "Enabling model training requires explicit human_approval_evidence"
        )


def active_hold_blocks_deletion(
    *,
    holds: list[Any],
    entity_type: str,
    entity_id: str | None = None,
) -> str | None:
    """Return blocked reason when an active legal hold covers the entity."""
    for hold in holds:
        if getattr(hold, "status", None) != "active":
            continue
        held_type = getattr(hold, "held_entity_type", None)
        held_id = getattr(hold, "held_entity_id", None)
        if held_type is None:
            return f"Active legal hold '{getattr(hold, 'code', hold)}' blocks deletion"
        if held_type == entity_type and (
            held_id is None or entity_id is None or str(held_id) == str(entity_id)
        ):
            return f"Active legal hold '{getattr(hold, 'code', hold)}' blocks deletion"
    return None


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
