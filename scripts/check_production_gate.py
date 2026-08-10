"""CLI check for MOD-030 production release gate."""

from __future__ import annotations

import os
import sys

from masms_api.platform.release_gate import evaluate_production_gate


def main() -> int:
    confirmed = os.environ.get("CONFIRM_PRODUCTION", "").strip().lower() in {"1", "true", "yes"}
    try:
        evaluate_production_gate(
            environment="production",
            confirmed=confirmed,
            approver=os.environ.get("PRODUCTION_APPROVER"),
            reason=os.environ.get("PRODUCTION_APPROVAL_REASON"),
            git_sha=os.environ.get("GIT_SHA"),
        )
    except PermissionError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 1
    print("Production release gate passed (placeholder deploy may still be dry-run only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
