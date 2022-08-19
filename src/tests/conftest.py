import pytest
from starlette.testclient import TestClient

from src.app.main import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here

@pytest.fixture(scope="module")
def client():
    with TestClient(api) as c:
        yield c