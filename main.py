import sys

import cv2
import uvicorn
from fastapi import FastAPI, File, UploadFile
import numpy as np

app = FastAPI()


def detect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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
        # cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color)
    
    status = cv2.imwrite('faces_detected.jpg', image)
    return(faces.tolist())

@app.get("/path/{imagePath:path}")
async def detect_with_path(imagePath):
    image = cv2.imread(imagePath)
    return detect(image)
    
@app.post("/image/")
async def detect_with_file(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return detect(img)

# python main.py
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
