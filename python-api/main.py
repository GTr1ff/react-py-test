import logging
from typing import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from feature_locator import FeatureLocator
from core.exceptions import DatabaseException
from core.database import Database
from core.logging.config import setup_logging
from core.logging.request_logger import RequestLoggerMiddleware
from core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.db = Database(settings.DATABASE_URI)
    await app.state.db.initialize()
    print("zz-work is running")
    yield
    await app.state.db.dispose()

def create_app() -> FastAPI:
    setup_logging()

    application = FastAPI(
        title="zz-work",
        description="A proof of concept FastAPI application following the FOA architecture",
        version="1.0.0",
        lifespan=lifespan
    )

    origins = ["*"] if settings.ENV == "development" else []

    application.add_middleware(RequestLoggerMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.exception_handler(DatabaseException)
    async def database_exception_handler(request: Request, exc: DatabaseException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message}
        )

    locator = FeatureLocator()
    for router in locator.get_feature_routers().values():
        application.include_router(router, prefix="/api")

    return application

app = create_app()