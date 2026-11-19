"""FastAPI application factory."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1 import api_router
from app.core.config import settings
from app.core.logging import configure_logging, get_logger
from app.core.database import Base, engine
from app.models import *  # noqa: F401  ensure models registered for metadata
from app.permissions import ROLE_ADMIN, ROLE_AI_SERVICE, ROLE_REVIEWER, ROLE_STUDENT

logger = get_logger("assessiq")


def create_app() -> FastAPI:
    configure_logging(log_level=settings.log_level, log_format=settings.log_format)

    app = FastAPI(
        title="AssessIQ API",
        description="AI-powered competitive examination assessment platform",
        version="0.1.0",
        docs_url="/docs",
        openapi_url="/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error("database_error", error=str(exc))
        return JSONResponse(
            status_code=500,
            content={"detail": "A database error occurred"},
        )

    app.include_router(api_router, prefix="/api/v1")

    @app.on_event("startup")
    def on_startup() -> None:
        logger.info("application_started", env=settings.app_env)

    return app


def seed_default_roles() -> None:
    """Seed system roles. Intended to be invoked explicitly (CLI/migration), not on startup."""
    from app.core.database import SessionLocal
    from app.models.role import Role

    db = SessionLocal()
    try:
        for name in [ROLE_STUDENT, ROLE_ADMIN, ROLE_REVIEWER, ROLE_AI_SERVICE]:
            exists = db.query(Role).filter(Role.name == name).first()
            if not exists:
                db.add(Role(name=name, is_system=True))
        db.commit()
    finally:
        db.close()


app = create_app()
