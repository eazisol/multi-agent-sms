"""First live MASMS Temporal workflow.

Only query intake is registered in the local-sandbox slice. The remaining
catalog workflow types stay on the stub adapter until separately implemented.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from temporalio import workflow
from temporalio.common import RawValue


@workflow.defn(name="masms.query_intake")
class QueryIntakeWorkflow:
    def __init__(self) -> None:
        self._completed = False
        self._signal_names: list[str] = []

    @workflow.run
    async def run(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        await workflow.wait_condition(lambda: self._completed)
        return {
            "status": "completed",
            "input_keys": sorted(input_payload),
            "signals": self._signal_names,
        }

    @workflow.signal(dynamic=True)
    async def receive_signal(self, name: str, args: Sequence[RawValue]) -> None:
        _ = args
        self._signal_names.append(name)
        if name in {"complete", "resolved", "approved"}:
            self._completed = True
