"""Capacity application service (MOD-130)."""

from __future__ import annotations

from datetime import UTC, date
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from masms_api.errors import ConflictError, NotFoundError, ValidationAppError
from masms_api.kernel.context import RequestContext
from masms_api.kernel.pagination import PageMeta, build_page_meta, normalize_paging
from masms_api.kernel.rls import apply_tenant_rls
from masms_api.kernel.uow import SqlAlchemyUnitOfWork
from masms_api.modules.capacity import domain
from masms_api.modules.capacity.models import (
    ActorSkill,
    AvailabilityWindow,
    BusinessCalendar,
    CapacityAllocation,
    Holiday,
    LeavePeriod,
    OnCallSchedule,
    Skill,
)
from masms_api.modules.capacity.schemas import (
    ActorSkillCreate,
    AssignmentEvaluateRequest,
    AssignmentEvaluateResponse,
    AvailabilityCreate,
    BusinessCalendarCreate,
    CapacityAllocationCreate,
    HolidayCreate,
    LeavePeriodCreate,
    OnCallCreate,
    SkillCreate,
    SlaBusinessDayRequest,
    SlaBusinessDayResponse,
)
from masms_api.observability.writer import ObservabilityWriter


class CapacityService:
    def __init__(self, db: Session, ctx: RequestContext) -> None:
        self.db = db
        self.ctx = ctx
        self.uow = SqlAlchemyUnitOfWork(db)
        self.obs = ObservabilityWriter(db, ctx)
        apply_tenant_rls(db, ctx.organization_id)

    def create_skill(self, data: SkillCreate) -> Skill:
        if self.db.scalar(
            select(Skill).where(
                Skill.organization_id == self.ctx.organization_id,
                Skill.code == data.code,
            )
        ):
            raise ConflictError(f"Skill '{data.code}' already exists")
        row = Skill(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code,
            title=data.title,
            category=data.category,
            description=data.description,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.obs.write_audit(
            action="skill_create",
            entity_type="org_skill",
            entity_id=row.id,
            payload={"code": data.code},
        )
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_skills(self, *, limit: int = 20, offset: int = 0) -> tuple[list[Skill], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [Skill.organization_id == self.ctx.organization_id]
        total = self.db.scalar(select(func.count()).select_from(Skill).where(*filters)) or 0
        rows = self.db.scalars(
            select(Skill).where(*filters).order_by(Skill.code).offset(offset).limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def assign_actor_skill(self, data: ActorSkillCreate) -> ActorSkill:
        domain.assert_proficiency(data.proficiency)
        skill = self._get_skill(data.skill_id)
        if self.db.scalar(
            select(ActorSkill).where(
                ActorSkill.organization_id == self.ctx.organization_id,
                ActorSkill.actor_id == data.actor_id,
                ActorSkill.skill_id == skill.id,
            )
        ):
            raise ConflictError("Actor already has this skill")
        row = ActorSkill(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            actor_id=data.actor_id,
            skill_id=skill.id,
            proficiency=data.proficiency,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_availability(self, data: AvailabilityCreate) -> AvailabilityWindow:
        domain.assert_weekday(data.weekday)
        domain.assert_time_range(data.start_time, data.end_time)
        row = AvailabilityWindow(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            actor_id=data.actor_id,
            weekday=data.weekday,
            start_time=data.start_time,
            end_time=data.end_time,
            timezone=data.timezone,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_capacity(self, data: CapacityAllocationCreate) -> CapacityAllocation:
        domain.assert_allocation_pct(data.allocation_pct)
        if data.effective_to is not None:
            domain.assert_date_range(data.effective_from, data.effective_to, label="allocation")
        row = CapacityAllocation(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            actor_id=data.actor_id,
            project_id=data.project_id,
            allocation_pct=data.allocation_pct,
            status="active",
            effective_from=data.effective_from,
            effective_to=data.effective_to,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def list_allocations(
        self, *, limit: int = 20, offset: int = 0
    ) -> tuple[list[CapacityAllocation], PageMeta]:
        limit, offset = normalize_paging(limit, offset)
        filters = [CapacityAllocation.organization_id == self.ctx.organization_id]
        total = (
            self.db.scalar(select(func.count()).select_from(CapacityAllocation).where(*filters))
            or 0
        )
        rows = self.db.scalars(
            select(CapacityAllocation)
            .where(*filters)
            .order_by(CapacityAllocation.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(rows), build_page_meta(limit=limit, offset=offset, total=int(total))

    def create_calendar(self, data: BusinessCalendarCreate) -> BusinessCalendar:
        if self.db.scalar(
            select(BusinessCalendar).where(
                BusinessCalendar.organization_id == self.ctx.organization_id,
                BusinessCalendar.code == data.code,
            )
        ):
            raise ConflictError(f"Calendar '{data.code}' already exists")
        row = BusinessCalendar(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            code=data.code,
            title=data.title,
            timezone=data.timezone,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_holiday(self, data: HolidayCreate) -> Holiday:
        calendar = self._get_calendar(data.calendar_id)
        row = Holiday(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            calendar_id=calendar.id,
            holiday_date=data.holiday_date,
            title=data.title,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_leave(self, data: LeavePeriodCreate) -> LeavePeriod:
        domain.assert_date_range(data.starts_on, data.ends_on, label="leave")
        row = LeavePeriod(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            actor_id=data.actor_id,
            leave_type=data.leave_type,
            starts_on=data.starts_on,
            ends_on=data.ends_on,
            status="approved",
            notes=data.notes,
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def create_oncall(self, data: OnCallCreate) -> OnCallSchedule:
        starts = data.starts_at if data.starts_at.tzinfo else data.starts_at.replace(tzinfo=UTC)
        ends = data.ends_at if data.ends_at.tzinfo else data.ends_at.replace(tzinfo=UTC)
        if ends <= starts:
            raise ValidationAppError("on-call ends_at must be after starts_at")
        row = OnCallSchedule(
            id=uuid4(),
            organization_id=self.ctx.organization_id,
            actor_id=data.actor_id,
            rotation_name=data.rotation_name,
            starts_at=starts,
            ends_at=ends,
            status="active",
            created_by_actor_id=self.ctx.actor_id,
        )
        self.uow.add(row)
        self.uow.commit()
        self.uow.refresh(row)
        return row

    def evaluate_assignment(self, data: AssignmentEvaluateRequest) -> AssignmentEvaluateResponse:
        reasons: list[str] = []
        as_of = data.as_of or date.today()
        remaining: Decimal | None = None
        deadline_biz: bool | None = None

        if data.skill_code:
            skill = self.db.scalar(
                select(Skill).where(
                    Skill.organization_id == self.ctx.organization_id,
                    Skill.code == data.skill_code,
                    Skill.status == "active",
                )
            )
            if skill is None:
                reasons.append(f"skill '{data.skill_code}' not found")
            else:
                link = self.db.scalar(
                    select(ActorSkill).where(
                        ActorSkill.organization_id == self.ctx.organization_id,
                        ActorSkill.actor_id == data.actor_id,
                        ActorSkill.skill_id == skill.id,
                        ActorSkill.status == "active",
                    )
                )
                if link is None or link.proficiency < data.min_proficiency:
                    reasons.append("skill proficiency below required minimum")

        allocations = list(
            self.db.scalars(
                select(CapacityAllocation).where(
                    CapacityAllocation.organization_id == self.ctx.organization_id,
                    CapacityAllocation.actor_id == data.actor_id,
                    CapacityAllocation.status == "active",
                    CapacityAllocation.effective_from <= as_of,
                )
            )
        )
        used = Decimal("0")
        for alloc in allocations:
            if alloc.effective_to is not None and alloc.effective_to < as_of:
                continue
            if data.project_id is not None and alloc.project_id not in {None, data.project_id}:
                continue
            used += Decimal(alloc.allocation_pct)
        remaining = Decimal("100") - used
        if remaining < 0:
            reasons.append("capacity over-allocated")

        leave = self.db.scalar(
            select(LeavePeriod).where(
                LeavePeriod.organization_id == self.ctx.organization_id,
                LeavePeriod.actor_id == data.actor_id,
                LeavePeriod.status == "approved",
                LeavePeriod.starts_on <= as_of,
                LeavePeriod.ends_on >= as_of,
            )
        )
        if leave is not None:
            reasons.append("actor is on leave")

        if data.deadline is not None and data.calendar_id is not None:
            holidays = self._holiday_dates(data.calendar_id)
            deadline_biz = domain.is_business_day(
                weekday=data.deadline.weekday(),
                is_holiday=data.deadline in holidays,
            )
            if not deadline_biz:
                reasons.append("deadline is not a business day on calendar")

        avail = self.db.scalar(
            select(AvailabilityWindow).where(
                AvailabilityWindow.organization_id == self.ctx.organization_id,
                AvailabilityWindow.actor_id == data.actor_id,
                AvailabilityWindow.status == "active",
            )
        )
        if avail is None:
            reasons.append("no availability windows configured")

        return AssignmentEvaluateResponse(
            eligible=len(reasons) == 0,
            reasons=reasons,
            remaining_capacity_pct=remaining,
            deadline_is_business_day=deadline_biz,
        )

    def add_business_days(self, data: SlaBusinessDayRequest) -> SlaBusinessDayResponse:
        calendar = self._get_calendar(data.calendar_id)
        holidays = self._holiday_dates(calendar.id)
        due = domain.add_business_days(
            data.start_date,
            business_days=data.business_days,
            holiday_dates=holidays,
        )
        return SlaBusinessDayResponse(due_date=due, calendar_timezone=calendar.timezone)

    def _holiday_dates(self, calendar_id: UUID) -> set[date]:
        rows = self.db.scalars(
            select(Holiday).where(
                Holiday.organization_id == self.ctx.organization_id,
                Holiday.calendar_id == calendar_id,
                Holiday.status == "active",
            )
        )
        return {row.holiday_date for row in rows}

    def _get_skill(self, skill_id: UUID) -> Skill:
        row = self.db.scalar(select(Skill).where(Skill.id == skill_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Skill not found")
        return row

    def _get_calendar(self, calendar_id: UUID) -> BusinessCalendar:
        row = self.db.scalar(select(BusinessCalendar).where(BusinessCalendar.id == calendar_id))
        if row is None or row.organization_id != self.ctx.organization_id:
            raise NotFoundError("Business calendar not found")
        return row
