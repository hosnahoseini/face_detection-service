import pytest
from starlette.testclient import TestClient

from src.face.main import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c