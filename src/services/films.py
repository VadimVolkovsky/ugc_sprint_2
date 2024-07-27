import logging
from operator import itemgetter

from models.films import Film, LikeUser, ReviewUser
from services.base import Service
from utils import exceptions
from utils.params import Sort, sort_by_count

logger = logging.getLogger(__name__)


class FilmService(Service):
    """Сервис для работы с кинопроизведениями"""
    def __init__(self):
        super().__init__()
        self.collection = Film
        self.like_user = LikeUser
        self.review = ReviewUser

    async def update_film_review(self, user_id, film_id, review_id, text):
        review = self.review(id=review_id, user_id=user_id, text=text, likes=[])
        await self.update_review(self.collection, film_id, review)

    async def update_film_like(self, user_id, film_id, grade):
        dict_like = {"user_id": user_id, "grade": grade}
        await self.update_like(dict_like, self.collection, film_id, self.like_user)

    async def update_film_review_like(self, review_id, user_id, grade):
        await self.update_review_like(self.collection, review_id, user_id, grade)

    async def remove_film_review_like(self, review_id, user_id):
        await self.remove_review_like(self.collection, review_id, user_id)

    async def get_film(self, film_id):
        film = await self.collection.get(film_id)
        if not film:
            logger.exception("Fail request to not exist film")
            raise exceptions.FilmNotExistError
        return film

    async def remove_film_like(self, user_id, film_id):
        film = await self.get_film(film_id)
        await self.remove_like(film, self.collection, "user_id", user_id)

    async def remove_film_review(self, user_id, film_id):
        user = await self.get_film(film_id)
        await self.remove_review(user, self.collection, "user_id", user_id)

    async def film_likes(self, film_id):
        film = await self.get_film(film_id)
        likes = [r.grade for r in film.likes]
        score = 0 if not likes else sum(likes) / len(likes)
        return {"score": score}

    async def film_reviews(self, film_id, params):
        film = await self.get_film(film_id)
        reviews = [r.model_dump() for r in film.reviews]

        if reviews:
            if params.sort == Sort.popular:
                reviews = sorted(reviews, key=sort_by_count, reverse=True)
            elif params.sort == Sort.desc:
                reviews = sorted(reviews, key=itemgetter('created_at'), reverse=True)

        offset = 0 if params.page_number == 1 else params.page_size * params.page_number - params.page_size
        limit = offset + params.page_size
        return reviews[offset:limit]

    async def film_review_likes(self, film_id, review_id):
        film = await self.get_film(film_id)
        score = await self.review_likes(film, review_id)
        return score


def get_film_service() -> FilmService:
    return FilmService()
