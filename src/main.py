import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from src.controllers import coins

from src.core.containers import Container
from src.core.logging import setup_logging
from src.settings import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()
setup_logging(settings)

API_PREFIX = "/api"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Startup novalex-api app")
    yield
    logger.info("Shutdown novalex-api app")


def init_fastapi_app() -> FastAPI:
    container = Container()

    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version="0.1.0",
        docs_url=f"{API_PREFIX}/docs",
        redoc_url=f"{API_PREFIX}/redoc",
        openapi_url=f"{API_PREFIX}/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
    app.container = container

    app.include_router(coins.router, prefix=API_PREFIX)

    return app


app = init_fastapi_app()
