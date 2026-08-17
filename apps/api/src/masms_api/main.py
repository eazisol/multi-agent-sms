"""FastAPI application entrypoint."""

from __future__ import annotations

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from masms_api.config import get_settings
from masms_api.db import get_db
from masms_api.errors import AppError
from masms_api.kernel.problem import PROBLEM_JSON_MEDIA_TYPE, problem_body
from masms_api.modules.access.router import router as access_router
from masms_api.modules.agents.router import router as agents_router
from masms_api.modules.approvalgates.router import router as approvalgates_router
from masms_api.modules.assignments.router import router as assignments_router
from masms_api.modules.auth.router import router as auth_router
from masms_api.modules.bugs.router import router as bugs_router
from masms_api.modules.capacity.router import router as capacity_router
from masms_api.modules.changecontrol.router import router as changecontrol_router
from masms_api.modules.clients.router import router as clients_router
from masms_api.modules.comms.router import router as comms_router
from masms_api.modules.configadmin.router import router as config_router
from masms_api.modules.documents.router import router as documents_router
from masms_api.modules.followups.router import router as followups_router
from masms_api.modules.gmail.router import router as gmail_router
from masms_api.modules.governance.router import router as governance_router
from masms_api.modules.identity.router import router as identity_router
from masms_api.modules.insights.router import router as insights_router
from masms_api.modules.integrations.router import router as integrations_router
from masms_api.modules.jira.router import router as jira_router
from masms_api.modules.knowledge.router import router as knowledge_router
from masms_api.modules.notifications.router import router as notifications_router
from masms_api.modules.orchestrator.router import router as orchestrator_router
from masms_api.modules.pilot.router import router as pilot_router
from masms_api.modules.projects.router import router as projects_router
from masms_api.modules.queries.router import router as queries_router
from masms_api.modules.releases.router import router as releases_router
from masms_api.modules.reliability.router import router as reliability_router
from masms_api.modules.requirements.router import router as requirements_router
from masms_api.modules.roadmap.router import router as roadmap_router
from masms_api.modules.securityhardening.router import router as securityhardening_router
from masms_api.modules.statusengine.router import router as statusengine_router
from masms_api.modules.testcases.router import router as testcases_router
from masms_api.modules.tickets.router import router as tickets_router
from masms_api.modules.traceability.router import router as traceability_router
from masms_api.modules.uateval.router import router as uateval_router
from masms_api.observability.health import build_readiness
from masms_api.observability.router import router as observability_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.api_title, version=settings.api_version)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    @app.exception_handler(AppError)
    async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=problem_body(exc),
            media_type=PROBLEM_JSON_MEDIA_TYPE,
        )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "env": settings.env}

    @app.get("/health/live")
    def health_live() -> dict[str, str]:
        return {"status": "live", "env": settings.env}

    @app.get("/health/ready")
    def health_ready(db: Session = Depends(get_db)) -> dict[str, object]:
        return build_readiness(db=db, redis_url=settings.redis_url, env=settings.env)

    @app.get("/api/v1/meta")
    def meta() -> dict[str, object]:
        return {
            "name": settings.api_title,
            "version": settings.api_version,
            "modules": [
                "MOD-000",
                "MOD-020",
                "MOD-030",
                "MOD-040",
                "MOD-100",
                "MOD-110",
                "MOD-120",
                "MOD-130",
                "MOD-140",
                "MOD-200",
                "MOD-210",
                "MOD-220",
                "MOD-230",
                "MOD-240",
                "MOD-250",
                "MOD-260",
                "MOD-300",
                "MOD-310",
                "MOD-320",
                "MOD-330",
                "MOD-340",
                "MOD-350",
                "MOD-360",
                "MOD-370",
                "MOD-400",
                "MOD-410",
                "MOD-420",
                "MOD-430",
                "MOD-440",
                "MOD-450",
                "MOD-460",
                "MOD-500",
                "MOD-510",
                "MOD-520",
                "MOD-600",
                "MOD-610",
                "MOD-620",
                "MOD-630",
            ],
            "kernel": "masms_api.kernel",
            "environment": settings.env,
            "secret_backend": settings.secret_backend,
            "auth_provider": settings.auth_provider,
            "default_organization_id": settings.default_organization_id,
        }

    app.include_router(governance_router, prefix="/api/v1")
    app.include_router(observability_router, prefix="/api/v1")
    app.include_router(identity_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(access_router, prefix="/api/v1")
    app.include_router(capacity_router, prefix="/api/v1")
    app.include_router(config_router, prefix="/api/v1")
    app.include_router(clients_router, prefix="/api/v1")
    app.include_router(queries_router, prefix="/api/v1")
    app.include_router(comms_router, prefix="/api/v1")
    app.include_router(requirements_router, prefix="/api/v1")
    app.include_router(projects_router, prefix="/api/v1")
    app.include_router(documents_router, prefix="/api/v1")
    app.include_router(roadmap_router, prefix="/api/v1")
    app.include_router(tickets_router, prefix="/api/v1")
    app.include_router(assignments_router, prefix="/api/v1")
    app.include_router(statusengine_router, prefix="/api/v1")
    app.include_router(approvalgates_router, prefix="/api/v1")
    app.include_router(followups_router, prefix="/api/v1")
    app.include_router(orchestrator_router, prefix="/api/v1")
    app.include_router(agents_router, prefix="/api/v1")
    app.include_router(knowledge_router, prefix="/api/v1")
    app.include_router(testcases_router, prefix="/api/v1")
    app.include_router(bugs_router, prefix="/api/v1")
    app.include_router(changecontrol_router, prefix="/api/v1")
    app.include_router(releases_router, prefix="/api/v1")
    app.include_router(notifications_router, prefix="/api/v1")
    app.include_router(insights_router, prefix="/api/v1")
    app.include_router(traceability_router, prefix="/api/v1")
    app.include_router(integrations_router, prefix="/api/v1")
    app.include_router(gmail_router, prefix="/api/v1")
    app.include_router(jira_router, prefix="/api/v1")
    app.include_router(securityhardening_router, prefix="/api/v1")
    app.include_router(reliability_router, prefix="/api/v1")
    app.include_router(uateval_router, prefix="/api/v1")
    app.include_router(pilot_router, prefix="/api/v1")
    return app


app = create_app()
