import json

import pytest

from src.app import crud


def test_create_image(test_app, monkeypatch):
    test_request_payload = {"name": "something", "address": "something else", "date": "2022-2-2"}
    test_response_payload = {"id": 1, "name": "something", "address": "something else", "date": "2022-2-2"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/images/", data=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_image_invalid_json(test_app):
    response = test_app.post("/images/", data=json.dumps({"name": "something"}))
    assert response.status_code == 422

def test_read_image(test_app, monkeypatch):
    test_data = {"id": 1, "name": "something", "address": "something else",  "date": "2022-2-2",}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/images/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_image_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/images/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"

def test_read_all_images(test_app, monkeypatch):
    test_data = [
        {"name": "something", "address": "something else", "date": "2022-2-2", "id": 1},
        {"name": "someone", "address": "someone else", "date": "2022-2-2", "id": 2},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/images/")
    assert response.status_code == 200
    assert response.json() == test_data
def test_update_image(test_app, monkeypatch):
    test_update_data = {"name": "someone", "address": "someone else", "date": "2022-2-2", "id": 1}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/images/1/", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"address": "bar",  "date": "2022-2-2"}, 422],
        [999, {"name": "foo", "address": "bar",  "date": "2022-2-2"}, 404],
    ],
)
def test_update_image_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/images/{id}/", data=json.dumps(payload),)
    assert response.status_code == status_code

def test_remove_image(test_app, monkeypatch):
    test_data = {"name": "something", "address": "something else", "date": "2022-2-2", "id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/images/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_image_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/images/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"