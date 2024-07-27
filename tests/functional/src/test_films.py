from http import HTTPStatus
import pytest

from tests.functional.testdata.films import (
    FILM_ID,
    ENDPOINT,
    film_data,
    user_data,
    WRONG_GRADE,
    EXPECTED_USER_ADD_LIKE,
    EXPECTED_FILM_ADD_LIKE,
    EXPECTED_REMOVE_LIKE_USER,
    EXPECTED_REMOVE_LIKE_FILM,
    EXPECTED_USER_ADD_REVIEW,
    EXPECTED_FILM_ADD_REVIEW,
)


class TestUserEndpointFilms:
    @pytest.mark.parametrize(
        "query_data, expected_answer",
        [
            (
                {"grade": 1},
                {"status": HTTPStatus.NO_CONTENT, "body": None},
            ),
            (
                {"grade": 10},
                {"status": HTTPStatus.UNPROCESSABLE_ENTITY, "body": WRONG_GRADE},
            ),
        ],
    )
    @pytest.mark.asyncio(scope="session")
    async def test_endpoint_add_like_film_wrong_grade(
            self, clean_db, make_request, authorize, get_from_db, mongo_client, query_data, expected_answer
    ):
        token = await authorize()

        body, status = await make_request("post", f"{ENDPOINT}/{FILM_ID}/like/", json=query_data, token=token)

        assert expected_answer == {"status": status, "body": body}

    @pytest.mark.asyncio(scope="session")
    async def test_like_film_added_to_db(
            self, clean_db, make_request, authorize, get_from_db, mongo_client
    ):
        params = {"grade": 1}
        token = await authorize()

        _, status = await make_request("post", f"{ENDPOINT}/{FILM_ID}/like/", json=params, token=token)
        db = mongo_client
        film = get_from_db(collection=db["Film"], condition=film_data)
        del film["created_at"]
        user = get_from_db(collection=db["User"], condition=user_data)
        del user["created_at"]

        assert film == EXPECTED_FILM_ADD_LIKE
        assert user == EXPECTED_USER_ADD_LIKE

    @pytest.mark.asyncio(scope="session")
    async def test_endpoint_remove_like_film(
            self, make_request, authorize, get_from_db, mongo_client
    ):
        params = {"grade": 1}
        token = await authorize()

        _, status = await make_request("delete", f"{ENDPOINT}/{FILM_ID}/like/", json=params, token=token)
        db = mongo_client
        film = get_from_db(collection=db["Film"], condition=film_data)
        del film["created_at"]
        user = get_from_db(collection=db["User"], condition=user_data)
        del user["created_at"]

        assert film == EXPECTED_REMOVE_LIKE_FILM
        assert user == EXPECTED_REMOVE_LIKE_USER

    @pytest.mark.asyncio(scope="session")
    async def test_endpoint_likes_film(
            self, make_request, get_from_db, mongo_client
    ):

        body, status = await make_request("get", f"{ENDPOINT}/{FILM_ID}/like/")

        assert status == HTTPStatus.OK
        assert body == {"score": 0}

    @pytest.mark.asyncio(scope="session")
    async def test_endpoint_add_review_film(
            self, clean_db, make_request, authorize, get_from_db, mongo_client
    ):
        params = {"text": "good film"}
        token = await authorize()

        _, status = await make_request("post", f"{ENDPOINT}/{FILM_ID}/review/", json=params, token=token)
        db = mongo_client
        film = get_from_db(collection=db["Film"], condition=film_data)
        del film["created_at"]
        del film["reviews"][0]["id"]
        del film["reviews"][0]["created_at"]
        user = get_from_db(collection=db["User"], condition=user_data)
        del user["created_at"]
        del user["reviews"][0]["id"]
        del user["reviews"][0]["created_at"]

        assert film == EXPECTED_FILM_ADD_REVIEW
        assert user == EXPECTED_USER_ADD_REVIEW
