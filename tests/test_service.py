import os
import pytest
from src.repository import SQLiteRepository
from src.service import URLShortenerService
from src.exceptions import URLNotFoundException, AliasConflictException

TEST_DB = "test_service_urls.db"


@pytest.fixture(autouse=True)
def setup_and_cleanup_db():
    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except PermissionError:
            pass

    yield

    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except PermissionError:
            pass


def test_shorten_url_generates_code():
    repo = SQLiteRepository(db_path=TEST_DB)
    service = URLShortenerService(repository=repo)
    record = service.shorten_url("https://www.example.com")
    assert "short_code" in record
    assert record["original_url"] == "https://www.example.com"


def test_resolve_url_success():
    repo = SQLiteRepository(db_path=TEST_DB)
    service = URLShortenerService(repository=repo)
    record = service.shorten_url("https://www.example.com")
    resolved_url = service.resolve_url(record["short_code"])
    assert resolved_url == "https://www.example.com"


def test_resolve_url_not_found():
    repo = SQLiteRepository(db_path=TEST_DB)
    service = URLShortenerService(repository=repo)
    with pytest.raises(URLNotFoundException):
        service.resolve_url("nonexistent")


def test_custom_alias_success():
    repo = SQLiteRepository(db_path=TEST_DB)
    service = URLShortenerService(repository=repo)
    record = service.shorten_url("https://www.example.com", custom_alias="my-link")
    assert record["short_code"] == "my-link"
    assert service.resolve_url("my-link") == "https://www.example.com"


def test_custom_alias_conflict():
    repo = SQLiteRepository(db_path=TEST_DB)
    service = URLShortenerService(repository=repo)
    service.shorten_url("https://www.example.com", custom_alias="duplicate")
    with pytest.raises(AliasConflictException):
        service.shorten_url("https://www.another.com", custom_alias="duplicate")
