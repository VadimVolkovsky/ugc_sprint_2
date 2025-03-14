import logging
import sentry_sdk
from contextlib import asynccontextmanager
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from beanie import init_beanie
from asgi_correlation_id import CorrelationIdMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration

from api.v1 import films
from core.config import settings
from core.logger import configure_logging
from middleware.request_log import RequestLogMiddleware
from models.films import User, Film


@asynccontextmanager
async def lifespan(app: FastAPI):
    # при старте сервера
    mongo = AsyncIOMotorClient(
        f"mongodb://{settings.mongo.username}:{settings.mongo.password}@{settings.mongo.host}:{settings.mongo.port}"
    )
    configure_logging()
    await init_beanie(database=mongo.ugc, document_models=[User, Film])
    if settings.sentry_enabled:
        sentry_sdk.init(
            dsn=settings.sentry_sdn,
            integrations=[FastApiIntegration(
                transaction_style="endpoint",
                failed_request_status_codes=[403, range(500, 599)],
            )],
        )
    yield
    # при выключении сервера
    mongo.close()


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(films.router, prefix="/api/v1/films")
app.add_middleware(RequestLogMiddleware)
app.add_middleware(CorrelationIdMiddleware)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=settings.app_port,
        log_level=logging.DEBUG,
        reload=True,
    )
