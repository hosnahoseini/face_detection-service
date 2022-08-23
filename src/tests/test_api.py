
from fastapi.testclient import TestClient
from src.face import crud
from src.face.main import app

PREFIX = "/face/v1"

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

        response = client.get(PREFIX + "/read_all_images/")
        assert response.json() == test_data
        assert response.status_code == 200

def test_read_image():
    with TestClient(app) as client:  
        response = client.get(PREFIX + "/read_image/5/")
        assert response.status_code == 200
        assert response.json() ==     {
                                        "id": 5,
                                        "name": "t1.jpg",
                                        "address": "/app/resources/output/t1_output.png",
                                        "date": "2022-08-21",
                                        "result": "[[1254, 216, 248, 248], [1001, 549, 277, 277], [787, 540, 302, 302], [248, 604, 331, 331]]"
                                    }
    
def test_put_image():
    with TestClient(app) as client:  
        
        response = client.put(PREFIX + "/update_image/3/", json={
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

        response = client.delete(PREFIX + "/delete_image/5/")
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

        response = client.get(PREFIX + "/detect_with_path/%2Fresources%2Finput%2Ft1.jpg")
        
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
        response = client.post(PREFIX + "/detect_with_image/", files=files)

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
        response = client.get(PREFIX + "/array_result/2")
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
    response = test_app.post(PREFIX + "/create_image/", json={"name": "something"})
    assert response.status_code == 422

def test_read_image_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get(PREFIX + "/read_image/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"

def test_remove_image_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete(PREFIX + "/delete_image/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"
    
def test_detect_invalid_address():
    with TestClient(app) as client:  
        response = client.get(PREFIX + "/detect_with_path/%2Fresoes%2Finput%2Ft1.jpg")

        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid path"

def test_detect_address_invalid_type_valid_extension():
    with TestClient(app) as client:  
        response = client.get(PREFIX + "/detect_with_path/%2Fresources%2Finput%2Fvideo.png")

        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid document type"

def test_detect_address_invalid_type():
    with TestClient(app) as client:  
        response = client.get(PREFIX + "/detect_with_path/%2Fresources%2Finput%2Fvideo.mp4")

        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid document type"

def test_detect_image_file_invalid_type():
    with TestClient(app) as client:

        files = {'file': open("/app/resources/input/video.mp4",'rb')}
        response = client.post(PREFIX + "/detect_with_image/", files=files)
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid document type"

def test_detect_image_file_invalid_type_valid_extension():
    with TestClient(app) as client:

        files = {'file': open("/app/resources/input/video.png",'rb')}
        response = client.post(PREFIX + "/detect_with_image/", files=files)
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid document type"

