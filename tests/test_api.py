import os
import pytest
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from src.main import app, repo

client = TestClient(app)
TEST_API_DB = "test_api_urls.db"


@pytest.fixture(autouse=True)
def setup_and_cleanup_db():
    repo.db_path = TEST_API_DB
    repo._init_db()

    yield

    if os.path.exists(TEST_API_DB):
        try:
            os.remove(TEST_API_DB)
        except PermissionError:
            pass


def test_health_check():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_shorten_and_redirect_flow():
    payload = {"original_url": "https://example.com/test"}
    res = client.post("/api/v1/shorten", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert "short_code" in data
    assert "created_at" in data

    code = data["short_code"]
    redirect_res = client.get(f"/{code}", follow_redirects=False)
    assert redirect_res.status_code == 302
    assert redirect_res.headers["location"] == "https://example.com/test"


def test_custom_alias_conflict_returns_400():
    payload = {"original_url": "https://example.com", "custom_alias": "my-alias"}
    client.post("/api/v1/shorten", json=payload)

    dup_res = client.post("/api/v1/shorten", json=payload)
    assert dup_res.status_code == 400


def test_concurrency_alias_creation():
    payload = {"original_url": "https://example.com", "custom_alias": "race-alias"}

    def make_request():
        return client.post("/api/v1/shorten", json=payload)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(5)]
        results = [f.result() for f in futures]

    status_codes = [r.status_code for r in results]
    assert status_codes.count(201) == 1
    assert status_codes.count(400) == 4
