"""Temporal client stub/adapter (MOD-350 M1).

A live Temporal server is NOT required. The stub returns deterministic-looking
run identifiers and no-ops signal/cancel calls so FastAPI can own business state.
"""

from __future__ import annotations

import logging
from typing import Any
from uuid import uuid4

logger = logging.getLogger(__name__)


class TemporalAdapter:
    """Default stub Temporal adapter used until a real client is configured."""

    def start_workflow(
        self,
        *,
        workflow_type: str,
        workflow_id: str,
        input_payload: dict[str, Any] | None = None,
    ) -> str:
        run_id = f"stub-{uuid4()}"
        logger.info(
            "temporal_stub.start_workflow type=%s workflow_id=%s run_id=%s payload_keys=%s",
            workflow_type,
            workflow_id,
            run_id,
            sorted((input_payload or {}).keys()),
        )
        return run_id

    def signal_workflow(
        self,
        *,
        workflow_id: str,
        signal_name: str,
        payload: dict[str, Any] | None = None,
        run_id: str | None = None,
    ) -> None:
        logger.info(
            "temporal_stub.signal_workflow workflow_id=%s run_id=%s signal=%s payload_keys=%s",
            workflow_id,
            run_id,
            signal_name,
            sorted((payload or {}).keys()),
        )

    def cancel_workflow(
        self,
        *,
        workflow_id: str,
        run_id: str | None = None,
        reason: str | None = None,
    ) -> None:
        logger.info(
            "temporal_stub.cancel_workflow workflow_id=%s run_id=%s reason=%s",
            workflow_id,
            run_id,
            reason,
        )


def get_temporal_adapter() -> TemporalAdapter:
    """Factory hook for a future real client; M1 always returns the stub."""
    return TemporalAdapter()
