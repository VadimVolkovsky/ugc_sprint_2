import asyncio
import os
import time

import asyncpg
from dotenv import load_dotenv

load_dotenv()

NUMBER_OF_USERS = 10000


async def extract_users_likes(conn: asyncpg.connection.Connection):
    print('________________________________________________________')
    print(f'Получение лайков {NUMBER_OF_USERS} пользователей из БД ...')
    start_time = time.time()
    query = """SELECT id FROM users LIMIT 10000;"""
    users = await conn.fetch(query)
    users_id = tuple(user[0] for user in users)

    query = f"""SELECT film_id, user_id, grade FROM like_film WHERE user_id IN {users_id}"""
    users_likes = await conn.fetch(query)
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
    await extract_users_likes(conn)


asyncio.run(main())