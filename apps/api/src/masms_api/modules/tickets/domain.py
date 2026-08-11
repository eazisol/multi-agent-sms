"""Ticket domain rules (MOD-300)."""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from masms_api.errors import ForbiddenError, InvalidTransitionError, ValidationAppError

STATUS_BACKLOG = "backlog"
STATUS_READY = "ready"
STATUS_ASSIGNED = "assigned"
STATUS_IN_PROGRESS = "in_progress"
STATUS_PASSED_QA = "passed_qa"
STATUS_DONE = "done"
STATUS_BLOCKED = "blocked"

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    STATUS_BACKLOG: {STATUS_READY},
    STATUS_READY: {STATUS_ASSIGNED, STATUS_BACKLOG},
    STATUS_ASSIGNED: {STATUS_IN_PROGRESS, STATUS_READY, STATUS_BLOCKED},
    STATUS_IN_PROGRESS: {
        "code_review",
        "ready_for_qa",
        STATUS_BLOCKED,
        STATUS_ASSIGNED,
    },
    "code_review": {"ready_for_qa", STATUS_IN_PROGRESS, STATUS_BLOCKED},
    "ready_for_qa": {"qa_in_progress", STATUS_IN_PROGRESS, STATUS_BLOCKED},
    "qa_in_progress": {STATUS_PASSED_QA, "failed_qa", STATUS_BLOCKED},
    "failed_qa": {STATUS_IN_PROGRESS, STATUS_ASSIGNED},
    STATUS_PASSED_QA: {STATUS_DONE, "qa_in_progress", STATUS_IN_PROGRESS},
    STATUS_BLOCKED: {
        STATUS_IN_PROGRESS,
        STATUS_ASSIGNED,
        STATUS_READY,
        "ready_for_qa",
        STATUS_BACKLOG,
    },
    STATUS_DONE: {STATUS_IN_PROGRESS, "qa_in_progress"},
}

DEFAULT_READINESS_CHECKS: list[tuple[str, str]] = [
    ("description", "Clear description"),
    ("requirement", "Requirement reference"),
    ("acceptance_criteria", "Acceptance criteria"),
    ("priority", "Priority"),
    ("estimate", "Estimate or sizing"),
    ("definition_of_done", "Definition of Done"),
]

DEFAULT_DONE_CHECKS: list[tuple[str, str]] = [
    ("acceptance_results", "Acceptance criteria results"),
    ("qa_evidence", "QA evidence"),
    ("no_blocking_defects", "No unresolved blocking defects"),
]


def assert_no_self_dependency(predecessor_id: UUID, successor_id: UUID) -> None:
    if predecessor_id == successor_id:
        raise ValidationAppError("A ticket cannot depend on itself")


def assert_owner_or_queue(
    *,
    owner_actor_id: UUID | None,
    queue_code: str | None,
) -> None:
    """AC-002: tickets need an owner or a queue."""
    if owner_actor_id is None and not (queue_code and queue_code.strip()):
        raise ValidationAppError("Ticket requires an owner or a queue")


def assert_can_become_ready(
    *,
    status: str,
    description: str | None,
    acceptance_criteria: str | None,
    priority: str | None,
    estimate_points: Decimal | None,
    definition_of_done: str | None,
    phase_id: UUID | None,
    has_requirement_link: bool,
    owner_actor_id: UUID | None,
    queue_code: str | None,
    unsatisfied_required_checks: list[str],
) -> None:
    """AC-001: no ticket becomes Ready without required information."""
    if status != STATUS_BACKLOG:
        raise InvalidTransitionError("Only backlog tickets can move to Ready")
    missing: list[str] = []
    if not (description and description.strip()):
        missing.append("description")
    if not has_requirement_link:
        missing.append("requirement link")
    if not (acceptance_criteria and acceptance_criteria.strip()):
        missing.append("acceptance criteria")
    if not priority:
        missing.append("priority")
    if estimate_points is None:
        missing.append("estimate")
    if not (definition_of_done and definition_of_done.strip()):
        missing.append("definition of done")
    if phase_id is None:
        missing.append("phase")
    try:
        assert_owner_or_queue(owner_actor_id=owner_actor_id, queue_code=queue_code)
    except ValidationAppError:
        missing.append("owner or queue")
    if unsatisfied_required_checks:
        missing.extend(f"check:{c}" for c in unsatisfied_required_checks)
    if missing:
        raise ValidationAppError(
            "Ticket is not Ready; missing: " + ", ".join(missing)
        )


def assert_allowed_transition(current: str, nxt: str) -> None:
    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if nxt not in allowed:
        raise InvalidTransitionError(f"Cannot transition from {current} to {nxt}")


def assert_can_complete(
    *,
    status: str,
    unsatisfied_required_checks: list[str],
) -> None:
    if status != STATUS_PASSED_QA:
        raise InvalidTransitionError("Only Passed QA tickets can move to Done")
    if unsatisfied_required_checks:
        raise ValidationAppError(
            "Ticket cannot be Done; unsatisfied checks: "
            + ", ".join(unsatisfied_required_checks)
        )


def assert_can_reopen(
    *,
    status: str,
    actor_kind: str,
    reopen_reason: str | None,
    evidence_id: UUID | None,
) -> None:
    """AC-003: Done tickets reopen only with authority and evidence."""
    if status != STATUS_DONE:
        raise InvalidTransitionError("Only Done tickets can be reopened")
    if actor_kind != "human":
        raise ForbiddenError("Only a human actor may reopen a Done ticket")
    if not (reopen_reason and reopen_reason.strip()):
        raise ValidationAppError("Reopen requires a reason")
    if evidence_id is None:
        raise ValidationAppError("Reopen requires evidence")
