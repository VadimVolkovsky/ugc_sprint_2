from typing import Annotated
from uuid import uuid4
from fastapi import APIRouter, Depends, Path, status, Response, Security
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer

from api.v1.handlers import ExceptionHandlerRoute
from core.config import settings
from schemas.films import ScoreSchemaOut, ReviewSchemaIn, ReviewFilmSchemaOut, GradeSchemaIn
from utils.params import CommonQueryParams
from services.films import get_film_service, FilmService
from services.users import get_user_service, UserService


router = APIRouter()
router.route_class = ExceptionHandlerRoute

access_security = JwtAccessBearer(secret_key=settings.secret_key, auto_error=True)


@router.post(
    "/{film_id}/like",
    tags=["film likes"],
    responses={status.HTTP_204_NO_CONTENT: {"description": "Лайк успешно добавлен"}}
)
async def add_like_film(
    film_id: Annotated[str, Path(description="ID фильма в форматее UUID")],
    grade: GradeSchemaIn,
    film_service: FilmService = Depends(get_film_service),
    user_service: UserService = Depends(get_user_service),
    credentials: JwtAuthorizationCredentials = Security(access_security)
):
    user_id = credentials["user_id"]
    await film_service.update_film_like(user_id, film_id, grade.grade)
    await user_service.update_user_like(user_id, film_id, grade.grade)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{film_id}/like",
    tags=["film likes"],
    responses={status.HTTP_204_NO_CONTENT: {"description": "Лайк успешно удален"}}
)
async def remove_like_film(
    film_id: Annotated[str, Path(description="ID фильма в форматее UUID")],
    film_service: FilmService = Depends(get_film_service),
    user_service: UserService = Depends(get_user_service),
    credentials: JwtAuthorizationCredentials = Security(access_security)
):
    user_id = credentials["user_id"]
    await film_service.remove_film_like(user_id, film_id)
    await user_service.remove_user_like(user_id, film_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{film_id}/like", tags=["film likes"], response_model=ScoreSchemaOut)
async def like_film(
        film_id: Annotated[str, Path(description="ID фильма в форматее UUID")],
        film_service: FilmService = Depends(get_film_service),
):
    score = await film_service.film_likes(film_id)
    return score


@router.post(
    "/{film_id}/review",
    tags=["reviews"],
    responses={status.HTTP_204_NO_CONTENT: {"description": "Рецензия успешно добавлена"}}
)
async def add_review_film(
    film_id: Annotated[str, Path(description="ID фильма в форматее UUID")],
    review_schema_in: ReviewSchemaIn,
    film_service: FilmService = Depends(get_film_service),
    user_service: UserService = Depends(get_user_service),
    credentials: JwtAuthorizationCredentials = Security(access_security)
):
    user_id = credentials["user_id"]
    text = review_schema_in.text
    review_id = uuid4()
    await film_service.update_film_review(user_id, film_id, review_id, text)
    await user_service.update_user_review(user_id, film_id, review_id, text)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{film_id}/review",
    tags=["reviews"],
    responses={status.HTTP_204_NO_CONTENT: {"description": "Рецензия успешно удалена"}}
)
async def remove_review_film(
    film_id: Annotated[str, Path(description="ID фильма в форматее UUID")],
    film_service: FilmService = Depends(get_film_service),
    user_service: UserService = Depends(get_user_service),
    credentials: JwtAuthorizationCredentials = Security(access_security)
):
    user_id = credentials["user_id"]
    await film_service.remove_film_review(user_id, film_id)
    await user_service.remove_user_review(user_id, film_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{film_id}/review", tags=["reviews"], response_model=list[ReviewFilmSchemaOut])
async def review_film(
    query_params: Annotated[CommonQueryParams, Depends()],
    film_id: Annotated[str, Path(description="ID фильма в форматее UUID")],
    film_service: FilmService = Depends(get_film_service),
):
    reviews = await film_service.film_reviews(film_id, query_params)
    return reviews


@router.post(
    "/{film_id}/review/{review_id}/like",
    tags=["review likes"],
    responses={status.HTTP_204_NO_CONTENT: {"description": "Лайк на рецензию успешно добавлен"}}
)
async def add_like_review(
    film_id: Annotated[str, Path(description="ID фильма в форматее UUID")],
    review_id: Annotated[str, Path(description="ID фильма в форматее UUID")],
    grade: GradeSchemaIn,
    film_service: FilmService = Depends(get_film_service),
    user_service: UserService = Depends(get_user_service),
    credentials: JwtAuthorizationCredentials = Security(access_security)
):
    user_id = credentials["user_id"]
    await film_service.update_film_review_like(review_id, user_id, grade.grade)
    await user_service.update_user_review_like(review_id, user_id, grade.grade)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{film_id}/review/{review_id}/like",
    tags=["review likes"],
    responses={status.HTTP_204_NO_CONTENT: {"description": "Лайк на рецензию успешно удален"}}
)
async def remove_like_review(
    film_id: Annotated[str, Path(description="ID фильма в форматее UUID")],
    review_id: Annotated[str, Path(description="ID фильма в форматее UUID")],
    film_service: FilmService = Depends(get_film_service),
    user_service: UserService = Depends(get_user_service),
    credentials: JwtAuthorizationCredentials = Security(access_security)
):
    user_id = credentials["user_id"]
    await film_service.remove_film_review_like(review_id, user_id)
    await user_service.remove_user_review_like(review_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{film_id}/review/{review_id}/like",
    tags=["review likes"],
    response_model=ScoreSchemaOut
)
async def like_review(
    film_id: Annotated[str, Path(description="ID фильма в форматее UUID")],
    review_id: Annotated[str, Path(description="ID фильма в форматее UUID")],
    film_service: FilmService = Depends(get_film_service),
):
    score = await film_service.film_review_likes(film_id, review_id)
    return score
