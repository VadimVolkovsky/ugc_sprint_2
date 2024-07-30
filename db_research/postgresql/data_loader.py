import os
import random
import time
from datetime import datetime, timezone
from uuid import UUID, uuid4

from dotenv import load_dotenv
from faker import Faker
from pydantic import Field, BaseModel
import asyncio
import asyncpg

# список понравившихся пользователю фильмов (список лайков пользователя);
# список закладок;
# средняя пользовательская оценка фильма.

faker = Faker()

load_dotenv()

NUMBER_OF_USERS = 10000
NUMBER_OF_FILMS = 10000


class Bookmark(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    film_id: UUID
    user_id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LikeFilm(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    film_id: UUID
    user_id: UUID
    grade: int


class LikeReview(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    review_id: UUID
    grade: int


class ReviewFilm(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    film_id: UUID
    user_id: UUID


class ReviewUser(BaseModel):
    id: UUID
    text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: UUID
    likes: list[LikeReview]


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Film(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


async def create_tables(conn):
    try:
        create_user_table = '''
            CREATE TABLE users(
                id uuid PRIMARY KEY,
                created_at date
            )
        '''

        create_film_table = '''
            CREATE TABLE films(
                id uuid PRIMARY KEY,
                created_at date
            )
        '''

        create_bookmark_table = '''
            CREATE TABLE bookmark(
                id uuid PRIMARY KEY,
                film_id uuid REFERENCES films (id),
                user_id uuid REFERENCES users (id),
                created_at date
            )
        '''

        create_like_film_table = '''
            CREATE TABLE like_film(
                id uuid PRIMARY KEY,
                film_id uuid REFERENCES films (id),
                user_id uuid REFERENCES users (id),
                grade integer
            )
        '''

        create_review_film_table = '''
            CREATE TABLE review_film(
                id uuid PRIMARY KEY,
                text TEXT,
                created_at date,
                film_id uuid REFERENCES films (id),
                user_id uuid REFERENCES users (id)
            )
        '''

        create_like_reviews_table = '''
            CREATE TABLE like_review(
                id uuid PRIMARY KEY,
                review_id uuid REFERENCES review_film (id),
                user_id uuid REFERENCES users (id),
                grade integer
            )
        '''

        await conn.execute(create_user_table)
        await conn.execute(create_film_table)

        await conn.execute(create_bookmark_table)
        await conn.execute(create_like_film_table)
        await conn.execute(create_review_film_table)
        await conn.execute(create_like_reviews_table)
    except asyncpg.exceptions.DuplicateTableError:
        pass


async def generate_users():
    data = [User(id=uuid4()) for _ in range(NUMBER_OF_USERS)]
    return data


async def generate_films():
    data = [Film(id=uuid4()) for _ in range(NUMBER_OF_FILMS)]
    return data


async def generate_film_likes(users, films):
    data = []
    for film in films:
        for user in random.sample(users, random.randint(1, 3)):
            data.append(
                LikeFilm(
                    id=uuid4(),
                    film_id=film.id,
                    user_id=user.id,
                    grade=random.randint(1, 10),
                )
            )
    return data


async def generate_film_reviews(users, films):
    data = []
    for film in films:
        for user in random.sample(users, random.randint(1, 3)):
            data.append(
                ReviewFilm(
                    id=uuid4(),
                    text=faker.text(1000),
                    film_id=film.id,
                    user_id=user.id,
                )
            )
    return data


async def generate_review_likes(users, reviews):
    data = []
    for review in reviews:
        for user in random.sample(users, random.randint(1, 3)):
            data.append(
                LikeReview(
                    id=uuid4(),
                    review_id=review.id,
                    user_id=user.id,
                    grade=random.randint(1, 10),
                )
            )
    return data


async def load_data_to_postgres(conn: asyncpg.connection.Connection, data, table_name):
    data_dicts = [item.dict() for item in data]

    # Создание списка кортежей значений для вставки
    args = [tuple(item.values()) for item in data_dicts]

    # Определение столбцов таблицы на основе первого элемента (предполагая, что все элементы имеют одинаковую структуру)
    columns = ', '.join(data_dicts[0].keys())

    # В зависимости от количества колонок генерируем под них %s.
    values = ', '.join([f'${i}' for i in range(1, len(columns.split(',')) + 1)])

    # Формирование SQL запроса
    query = f"""INSERT INTO {table_name} ({columns}) VALUES({values});"""

    print(f'Загрузка в PostgreSQL {len(data)} объектов в таблицу {table_name}')
    start_time = time.time()
    await conn.executemany(query, args)
    end_time = time.time()
    print(f'Время выполнения: {end_time - start_time} сек')


async def main():
    dsl = {
        'database': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT'),
    }
    conn = await asyncpg.connect(**dsl)
    await create_tables(conn)
    users = await generate_users()
    films = await generate_films()
    films_likes = await generate_film_likes(users, films)
    reviews = await generate_film_reviews(users, films)
    reviews_likes = await generate_review_likes(users, reviews)

    await load_data_to_postgres(conn, users, table_name='users')
    await load_data_to_postgres(conn, films, table_name='films')
    await load_data_to_postgres(conn, films_likes, table_name='like_film')
    await load_data_to_postgres(conn, reviews, table_name='review_film')
    await load_data_to_postgres(conn, reviews_likes, table_name='like_review')

    await conn.close()


asyncio.get_event_loop().run_until_complete(main())
