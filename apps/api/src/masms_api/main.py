"""FastAPI application entrypoint."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from masms_api.config import get_settings
from masms_api.errors import AppError
from masms_api.kernel.problem import PROBLEM_JSON_MEDIA_TYPE, problem_body
from masms_api.modules.governance.router import router as governance_router


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

    @app.get("/api/v1/meta")
    def meta() -> dict[str, object]:
        return {
            "name": settings.api_title,
            "version": settings.api_version,
            "modules": ["MOD-000", "MOD-020"],
            "kernel": "masms_api.kernel",
            "default_organization_id": settings.default_organization_id,
        }

    app.include_router(governance_router, prefix="/api/v1")
    return app


app = create_app()
