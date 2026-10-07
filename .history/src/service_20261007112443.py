import logging
import threading
from typing import Optional
from src.encoder import Base62Encoder
from src.models import URLRecord, AnalyticsResponse
from src.repository import BaseRepository
from src.exceptions import URLNotFoundException, AliasConflictException
logger = logging.getLogger(__name__)


class URLShortenerService:
    """Core domain service handling business logic, synchronization, and coordination."""

    def __init__(self, repository: BaseRepository, seed_counter: int = 10_000_000):
        self.repo = repository
        self._counter = seed_counter
        self._counter_lock = threading.Lock()

    def shorten_url(self, original_url: str, custom_alias: Optional[str] = None) -> str:
        if custom_alias:
            if self.repo.find_by_code(custom_alias):
                logger.warning("Conflict detected for custom alias: '%s'", custom_alias)
                raise AliasConflictException(f"Alias '{custom_alias}' is already in use.")
            code = custom_alias
        else:
            with self._counter_lock:
                self._counter += 1
                code = Base62Encoder.encode(self._counter)

        record = URLRecord(short_code=code, original_url=original_url)
        self.repo.save(record)
        logger.info("Successfully shortened URL: %s -> %s", original_url, code)
        return code

    def resolve_url(self, short_code: str) -> str:
        record = self.repo.find_by_code(short_code)
        if not record:
            logger.warning("Resolution failed: Code '%s' not found", short_code)
            raise URLNotFoundException(f"Short code '{short_code}' not found.")

        self.repo.increment_clicks(short_code)
        logger.info("Resolved code '%s' -> '%s'", short_code, record.original_url)
        return record.original_url

    def get_analytics(self, short_code: str) -> AnalyticsResponse:
        record = self.repo.find_by_code(short_code)
        if not record:
            logger.error("Analytics lookup failed: Code '%s' not found", short_code)
            raise URLNotFoundException(f"Short code '{short_code}' not found.")

        total_clicks = self.repo.get_clicks(short_code)
        return AnalyticsResponse(
            short_code=record.short_code,
            original_url=record.original_url,
            total_clicks=total_clicks,
            created_at=record.created_at,
        )