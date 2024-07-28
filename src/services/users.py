import logging
from models.films import User, LikeFilm, ReviewFilm
from services.base import Service
from utils import exceptions

logger = logging.getLogger(__name__)


class UserService(Service):
    """Сервис для работы с кинопроизведениями"""
    def __init__(self):
        super().__init__()
        self.collection = User
        self.like_film = LikeFilm
        self.review = ReviewFilm

    async def update_user_review(self, user_id, film_id, review_id, text):
        review = self.review(id=review_id, film_id=film_id, text=text, likes=[])
        await self.update_review(self.collection, user_id, review)

    async def update_user_like(self, user_id, film_id, grade):
        dict_like = {"film_id": film_id, "grade": grade}
        await self.update_like(dict_like, self.collection, user_id, self.like_film)

    async def update_user_review_like(self, review_id, user_id, grade):
        await self.update_review_like(self.collection, review_id, user_id, grade)

    async def remove_user_review_like(self, review_id, user_id):
        await self.remove_review_like(self.collection, review_id, user_id)

    async def get_user(self, film_id):
        user = await self.collection.get(film_id)
        if not user:
            logger.exception("Fail request to not exist user")
            raise exceptions.UserNotExistError
        return user

    async def remove_user_like(self, user_id, film_id):
        user = await self.get_user(user_id)
        await self.remove_like(user, self.collection, "film_id", film_id)

    async def remove_user_review(self, user_id, film_id):
        user = await self.get_user(user_id)
        await self.remove_review(user, self.collection, "film_id", film_id)


def get_user_service() -> UserService:
    return UserService()
