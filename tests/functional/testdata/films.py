from uuid import UUID

ENDPOINT = "api/v1/films"
USER_ID = "e583fb6b-662b-47e4-8642-6e7a18dfe994"
FILM_ID = "e583fb6b-662b-47e4-8642-6e7a18dfe993"

film_data = {'_id': UUID(FILM_ID)}
user_data = {'_id': UUID(USER_ID)}

EXPECTED_FILM_ADD_LIKE = {
    '_id': UUID('e583fb6b-662b-47e4-8642-6e7a18dfe993'),
    'likes': [
        {'user_id': UUID('e583fb6b-662b-47e4-8642-6e7a18dfe994'), 'grade': 1}
    ],
    'reviews': []
}

EXPECTED_FILM_ADD_REVIEW = {
    '_id': UUID('e583fb6b-662b-47e4-8642-6e7a18dfe993'),
    'likes': [],
    'reviews': [
        {
            'text': 'good film',
            'user_id': UUID('e583fb6b-662b-47e4-8642-6e7a18dfe994'),
            'likes': []
        }
    ]
}

EXPECTED_USER_ADD_REVIEW = {
    '_id': UUID('e583fb6b-662b-47e4-8642-6e7a18dfe994'),
    'likes': [],
    'reviews': [
        {
            'text': 'good film',
            'film_id': UUID('e583fb6b-662b-47e4-8642-6e7a18dfe993'),
            'likes': []
        }
    ],
    'bookmarks': []
}


EXPECTED_USER_ADD_LIKE = {
    '_id': UUID('e583fb6b-662b-47e4-8642-6e7a18dfe994'),
    'likes': [
        {'film_id': UUID('e583fb6b-662b-47e4-8642-6e7a18dfe993'), 'grade': 1}
    ],
    'reviews': [],
    'bookmarks': []
}

EXPECTED_REMOVE_LIKE_USER = {
    '_id': UUID('e583fb6b-662b-47e4-8642-6e7a18dfe994'),
    'likes': [],
    'reviews': [],
    'bookmarks': []
}

EXPECTED_REMOVE_LIKE_FILM = {
    '_id': UUID('e583fb6b-662b-47e4-8642-6e7a18dfe993'),
    'likes': [],
    'reviews': []
}

WRONG_GRADE = {
    'detail': [
        {
            'type': 'less_than_equal',
            'loc': ['body', 'grade'],
            'msg': 'Input should be less than or equal to 1',
            'input': 10,
            'ctx': {'le': 1}
        }
    ]
}
