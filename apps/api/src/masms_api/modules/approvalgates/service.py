"""Approval gates application service (MOD-330)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TypedDict
from uuid import UUID, uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from masms_api.errors import (
    ConflictError,
    ForbiddenError,
    InvalidTransitionError,
    NotFoundError,
    ValidationAppError,
)
from masms_api.kernel.context import RequestContext
from masms_api.kernel.outbox import enqueue_outbox
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.approvalgates import domain
from masms_api.modules.approvalgates.models import (
    ApprovalDecision,
    ApprovalDelegation,
    ApprovalEvidence,
    ApprovalRequest,
    ApprovalStep,
    ApprovalWorkflowInstance,
    HumanOverride,
)
from masms_api.modules.approvalgates.schemas import (
    ApprovalCreate,
    DecisionCreate,
    DelegationCreate,
    EvidenceCreate,
    GateCheckRequest,
    GateCheckResponse,
    OverrideCreate,
)
from masms_api.modules.configadmin import domain as config_domain
from masms_api.modules.configadmin.models import ApprovalWorkflowConfig, ConfigurationVersion
from masms_api.observability.writer import ObservabilityWriter


class _StepSpec(TypedDict):
    order: int
    role_code: str
    required_authority_level: int
    assignee_actor_id: UUID | None



class ApprovalGatesService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_approval(self, data: ApprovalCreate) -> ApprovalRequest:
        steps_spec = self._resolve_steps(data)
        if not steps_spec:
            raise ValidationAppError("Approval requires at least one step")

        row = ApprovalRequest(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            action_code=data.action_code,
            title=data.title,
            target_entity_type=data.target_entity_type,
            target_entity_id=data.target_entity_id,
            target_version=data.target_version,
            workflow_code=data.workflow_code,
            status="pending",
            current_step_order=1,
            submitted_by_actor_id=self.ctx.actor_id,
            submitted_by_actor_kind=self.ctx.actor_kind.value,
            recommendation_source_actor_id=data.recommendation_source_actor_id,
            version=1,
            owner_actor_id=data.owner_actor_id or self.ctx.actor_id,
            created_by_actor_id=self.ctx.actor_id,
            updated_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)

        wf = ApprovalWorkflowInstance(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            approval_id=row.id,
            code=data.workflow_code or "ad_hoc",
            title=data.title,
            steps_json=steps_spec,
            configuration_version_id=self._effective_config_id(),
        )
        self.uow.add(wf)

        for idx, step in enumerate(steps_spec, start=1):
            self.uow.add(
                ApprovalStep(
                    id=uuid4(),
                    organization_id=self.ctx.organization_id,
                    approval_id=row.id,
                    step_order=idx,
                    role_code=step["role_code"],
                    required_authority_level=step["required_authority_level"],
                    status="pending",
                    assignee_actor_id=step["assignee_actor_id"],
                )
            )

        self.obs.write_audit(
            action="apr_request_create",
            entity_type="apr_request",
            entity_id=row.id,
            payload={
                "action_code": row.action_code,
                "target_entity_type": row.target_entity_type,
                "target_version": row.target_version,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="apr_request",
            aggregate_id=row.id,
            event_type="approval.submitted",
            payload={
                "action_code": row.action_code,
                "target_entity_id": str(row.target_entity_id),
                "target_version": row.target_version,
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def get_approval(self, approval_id: UUID) -> ApprovalRequest:
        return self._get_approval(approval_id)

    def list_approvals(
        self,
        *,
        status: str | None = None,
        action_code: str | None = None,
        q: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[ApprovalRequest], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [ApprovalRequest.organization_id == self.ctx.organization_id]
        if status:
            filters.append(ApprovalRequest.status == status)
        if action_code:
            filters.append(ApprovalRequest.action_code == action_code)
        if q and q.strip():
            like = f"%{q.strip()}%"
            filters.append(
                or_(
                    ApprovalRequest.title.ilike(like),
                    ApprovalRequest.action_code.ilike(like),
                )
            )
        total = (
            self.db.scalar(
                select(func.count()).select_from(ApprovalRequest).where(*filters)
            )
            or 0
        )
        rows = list(
            self.db.scalars(
                select(ApprovalRequest)
                .where(*filters)
                .order_by(ApprovalRequest.created_at.desc())
                .offset(offset)
                .limit(limit)
            )
        )
        return rows, build_page_meta(limit=limit, offset=offset, total=int(total))

    def get_workflow(self, approval_id: UUID) -> ApprovalWorkflowInstance:
        self._get_approval(approval_id)
        row = self.db.scalar(
            select(ApprovalWorkflowInstance).where(
                ApprovalWorkflowInstance.organization_id == self.ctx.organization_id,
                ApprovalWorkflowInstance.approval_id == approval_id,
            )
        )
        if row is None:
            raise NotFoundError("Approval workflow not found")
        return row

    def list_steps(self, approval_id: UUID) -> list[ApprovalStep]:
        self._get_approval(approval_id)
        return list(
            self.db.scalars(
                select(ApprovalStep)
                .where(
                    ApprovalStep.organization_id == self.ctx.organization_id,
                    ApprovalStep.approval_id == approval_id,
                )
                .order_by(ApprovalStep.step_order.asc())
            ).all()
        )

    def list_decisions(self, approval_id: UUID) -> list[ApprovalDecision]:
        self._get_approval(approval_id)
        return list(
            self.db.scalars(
                select(ApprovalDecision)
                .where(
                    ApprovalDecision.organization_id == self.ctx.organization_id,
                    ApprovalDecision.approval_id == approval_id,
                )
                .order_by(ApprovalDecision.decided_at.asc())
            ).all()
        )

    def decide(self, approval_id: UUID, data: DecisionCreate) -> ApprovalDecision:
        domain.assert_human_decider(self.ctx.actor_kind)
        approval = self._get_approval(approval_id)
        domain.assert_pending(approval.status)
        if data.expected_version is not None and approval.version != data.expected_version:
            raise ConflictError("Approval version mismatch")
        domain.assert_decision_reason(decision=data.decision, reason=data.reason)
        domain.assert_not_self_recommendation(
            actor_id=self.ctx.actor_id,
            actor_kind=self.ctx.actor_kind,
            recommendation_source_actor_id=approval.recommendation_source_actor_id,
        )

        step = self.db.scalar(
            select(ApprovalStep).where(
                ApprovalStep.organization_id == self.ctx.organization_id,
                ApprovalStep.approval_id == approval_id,
                ApprovalStep.step_order == approval.current_step_order,
            )
        )
        if step is None:
            raise NotFoundError("Current approval step not found")
        domain.assert_step_pending(step.status)

        delegation = self._find_active_delegation(
            action_code=approval.action_code, project_id=approval.project_id
        )
        authority_mode = "delegated" if delegation else "direct"
        if step.assignee_actor_id is not None and step.assignee_actor_id != self.ctx.actor_id:
            if delegation is None or delegation.from_actor_id != step.assignee_actor_id:
                raise ForbiddenError("Actor is not assigned to this approval step")

        decision = ApprovalDecision(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            approval_id=approval.id,
            step_id=step.id,
            decision=data.decision,
            actor_id=self.ctx.actor_id,
            actor_kind=self.ctx.actor_kind.value,
            authority_mode=authority_mode,
            delegation_id=delegation.id if delegation else None,
            reason=data.reason,
            decided_at=datetime.now(UTC),
        )
        self.uow.add(decision)

        if data.decision == "approve":
            step.status = "approved"
            self.uow.add(step)
            remaining = self.db.scalars(
                select(ApprovalStep).where(
                    ApprovalStep.organization_id == self.ctx.organization_id,
                    ApprovalStep.approval_id == approval_id,
                    ApprovalStep.step_order > step.step_order,
                )
            ).all()
            if remaining:
                approval.current_step_order = step.step_order + 1
            else:
                approval.status = "approved"
                approval.decided_at = decision.decided_at
        elif data.decision == "reject":
            step.status = "rejected"
            approval.status = "rejected"
            approval.decided_at = decision.decided_at
            self.uow.add(step)
        else:
            step.status = "withdrawn"
            approval.status = "withdrawn"
            approval.decided_at = decision.decided_at
            self.uow.add(step)

        approval.version += 1
        approval.updated_by_actor_id = self.ctx.actor_id
        self.uow.add(approval)

        self.obs.write_audit(
            action="apr_decision",
            entity_type="apr_request",
            entity_id=approval.id,
            payload={
                "decision": data.decision,
                "status": approval.status,
                "step_order": step.step_order,
                "authority_mode": authority_mode,
            },
        )
        if data.decision == "approve":
            event_type = (
                "approval.approved"
                if approval.status == "approved"
                else "approval.step_approved"
            )
        elif data.decision == "reject":
            event_type = "approval.rejected"
        else:
            event_type = "approval.withdrawn"
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="apr_request",
            aggregate_id=approval.id,
            event_type=event_type,
            payload={
                "decision": data.decision,
                "status": approval.status,
                "target_version": approval.target_version,
            },
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(decision)
        return decision

    def supersede(self, approval_id: UUID, *, reason: str) -> ApprovalRequest:
        """Invalidate prior approval when target material version changes."""
        approval = self._get_approval(approval_id)
        if approval.status in domain.TERMINAL_STATUSES and approval.status != "approved":
            raise InvalidTransitionError("Cannot supersede a closed non-approved request")
        if not (reason and reason.strip()):
            raise ValidationAppError("Supersede requires a reason")
        if approval.status == "superseded":
            raise ConflictError("Approval already superseded")

        approval.status = "superseded"
        approval.version += 1
        approval.updated_by_actor_id = self.ctx.actor_id
        approval.decided_at = datetime.now(UTC)
        self.uow.add(approval)
        self.obs.write_audit(
            action="apr_supersede",
            entity_type="apr_request",
            entity_id=approval.id,
            payload={"reason": reason},
        )
        self.uow.commit()
        self.uow.refresh(approval)
        return approval

    def create_delegation(self, data: DelegationCreate) -> ApprovalDelegation:
        domain.assert_human_decider(self.ctx.actor_kind)
        domain.assert_delegation_reason(data.reason)
        now = datetime.now(UTC)
        starts = data.starts_at if data.starts_at.tzinfo else data.starts_at.replace(tzinfo=UTC)
        ends = data.ends_at if data.ends_at.tzinfo else data.ends_at.replace(tzinfo=UTC)
        domain.assert_delegation_window(starts_at=starts, ends_at=ends, now=now)
        if data.to_actor_id == self.ctx.actor_id:
            raise ValidationAppError("Cannot delegate to yourself")

        row = ApprovalDelegation(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            from_actor_id=self.ctx.actor_id,
            to_actor_id=data.to_actor_id,
            action_code=data.action_code,
            reason=data.reason.strip(),
            status="active",
            starts_at=starts,
            ends_at=ends,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="apr_delegation_create",
            entity_type="apr_delegation",
            entity_id=row.id,
            payload={"to_actor_id": str(row.to_actor_id), "action_code": row.action_code},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def revoke_delegation(self, delegation_id: UUID) -> ApprovalDelegation:
        domain.assert_human_decider(self.ctx.actor_kind)
        row = self.db.scalar(
            select(ApprovalDelegation).where(
                ApprovalDelegation.id == delegation_id,
                ApprovalDelegation.organization_id == self.ctx.organization_id,
            )
        )
        if row is None:
            raise NotFoundError("Delegation not found")
        if row.status != "active":
            raise ConflictError("Delegation is not active")
        if row.from_actor_id != self.ctx.actor_id:
            raise ForbiddenError("Only the delegating actor may revoke")
        row.status = "revoked"
        row.revoked_at = datetime.now(UTC)
        row.revoked_by_actor_id = self.ctx.actor_id
        self.uow.add(row)
        self.obs.write_audit(
            action="apr_delegation_revoke",
            entity_type="apr_delegation",
            entity_id=row.id,
            payload={},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_delegations(self) -> list[ApprovalDelegation]:
        return list(
            self.db.scalars(
                select(ApprovalDelegation)
                .where(ApprovalDelegation.organization_id == self.ctx.organization_id)
                .order_by(ApprovalDelegation.created_at.desc())
            ).all()
        )

    def add_evidence(self, approval_id: UUID, data: EvidenceCreate) -> ApprovalEvidence:
        self._get_approval(approval_id)
        domain.assert_evidence_ref(data.evidence_ref)
        row = ApprovalEvidence(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            approval_id=approval_id,
            evidence_type=data.evidence_type,
            evidence_ref=data.evidence_ref.strip(),
            note=data.note,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="apr_evidence_add",
            entity_type="apr_request",
            entity_id=approval_id,
            payload={"evidence_id": str(row.id), "evidence_type": row.evidence_type},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_evidence(self, approval_id: UUID) -> list[ApprovalEvidence]:
        self._get_approval(approval_id)
        return list(
            self.db.scalars(
                select(ApprovalEvidence)
                .where(
                    ApprovalEvidence.organization_id == self.ctx.organization_id,
                    ApprovalEvidence.approval_id == approval_id,
                )
                .order_by(ApprovalEvidence.created_at.asc())
            ).all()
        )

    def create_override(self, data: OverrideCreate) -> HumanOverride:
        domain.assert_human_decider(self.ctx.actor_kind)
        domain.assert_override_reason(data.reason)
        if data.approval_id is not None:
            self._get_approval(data.approval_id)

        row = HumanOverride(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            project_id=data.project_id,
            approval_id=data.approval_id,
            action_code=data.action_code,
            target_entity_type=data.target_entity_type,
            target_entity_id=data.target_entity_id,
            target_version=data.target_version,
            reason=data.reason.strip(),
            authority_used=data.authority_used.strip(),
            retrospective_required=True,
            authorized_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="apr_override",
            entity_type="apr_override",
            entity_id=row.id,
            payload={
                "action_code": row.action_code,
                "authority_used": row.authority_used,
                "target_version": row.target_version,
            },
        )
        enqueue_outbox(
            self.db,
            organization_id=self.ctx.organization_id,
            aggregate_type="apr_override",
            aggregate_id=row.id,
            event_type="approval.override",
            payload={"action_code": row.action_code, "retrospective_required": True},
            correlation_id=self.ctx.correlation_id,
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def check_gate(self, data: GateCheckRequest) -> GateCheckResponse:
        approved = self.db.scalar(
            select(ApprovalRequest)
            .where(
                ApprovalRequest.organization_id == self.ctx.organization_id,
                ApprovalRequest.action_code == data.action_code,
                ApprovalRequest.target_entity_type == data.target_entity_type,
                ApprovalRequest.target_entity_id == data.target_entity_id,
                ApprovalRequest.target_version == data.target_version,
                ApprovalRequest.status == "approved",
            )
            .order_by(ApprovalRequest.decided_at.desc())
        )
        if approved is not None:
            return GateCheckResponse(
                allowed=True,
                reason="approved for exact target version",
                approval_id=approved.id,
                approval_status=approved.status,
            )

        override = self.db.scalar(
            select(HumanOverride)
            .where(
                HumanOverride.organization_id == self.ctx.organization_id,
                HumanOverride.action_code == data.action_code,
                HumanOverride.target_entity_type == data.target_entity_type,
                HumanOverride.target_entity_id == data.target_entity_id,
                HumanOverride.target_version == data.target_version,
            )
            .order_by(HumanOverride.created_at.desc())
        )
        if override is not None:
            return GateCheckResponse(
                allowed=True,
                reason="human override recorded for exact target version",
                approval_id=override.approval_id,
                approval_status="override",
            )

        pending = self.db.scalar(
            select(ApprovalRequest)
            .where(
                ApprovalRequest.organization_id == self.ctx.organization_id,
                ApprovalRequest.action_code == data.action_code,
                ApprovalRequest.target_entity_type == data.target_entity_type,
                ApprovalRequest.target_entity_id == data.target_entity_id,
                ApprovalRequest.target_version == data.target_version,
                ApprovalRequest.status == "pending",
            )
            .order_by(ApprovalRequest.created_at.desc())
        )
        if pending is not None:
            return GateCheckResponse(
                allowed=False,
                reason="approval pending",
                approval_id=pending.id,
                approval_status=pending.status,
            )

        return GateCheckResponse(
            allowed=False,
            reason="no approval for exact target version",
            approval_id=None,
            approval_status=None,
        )

    def assert_gate(self, data: GateCheckRequest) -> GateCheckResponse:
        result = self.check_gate(data)
        domain.assert_approved_for_action(
            approved=result.allowed,
            target_version_matches=result.allowed,
        )
        return result

    def _resolve_steps(self, data: ApprovalCreate) -> list[_StepSpec]:
        if data.steps:
            ordered: list[_StepSpec] = []
            for i, step in enumerate(data.steps, start=1):
                ordered.append(
                    {
                        "order": step.order or i,
                        "role_code": step.role_code,
                        "required_authority_level": step.required_authority_level,
                        "assignee_actor_id": step.assignee_actor_id,
                    }
                )
            return sorted(ordered, key=lambda s: s["order"])

        if not data.workflow_code:
            return [
                {
                    "order": 1,
                    "role_code": "approver",
                    "required_authority_level": 1,
                    "assignee_actor_id": None,
                }
            ]

        effective_id = self._effective_config_id()
        if effective_id is None:
            raise NotFoundError("No effective configuration for workflow_code")
        cfg = self.db.scalar(
            select(ApprovalWorkflowConfig).where(
                ApprovalWorkflowConfig.organization_id == self.ctx.organization_id,
                ApprovalWorkflowConfig.configuration_version_id == effective_id,
                ApprovalWorkflowConfig.code == data.workflow_code,
                ApprovalWorkflowConfig.status == "active",
            )
        )
        if cfg is None:
            raise NotFoundError(f"Approval workflow '{data.workflow_code}' not in effective config")
        steps: list[_StepSpec] = []
        for i, raw in enumerate(cfg.steps_json or [], start=1):
            steps.append(
                {
                    "order": int(raw.get("order") or i),
                    "role_code": str(raw.get("role") or raw.get("role_code") or "approver"),
                    "required_authority_level": int(raw.get("required_authority_level") or 1),
                    "assignee_actor_id": None,
                }
            )
        return sorted(steps, key=lambda s: s["order"])

    def _effective_config_id(self) -> UUID | None:
        row = self.db.scalar(
            select(ConfigurationVersion).where(
                ConfigurationVersion.organization_id == self.ctx.organization_id,
                ConfigurationVersion.status == config_domain.STATUS_EFFECTIVE,
            )
        )
        return row.id if row else None

    def _get_approval(self, approval_id: UUID) -> ApprovalRequest:
        row = self.db.scalar(
            select(ApprovalRequest).where(
                ApprovalRequest.id == approval_id,
                ApprovalRequest.organization_id == self.ctx.organization_id,
            )
        )
        if row is None:
            raise NotFoundError("Approval request not found")
        return row

    def _find_active_delegation(
        self, *, action_code: str, project_id: UUID | None
    ) -> ApprovalDelegation | None:
        now = datetime.now(UTC)
        rows = list(
            self.db.scalars(
                select(ApprovalDelegation).where(
                    ApprovalDelegation.organization_id == self.ctx.organization_id,
                    ApprovalDelegation.to_actor_id == self.ctx.actor_id,
                    ApprovalDelegation.status == "active",
                    ApprovalDelegation.starts_at <= now,
                    ApprovalDelegation.ends_at >= now,
                )
            ).all()
        )
        for row in rows:
            if (
                row.project_id is not None
                and project_id is not None
                and row.project_id != project_id
            ):
                continue
            if row.action_code in {action_code, "*", "all"}:
                return row
            if row.action_code.endswith(".*") and action_code.startswith(row.action_code[:-1]):
                return row
        return None
