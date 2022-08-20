
from unittest import result
from fastapi.testclient import TestClient
from src.app import crud
from src.app.main import app
import pytest

def test_read_all_images():
    with TestClient(app) as client:  
        response = client.get("/images/")
        assert response.status_code == 200
        assert len(response.json()) == 20


def test_read_all_images(test_app, monkeypatch):
    with TestClient(app) as client:  
        test_data = [
                        {
                            "id": 2,
                            "name": "t1.jpg",
                            "address": "/app/resources/output/t1_output.png",
                            "date": "2022-08-02",
                            "result" : "[]"
                        },
                    ]

        async def mock_get_all():
            return test_data

        monkeypatch.setattr(crud, "get_all", mock_get_all)

        response = client.get("/images/")
        assert response.status_code == 200
        assert response.json() == test_data

def test_read_image():
    with TestClient(app) as client:  
        response = client.get("/image/2/")
        assert response.status_code == 200
        assert response.json() ==   {
                                    "id": 2,
                                    "name": "t2.jpeg",
                                    "address": "/app/resources/output/t2_output.png",
                                    "date": "2022-08-20",
                                    "result": "[[1194, 264, 75, 75], [840, 270, 71, 71], [232, 310, 72, 72], [1011, 221, 73, 73], [392, 284, 80, 80], [1382, 278, 77, 77], [560, 219, 101, 101], [820, 496, 151, 151]]"
                                }
    
def test_put_image():
    with TestClient(app) as client:  
        
        response = client.put("/image/3/", json={
                                                    "name": "boo",
                                                    "address": "foo",
                                                    "date": "2022-08-20",
                                                    "result": "[]"
                                                })
        assert response.json() ==   {
                                    "id": 3,
                                    "name": "boo",
                                    "address": "foo",
                                    "date": "2022-08-20",
                                    "result": "[]"

                                    }
        assert response.status_code == 200

# def test_create_image(test_app, monkeypatch):
#     with TestClient(app) as client:  

#         test_request_payload = {
#                                 "name": "string",
#                                 "address": "string",
#                                 "date": "2022-08-17",
#                                 "result": "[]"
#                                 }
#         test_response_payload = {
#                                 "id":16,
#                                 "name": "string",
#                                 "address": "string",
#                                 "date": "2022-08-17",
#                                 "result": "[]"
#                                 }

#         async def mock_post(payload):
#             return test_response_payload

#         monkeypatch.setattr(crud, "post", mock_post)

#         response = client.post("/image/", json=test_request_payload)

        
#         assert response.json() == test_response_payload
#         assert response.status_code == 201

def test_delete_image(monkeypatch):
    with TestClient(app) as client:  
        test_data =  {
            "id": 5,
            "name": "t3.jpg",
            "address": "/app/resources/output/t3_output.png",
            "date": "2022-08-09",
            "result": "[]"

            }

        async def mock_get(id):
            return test_data

        monkeypatch.setattr(crud, "get", mock_get)

        async def mock_delete(id):
            return id

        monkeypatch.setattr(crud, "delete", mock_delete)

        response = client.delete("/image/5/")
        assert response.status_code == 200
        assert response.json() ==   {
                                        "id": 5,
                                        "name": "t3.jpg",
                                        "address": "/app/resources/output/t3_output.png",
                                        "date": "2022-08-09",
                                        "result": "[]"

                                    }
    
def test_detect_address(test_app, monkeypatch):
    with TestClient(app) as client:  

        async def mock_post(payload):
            return None

        monkeypatch.setattr(crud, "post", mock_post)

        response = client.get("/detect_with_path/%2Fresources%2Finput%2Ft1.jpg")
        
        expected = [
                    [
                        1254,
                        216,
                        248,
                        248
                    ],
                    [
                        1001,
                        549,
                        277,
                        277
                    ],
                    [
                        787,
                        540,
                        302,
                        302
                    ],
                    [
                        248,
                        604,
                        331,
                        331
                    ]
                    ]
        assert response.status_code == 200
        assert to_set(response.json()) == to_set(expected)


def test_detect_image_file(monkeypatch):
    with TestClient(app) as client:

        async def mock_post(payload):
            return None

        monkeypatch.setattr(crud, "post", mock_post)  

        files = {'file': open("/app/resources/input/t1.jpg",'rb')}
        response = client.post("/detect_with_image/", files=files)

        expected = [
                    [
                        1254,
                        216,
                        248,
                        248
                    ],
                    [
                        1001,
                        549,
                        277,
                        277
                    ],
                    [
                        787,
                        540,
                        302,
                        302
                    ],
                    [
                        248,
                        604,
                        331,
                        331
                    ]
                ]

        assert to_set(response.json()) == to_set(expected)

def test_result_array(monkeypatch):
    with TestClient(app) as client:

        async def mock_get(payload):
            return {
                    "id": 2,
                    "name": "t2.jpeg",
                    "address": "/app/resources/output/t2_output.png",
                    "date": "2022-08-20",
                    "result": "[[1194, 264, 75, 75], [840, 270, 71, 71], [232, 310, 72, 72], [1011, 221, 73, 73], [392, 284, 80, 80], [1382, 278, 77, 77], [560, 219, 101, 101], [820, 496, 151, 151]]"
                }

        monkeypatch.setattr(crud, "get", mock_get)  
        response = client.get("/array_result/2")
        assert response.status_code == 200
        assert response.json() == "[[1194, 264, 75, 75], [840, 270, 71, 71], [232, 310, 72, 72], [1011, 221, 73, 73], [392, 284, 80, 80], [1382, 278, 77, 77], [560, 219, 101, 101], [820, 496, 151, 151]]"

def to_set(myList):
    mySet = set()                   
    for list in myList:             
        for item in list:          
            mySet.add(item)  
    return mySet

######################################### invalid tests ######################################

def test_create_image_invalid_json(test_app):
    response = test_app.post("/image/", json={"name": "something"})
    assert response.status_code == 422

def test_read_image_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/image/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"

def test_remove_image_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/image/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"
    
def test_detect_invalid_address(test_app, monkeypatch):
    with TestClient(app) as client:  
        response = client.get("/detect_with_path/%2Fresoes%2Finput%2Ft1.jpg")

        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid path"

def test_detect_address_invalid_type(test_app, monkeypatch):
    with TestClient(app) as client:  
        response = client.get("/detect_with_path/%2Fresources%2Finput%2Finvalid.py")

        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid document type"

