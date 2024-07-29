import asyncio
import random
import time

import faker

from src.models.films import Bookmark, LikeFilm, LikeUser, ReviewFilm, User, Film

faker = faker.Faker()


async def generate_user_data(size) -> list[User]:
    """Генерация тестовых данных для коллекции Users"""

    films_likes = [LikeFilm(film_id=faker.uuid4(), grade=random.randint(1, 10)) for _ in range(100)]
    users_likes = [LikeUser(user_id=faker.uuid4(), grade=random.randint(1, 10)) for _ in range(100)]
    reviews = [
        ReviewFilm(
            id=faker.uuid4(),
            text=faker.text(100),
            film_id=faker.uuid4(),
            likes=random.sample(users_likes, random.randint(1, 20)),
        )
        for _ in range(100)
    ]
    bookmarks = [Bookmark(id=faker.uuid4(), film_id=faker.uuid4()) for _ in range(100)]

    users = []
    for _ in range(size):
        users.append(
            User(
                id=faker.uuid4(),
                likes=random.sample(films_likes, random.randint(1, 30)),
                reviews=random.sample(reviews, random.randint(0, 5)),
                bookmarks=random.sample(bookmarks, random.randint(0, 5)),
            )
        )
    print(f'Сгенерированно {len(users)} объектов Users')
    return users


async def load_data_to_db(data_to_load: list[Film | User]):
    """Загрузка данных в MongoDB"""
    print(f'Загрузка {len(data_to_load)} объектов в БД ...')
    start_time = time.time()
    for obj in data_to_load:
        await obj.insert()
    end_time = time.time()
    print(f'Загружено {len(data_to_load)} объектов')
    print(f'Время выполнения: {end_time - start_time} сек')


async def main(size: int):
    """Основной метод для запуска приложения"""
    print('________________________________________________________')
    print('Тестирование скорости загрузки данных в БД ...')
    users = await generate_user_data(size)
    await load_data_to_db(data_to_load=users)

if "__main__" == __name__:
    asyncio.run(main())
