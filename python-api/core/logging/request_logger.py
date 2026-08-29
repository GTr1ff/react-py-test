import logging
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """
    This middleware logs the request information to the console.
    """
    def __init__(self, app):
        super().__init__(app)
        self._logger = logging.getLogger("app.requests")

    async def dispatch(self, request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = request_id
        start = time.perf_counter()
        status = 500
        try:
            response = await call_next(request)
            status = response.status_code
            return response
        except Exception:
            self._logger.exception(
                "%s %s -> error req_id=%s", request.method, request.url.path, request_id,
            )
            raise
        finally:
            duration_ms = (time.perf_counter() - start) * 1000.0
            self._logger.info(
                "%s %s -> %s in %.3fms req_id=%s",
                request.method, request.url.path, status, duration_ms, request_id,
            )