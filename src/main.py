import logging
import sys
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse

from src.config import settings
from src.models import ShortenRequest, ShortenResponse, AnalyticsResponse
from src.repository import SQLiteRepository
from src.service import URLShortenerService
from src.exceptions import URLNotFoundException, AliasConflictException
from src.middleware import RequestCorrelationMiddleware

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("app")

repo = SQLiteRepository()
service = URLShortenerService(repository=repo, seed_counter=settings.base_counter_seed)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Production-ready URL Shortener Microservice",
)

app.add_middleware(RequestCorrelationMiddleware)


@app.get("/healthz", status_code=status.HTTP_200_OK, tags=["Health"])
def liveness_probe():
    return {"status": "healthy", "service": settings.app_name}


@app.get("/readyz", status_code=status.HTTP_200_OK, tags=["Health"])
def readiness_probe():
    return {"status": "ready", "storage": "sqlite_ok"}


@app.post(
    "/api/v1/shorten",
    response_model=ShortenResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["URL Operations"],
)
def shorten_url(payload: ShortenRequest):
    try:
        record = service.shorten_url(
            original_url=str(payload.original_url),
            custom_alias=payload.custom_alias,
        )
        return record
    except AliasConflictException as e:
        logger.warning("Alias Conflict: %s", e.message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@app.get(
    "/{short_code}",
    response_class=RedirectResponse,
    status_code=status.HTTP_302_FOUND,
    tags=["URL Operations"],
)
def redirect_to_url(short_code: str):
    try:
        target_url = service.resolve_url(short_code)
        return RedirectResponse(url=target_url, status_code=status.HTTP_302_FOUND)
    except URLNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@app.get("/api/v1/analytics/{short_code}", response_model=AnalyticsResponse, tags=["Analytics"])
def get_analytics(short_code: str):
    try:
        return service.get_analytics(short_code)
    except URLNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
