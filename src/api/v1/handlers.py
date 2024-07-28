from typing import Callable
from fastapi import HTTPException, status, Request, Response
from fastapi.routing import APIRoute

from utils import exceptions


class ExceptionHandlerRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except exceptions.FilmNotExistError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The wrong film_id. Film not exist.",
                )
            except exceptions.UserNotExistError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The wrong user_id. User not exist.",
                )
            except exceptions.ReviewNotExistError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The wrong review_id. Review not exist.",
                )

        return custom_route_handler
