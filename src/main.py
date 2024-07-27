import logging
from contextlib import asynccontextmanager
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


from api.v1 import films
from core.config import settings
from core.logger import LOGGING
from beanie import init_beanie
from models.films import User, Film


@asynccontextmanager
async def lifespan(app: FastAPI):
    # при старте сервера
    mongo = AsyncIOMotorClient(
        f"mongodb://{settings.mongo.username}:{settings.mongo.password}@{settings.mongo.host}:{settings.mongo.port}"
    )
    await init_beanie(database=mongo.ugc, document_models=[User, Film])
    yield
    # при выключении сервера
    mongo.mongo.close()


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(films.router, prefix="/api/v1/films")



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=settings.app_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
