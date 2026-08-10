"""Human production release gate helpers (MOD-030-MP-005 / AC-002)."""

from __future__ import annotations

from dataclasses import dataclass

from masms_api.platform.environment import Environment, is_production


@dataclass(frozen=True, slots=True)
class ProductionReleaseGate:
    """Placeholder for GitHub Environment protection + human approval evidence."""

    environment: Environment
    confirmed: bool
    approver: str | None
    reason: str | None
    git_sha: str | None

    def assert_allowed(self) -> None:
        if not is_production(self.environment):
            return
        if not self.confirmed:
            raise PermissionError(
                "Production deploy blocked: set CONFIRM_PRODUCTION=true after human approval"
            )
        if not self.approver:
            raise PermissionError("Production deploy blocked: PRODUCTION_APPROVER is required")
        if not self.reason or len(self.reason.strip()) < 8:
            raise PermissionError(
                "Production deploy blocked: PRODUCTION_APPROVAL_REASON must explain the release"
            )
        if not self.git_sha:
            raise PermissionError("Production deploy blocked: GIT_SHA is required for traceability")


def evaluate_production_gate(
    *,
    environment: str,
    confirmed: bool,
    approver: str | None,
    reason: str | None,
    git_sha: str | None,
) -> ProductionReleaseGate:
    from masms_api.platform.environment import parse_environment

    gate = ProductionReleaseGate(
        environment=parse_environment(environment),
        confirmed=confirmed,
        approver=approver,
        reason=reason,
        git_sha=git_sha,
    )
    gate.assert_allowed()
    return gate
