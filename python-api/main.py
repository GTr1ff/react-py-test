import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from feature_locator import FeatureLocator
from core.exceptions import DatabaseException
from core.logging.config import setup_logging
from core.logging.request_logger import RequestLoggerMiddleware
from core.config import settings
def create_app() -> FastAPI:
    setup_logging()

    application = FastAPI(
        title="worker-wip",
        description="A proof of concept FastAPI application following the FOA architecture",
        version="1.0.0",
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