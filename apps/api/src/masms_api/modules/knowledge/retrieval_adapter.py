"""Knowledge embedding and fallback ranking adapters."""

from __future__ import annotations

import hashlib
import logging
import re
from typing import Any

from openai import OpenAI

from masms_api.config import get_settings

logger = logging.getLogger(__name__)

_TOKEN = re.compile(r"[a-z0-9_]+", re.IGNORECASE)


class KnowledgeRetrievalAdapter:
    """Default stub retrieval: token overlap scoring + deterministic stub vectors."""

    model_name = "stub-embed-v1"
    dims = 8
    is_live = False

    def embed_stub(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        # Map bytes to [0,1) floats — deterministic, not semantic.
        return [b / 255.0 for b in digest[:8]]

    def embed(self, text: str) -> list[float] | None:
        _ = text
        return None

    def score(self, *, query: str, content: str) -> float:
        q = set(_TOKEN.findall(query.lower()))
        if not q:
            return 0.0
        c = set(_TOKEN.findall(content.lower()))
        if not c:
            return 0.0
        overlap = len(q & c)
        return overlap / float(len(q))

    def rank(
        self,
        *,
        query: str,
        candidates: list[dict[str, Any]],
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        scored: list[dict[str, Any]] = []
        for row in candidates:
            s = self.score(query=query, content=str(row.get("content_text") or ""))
            if s <= 0:
                continue
            scored.append({**row, "score": round(s, 4)})
        scored.sort(key=lambda r: (-float(r["score"]), str(r.get("chunk_id"))))
        logger.info(
            "knowledge_stub.rank query_tokens=%s candidates=%s hits=%s",
            len(_TOKEN.findall(query.lower())),
            len(candidates),
            min(limit, len(scored)),
        )
        return scored[: max(1, limit)]


class OpenAIKnowledgeRetrievalAdapter(KnowledgeRetrievalAdapter):
    """Generate embeddings for storage and pgvector similarity queries."""

    dims = 1536
    is_live = True

    def __init__(self, *, api_key: str, model_name: str) -> None:
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key)

    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.model_name,
            input=text,
            dimensions=self.dims,
        )
        if not response.data:
            raise RuntimeError("OpenAI embedding response was empty")
        return list(response.data[0].embedding)


def get_retrieval_adapter() -> KnowledgeRetrievalAdapter:
    settings = get_settings()
    if settings.openai_api_key and settings.embedding_model:
        return OpenAIKnowledgeRetrievalAdapter(
            api_key=settings.openai_api_key,
            model_name=settings.embedding_model,
        )
    return KnowledgeRetrievalAdapter()
