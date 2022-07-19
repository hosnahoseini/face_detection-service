import sys

import cv2
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/predict/{imagePath:path}")
async def predict(imagePath:str):

    image = cv2.imread(imagePath)
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


# python main.py
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
