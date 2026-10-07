import pytest
from src.repository import InMemoryRepository
from src.service import URLShortenerService
from src.exceptions import URLNotFoundException, AliasConflictException


def test_shorten_url_generates_code():
    repo = InMemoryRepository()
    service = URLShortenerService(repository=repo)
    code = service.shorten_url("https://www.example.com")
    assert code is not None
    assert isinstance(code, str)


def test_resolve_url_success():
    repo = InMemoryRepository()
    service = URLShortenerService(repository=repo)
    code = service.shorten_url("https://www.example.com")
    resolved_url = service.resolve_url(code)
    assert resolved_url == "https://www.example.com"


def test_resolve_url_not_found():
    repo = InMemoryRepository()
    service = URLShortenerService(repository=repo)
    with pytest.raises(URLNotFoundException):
        service.resolve_url("nonexistent")


def test_custom_alias_success():
    repo = InMemoryRepository()
    service = URLShortenerService(repository=repo)
    alias = service.shorten_url("https://www.example.com", custom_alias="my-link")
    assert alias == "my-link"
    assert service.resolve_url("my-link") == "https://www.example.com"


def test_custom_alias_conflict():
    repo = InMemoryRepository()
    service = URLShortenerService(repository=repo)
    service.shorten_url("https://www.example.com", custom_alias="duplicate")
    with pytest.raises(AliasConflictException):
        service.shorten_url("https://www.another.com", custom_alias="duplicate")
