import logging
import sys
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse

from app.config import settings
from app.models import ShortenRequest, AnalyticsResponse
from app.repository import InMemoryRepository
from app.service import URLShortenerService
from app.exceptions import URLNotFoundException, AliasConflictException
from app.middleware import RequestCorrelationMiddleware

# -----------------------------------------------------------------------------
# Logging Configuration
# -----------------------------------------------------------------------------
log_formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)

file_handler = logging.FileHandler(settings.log_file_path, mode="a", encoding="utf-8")
file_handler.setFormatter(log_formatter)

root_logger = logging.getLogger()
root_logger.setLevel(settings.log_level)
root_logger.addHandler(console_handler)
root_logger.addHandler(file_handler)

logger = logging.getLogger("app")

# Initialize Dependencies
repo = InMemoryRepository()
service = URLShortenerService(repository=repo, seed_counter=settings.base_counter_seed)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Production-grade URL Shortener microservice with correlation middleware and health probes.",
)

# Register Custom Middleware
app.add_middleware(RequestCorrelationMiddleware)


# -----------------------------------------------------------------------------
# Liveness & Readiness Health Probes
# -----------------------------------------------------------------------------
@app.get("/healthz", status_code=status.HTTP_200_OK, tags=["Health"])
def liveness_probe():
    """Liveness probe for container orchestrators (Kubernetes/Docker)."""
    return {"status": "healthy", "service": settings.app_name}


@app.get("/readyz", status_code=status.HTTP_200_OK, tags=["Health"])
def readiness_probe():
    """Readiness probe checking storage dependency health."""
    # Add database/cache ping logic here when migrating to SQL/Redis
    return {"status": "ready", "storage": "in_memory_ok"}


# -----------------------------------------------------------------------------
# Domain Endpoints
# -----------------------------------------------------------------------------
@app.post("/api/v1/shorten", status_code=status.HTTP_201_CREATED, tags=["URL Operations"])
def shorten_url(payload: ShortenRequest):
    try:
        short_code = service.shorten_url(
            original_url=str(payload.url), custom_alias=payload.custom_alias
        )
        return {"short_code": short_code, "original_url": str(payload.url)}
    except AliasConflictException as e:
        logger.warning("HTTP 409 Conflict: %s", e.message)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except Exception as e:
        logger.error("Unhandled error during shorten operation: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during URL shortening.",
        )


@app.get("/{short_code}", response_class=RedirectResponse, status_code=status.HTTP_302_FOUND, tags=["URL Operations"])
def redirect_to_url(short_code: str):
    try:
        target_url = service.resolve_url(short_code)
        return RedirectResponse(url=target_url, status_code=status.HTTP_302_FOUND)
    except URLNotFoundException as e:
        logger.warning("HTTP 404 Not Found for short_code: '%s'", short_code)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@app.get("/api/v1/analytics/{short_code}", response_model=AnalyticsResponse, tags=["Analytics"])
def get_analytics(short_code: str):
    try:
        return service.get_analytics(short_code)
    except URLNotFoundException as e:
        logger.warning("HTTP 404 Analytics lookup failed for short_code: '%s'", short_code)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)