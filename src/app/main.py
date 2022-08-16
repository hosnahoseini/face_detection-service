
import imghdr
import io
import os
from datetime import datetime
from os import path
from typing import List
from src.app.api import ping

import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from src.db.db import database, images
from src.db.schema import Image, ImageIn
from starlette.responses import StreamingResponse

PATH = "/app"
app = FastAPI(title = "Face Detection")
app.include_router(ping.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@router.get("/ping")
async def ping():
    return {"output": "pong"}

@app.get("/image/{image_id}/", response_model=Image, status_code = status.HTTP_200_OK)
async def read_image(image_id: int):
    
    query = images.select().where(images.c.id == image_id)
    res = await database.fetch_one(query)

    # validate input
    if (not res):
        raise HTTPException(404, detail="The requested resource was not found.")

    return res

@app.post("/image/", response_model=Image, status_code = status.HTTP_201_CREATED)
async def create_image(image: ImageIn):
    query = images.insert().values(name=image.name, address=image.address, date=datetime.now())
    last_record_id = await database.execute(query)
    return {**image.dict(), "id": last_record_id}

@app.put("/image/{image_id}/", response_model=Image, status_code = status.HTTP_200_OK)
async def update_image(image_id: int, payload: ImageIn):
    query = images.update().where(images.c.id == image_id).values(name=payload.name, address=payload.address, date=payload)
    res = await database.execute(query)

    # validate input
    if (not res):
        raise HTTPException(404, detail="The requested resource was not found.")
    
    return {**payload.dict(), "id": image_id}

@app.delete("/image/{image_id}/", status_code = status.HTTP_200_OK)
async def delete_image(image_id: int):
    query = images.select().where(images.c.id == image_id)
    res = await database.fetch_one(query)

    # validate input
    if (not res):
        raise HTTPException(404, detail="The requested resource was not found.")


    # remove imaage
    add = res["address"]
    os.remove(add)

    query = images.delete().where(images.c.id == image_id)
    await database.execute(query)
    return {"message": "Image with id: {} deleted successfully!".format(image_id)}

@app.get("/detect_with_path/{image_path:path}")
async def detect_with_path(image_path):
    image_path = PATH + '/' + image_path
    
    # validate input 
    if (not path.exists(image_path)):
        raise HTTPException(400, detail="Invalid path")

    image_types=['rgb','gif', 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png', 'webp', 'exr']
    if(imghdr.what(image_path) not in image_types):
        raise HTTPException(400, detail="Invalid document type")
        
    file_name = image_path.strip("/")[-1].strip(".")[0]
    image = cv2.imread(image_path)

    add = PATH + f'/resources/output/{file_name.split(".")[0]}_output.png'
    query = images.insert().values(name=file_name, address=add, date=datetime.now())
    last_record_id = await database.execute(query)

    return detect(image, file_name)
    
@app.post("/detect_with_image/")
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

@app.get("/result/{image_id:int}")
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

if __name__ == '__main__':
    uvicorn.run("src.app.main:app",host='0.0.0.0', port=5000, reload=True, debug=True)
