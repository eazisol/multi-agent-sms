"""LangGraph adapters for stubbed and bounded live agent execution."""

from __future__ import annotations

import logging
from typing import Any, NotRequired, TypedDict
from uuid import uuid4

from langgraph.graph import END, START, StateGraph

from masms_api.config import get_settings
from masms_api.kernel.redact import redact_mapping
from masms_api.modules.agents.llm_provider import LlmProvider, OpenAILlmProvider

logger = logging.getLogger(__name__)
LIVE_AGENT_CODE = "query_intake_agent"


class AgentGraphState(TypedDict):
    agent_code: str
    prompt_version: int
    input_payload: dict[str, Any]
    allowed_tools: list[str]
    max_output_tokens: int
    result: NotRequired[dict[str, Any]]


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

    def invoke(
        self,
        *,
        agent_code: str,
        prompt_version: int,
        model_name: str,
        input_payload: dict[str, Any] | None = None,
        allowed_tools: list[Any] | None = None,
        max_output_tokens: int = 1200,
    ) -> dict[str, Any]:
        return self.invoke_stub(
            agent_code=agent_code,
            prompt_version=prompt_version,
            model_name=model_name,
            input_payload=input_payload,
            allowed_tools=allowed_tools,
        )


class LiveLangGraphAdapter(LangGraphAdapter):
    """One bounded live graph; catalog agents not yet migrated remain stubbed."""

    def __init__(self, provider: LlmProvider) -> None:
        self.provider = provider
        builder = StateGraph(AgentGraphState)
        builder.add_node("reason", self._reason)
        builder.add_edge(START, "reason")
        builder.add_edge("reason", END)
        self.graph = builder.compile()

    def start_run(
        self,
        *,
        agent_code: str,
        run_id: str,
        input_payload: dict[str, Any] | None = None,
    ) -> str:
        if agent_code != LIVE_AGENT_CODE:
            return super().start_run(
                agent_code=agent_code,
                run_id=run_id,
                input_payload=input_payload,
            )
        return f"lg-{uuid4()}"

    def _reason(self, state: AgentGraphState) -> dict[str, Any]:
        output = self.provider.generate_recommendation(
            agent_code=state["agent_code"],
            prompt_version=state["prompt_version"],
            input_payload=state["input_payload"],
            allowed_tools=state["allowed_tools"],
            max_output_tokens=state["max_output_tokens"],
        )
        recommendation = output.recommendation
        allowed_tools = set(state["allowed_tools"])
        supplied_sources = _source_refs(state["input_payload"])
        return {
            "result": {
                "summary": recommendation.summary,
                "confidence": recommendation.confidence,
                "tools_used": [
                    tool for tool in recommendation.proposed_tools if tool in allowed_tools
                ],
                "sources": [
                    {"type": "knowledge", "ref": ref}
                    for ref in recommendation.source_refs
                    if ref in supplied_sources
                ],
                "cost_units": float(output.total_tokens),
                "usage": {
                    "input_tokens": output.input_tokens,
                    "output_tokens": output.output_tokens,
                },
                "model_name": output.model_name,
                "stub": False,
            }
        }

    def invoke(
        self,
        *,
        agent_code: str,
        prompt_version: int,
        model_name: str,
        input_payload: dict[str, Any] | None = None,
        allowed_tools: list[Any] | None = None,
        max_output_tokens: int = 1200,
    ) -> dict[str, Any]:
        if agent_code != LIVE_AGENT_CODE:
            return super().invoke(
                agent_code=agent_code,
                prompt_version=prompt_version,
                model_name=model_name,
                input_payload=input_payload,
                allowed_tools=allowed_tools,
                max_output_tokens=max_output_tokens,
            )
        safe_payload = _redact_model_input(input_payload or {})
        safe_tools = [tool for tool in (allowed_tools or []) if isinstance(tool, str)]
        state = self.graph.invoke(
            {
                "agent_code": agent_code,
                "prompt_version": prompt_version,
                "input_payload": safe_payload,
                "allowed_tools": safe_tools,
                "max_output_tokens": max_output_tokens,
            }
        )
        result = state.get("result")
        if not isinstance(result, dict):
            raise RuntimeError("LangGraph completed without a structured result")
        return result


def _source_refs(payload: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    sources = payload.get("sources")
    if not isinstance(sources, list):
        return refs
    for source in sources:
        if isinstance(source, str):
            refs.add(source)
        elif isinstance(source, dict):
            ref = source.get("ref") or source.get("source_citation")
            if isinstance(ref, str):
                refs.add(ref)
    return refs


def _redact_model_input(payload: dict[str, Any]) -> dict[str, Any]:
    redacted = redact_mapping(payload)
    pii_fragments = ("email", "phone", "address", "date_of_birth")

    def walk(value: Any) -> Any:
        if isinstance(value, dict):
            return {
                key: (
                    "[REDACTED]"
                    if any(fragment in str(key).lower() for fragment in pii_fragments)
                    else walk(item)
                )
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [walk(item) for item in value]
        return value

    result = walk(redacted)
    assert isinstance(result, dict)
    return result


def get_langgraph_adapter() -> LangGraphAdapter:
    """Enable one live graph only when an OpenAI sandbox key is configured."""
    settings = get_settings()
    if settings.openai_api_key:
        return LiveLangGraphAdapter(
            OpenAILlmProvider(
                api_key=settings.openai_api_key,
                model_name=settings.openai_model,
            )
        )
    return LangGraphAdapter()
