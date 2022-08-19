from fastapi import APIRouter, HTTPException, status

import imghdr
import io
import os
from datetime import datetime
from os import path
from typing import List


import cv2
import numpy as np
import uvicorn
from fastapi import APIRouter, FastAPI, File, HTTPException, UploadFile, status
from src.app import crud
from src.db.schema import Image, ImageIn
import cv2
import numpy as np
import uvicorn
from fastapi import APIRouter, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from src.db.db import database, images
from src.db.schema import Image, ImageIn
from starlette.responses import StreamingResponse
from src.app import api

router = APIRouter()
PATH = "/app"

def detect(image, name):
    # convert image to grayscale
    gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)

    # create the cascade and initialize it with our face cascade. This loads the face cascade into memory
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 5)

    # save result    
    address = PATH + f'/resources/output/{name.split(".")[0]}_output.png'
    cv2.imwrite(address, image)

    return(faces.tolist())

async def insert_image_to_db(file_name):
    addr = PATH + f'/resources/output/{file_name.split(".")[0]}_output.png'
    query = images.insert().values(name=file_name, address=addr, date=datetime.now())
    last_record_id = await database.execute(query)

   
@router.post("/detect_with_image/")
async def detect_with_file(file: UploadFile = File(...)):

    # validate input
    image_types = ["image/apng", "image/webp", "image/avif", "image/gif", "image/jpeg", "image/png", "image/svg+xml"]
    if file.content_type not in image_types:
        raise HTTPException(400, detail="Invalid document type")
        
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    insert_image_to_db(file.filename)

    add = PATH + f'/resources/output/{file.filename.split(".")[0]}_output.png'
    query = images.insert().values(name=file.filename, address=add, date=datetime.now())
    last_record_id = await database.execute(query)

    return detect(img, file.filename)

@router.get("/result/{image_id:int}")
async def get_result(image_id: int):
    # Returns a cv2 image array from the document vector
    query = images.select().where(images.c.id == image_id)
    res = await database.fetch_one(query)

    # validate input
    if (not res):
        raise HTTPException(404, detail="The requested resource was not found.")

    add = res["address"]
    cv2img = cv2.imread(add)
    res, im_png = cv2.imencode(".png", cv2img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")
    
@router.get("/detect_with_path/{image_path:path}")
async def detect_with_path(image_path):
    image_path = PATH + '/' + image_path
    
    # validate input 
    if (not path.exists(image_path)):
        raise HTTPException(400, detail="Invalid path")

    image_types=['rgb','gif', 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png', 'webp', 'exr', 'jpg']
    if(imghdr.what(image_path) not in image_types):
        raise HTTPException(400, detail="Invalid document type")
        
    file_name = image_path.strip("/")[-1].strip(".")[0]
    image = cv2.imread(image_path)

    add = PATH + f'/resources/output/{file_name.split(".")[0]}_output.png'
    query = images.insert().values(name=file_name, address=add, date=datetime.now())
    last_record_id = await database.execute(query)

    return detect(image, file_name)


@router.post("/image/", response_model=Image, status_code=201)
async def create_image(payload: ImageIn):
    image_id = await crud.post(payload)

    response_object = {
        "id": image_id,
        "name": payload.name,
        "address": payload.address,
        "date": payload.date
    }
    return response_object

@router.get("/image/{id}/", response_model=Image)
async def read_image(id: int):
    image = await crud.get(id)
    if not image:
        raise HTTPException(status_code=404, detail="Not Found")
    return image

    
@router.get("/images/", response_model=List[Image])
async def read_all_images():
    return await crud.get_all()

@router.put("/image/{id}/", response_model=Image)
async def update_image(id: int, payload: ImageIn):
    image = await crud.get(id)
    if not image:
        raise HTTPException(status_code=404, detail="Not Found")

    image_id = await crud.put(id, payload)

    response_object = {
        "id": image_id,
        "name": payload.name,
        "address": payload.address,
        "date": payload.date
    }
    return response_object

@router.delete("/image/{id}/", response_model=Image)
async def delete_image(id: int):
    image = await crud.get(id)
    if not image:
        raise HTTPException(status_code=404, detail="Not Found")

    await crud.delete(id)

    return image