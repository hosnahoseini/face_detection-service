
from email.headerregistry import Address
from time import sleep
from typing import List
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from src.db.db import database
from src.db.schema import Image, ImageIn
from src.db.db import images, images
import cv2
from fastapi import FastAPI, File, UploadFile
import io
import numpy as np
from starlette.responses import StreamingResponse
from datetime import datetime
import os

PATH = "/app"
app = FastAPI(title = "Face Detection")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def detect(image, name):
    # insert_image_to_db(name)
    gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_color = image[y:y + h, x:x + w]
        # cv2.imwrite(str(w) + str(h) + '_faces.png', roi_color)
    add = PATH + f'/resources/output/{name.split(".")[0]}_output.png'
    cv2.imwrite(add, image)

    return(faces.tolist())

async def insert_image_to_db(file_name):
    addr = PATH + f'/resources/output/{file_name.split(".")[0]}_output.png'
    query = images.insert().values(name=file_name, address=addr, date=datetime.now())
    last_record_id = await database.execute(query)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/images/", response_model=List[Image], status_code = status.HTTP_200_OK)
async def read_images(skip: int = 0, take: int = 20):
    query = images.select().offset(skip).limit(take)
    return await database.fetch_all(query)

@app.get("/images/{image_id}/", response_model=Image, status_code = status.HTTP_200_OK)
async def read_images(image_id: int):
    query = images.select().where(images.c.id == image_id)
    return await database.fetch_one(query)

@app.post("/images/", response_model=Image, status_code = status.HTTP_201_CREATED)
async def create_image(image: ImageIn):
    query = images.insert().values(name=image.name, address=image.address, date=datetime.now())
    last_record_id = await database.execute(query)
    return {**image.dict(), "id": last_record_id}

@app.put("/images/{image_id}/", response_model=Image, status_code = status.HTTP_200_OK)
async def update_image(image_id: int, payload: ImageIn):
    query = images.update().where(images.c.id == image_id).values(name=payload.name, address=payload.address, date=payload)
    await database.execute(query)
    return {**payload.dict(), "id": image_id}

@app.delete("/images/{image_id}/", status_code = status.HTTP_200_OK)
async def delete_image(image_id: int):
    query = images.select().where(images.c.id == image_id)
    res = await database.fetch_one(query)
    add = res["address"]
    os.remove(add)

    query = images.delete().where(images.c.id == image_id)
    await database.execute(query)
    return {"message": "Image with id: {} deleted successfully!".format(image_id)}

@app.get("/detect_with_path/{image_path:path}")
async def detect_with_path(image_path):
    image_path = PATH + '/' + image_path
    file_name = image_path.strip("/")[-1].strip(".")[0]
    image = cv2.imread(image_path)
    
    add = PATH + f'/resources/output/{file_name.split(".")[0]}_output.png'
    query = images.insert().values(name=file_name, address=add, date=datetime.now())
    last_record_id = await database.execute(query)

    return detect(image, file_name)

    
@app.post("/detect_with_image/")
async def detect_with_file(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    insert_image_to_db(file.filename)

    add = PATH + f'/resources/output/{file.filename.split(".")[0]}_output.png'
    query = images.insert().values(name=file.filename, address=add, date=datetime.now())
    last_record_id = await database.execute(query)

    return detect(img, file.filename)

@app.get("/result/{image_id:int}")
async def get_result(image_id: int):
    # Returns a cv2 image array from the document vector
    query = images.select().where(images.c.id == image_id)
    res = await database.fetch_one(query)
    add = res["address"]
    cv2img = cv2.imread(add)
    res, im_png = cv2.imencode(".png", cv2img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")
