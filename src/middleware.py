import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

logger = logging.getLogger("app.middleware")


class RequestCorrelationMiddleware(BaseHTTPMiddleware):
    """Injects a unique X-Request-ID header into every request and response cycle."""

    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id

        logger.info("Incoming Request [%s] %s %s", correlation_id, request.method, request.url.path)

        response = await call_next(request)
        response.headers["X-Request-ID"] = correlation_id

        logger.info("Completed Request [%s] Status: %d", correlation_id, response.status_code)
        return response
