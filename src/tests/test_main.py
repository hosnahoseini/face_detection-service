import json

import pytest

from src.app import crud

def test_create_image(test_app, monkeypatch):
    test_request_payload = {
        "name": "string",
        "address": "string",
        "date": "2022-08-16"
        }
    test_response_payload = {
        "name": "string",
        "address": "string",
        "date": "2022-08-16",
        "id": 100,

        }

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)
    response = test_app.post("/image/", data=json.dumps(test_request_payload),)
    assert response.json() == test_response_payload

    assert response.status_code == 201


def test_create_image_invalid_json(test_app):
    response = test_app.post("/image/", data=json.dumps({"name": "something"}))
    assert response.status_code == 422


def test_read_image(test_app, monkeypatch):
    test_data = {
                "id": 100,
                "name": "string",
                "address": "string",
                "date": "2022-08-16"
                }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/images/100")
    assert response.status_code == 201
    assert response.json() == test_data


def test_read_image_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/images/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "image not found"