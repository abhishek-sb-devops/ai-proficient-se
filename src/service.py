import logging
import threading
from src.encoder import Base62Encoder
from src.exceptions import URLNotFoundException, AliasConflictException

logger = logging.getLogger("app.service")


class URLShortenerService:
    def __init__(self, repository):
        self.repository = repository
        self.lock = threading.Lock()

    def shorten_url(self, original_url: str, custom_alias: str = None) -> dict:
        with self.lock:
            if custom_alias:
                logger.info("Attempting custom alias creation: '%s'", custom_alias)
                if self.repository.get_by_code(custom_alias):
                    logger.warning("Custom alias conflict: '%s'", custom_alias)
                    raise AliasConflictException(f"Alias '{custom_alias}' already exists.")
                short_code = custom_alias
            else:
                next_id = self.repository.get_next_sequence_id()
                short_code = Base62Encoder.encode(next_id)
                while self.repository.get_by_code(short_code):
                    next_id = self.repository.get_next_sequence_id()
                    short_code = Base62Encoder.encode(next_id)

            record = self.repository.save(short_code, original_url)
            logger.info("Successfully shortened URL: '%s' -> '%s'", original_url, short_code)
            return record

    def resolve_url(self, short_code: str) -> str:
        logger.info("Resolving short code: '%s'", short_code)
        try:
            target_url = self.repository.increment_clicks(short_code)
            logger.info("Resolved short code '%s' to '%s'", short_code, target_url)
            return target_url
        except URLNotFoundException as e:
            logger.warning("Failed to resolve short code: '%s' (Not Found)", short_code)
            raise e

    def get_analytics(self, short_code: str) -> dict:
        logger.info("Fetching analytics for short code: '%s'", short_code)
        record = self.repository.get_by_code(short_code)
        if not record:
            logger.warning("Analytics failed for short code: '%s' (Not Found)", short_code)
            raise URLNotFoundException(f"URL code '{short_code}' not found.")
        return record
