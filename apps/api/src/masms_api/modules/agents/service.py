"""Agent runtime application service (MOD-360)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, NotFoundError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.agents import domain
from masms_api.modules.agents.langgraph_adapter import LangGraphAdapter, get_langgraph_adapter
from masms_api.modules.agents.models import (
    AgentDefinition,
    AgentEvaluation,
    AgentReview,
    AgentRun,
    ContextProfile,
    PromptVersion,
    ToolPolicy,
)
from masms_api.modules.agents.schemas import (
    ContextProfileCreate,
    EvaluationCreate,
    FailRun,
    PromptVersionCreate,
    ReviewCreate,
    RunCreate,
    ToolPolicyCreate,
)
from masms_api.modules.knowledge.schemas import SearchRequest
from masms_api.modules.knowledge.service import KnowledgeService
from masms_api.observability.writer import ObservabilityWriter


def _provider_failure_code(exc: Exception) -> str:
    """Map provider failures to a safe, non-secret-bearing category."""
    name = type(exc).__name__.lower()
    if "authentication" in name:
        return "provider_authentication_failed"
    if "rate" in name and "limit" in name:
        return "provider_rate_limited"
    if "timeout" in name:
        return "provider_timeout"
    if "apiresponsevalidation" in name or "validation" in name:
        return "provider_invalid_response"
    return "provider_unavailable"


class AgentRuntimeService:
    def __init__(
        self,
        db: Session,
        ctx: RequestContext,
        langgraph: LangGraphAdapter | None = None,
        knowledge: KnowledgeService | None = None,
    ) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        self.langgraph = langgraph or get_langgraph_adapter()
        self.knowledge = knowledge or KnowledgeService(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def ensure_definitions(self) -> list[AgentDefinition]:
        existing = list(
            self.db.scalars(
                select(AgentDefinition).where(
                    AgentDefinition.organization_id == self.ctx.organization_id
                )
            )
        )
        by_code = {row.code: row for row in existing}
        created = False
        for code in sorted(domain.ALLOWED_CODES):
            if code in by_code:
                continue
            row = AgentDefinition(
                id=uuid4(),
                organization_id=self.ctx.organization_id,
                code=code,
                title=domain.AGENT_TITLES[code],
                description=f"Approved MASMS agent: {domain.AGENT_TITLES[code]}",
                status="active",
                department_code=domain.AGENT_DEPARTMENTS[code],
                authority_level="assist",
                created_by_actor_id=self.ctx.actor_id,
            )
            self.uow.add(row)
            by_code[code] = row
            created = True
        if created:
            self.obs.write_audit(
                action="agr_definitions_seeded",
                entity_type="agr_agent_definition",
                entity_id=self.ctx.organization_id,
                payload={"codes": sorted(by_code.keys())},
            )
            self.uow.commit()
        return [by_code[c] for c in sorted(domain.ALLOWED_CODES)]

    def list_definitions(self) -> list[AgentDefinition]:
        return self.ensure_definitions()

    def _get_definition(self, code: str) -> AgentDefinition:
        domain.assert_allowed_agent_code(code)
        definitions = {d.code: d for d in self.ensure_definitions()}
        return definitions[code]

    def create_prompt_version(self, code: str, data: PromptVersionCreate) -> PromptVersion:
        definition = self._get_definition(code)
        next_number = (
            self.db.scalar(
                select(func.coalesce(func.max(PromptVersion.version_number), 0)).where(
                    PromptVersion.definition_id == definition.id,
                    PromptVersion.organization_id == self.ctx.organization_id,
                )
            )
            or 0
        ) + 1
        row = PromptVersion(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            definition_id=definition.id,
            version_number=next_number,
            status="draft",
            prompt_text=data.prompt_text,
            model_name=data.model_name,
            temperature=data.temperature,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="agr_prompt_create",
            entity_type="agr_prompt_version",
            entity_id=row.id,
            payload={"agent_code": code, "version_number": next_number},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_prompt_versions(self, definition_id: UUID | None = None) -> list[PromptVersion]:
        stmt = select(PromptVersion).where(
            PromptVersion.organization_id == self.ctx.organization_id
        )
        if definition_id is not None:
            stmt = stmt.where(PromptVersion.definition_id == definition_id)
        return list(self.db.scalars(stmt.order_by(PromptVersion.version_number.desc())))

    def activate_prompt_version(self, version_id: UUID) -> PromptVersion:
        row = self.db.get(PromptVersion, version_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Prompt version not found")
        for other in self.db.scalars(
            select(PromptVersion).where(
                PromptVersion.definition_id == row.definition_id,
                PromptVersion.organization_id == self.ctx.organization_id,
                PromptVersion.status == "active",
                PromptVersion.id != row.id,
            )
        ):
            other.status = "retired"
            other.updated_at = datetime.now(UTC)
        row.status = "active"
        row.updated_at = datetime.now(UTC)
        self.obs.write_audit(
            action="agr_prompt_activate",
            entity_type="agr_prompt_version",
            entity_id=row.id,
            payload={"version_number": row.version_number},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="agr_prompt_version",
            aggregate_id=row.id,
            event_type="agent_runtime.prompt.activated",
            payload={"version_id": str(row.id)},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def create_tool_policy(self, code: str, data: ToolPolicyCreate) -> ToolPolicy:
        definition = self._get_definition(code)
        existing = self.db.scalar(
            select(ToolPolicy).where(
                ToolPolicy.organization_id == self.ctx.organization_id,
                ToolPolicy.definition_id == definition.id,
                ToolPolicy.policy_key == data.policy_key,
            )
        )
        if existing is not None:
            raise ConflictError(f"Tool policy '{data.policy_key}' already exists")
        row = ToolPolicy(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            definition_id=definition.id,
            policy_key=data.policy_key,
            status="active",
            allowed_tools=list(data.allowed_tools),
            denied_tools=list(data.denied_tools),
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="agr_tool_policy_create",
            entity_type="agr_tool_policy",
            entity_id=row.id,
            payload={"agent_code": code, "policy_key": data.policy_key},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_tool_policies(self, definition_id: UUID | None = None) -> list[ToolPolicy]:
        stmt = select(ToolPolicy).where(ToolPolicy.organization_id == self.ctx.organization_id)
        if definition_id is not None:
            stmt = stmt.where(ToolPolicy.definition_id == definition_id)
        return list(self.db.scalars(stmt))

    def create_context_profile(self, code: str, data: ContextProfileCreate) -> ContextProfile:
        definition = self._get_definition(code)
        existing = self.db.scalar(
            select(ContextProfile).where(
                ContextProfile.organization_id == self.ctx.organization_id,
                ContextProfile.definition_id == definition.id,
                ContextProfile.code == data.code,
            )
        )
        if existing is not None:
            raise ConflictError(f"Context profile '{data.code}' already exists")
        row = ContextProfile(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            definition_id=definition.id,
            code=data.code,
            min_sources=data.min_sources,
            max_tokens=data.max_tokens,
            include_rules=dict(data.include_rules),
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="agr_context_profile_create",
            entity_type="agr_context_profile",
            entity_id=row.id,
            payload={"agent_code": code, "code": data.code},
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_context_profiles(self, definition_id: UUID | None = None) -> list[ContextProfile]:
        stmt = select(ContextProfile).where(
            ContextProfile.organization_id == self.ctx.organization_id
        )
        if definition_id is not None:
            stmt = stmt.where(ContextProfile.definition_id == definition_id)
        return list(self.db.scalars(stmt))

    def _ensure_active_prompt(self, definition: AgentDefinition) -> PromptVersion:
        active = self.db.scalar(
            select(PromptVersion).where(
                PromptVersion.organization_id == self.ctx.organization_id,
                PromptVersion.definition_id == definition.id,
                PromptVersion.status == "active",
            )
        )
        if active is not None:
            return active
        draft = PromptVersionCreate(
            prompt_text=f"Stub system prompt for {definition.code} (MOD-360 M1).",
            model_name="stub-model",
            temperature=0.0,
        )
        created = self.create_prompt_version(definition.code, draft)
        return self.activate_prompt_version(created.id)

    def _ensure_default_tool_policy(self, definition: AgentDefinition) -> ToolPolicy | None:
        row = self.db.scalar(
            select(ToolPolicy).where(
                ToolPolicy.organization_id == self.ctx.organization_id,
                ToolPolicy.definition_id == definition.id,
                ToolPolicy.policy_key == "default",
                ToolPolicy.status == "active",
            )
        )
        if row is not None:
            return row
        return self.create_tool_policy(
            definition.code,
            ToolPolicyCreate(
                policy_key="default",
                allowed_tools=["read_entity", "search_knowledge"],
                denied_tools=["write_database", "expose_secret"],
            ),
        )

    def start_run(self, data: RunCreate) -> AgentRun:
        definition = self._get_definition(data.agent_code)

        if data.idempotency_key:
            prior = self.db.scalar(
                select(AgentRun).where(
                    AgentRun.organization_id == self.ctx.organization_id,
                    AgentRun.idempotency_key == data.idempotency_key,
                )
            )
            if prior is not None:
                return prior

        if data.prompt_version_id is not None:
            prompt = self.db.get(PromptVersion, data.prompt_version_id)
            if (
                prompt is None
                or prompt.organization_id != self.ctx.organization_id
                or prompt.definition_id != definition.id
            ):
                raise NotFoundError("Prompt version not found for agent")
        else:
            prompt = self._ensure_active_prompt(definition)

        tool_policy: ToolPolicy | None = None
        if data.tool_policy_id is not None:
            tool_policy = self.db.get(ToolPolicy, data.tool_policy_id)
            if (
                tool_policy is None
                or tool_policy.organization_id != self.ctx.organization_id
            ):
                raise NotFoundError("Tool policy not found")
        else:
            tool_policy = self._ensure_default_tool_policy(definition)

        context_profile: ContextProfile | None = None
        if data.context_profile_id is not None:
            context_profile = self.db.get(ContextProfile, data.context_profile_id)
            if (
                context_profile is None
                or context_profile.organization_id != self.ctx.organization_id
            ):
                raise NotFoundError("Context profile not found")

        run_id = uuid4()
        row = AgentRun(
            id=run_id,
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            definition_id=definition.id,
            agent_code=definition.code,
            prompt_version_id=prompt.id,
            tool_policy_id=tool_policy.id if tool_policy else None,
            context_profile_id=context_profile.id if context_profile else None,
            related_entity_type=data.related_entity_type,
            related_entity_id=data.related_entity_id,
            status="running",
            model_name=prompt.model_name,
            prompt_version_number=prompt.version_number,
            input_json=dict(data.input_json),
            output_json={},
            sources_json=[],
            tools_used_json=[],
            review_required=False,
            owner_actor_id=data.owner_actor_id or self.ctx.actor_id,
            correlation_id=self.ctx.correlation_id,
            idempotency_key=data.idempotency_key,
            version=1,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="agr_run_start",
            entity_type="agr_agent_run",
            entity_id=row.id,
            payload={"agent_code": definition.code, "status": "running"},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="agr_agent_run",
            aggregate_id=row.id,
            event_type="agent_runtime.run.started",
            payload={"run_id": str(row.id), "agent_code": definition.code},
            correlation_id=row.correlation_id,
        )
        self.uow.commit()

        try:
            model_input = self._build_model_input(
                agent_code=definition.code,
                input_json=data.input_json,
                project_id=data.project_id,
                max_sources=context_profile.min_sources if context_profile else 5,
            )
            lg_id = self.langgraph.start_run(
                agent_code=definition.code,
                run_id=str(run_id),
                input_payload=model_input,
            )
            result = self.langgraph.invoke(
                agent_code=definition.code,
                prompt_version=prompt.version_number,
                model_name=prompt.model_name,
                input_payload=model_input,
                allowed_tools=list(tool_policy.allowed_tools) if tool_policy else [],
                max_output_tokens=context_profile.max_tokens if context_profile else 1200,
            )
        except Exception as exc:
            row.status = "failed"
            row.version += 1
            row.updated_by_actor_id = self.ctx.actor_id
            row.updated_at = datetime.now(UTC)
            row.output_json = {
                "failure": {
                    "code": _provider_failure_code(exc),
                    "message": "The agent provider could not complete this recommendation.",
                }
            }
            self.obs.write_audit(
                action="agr_run_provider_failed",
                entity_type="agr_agent_run",
                entity_id=row.id,
                payload={
                    "agent_code": definition.code,
                    "failure_code": _provider_failure_code(exc),
                },
            )
            enqueue_outbox(
                self.db,
                organization_id=self.ctx.organization_id,
                aggregate_type="agr_agent_run",
                aggregate_id=row.id,
                event_type="agent_runtime.run.failed",
                payload={"run_id": str(row.id), "failure_code": _provider_failure_code(exc)},
                correlation_id=row.correlation_id,
            )
            self.uow.commit()
            self.db.refresh(row)
            return row

        confidence = float(result.get("confidence", 0.0))
        review_flag = bool(data.input_json.get("force_review")) or (
            confidence < domain.LOW_CONFIDENCE_THRESHOLD
        )
        final_status = domain.resolve_run_status_after_stub(
            confidence=confidence, review_required_flag=review_flag
        )
        domain.assert_run_transition(from_status="pending", to_status="running")
        domain.assert_run_transition(from_status="running", to_status=final_status)

        now = datetime.now(UTC)
        row.status = final_status
        row.langgraph_run_id = lg_id
        row.model_name = str(result.get("model_name") or prompt.model_name)
        row.output_json = {
            "summary": result.get("summary"),
            "stub": bool(result.get("stub", True)),
            "raw": {k: v for k, v in result.items() if k != "summary"},
        }
        row.sources_json = list(result.get("sources") or [])
        row.tools_used_json = list(result.get("tools_used") or [])
        row.confidence = confidence
        row.cost_units = float(result.get("cost_units") or 0.0)
        row.review_required = final_status == "review_required"
        row.updated_at = now
        row.closed_at = now if final_status == "completed" else None
        self.obs.write_audit(
            action="agr_run_completed",
            entity_type="agr_agent_run",
            entity_id=row.id,
            payload={
                "agent_code": definition.code,
                "status": final_status,
                "confidence": confidence,
                "langgraph_run_id": lg_id,
            },
        )
        event_done = (
            "agent_runtime.run.review_required"
            if final_status == "review_required"
            else "agent_runtime.run.completed"
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="agr_agent_run",
            aggregate_id=row.id,
            event_type=event_done,
            payload={"run_id": str(row.id), "status": final_status},
            correlation_id=row.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def _build_model_input(
        self,
        *,
        agent_code: str,
        input_json: dict[str, Any],
        project_id: UUID | None,
        max_sources: int,
    ) -> dict[str, Any]:
        payload = dict(input_json)
        if agent_code != "query_intake_agent":
            return payload

        payload["sources"] = []
        query = self._knowledge_query(input_json)
        if query is None:
            return payload
        limit = max(1, min(max_sources or 5, 10))
        hits = self.knowledge.search(
            SearchRequest(query=query, project_id=project_id, limit=limit)
        )
        payload["sources"] = [
            {"type": "knowledge", "ref": str(hit["source_citation"])} for hit in hits
        ]
        payload["retrieved_knowledge"] = [
            {
                "source_citation": str(hit["source_citation"]),
                "content_text": str(hit["content_text"]),
                "untrusted_content": True,
            }
            for hit in hits
        ]
        return payload

    @staticmethod
    def _knowledge_query(input_json: dict[str, Any]) -> str | None:
        for key in ("knowledge_query", "query", "summary", "note"):
            value = input_json.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return None
    def get_run(self, run_id: UUID) -> AgentRun:
        row = self.db.get(AgentRun, run_id)
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Agent run not found")
        return row

    def list_runs(
        self,
        *,
        status: str | None = None,
        q: str | None = None,
        agent_code: str | None = None,
        project_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[AgentRun], PageMeta]:
        limit, offset = normalize_paging(limit=limit, offset=offset)
        stmt = select(AgentRun).where(AgentRun.organization_id == self.ctx.organization_id)
        if status:
            stmt = stmt.where(AgentRun.status == status)
        if agent_code:
            stmt = stmt.where(AgentRun.agent_code == agent_code)
        if project_id is not None:
            stmt = stmt.where(AgentRun.project_id == project_id)
        if q:
            like = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(
                    AgentRun.agent_code.ilike(like),
                    AgentRun.related_entity_type.ilike(like),
                    AgentRun.langgraph_run_id.ilike(like),
                )
            )
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        items = list(
            self.db.scalars(
                stmt.order_by(AgentRun.created_at.desc()).limit(limit).offset(offset)
            )
        )
        return items, build_page_meta(total=total, limit=limit, offset=offset)

    def fail_run(self, run_id: UUID, data: FailRun) -> AgentRun:
        row = self.get_run(run_id)
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        domain.assert_run_transition(from_status=row.status, to_status="failed")
        row.status = "failed"
        row.review_required = False
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        row.updated_at = datetime.now(UTC)
        row.output_json = {
            **(row.output_json or {}),
            "failure_reason": data.reason,
        }
        self.obs.write_audit(
            action="agr_run_fail",
            entity_type="agr_agent_run",
            entity_id=row.id,
            payload={"reason": data.reason},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="agr_agent_run",
            aggregate_id=row.id,
            event_type="agent_runtime.run.failed",
            payload={"run_id": str(row.id), "reason": data.reason},
            correlation_id=row.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def submit_review(self, run_id: UUID, data: ReviewCreate) -> AgentReview:
        row = self.get_run(run_id)
        domain.assert_expected_version(current=row.version, expected=data.expected_version)
        domain.assert_review_decision(data.decision)
        if row.status != "review_required":
            raise ConflictError("Reviews are only accepted when status is review_required")

        if data.decision == "approved":
            target = "completed"
        elif data.decision == "rejected":
            target = "failed"
        else:
            target = "failed"

        domain.assert_run_transition(from_status=row.status, to_status=target)
        now = datetime.now(UTC)
        review = AgentReview(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            run_id=row.id,
            status=data.decision,
            reviewer_actor_id=self.ctx.actor_id,
            decision_reason=data.decision_reason,
            outcome_json=dict(data.outcome_json),
        )
        self.uow.add(review)
        row.status = target
        row.review_required = False
        row.version += 1
        row.updated_by_actor_id = self.ctx.actor_id
        row.updated_at = now
        if target in domain.TERMINAL_RUN_STATUSES:
            row.closed_at = now
        self.obs.write_audit(
            action="agr_run_reviewed",
            entity_type="agr_agent_run",
            entity_id=row.id,
            payload={"decision": data.decision, "next_status": target},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="agr_agent_run",
            aggregate_id=row.id,
            event_type="agent_runtime.run.reviewed",
            payload={
                "run_id": str(row.id),
                "decision": data.decision,
                "status": target,
            },
            correlation_id=row.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(review)
        return review

    def list_reviews(self, run_id: UUID) -> list[AgentReview]:
        self.get_run(run_id)
        return list(
            self.db.scalars(
                select(AgentReview)
                .where(
                    AgentReview.organization_id == self.ctx.organization_id,
                    AgentReview.run_id == run_id,
                )
                .order_by(AgentReview.created_at.desc())
            )
        )

    def create_evaluation(self, run_id: UUID, data: EvaluationCreate) -> AgentEvaluation:
        self.get_run(run_id)
        row = AgentEvaluation(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            run_id=run_id,
            score=data.score,
            rubric_code=data.rubric_code,
            notes=data.notes,
            evaluator_actor_id=self.ctx.actor_id,
            metrics_json=dict(data.metrics_json),
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="agr_run_evaluated",
            entity_type="agr_agent_evaluation",
            entity_id=row.id,
            payload={"run_id": str(run_id), "score": data.score},
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="agr_agent_run",
            aggregate_id=run_id,
            event_type="agent_runtime.run.evaluated",
            payload={"run_id": str(run_id), "score": data.score},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.db.refresh(row)
        return row

    def list_evaluations(self, run_id: UUID) -> list[AgentEvaluation]:
        self.get_run(run_id)
        return list(
            self.db.scalars(
                select(AgentEvaluation)
                .where(
                    AgentEvaluation.organization_id == self.ctx.organization_id,
                    AgentEvaluation.run_id == run_id,
                )
                .order_by(AgentEvaluation.created_at.desc())
            )
        )
