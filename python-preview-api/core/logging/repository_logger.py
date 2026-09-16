import logging
import functools
from typing import Callable

logger = logging.getLogger("app.repository")

def log_repository_call(entity_name: str):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger.info("%s called for entity: %s", func.__name__, entity_name)
            try:
                result = await func(*args, **kwargs)
                logger.info("%s succeeded for entity: %s", func.__name__, entity_name)
                return result
            except Exception as e:
                logger.exception("%s failed for entity: %s — %s", func.__name__, entity_name, e, exc_info=True)
                raise
        return wrapper
    return decorator
