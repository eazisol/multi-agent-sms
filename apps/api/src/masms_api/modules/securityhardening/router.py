"""HTTP routes for MOD-600 security hardening."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from masms_api.db import get_db
from masms_api.deps import RequestContext, get_request_context
from masms_api.kernel.pagination import PageMeta
from masms_api.modules.securityhardening.schemas import (
    BackupRecordCreate,
    BackupRecordRead,
    DeletionJobCreate,
    DeletionJobRead,
    LegalHoldCreate,
    LegalHoldRead,
    PiiInventoryCreate,
    PiiInventoryRead,
    RecoveryValidationRead,
    RestoreTestCreate,
    RestoreTestRead,
    RetentionPolicyCreate,
    RetentionPolicyRead,
    SecurityGateRead,
    SecurityIncidentClose,
    SecurityIncidentCreate,
    SecurityIncidentRead,
    ThreatModelCreate,
    ThreatModelRead,
    TrainingPolicyRead,
    TrainingPolicyUpdate,
)
from masms_api.modules.securityhardening.service import SecurityHardeningService

router = APIRouter(prefix="/security", tags=["security"])


class ThreatModelPage(BaseModel):
    items: list[ThreatModelRead]
    page: PageMeta = Field(description="Pagination metadata")


class PiiInventoryPage(BaseModel):
    items: list[PiiInventoryRead]
    page: PageMeta = Field(description="Pagination metadata")


class RetentionPolicyPage(BaseModel):
    items: list[RetentionPolicyRead]
    page: PageMeta = Field(description="Pagination metadata")


class LegalHoldPage(BaseModel):
    items: list[LegalHoldRead]
    page: PageMeta = Field(description="Pagination metadata")


class DeletionJobPage(BaseModel):
    items: list[DeletionJobRead]
    page: PageMeta = Field(description="Pagination metadata")


class BackupRecordPage(BaseModel):
    items: list[BackupRecordRead]
    page: PageMeta = Field(description="Pagination metadata")


class RestoreTestPage(BaseModel):
    items: list[RestoreTestRead]
    page: PageMeta = Field(description="Pagination metadata")


class SecurityIncidentPage(BaseModel):
    items: list[SecurityIncidentRead]
    page: PageMeta = Field(description="Pagination metadata")


def _service(
    db: Session = Depends(get_db),
    ctx: RequestContext = Depends(get_request_context),
) -> SecurityHardeningService:
    return SecurityHardeningService(db, ctx)


@router.get("/gate", response_model=SecurityGateRead)
def security_gate(service: SecurityHardeningService = Depends(_service)) -> SecurityGateRead:
    return SecurityGateRead.model_validate(service.security_gate())


@router.get("/recovery-validation", response_model=RecoveryValidationRead)
def recovery_validation(
    service: SecurityHardeningService = Depends(_service),
) -> RecoveryValidationRead:
    return RecoveryValidationRead.model_validate(service.recovery_validation())


@router.get("/training-policy", response_model=TrainingPolicyRead)
def get_training_policy(
    service: SecurityHardeningService = Depends(_service),
) -> TrainingPolicyRead:
    return TrainingPolicyRead.model_validate(service.get_or_create_training_policy())


@router.put("/training-policy", response_model=TrainingPolicyRead)
def update_training_policy(
    body: TrainingPolicyUpdate,
    service: SecurityHardeningService = Depends(_service),
) -> TrainingPolicyRead:
    return TrainingPolicyRead.model_validate(service.update_training_policy(body))


@router.post("/threat-models", response_model=ThreatModelRead, status_code=201)
def create_threat_model(
    body: ThreatModelCreate, service: SecurityHardeningService = Depends(_service)
) -> ThreatModelRead:
    return ThreatModelRead.model_validate(service.create_threat_model(body))


@router.get("/threat-models", response_model=ThreatModelPage)
def list_threat_models(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: SecurityHardeningService = Depends(_service),
) -> ThreatModelPage:
    items, page = service.list_threat_models(limit=limit, offset=offset)
    return ThreatModelPage(
        items=[ThreatModelRead.model_validate(item) for item in items], page=page
    )


@router.post("/pii-inventory", response_model=PiiInventoryRead, status_code=201)
def create_pii_inventory(
    body: PiiInventoryCreate, service: SecurityHardeningService = Depends(_service)
) -> PiiInventoryRead:
    return PiiInventoryRead.model_validate(service.create_pii_inventory(body))


@router.get("/pii-inventory", response_model=PiiInventoryPage)
def list_pii_inventory(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: SecurityHardeningService = Depends(_service),
) -> PiiInventoryPage:
    items, page = service.list_pii_inventory(limit=limit, offset=offset)
    return PiiInventoryPage(
        items=[PiiInventoryRead.model_validate(item) for item in items], page=page
    )


@router.post("/retention-policies", response_model=RetentionPolicyRead, status_code=201)
def create_retention_policy(
    body: RetentionPolicyCreate, service: SecurityHardeningService = Depends(_service)
) -> RetentionPolicyRead:
    return RetentionPolicyRead.model_validate(service.create_retention_policy(body))


@router.get("/retention-policies", response_model=RetentionPolicyPage)
def list_retention_policies(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: SecurityHardeningService = Depends(_service),
) -> RetentionPolicyPage:
    items, page = service.list_retention_policies(limit=limit, offset=offset)
    return RetentionPolicyPage(
        items=[RetentionPolicyRead.model_validate(item) for item in items], page=page
    )


@router.post("/legal-holds", response_model=LegalHoldRead, status_code=201)
def create_legal_hold(
    body: LegalHoldCreate, service: SecurityHardeningService = Depends(_service)
) -> LegalHoldRead:
    return LegalHoldRead.model_validate(service.create_legal_hold(body))


@router.get("/legal-holds", response_model=LegalHoldPage)
def list_legal_holds(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: SecurityHardeningService = Depends(_service),
) -> LegalHoldPage:
    items, page = service.list_legal_holds(limit=limit, offset=offset)
    return LegalHoldPage(
        items=[LegalHoldRead.model_validate(item) for item in items], page=page
    )


@router.post("/legal-holds/{hold_id}/release", response_model=LegalHoldRead)
def release_legal_hold(
    hold_id: UUID, service: SecurityHardeningService = Depends(_service)
) -> LegalHoldRead:
    return LegalHoldRead.model_validate(service.release_legal_hold(hold_id))


@router.post("/deletion-jobs", response_model=DeletionJobRead, status_code=201)
def create_deletion_job(
    body: DeletionJobCreate, service: SecurityHardeningService = Depends(_service)
) -> DeletionJobRead:
    return DeletionJobRead.model_validate(service.create_deletion_job(body))


@router.get("/deletion-jobs", response_model=DeletionJobPage)
def list_deletion_jobs(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: SecurityHardeningService = Depends(_service),
) -> DeletionJobPage:
    items, page = service.list_deletion_jobs(limit=limit, offset=offset)
    return DeletionJobPage(
        items=[DeletionJobRead.model_validate(item) for item in items], page=page
    )


@router.post("/backups", response_model=BackupRecordRead, status_code=201)
def create_backup_record(
    body: BackupRecordCreate, service: SecurityHardeningService = Depends(_service)
) -> BackupRecordRead:
    return BackupRecordRead.model_validate(service.create_backup_record(body))


@router.get("/backups", response_model=BackupRecordPage)
def list_backup_records(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: SecurityHardeningService = Depends(_service),
) -> BackupRecordPage:
    items, page = service.list_backup_records(limit=limit, offset=offset)
    return BackupRecordPage(
        items=[BackupRecordRead.model_validate(item) for item in items], page=page
    )


@router.post("/restore-tests", response_model=RestoreTestRead, status_code=201)
def create_restore_test(
    body: RestoreTestCreate, service: SecurityHardeningService = Depends(_service)
) -> RestoreTestRead:
    return RestoreTestRead.model_validate(service.create_restore_test(body))


@router.get("/restore-tests", response_model=RestoreTestPage)
def list_restore_tests(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: SecurityHardeningService = Depends(_service),
) -> RestoreTestPage:
    items, page = service.list_restore_tests(limit=limit, offset=offset)
    return RestoreTestPage(
        items=[RestoreTestRead.model_validate(item) for item in items], page=page
    )


@router.post("/incidents", response_model=SecurityIncidentRead, status_code=201)
def create_incident(
    body: SecurityIncidentCreate, service: SecurityHardeningService = Depends(_service)
) -> SecurityIncidentRead:
    return SecurityIncidentRead.model_validate(service.create_incident(body))


@router.get("/incidents", response_model=SecurityIncidentPage)
def list_incidents(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: SecurityHardeningService = Depends(_service),
) -> SecurityIncidentPage:
    items, page = service.list_incidents(limit=limit, offset=offset)
    return SecurityIncidentPage(
        items=[SecurityIncidentRead.model_validate(item) for item in items], page=page
    )


@router.post("/incidents/{incident_id}/close", response_model=SecurityIncidentRead)
def close_incident(
    incident_id: UUID,
    body: SecurityIncidentClose | None = None,
    service: SecurityHardeningService = Depends(_service),
) -> SecurityIncidentRead:
    return SecurityIncidentRead.model_validate(
        service.close_incident(incident_id, body or SecurityIncidentClose())
    )
