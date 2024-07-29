import logging
from asgi_correlation_id.context import correlation_id
from uuid import uuid4
import logstash


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        request_id = correlation_id.get()
        if not request_id:
            request_id = uuid4()
        record.request_id = request_id
        return True


def configure_logging():
    uvicorn_logger = logging.getLogger("uvicorn.access")
    handler = logstash.LogstashHandler('logstash', 5044, version=1)
    handler.addFilter(RequestIdFilter())
    uvicorn_logger.addHandler(handler)
    logging.basicConfig(
        handlers=[handler],
        level=logging.INFO,
        format='%(levelname)s: \t  %(asctime)s %(name)s [%(request_id)s] %(message)s'
    )
