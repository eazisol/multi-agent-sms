"""Stub embedding + keyword retrieval adapter (MOD-370 M1).

A live embedding model / pgvector cluster is NOT required.
"""

from __future__ import annotations

import hashlib
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

_TOKEN = re.compile(r"[a-z0-9_]+", re.IGNORECASE)


class KnowledgeRetrievalAdapter:
    """Default stub retrieval: token overlap scoring + deterministic stub vectors."""

    model_name = "stub-embed-v1"
    dims = 8

    def embed_stub(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        # Map bytes to [0,1) floats — deterministic, not semantic.
        return [b / 255.0 for b in digest[: self.dims]]

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


def get_retrieval_adapter() -> KnowledgeRetrievalAdapter:
    return KnowledgeRetrievalAdapter()
