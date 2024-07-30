import asyncio

import faker
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from data_extract import main as data_extract_main
from data_loader import main as data_loader_main
from db_research.mongo_db.config import settings
from real_time_data_reader import main as real_time_data_reader_main
from src.models.films import User, Film

faker = faker.Faker()

NUMBER_OF_USERS = 10000

# список понравившихся пользователю фильмов (список лайков пользователя);
# список закладок;
# средняя пользовательская оценка фильма.


async def connect_to_db() -> None:
    """Подключение к MongoDB"""
    mongo = AsyncIOMotorClient(
        f"mongodb://{settings.mongo.username}:{settings.mongo.password}@{settings.mongo.host}:{settings.mongo.port}"
    )
    await init_beanie(database=mongo.ugc, document_models=[User, Film])


async def main():
    await connect_to_db()
    await data_loader_main(size=NUMBER_OF_USERS)
    await data_extract_main(size=NUMBER_OF_USERS)
    await real_time_data_reader_main(size=NUMBER_OF_USERS)


if "__main__" == __name__:
    asyncio.run(main())
