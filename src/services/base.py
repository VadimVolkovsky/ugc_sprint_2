import logging
from uuid import UUID
from models.films import LikeUser
from utils import exceptions

logger = logging.getLogger(__name__)


class Service:
    def __init__(self):
        self.review_like = LikeUser

    @staticmethod
    async def update_like(dict_like, collection, collection_id, model_like):
        instance = await collection.get(collection_id)
        like = model_like(**dict_like)
        if not instance:
            await collection(id=collection_id, likes=[like], reviews=[]).insert()
        else:
            await instance.update({"$push": {collection.likes: like}})

    async def update_review_like(self, collection, review_id, user_id, grade):
        await collection.find_one({"reviews.id": UUID(review_id)}).update(
            {"$push": {"reviews.$.likes": self.review_like(user_id=user_id, grade=grade)}})

    @staticmethod
    async def remove_review_like(collection, review_id, user_id):
        instance = await collection.find_one({"reviews.id": UUID(review_id)})
        if not instance:
            logger.exception("Fail request to not exist review")
            raise exceptions.ReviewNotExistError
        reviews = [r for r in instance.reviews if r.id == UUID(review_id)]
        review = None if not reviews else reviews[0]
        if review:
            likes = [r for r in review.likes if r.user_id == UUID(user_id)]
            like = None if not likes else likes[0]
            await collection.find_one({"reviews.id": UUID(review_id)}).update({"$pull": {"reviews.$.likes": like}})

    @staticmethod
    async def remove_like(instance, collection, diff_attr_id, diff_id):
        likes = [r for r in instance.likes if r.__getattribute__(f"{diff_attr_id}") == UUID(diff_id)]
        like = None if not likes else likes[0]
        await instance.update({"$pull": {collection.likes: like}})

    @staticmethod
    async def update_review(collection, collection_id, review):
        instance = await collection.get(collection_id)
        if not instance:
            await collection(id=collection_id, likes=[], reviews=[review]).insert()
        else:
            await instance.update({"$push": {collection.reviews: review}})

    @staticmethod
    async def remove_review(instance, collection, diff_attr_id, diff_id):
        reviews = [r for r in instance.reviews if r.__getattribute__(f"{diff_attr_id}") == UUID(diff_id)]
        review = None if not reviews else reviews[0]
        await instance.update({"$pull": {collection.reviews: review}})

    @staticmethod
    async def review_likes(instance, review_id):
        reviews = [r for r in instance.reviews if r.id == UUID(review_id)]
        review = None if not reviews else reviews[0]
        if not review:
            logger.exception("Fail request to not exist review")
            raise exceptions.ReviewNotExistError

        likes = [r.grade for r in review.likes]
        score = 0 if not likes else sum(likes)/len(likes)
        return {"score": score}
