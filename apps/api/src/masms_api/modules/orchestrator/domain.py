"""Orchestrator domain rules (MOD-350)."""

from __future__ import annotations

from masms_api.errors import ConflictError, InvalidTransitionError, ValidationAppError

# Frozen catalog of approved Temporal business workflows (M1).
ALLOWED_CODES: frozenset[str] = frozenset(
    {
        "query_intake",
        "requirement_clarification",
        "project_handover",
        "assignment_ack",
        "blocker_resolution",
        "qa_rejection_loop",
        "client_status_report",
        "change_request_flow",
        "deployment_approval",
        "project_closure",
        "approval_gate_wait",
        "followup_escalation",
    }
)

WORKFLOW_TITLES: dict[str, str] = {
    "query_intake": "Query Intake",
    "requirement_clarification": "Requirement Clarification",
    "project_handover": "Project Handover",
    "assignment_ack": "Assignment Acknowledgement",
    "blocker_resolution": "Blocker Resolution",
    "qa_rejection_loop": "QA Rejection Loop",
    "client_status_report": "Client Status Report",
    "change_request_flow": "Change Request Flow",
    "deployment_approval": "Deployment Approval",
    "project_closure": "Project Closure",
    "approval_gate_wait": "Approval Gate Wait",
    "followup_escalation": "Follow-up Escalation",
}

INSTANCE_TRANSITIONS: dict[str, frozenset[str]] = {
    "pending": frozenset({"running"}),
    "running": frozenset({"waiting", "completed", "failed", "cancelled"}),
    "waiting": frozenset({"running", "completed", "failed", "cancelled"}),
    # retry / abandon / ops override from failed
    "failed": frozenset({"running", "cancelled", "completed"}),
    "completed": frozenset(),
    "cancelled": frozenset(),
}

TERMINAL_INSTANCE_STATUSES = frozenset({"completed", "cancelled"})
OPEN_INSTANCE_STATUSES = frozenset({"pending", "running", "waiting", "failed"})
TERMINAL_SIGNALS_BY_WORKFLOW: dict[str, frozenset[str]] = {
    "query_intake": frozenset({"complete", "resolved", "approved"}),
}

VERSION_STATUSES = frozenset({"draft", "active", "retired"})
SIGNAL_STATUSES = frozenset({"accepted", "applied", "rejected", "duplicate"})
INTERVENTION_ACTIONS = frozenset({"cancel", "retry", "resume", "override_complete"})
INTERVENTION_STATUSES = frozenset({"open", "resolved"})


def assert_allowed_workflow_code(code: str) -> None:
    if code not in ALLOWED_CODES:
        raise ValidationAppError(
            f"Unknown workflow_code '{code}'. Only the 12 approved catalog codes may be used."
        )


def assert_instance_transition(*, from_status: str, to_status: str) -> None:
    allowed = INSTANCE_TRANSITIONS.get(from_status, frozenset())
    if to_status not in allowed:
        raise InvalidTransitionError(
            f"Invalid workflow instance transition {from_status} → {to_status}"
        )


def assert_instance_open(status: str) -> None:
    if status in TERMINAL_INSTANCE_STATUSES:
        raise ConflictError(f"Workflow instance is closed (status={status})")
    if status not in OPEN_INSTANCE_STATUSES:
        raise ConflictError(f"Workflow instance is not open (status={status})")


def is_terminal_signal(*, workflow_code: str, signal_name: str) -> bool:
    return signal_name in TERMINAL_SIGNALS_BY_WORKFLOW.get(workflow_code, frozenset())


def assert_intervention_action(action_code: str) -> None:
    if action_code not in INTERVENTION_ACTIONS:
        raise ValidationAppError(f"Invalid intervention action_code '{action_code}'")


def assert_version_status(status: str) -> None:
    if status not in VERSION_STATUSES:
        raise ValidationAppError(f"Invalid workflow version status '{status}'")


def assert_expected_version(*, current: int, expected: int | None) -> None:
    if expected is not None and current != expected:
        raise ConflictError(
            f"Optimistic concurrency conflict: expected version {expected}, got {current}"
        )


def next_status_for_intervention(*, action_code: str, current_status: str) -> str:
    """Map intervention action to target instance status and validate transition."""
    assert_intervention_action(action_code)
    if action_code == "cancel":
        target = "cancelled"
    elif action_code == "retry":
        target = "running"
    elif action_code == "resume":
        target = "running"
    else:  # override_complete
        target = "completed"
    assert_instance_transition(from_status=current_status, to_status=target)
    return target
