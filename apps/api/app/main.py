from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes import company, feed, search, trends


def create_app() -> FastAPI:
    app = FastAPI(
        title="Town Crier API",
        version="0.1.0",
        description="Read API for the Town Crier AI/robotics intelligence platform.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    @app.get("/healthz", tags=["meta"])
    def healthz() -> dict:
        return {"status": "ok"}

    app.include_router(feed.router)
    app.include_router(search.router)
    app.include_router(trends.router)
    app.include_router(company.router)

    return app


app = create_app()
