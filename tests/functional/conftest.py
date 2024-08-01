import asyncio
from typing import (
    Any,
    Optional,
)

import aiohttp
import pytest
import pytest_asyncio
from pymongo import MongoClient
from pymongo.collection import Collection

from tests.functional.settings import test_settings as ts
from tests.functional.testdata.films import USER_ID
from fastapi_jwt import JwtAccessBearer


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="mongo_client", scope="session")
async def mongo_client():
    mongo = MongoClient(
        f"mongodb://{ts.mongo.username}:{ts.mongo.password}@{ts.mongo.host}:{ts.mongo.port}",
        UuidRepresentation='standard'
    )
    db = mongo['ugc']
    yield db
    mongo.close()


@pytest_asyncio.fixture(name="aiohttp_client", scope="session")
async def aiohttp_client():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(name="make_request")
def make_request(aiohttp_client: aiohttp.ClientSession):
    async def _make_request(
        method: str,
        path_to_endpoint: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
        token: Optional[str] = None,
    ):
        headers = None
        if token:
            headers = {"Authorization": f"Bearer {token}"}
        url = f"{ts.app_scheme}://{ts.app_host}:{ts.app_port}/{path_to_endpoint}"
        async with aiohttp_client.request(
            method=method, url=url, params=params, json=json, headers=headers
        ) as response:
            try:
                body = await response.json()
            except (aiohttp.ContentTypeError, ValueError):
                body = None
            status = response.status
        return body, status

    return _make_request


@pytest_asyncio.fixture(name="clean_db")
async def clean_db(mongo_client: MongoClient) -> None:
    db = mongo_client
    collection_film = db["Film"]
    collection_user = db["User"]
    collection_film.drop()
    collection_user.drop()


@pytest.fixture(name="get_from_db")
def get_from_db(mongo_client: MongoClient):
    def find(collection: Collection, condition: dict, multiple: bool = False):
        if multiple:
            results = collection.find(condition)
            return [item for item in results]
        return collection.find_one(condition)
    return find


@pytest.fixture(scope='session')
def authorize():
    def inner():
        access_security = JwtAccessBearer(secret_key=ts.secret_key, auto_error=True)
        subject = {"user_id": USER_ID}
        return access_security.create_access_token(subject=subject)

    return inner
