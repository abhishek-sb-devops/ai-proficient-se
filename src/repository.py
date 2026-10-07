from abc import ABC, abstractmethod
import threading
from typing import Optional, Dict
from src.models import URLRecord


class BaseRepository(ABC):
    """Abstract Base Repository enforcing persistence interface contract."""

    @abstractmethod
    def save(self, record: URLRecord) -> None:
        pass

    @abstractmethod
    def find_by_code(self, short_code: str) -> Optional[URLRecord]:
        pass

    @abstractmethod
    def increment_clicks(self, short_code: str) -> int:
        pass

    @abstractmethod
    def get_clicks(self, short_code: str) -> int:
        pass


class InMemoryRepository(BaseRepository):
    """Thread-safe in-memory repository implementation using RLock."""

    def __init__(self):
        self._records: Dict[str, URLRecord] = {}
        self._clicks: Dict[str, int] = {}
        self._lock = threading.RLock()

    def save(self, record: URLRecord) -> None:
        with self._lock:
            self._records[record.short_code] = record
            if record.short_code not in self._clicks:
                self._clicks[record.short_code] = 0

    def find_by_code(self, short_code: str) -> Optional[URLRecord]:
        with self._lock:
            return self._records.get(short_code)

    def increment_clicks(self, short_code: str) -> int:
        with self._lock:
            if short_code in self._clicks:
                self._clicks[short_code] += 1
                return self._clicks[short_code]
            return 0

    def get_clicks(self, short_code: str) -> int:
        with self._lock:
            return self._clicks.get(short_code, 0)
