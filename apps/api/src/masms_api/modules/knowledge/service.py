"""Knowledge application service (MOD-370)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.knowledge import domain
from masms_api.modules.knowledge.models import (
    KnowledgeChunk,
    KnowledgeConflict,
    KnowledgeEmbedding,
    KnowledgeItem,
    KnowledgePermission,
    KnowledgeUsageLog,
    KnowledgeVersion,
)
from masms_api.modules.knowledge.retrieval_adapter import (
    KnowledgeRetrievalAdapter,
    get_retrieval_adapter,
)
from masms_api.modules.knowledge.schemas import (
    ActivateVersion,
    ConflictCreate,
    ConflictResolve,
    ItemCreate,
    PermissionCreate,
    SearchRequest,
    VersionCreate,
)
from masms_api.observability.writer import ObservabilityWriter


def _chunk_text(body: str, *, max_chars: int = 800) -> list[str]:
    text = body.strip()
    if not text:
        return []
    parts: list[str] = []
    start = 0
    while start < len(text):
        parts.append(text[start : start + max_chars])
        start += max_chars
    return parts


class KnowledgeService:
    def __init__(
        self,
        db: Session,
        ctx: RequestContext,
        retrieval: KnowledgeRetrievalAdapter | None = None,
    ) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        self.retrieval = retrieval or get_retrieval_adapter()
        apply_tenant_rls(db, ctx.organization_id)

    def create_item(self, data: ItemCreate) -> KnowledgeItem:
        existing = self.db.scalar(
            select(KnowledgeItem).where(
                KnowledgeItem.organization_id == self.ctx.organization_id,
                KnowledgeItem.code == data.code,
            )
        )
        if existing is not None:
            raise ConflictError(f"Knowledge item code '{data.code}' already exists")
        row = KnowledgeItem(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            code=data.code.strip(),
            title=data.title.strip(),
            description=data.description,
            status="draft",
            classification=data.classification,
            owner_actor_id=data.owner_actor_id or self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        # Default org-wide allow retrieve
        self.uow.add(
            KnowledgePermission(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                item_id=row.id,
                effect="allow",
                principal_type="organization",
                principal_id=None,
                project_id=data.project_id,
                can_retrieve=True,
                can_manage=True,
                created_by_actor_id=self.ctx.actor_id,
            )
        )
        self.obs.write_audit(
            action="kn_item_create",
            entity_type="kn_item",
            entity_id=row.id,
            payload={
                "code": row.code,
                "project_id": str(data.project_id) if data.project_id else None,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="kn_item",
            aggregate_id=row.id,
            event_type="knowledge.item.created",
            payload={"item_id": str(row.id), "code": row.code},
            correlation_id=self.ctx.correlation_id,
            project_id=data.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_items(
        self,
        *,
        status: str | None = None,
        project_id: UUID | None = None,
        q: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[KnowledgeItem], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(KnowledgeItem).where(
            KnowledgeItem.organization_id == self.ctx.organization_id
        )
        if status:
            stmt = stmt.where(KnowledgeItem.status == status)
        if project_id is not None:
            stmt = stmt.where(
                or_(
                    KnowledgeItem.project_id == project_id,
                    KnowledgeItem.project_id.is_(None),
                )
            )
        if q:
            like = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(KnowledgeItem.code.ilike(like), KnowledgeItem.title.ilike(like))
            )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(KnowledgeItem.updated_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def get_item(self, item_id: UUID) -> KnowledgeItem:
        row = self.db.get(KnowledgeItem, item_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Knowledge item not found")
        return row

    def create_version(self, item_id: UUID, data: VersionCreate) -> KnowledgeVersion:
        item = self.get_item(item_id)
        next_number = (
            self.db.scalar(
                select(func.coalesce(func.max(KnowledgeVersion.version_number), 0)).where(
                    KnowledgeVersion.item_id == item.id,
                    KnowledgeVersion.organization_id == self.ctx.organization_id,
                )
            )
            or 0
        ) + 1
        row = KnowledgeVersion(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            item_id=item.id,
            version_number=next_number,
            status="draft",
            body_text=data.body_text,
            change_summary=data.change_summary,
            effective_from=data.effective_from,
            effective_to=data.effective_to,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="kn_version_create",
            entity_type="kn_version",
            entity_id=row.id,
            payload={"item_id": str(item.id), "version_number": next_number},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_versions(self, item_id: UUID | None = None) -> list[KnowledgeVersion]:
        stmt = select(KnowledgeVersion).where(
            KnowledgeVersion.organization_id == self.ctx.organization_id
        )
        if item_id is not None:
            self.get_item(item_id)
            stmt = stmt.where(KnowledgeVersion.item_id == item_id)
        return list(self.db.scalars(stmt.order_by(KnowledgeVersion.version_number.desc())))

    def activate_version(
        self,
        version_id: UUID,
        data: ActivateVersion | None = None,
    ) -> KnowledgeVersion:
        data = data or ActivateVersion()
        row = self.db.get(KnowledgeVersion, version_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Knowledge version not found")
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        domain.assert_version_transition(from_status=row.status, to_status="active")

        # Supersede other active versions for the same item
        for other in self.db.scalars(
            select(KnowledgeVersion).where(
                KnowledgeVersion.organization_id == self.ctx.organization_id,
                KnowledgeVersion.item_id == row.item_id,
                KnowledgeVersion.status == "active",
                KnowledgeVersion.id != row.id,
            )
        ):
            domain.assert_version_transition(from_status="active", to_status="superseded")
            other.status = "superseded"
            other.version += 1
            other.updated_at = datetime.now(UTC)

        row.status = "active"
        row.approved_by_actor_id = self.ctx.actor_id
        row.version += 1
        row.updated_at = datetime.now(UTC)
        if row.effective_from is None:
            row.effective_from = datetime.now(UTC)

        item = self.get_item(row.item_id)
        item.status = "approved"
        item.updated_by_actor_id = self.ctx.actor_id
        item.updated_at = datetime.now(UTC)

        # Rebuild chunks + stub embeddings
        for old in self.db.scalars(
            select(KnowledgeChunk).where(KnowledgeChunk.version_id == row.id)
        ):
            for emb in self.db.scalars(
                select(KnowledgeEmbedding).where(KnowledgeEmbedding.chunk_id == old.id)
            ):
                self.db.delete(emb)
            self.db.delete(old)

        for idx, part in enumerate(_chunk_text(row.body_text)):
            chunk = KnowledgeChunk(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                item_id=row.item_id,
                version_id=row.id,
                chunk_index=idx,
                content_text=part,
                token_estimate=max(1, len(part.split())),
            )
            self.uow.add(chunk)
            self.uow.add(
                KnowledgeEmbedding(
                    id=uuid4(),
                    organization_id=self.ctx.organization_id,
                    chunk_id=chunk.id,
                    model_name=self.retrieval.model_name,
                    dims=self.retrieval.dims,
                    vector_stub=self.retrieval.embed_stub(part),
                    embedding=self.retrieval.embed(part),
                )
            )

        self.obs.write_audit(
            action="kn_version_activate",
            entity_type="kn_version",
            entity_id=row.id,
            payload={"item_id": str(row.item_id), "version_number": row.version_number},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="kn_version",
            aggregate_id=row.id,
            event_type="knowledge.version.activated",
            payload={
                "version_id": str(row.id),
                "item_id": str(row.item_id),
                "version_number": row.version_number,
            },
            correlation_id=self.ctx.correlation_id,
            project_id=item.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_chunks(self, version_id: UUID) -> list[KnowledgeChunk]:
        version = self.db.get(KnowledgeVersion, version_id)
        if version is None or version.organization_id != self.ctx.organization_id:
            raise NotFoundError("Knowledge version not found")
        return list(
            self.db.scalars(
                select(KnowledgeChunk)
                .where(
                    KnowledgeChunk.organization_id == self.ctx.organization_id,
                    KnowledgeChunk.version_id == version_id,
                )
                .order_by(KnowledgeChunk.chunk_index.asc())
            )
        )

    def add_permission(self, item_id: UUID, data: PermissionCreate) -> KnowledgePermission:
        self.get_item(item_id)
        domain.assert_permission_effect(data.effect)
        row = KnowledgePermission(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            item_id=item_id,
            effect=data.effect,
            principal_type=data.principal_type,
            principal_id=data.principal_id,
            project_id=data.project_id,
            can_retrieve=data.can_retrieve,
            can_manage=data.can_manage,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="kn_permission_create",
            entity_type="kn_permission",
            entity_id=row.id,
            payload={"item_id": str(item_id), "effect": data.effect},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_permissions(self, item_id: UUID) -> list[KnowledgePermission]:
        self.get_item(item_id)
        return list(
            self.db.scalars(
                select(KnowledgePermission).where(
                    KnowledgePermission.organization_id == self.ctx.organization_id,
                    KnowledgePermission.item_id == item_id,
                )
            )
        )

    def _is_allowed(
        self,
        *,
        item: KnowledgeItem,
        project_id: UUID | None,
        permissions: list[KnowledgePermission],
    ) -> bool:
        """Deny overrides allow; default deny if no matching allow."""
        relevant = [
            p
            for p in permissions
            if p.item_id == item.id
            and (p.project_id is None or p.project_id == project_id or project_id is None)
        ]
        if any(p.effect == "deny" and p.can_retrieve for p in relevant):
            # explicit deny on retrieve
            deny_hits = [p for p in relevant if p.effect == "deny"]
            if deny_hits:
                return False
        allows = [p for p in relevant if p.effect == "allow" and p.can_retrieve]
        return bool(allows)

    def _effective_ok(self, version: KnowledgeVersion, *, now: datetime) -> bool:
        def _aware(value: datetime | None) -> datetime | None:
            if value is None:
                return None
            if value.tzinfo is None:
                return value.replace(tzinfo=UTC)
            return value

        eff_from = _aware(version.effective_from)
        eff_to = _aware(version.effective_to)
        from_ok = eff_from is None or eff_from <= now
        to_ok = eff_to is None or eff_to >= now
        return domain.is_retrievable_version(
            status=version.status, effective_from_ok=from_ok, effective_to_ok=to_ok
        )

    @property
    def live_search_enabled(self) -> bool:
        return self.retrieval.is_live and self.db.get_bind().dialect.name == "postgresql"

    def _rank_with_pgvector(
        self,
        *,
        query: str,
        candidates: list[dict[str, Any]],
        limit: int,
    ) -> list[dict[str, Any]]:
        query_embedding = self.retrieval.embed(query)
        if not query_embedding:
            return []
        by_chunk: dict[UUID, dict[str, Any]] = {
            candidate["chunk_id"]: candidate
            for candidate in candidates
            if isinstance(candidate.get("chunk_id"), UUID)
        }
        if not by_chunk:
            return []
        distance = KnowledgeEmbedding.embedding.cosine_distance(query_embedding)
        rows = self.db.execute(
            select(
                KnowledgeEmbedding.chunk_id,
                distance.label("distance"),
            )
            .where(
                KnowledgeEmbedding.organization_id == self.ctx.organization_id,
                KnowledgeEmbedding.chunk_id.in_(list(by_chunk)),
                KnowledgeEmbedding.embedding.is_not(None),
            )
            .order_by(distance)
            .limit(max(limit * 3, limit))
        ).all()
        ranked: list[dict[str, Any]] = []
        for chunk_id, raw_distance in rows:
            candidate = by_chunk.get(chunk_id)
            if candidate is None:
                continue
            ranked.append(
                {
                    **candidate,
                    "score": round(max(0.0, 1.0 - float(raw_distance)), 4),
                }
            )
        return ranked

    def search(self, data: SearchRequest) -> list[dict[str, Any]]:
        now = datetime.now(UTC)
        items = list(
            self.db.scalars(
                select(KnowledgeItem).where(
                    KnowledgeItem.organization_id == self.ctx.organization_id,
                    KnowledgeItem.status == "approved",
                )
            )
        )
        permissions = list(
            self.db.scalars(
                select(KnowledgePermission).where(
                    KnowledgePermission.organization_id == self.ctx.organization_id
                )
            )
        )
        versions = list(
            self.db.scalars(
                select(KnowledgeVersion).where(
                    KnowledgeVersion.organization_id == self.ctx.organization_id,
                    KnowledgeVersion.status == "active",
                )
            )
        )
        version_by_item = {v.item_id: v for v in versions}
        chunks = list(
            self.db.scalars(
                select(KnowledgeChunk).where(
                    KnowledgeChunk.organization_id == self.ctx.organization_id
                )
            )
        )

        # AC-002: when project_id set, prefer project-scoped items over generic org ones
        # for the same code by ranking project hits first (score boost).
        candidates: list[dict[str, Any]] = []
        for item in items:
            if data.project_id is not None and item.project_id not in (None, data.project_id):
                continue
            if not self._is_allowed(item=item, project_id=data.project_id, permissions=permissions):
                continue
            version = version_by_item.get(item.id)
            if version is None or not self._effective_ok(version, now=now):
                continue
            for chunk in chunks:
                if chunk.version_id != version.id:
                    continue
                scope_boost = 0.25 if (
                    data.project_id is not None and item.project_id == data.project_id
                ) else 0.0
                candidates.append(
                    {
                        "item_id": item.id,
                        "item_code": item.code,
                        "item_title": item.title,
                        "version_id": version.id,
                        "version_number": version.version_number,
                        "chunk_id": chunk.id,
                        "chunk_index": chunk.chunk_index,
                        "content_text": chunk.content_text,
                        "project_id": item.project_id,
                        "scope_boost": scope_boost,
                    }
                )

        if self.live_search_enabled:
            ranked = self._rank_with_pgvector(
                query=data.query,
                candidates=candidates,
                limit=data.limit,
            )
        else:
            ranked = self.retrieval.rank(
                query=data.query,
                candidates=candidates,
                limit=data.limit,
            )
        # Apply project boost after semantic or fallback rank.
        for hit in ranked:
            hit["score"] = round(float(hit["score"]) + float(hit.get("scope_boost") or 0), 4)
        ranked.sort(key=lambda r: (-float(r["score"]), str(r["chunk_id"])))
        ranked = ranked[: data.limit]

        # Record usage + build citations (AC-001)
        results: list[dict[str, Any]] = []
        for hit in ranked:
            citation = (
                f"{hit['item_code']}@v{hit['version_number']}#chunk-{hit['chunk_index']}"
            )
            self.uow.add(
                KnowledgeUsageLog(
                    id=uuid4(),
                    organization_id=self.ctx.organization_id,
                    project_id=data.project_id,
                    item_id=hit["item_id"],
                    version_id=hit["version_id"],
                    chunk_id=hit["chunk_id"],
                    query_text=data.query[:2000],
                    score=float(hit["score"]),
                    actor_id=self.ctx.actor_id,
                    correlation_id=self.ctx.correlation_id,
                )
            )
            results.append(
                {
                    **hit,
                    "source_citation": citation,
                }
            )
        if results:
            self.obs.write_audit(
                action="kn_search",
                entity_type="kn_item",
                entity_id=results[0]["item_id"],
                payload={"query_len": len(data.query), "hits": len(results)},
            )
            enqueue_outbox(
                self.db,
                organization_id=self.ctx.organization_id,
                aggregate_type="kn_item",
                aggregate_id=results[0]["item_id"],
                event_type="knowledge.search.completed",
                payload={"hits": len(results)},
                correlation_id=self.ctx.correlation_id,
                project_id=data.project_id,
            )
            self.uow.commit()
        return results

    def create_conflict(self, data: ConflictCreate) -> KnowledgeConflict:
        for iid, vid in (
            (data.item_id_a, data.version_id_a),
            (data.item_id_b, data.version_id_b),
        ):
            self.get_item(iid)
            version = self.db.get(KnowledgeVersion, vid)
            if version is None or version.organization_id != self.ctx.organization_id:
                raise NotFoundError("Knowledge version not found for conflict")
            if version.item_id != iid:
                raise ValidationAppError("version does not belong to item in conflict")
        row = KnowledgeConflict(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            item_id_a=data.item_id_a,
            version_id_a=data.version_id_a,
            item_id_b=data.item_id_b,
            version_id_b=data.version_id_b,
            status="open",
            reason=data.reason,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="kn_conflict_open",
            entity_type="kn_conflict",
            entity_id=row.id,
            payload={"reason": data.reason},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="kn_conflict",
            aggregate_id=row.id,
            event_type="knowledge.conflict.opened",
            payload={"conflict_id": str(row.id)},
            correlation_id=self.ctx.correlation_id,
            project_id=data.project_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def resolve_conflict(self, conflict_id: UUID, data: ConflictResolve) -> KnowledgeConflict:
        row = self.db.get(KnowledgeConflict, conflict_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Knowledge conflict not found")
        domain.assert_conflict_status(data.status)
        if data.status not in {"resolved", "dismissed"}:
            raise ValidationAppError("Conflict resolve status must be resolved or dismissed")
        if row.status != "open":
            raise ConflictError(f"Conflict is not open (status={row.status})")
        row.status = data.status
        row.resolution_notes = data.resolution_notes
        row.resolved_by_actor_id = self.ctx.actor_id
        row.resolved_at = datetime.now(UTC)
        self.obs.write_audit(
            action="kn_conflict_resolve",
            entity_type="kn_conflict",
            entity_id=row.id,
            payload={"status": data.status},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_conflicts(self, *, status: str | None = None) -> list[KnowledgeConflict]:
        stmt = select(KnowledgeConflict).where(
            KnowledgeConflict.organization_id == self.ctx.organization_id
        )
        if status:
            stmt = stmt.where(KnowledgeConflict.status == status)
        return list(self.db.scalars(stmt.order_by(KnowledgeConflict.created_at.desc())))

    def list_usage_logs(
        self,
        *,
        item_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[KnowledgeUsageLog], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(KnowledgeUsageLog).where(
            KnowledgeUsageLog.organization_id == self.ctx.organization_id
        )
        if item_id is not None:
            stmt = stmt.where(KnowledgeUsageLog.item_id == item_id)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(KnowledgeUsageLog.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)
