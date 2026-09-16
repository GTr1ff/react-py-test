from functools import wraps
from sqlalchemy.exc import IntegrityError, DataError, OperationalError, SQLAlchemyError
from core.exceptions import DatabaseException


def handle_db_exceptions_async(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            raise DatabaseException("Integrity constraint violated", status_code=409) from e
        except DataError as e:
            raise DatabaseException("Invalid data format", status_code=400) from e
        except OperationalError as e:
            raise DatabaseException("Database operational error", status_code=500) from e
        except SQLAlchemyError as e:
            raise DatabaseException("General database error", status_code=500) from e
    return async_wrapper