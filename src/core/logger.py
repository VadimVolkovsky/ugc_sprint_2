import logging
import os

from asgi_correlation_id.context import correlation_id
from uuid import uuid4

from core.config import settings

DEFAULT_LOG_FORMAT = '{"request_id": "%(request_id)s", "asctime": \
             "%(asctime)s", "levelname": "%(levelname)s", \
             "name": "%(name)s", "message": "%(message)s"}'


LOG_FORMAT = '{"request_id": "%(request_id)s", "asctime": \
             "%(asctime)s", "levelname": "%(levelname)s", \
             "name": "%(name)s", "message": "%(message)s", \
             "method": "%(method)s", "path": "%(path)s", \
             "query_params": "%(query_params)s", "status_code": "%(status_code)s"}'


logger = logging.getLogger('posts_logger')


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        request_id = correlation_id.get()
        if not request_id:
            request_id = uuid4()

        record.request_id = request_id
        correlation_id.set(request_id)
        return True


def configure_logging():
    if not os.path.exists(settings.app_path_log):
        open(settings.app_path_log, 'w').close()

    basic_handler = logging.FileHandler(filename=f"{settings.app_path_log}", mode="w")
    basic_handler.addFilter(RequestIdFilter())
    logging.basicConfig(
        handlers=[basic_handler],
        level=logging.INFO,
        format=DEFAULT_LOG_FORMAT
    )

    formatter = logging.Formatter(LOG_FORMAT)
    posts_handler = logging.FileHandler(filename=f"{settings.app_path_log}", mode="w")
    posts_handler.setFormatter(formatter)
    posts_handler.addFilter(RequestIdFilter())
    logger.addHandler(posts_handler)
