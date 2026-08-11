"""LangGraph client stub/adapter (MOD-360 M1).

A live LangGraph / LLM is NOT required. The stub returns structured outputs and
opaque run ids so FastAPI can own business state in agr_* tables.
"""

from __future__ import annotations

import logging
from typing import Any
from uuid import uuid4

logger = logging.getLogger(__name__)


class LangGraphAdapter:
    """Default stub LangGraph adapter used until a real runtime is configured."""

    def start_run(
        self,
        *,
        agent_code: str,
        run_id: str,
        input_payload: dict[str, Any] | None = None,
    ) -> str:
        stub_id = f"stub-lg-{uuid4()}"
        logger.info(
            "langgraph_stub.start_run agent=%s run_id=%s lg_id=%s payload_keys=%s",
            agent_code,
            run_id,
            stub_id,
            sorted((input_payload or {}).keys()),
        )
        return stub_id

    def invoke_stub(
        self,
        *,
        agent_code: str,
        prompt_version: int,
        model_name: str,
        input_payload: dict[str, Any] | None = None,
        allowed_tools: list[Any] | None = None,
    ) -> dict[str, Any]:
        payload = input_payload or {}
        force_low = bool(payload.get("force_low_confidence") or payload.get("force_review"))
        confidence = float(payload.get("stub_confidence", 0.4 if force_low else 0.85))
        summary = (
            f"Stub recommendation for {agent_code} "
            f"(prompt v{prompt_version}, model={model_name})."
        )
        tools = list(allowed_tools or [])[:3]
        sources = list(payload.get("sources") or [{"type": "stub", "ref": "m1"}])
        logger.info(
            "langgraph_stub.invoke agent=%s confidence=%s tool_count=%s",
            agent_code,
            confidence,
            len(tools),
        )
        return {
            "summary": summary,
            "confidence": confidence,
            "tools_used": tools,
            "sources": sources,
            "cost_units": 0.0,
            "model_name": model_name,
            "stub": True,
        }


def get_langgraph_adapter() -> LangGraphAdapter:
    """Factory hook for a future real client; M1 always returns the stub."""
    return LangGraphAdapter()
