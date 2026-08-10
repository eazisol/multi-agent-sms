"""FastAPI application entrypoint."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from masms_api.config import get_settings
from masms_api.errors import AppError
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
        body: dict[str, Any] = {
            "code": exc.code,
            "message": exc.message,
            "correlation_id": str(exc.correlation_id) if exc.correlation_id else None,
            "details": exc.details,
        }
        return JSONResponse(status_code=exc.status_code, content=body)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "env": settings.env}

    @app.get("/api/v1/meta")
    def meta() -> dict[str, str]:
        return {
            "name": settings.api_title,
            "version": settings.api_version,
            "module": "MOD-000",
            "default_organization_id": settings.default_organization_id,
        }

    app.include_router(governance_router, prefix="/api/v1")
    return app


app = create_app()
