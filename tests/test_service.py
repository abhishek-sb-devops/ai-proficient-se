import pytest
from app.repository import InMemoryRepository
from app.service import URLShortenerService
from app.exceptions import URLNotFoundException, AliasConflictException


@pytest.fixture
def service():
    repo = InMemoryRepository()
    return URLShortenerService(repository=repo, seed_counter=100)


def test_shorten_and_resolve_flow(service):
    code = service.shorten_url("https://python.org")
    assert code is not None

    resolved = service.resolve_url(code)
    assert resolved == "https://python.org"


def test_custom_alias_conflict(service):
    service.shorten_url("https://example.com/1", custom_alias="my-link")
    with pytest.raises(AliasConflictException):
        service.shorten_url("https://example.com/2", custom_alias="my-link")


def test_non_existent_code_raises_not_found(service):
    with pytest.raises(URLNotFoundException):
        service.resolve_url("missing")


def test_analytics_click_tracking(service):
    code = service.shorten_url("https://fastapi.tiangolo.com")
    service.resolve_url(code)
    service.resolve_url(code)

    analytics = service.get_analytics(code)
    assert analytics.total_clicks == 2