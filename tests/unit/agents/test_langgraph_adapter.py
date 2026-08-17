"""Unit tests for the MOD-360 LangGraph stub adapter."""

from __future__ import annotations

from typing import Any

import pytest
from masms_api.modules.agents.domain import ALLOWED_CODES
from masms_api.modules.agents.langgraph_adapter import (
    LangGraphAdapter,
    LiveLangGraphAdapter,
    get_langgraph_adapter,
)
from masms_api.modules.agents.llm_provider import (
    AgentRecommendation,
    LlmProvider,
    LlmResult,
)


class RecordingProvider(LlmProvider):
    def __init__(self) -> None:
        self.payload: dict[str, Any] = {}

    def generate_recommendation(
        self,
        *,
        agent_code: str,
        prompt_version: int,
        input_payload: dict[str, Any],
        allowed_tools: list[str],
        max_output_tokens: int,
    ) -> LlmResult:
        _ = (agent_code, prompt_version, allowed_tools, max_output_tokens)
        self.payload = input_payload
        return LlmResult(
            recommendation=AgentRecommendation(
                summary="Create a human-reviewed intake record.",
                confidence=0.82,
                source_refs=["KN-1@v1#chunk-0", "invented-source"],
                proposed_tools=["read_entity", "send_any_email"],
            ),
            model_name="sandbox-model",
            input_tokens=40,
            output_tokens=10,
        )


@pytest.mark.parametrize("agent_code", sorted(ALLOWED_CODES))
def test_stub_invoke_returns_structured_output_for_every_catalog_agent(agent_code: str) -> None:
    adapter = LangGraphAdapter()
    lg_id = adapter.start_run(agent_code=agent_code, run_id="run-1", input_payload={"note": "ok"})
    assert lg_id.startswith("stub-lg-")

    result = adapter.invoke_stub(
        agent_code=agent_code,
        prompt_version=1,
        model_name="stub-model",
        input_payload={"note": "ok"},
        allowed_tools=["read_entity", "search_knowledge"],
    )
    assert result["stub"] is True
    assert agent_code in str(result["summary"])
    assert result["model_name"] == "stub-model"
    assert result["confidence"] >= 0.6
    assert result["tools_used"] == ["read_entity", "search_knowledge"]
    assert result["sources"]


def test_stub_honors_force_low_confidence() -> None:
    result = get_langgraph_adapter().invoke_stub(
        agent_code="ticket_triage_agent",
        prompt_version=1,
        model_name="stub-model",
        input_payload={"force_low_confidence": True},
    )
    assert result["confidence"] < 0.6


def test_live_graph_redacts_input_and_filters_proposals() -> None:
    provider = RecordingProvider()
    adapter = LiveLangGraphAdapter(provider)

    result = adapter.invoke(
        agent_code="query_intake_agent",
        prompt_version=2,
        model_name="stub-model",
        input_payload={
            "summary": "Need a project",
            "client_email": "private@example.test",
            "api_key": "secret-value",
            "sources": [{"ref": "KN-1@v1#chunk-0"}],
        },
        allowed_tools=["read_entity"],
    )

    assert result["stub"] is False
    assert result["tools_used"] == ["read_entity"]
    assert result["sources"] == [{"type": "knowledge", "ref": "KN-1@v1#chunk-0"}]
    assert provider.payload["client_email"] == "[REDACTED]"
    assert provider.payload["api_key"] == "[REDACTED]"
