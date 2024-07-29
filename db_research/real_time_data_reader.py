import asyncio
import random
import time

import faker

from db_research.data_extract import UserFilmLikes
from src.models.films import Bookmark, LikeFilm, LikeUser, ReviewFilm, User

faker = faker.Faker()
time_result = []


async def generate_user_data(size) -> tuple[list[User], list[LikeFilm]]:
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
                likes=[],
                reviews=random.sample(reviews, random.randint(0, 5)),
                bookmarks=random.sample(bookmarks, random.randint(0, 5)),
            )
        )
    print(f'Генерация и загрузка {len(users)} объектов Users в БД (без лайков) ...')

    for user in users:
        await user.insert()
    print(f'Добавлено {len(users)} пользователей в БД (без лайков)')
    return users, films_likes


async def real_time_load_and_read_data(user, likes):

    user_in_db = await User.get(user.id)
    user_in_db.likes = likes
    await user_in_db.replace()

    start_time = time.time()
    user = await User.find_one(User.id == user.id).project(UserFilmLikes)
    end_time = time.time()
    if len(user.likes) == 0:
        print(f'не добавились лайки для юзера {user.id}')
    time_result.append(end_time - start_time)


async def async_execute(users, films_likes):
    print('Запуск тестирования параллельного добавления и чтения лайков из БД ...')
    tasks = [asyncio.ensure_future(real_time_load_and_read_data(user, random.sample(films_likes, random.randint(3, 15)))) for user in users]
    await asyncio.wait(tasks)
    time_sum = sum(time_result)
    print(f'Среднее время чтения при добавлении лайков: {time_sum/len(time_result)} сек')


async def main(size: int):
    print('________________________________________________________')
    print('Тестирование скорости параллельной загрузки и чтения объектов')
    users, films_likes = await generate_user_data(size)
    await async_execute(users, films_likes)

if "__main__" == __name__:
    asyncio.run(main())
