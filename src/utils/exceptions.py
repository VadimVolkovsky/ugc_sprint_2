class DbGeneralError(Exception):
    """Базовая ошибка при работе с данными верификации."""


class FilmNotExistError(DbGeneralError):
    """Фильм не найден"""


class UserNotExistError(DbGeneralError):
    """Пользователь не найден"""


class ReviewNotExistError(DbGeneralError):
    """Отзыв не найден"""
