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
from masms_api.modules.auth.router import router as auth_router
from masms_api.modules.governance.router import router as governance_router
from masms_api.modules.identity.router import router as identity_router
from masms_api.observability.health import build_readiness
from masms_api.observability.router import router as observability_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.api_title, version=settings.api_version)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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
    return app


app = create_app()
