import asyncio
import time

from pydantic import BaseModel

from src.models.films import User


class UserFilmLikes(BaseModel):
    likes: list


class UserFilmBookmarks(BaseModel):
    bookmarks: list


async def get_users_likes(size: int):
    """Список лайков пользователей"""
    print(f'Получение лайков {size} пользователей из БД ... ')
    start_time = time.time()
    await User.find().project(UserFilmLikes).limit(size).to_list()
    end_time = time.time()
    print(f'Время выполнения: {end_time - start_time} сек \n')


async def get_users_bookmarks(size: int):
    """Список закладок пользователей"""
    print(f'Получение закладок {size} пользователей из БД ... ')
    start_time = time.time()
    await User.find().project(UserFilmBookmarks).limit(size).to_list()
    end_time = time.time()
    print(f'Время выполнения: {end_time - start_time} сек \n')


async def get_users_average_rate(size: int):
    """Средняя пользовательская оценка фильма."""
    print(f'Получение средней оценки каждого пользователя для {size} пользователей из БД ... ')
    start_time = time.time()
    await User.find(limit=size).aggregate([
        {
            "$group": {
                "_id": "$_id",
                "avgRate": {
                    "$push": {
                        "likes": {"$avg": "$likes.grade"}
                    }
                }
            }
        }
    ]).to_list()
    end_time = time.time()
    print(f'Время выполнения: {end_time - start_time} сек')


async def main(size: int):
    print('________________________________________________________')
    print('Тестирование скорости чтения загруженных данных ...')
    await get_users_likes(size)
    await get_users_bookmarks(size)
    await get_users_average_rate(size)


if "__main__" == __name__:
    asyncio.run(main())
