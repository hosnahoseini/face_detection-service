import sys

import cv2
import uvicorn
from fastapi import FastAPI, File, UploadFile
import io
import numpy as np
from starlette.responses import StreamingResponse

PATH = "/home/app/"
app = FastAPI()


def detect(image):
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
    
    status = cv2.imwrite(PATH + 'output/faces_detected.png', image)
    return(faces.tolist())

@app.get("/path/{imagePath:path}")
async def detect_with_path(imagePath):
    imagePath = PATH + imagePath
    image = cv2.imread(imagePath)
    return detect(image)
    
@app.post("/image/")
async def detect_with_file(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return detect(img)

@app.get("/last_output/")
async def image_endpoint():
    # Returns a cv2 image array from the document vector
    cv2img = cv2.imread(PATH + "output/faces_detected.png")
    res, im_png = cv2.imencode(".png", cv2img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")

# python main.py
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
