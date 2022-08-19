from src.app.main import app
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
import cv2
from src.app.api import detect
from fastapi import APIRouter, FastAPI, File, HTTPException, UploadFile, status
import cv2

# @pytest.fixture() 
# def client(app): 
#     with TestClient(app) as client:   # context manager will invoke startup event 
#         yield client

# client = TestClient(app)   
# @pytest.mark.anyio
# async def test_root():
#     async with AsyncClient(app=app, base_url="http://127.0.0.1:4000") as ac:
#         response = await ac.get("/")
#     assert response.json() == {"message": "Tomato"}
#     assert response.status_code == 200

def test_read_all_images():
    with TestClient(app) as client:  
        response = client.get("/images/")
        assert response.status_code == 200
        assert len(response.json()) == 12
    

def test_detect_address():
    with TestClient(app) as client:  
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
        assert toset(response.json()) == toset(expected)


def test_detect_image():
    image = cv2.imread("/app/resources/input/t1.jpg")
    res = detect(image, "t1.jpg")
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
    assert toset(res) == toset(expected)

def toset(myList):
    mySet = set()                   
    for list in myList:             
        for item in list:          
            mySet.add(item)  
    return mySet

def test_detect_image_file():
    fpath = "/app/resources/input/t1.jpg"
    with open(fpath, "wb") as f:
        with TestClient(app) as client:  

            response = client.post("/detect_with_image/", files={"file": ("t1.jpg", f, "image/jpeg")})
        # image = cv2.imread("/app/resources/input/t1.jpg")
        # res = detect(image, "t1.jpg")
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
            assert toset(response.json()) == toset(expected)