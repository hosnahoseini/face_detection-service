
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
from fastapi.middleware.cors import CORSMiddleware
from src.db.db import database, images
from src.db.schema import Image, ImageIn
from starlette.responses import StreamingResponse
from src.app import api

PATH = "/app"
app = FastAPI(title = "Face Detection")
router = APIRouter()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(api.router, tags=["image"])

if __name__ == '__main__':
    uvicorn.run("src.app.main:app",host='0.0.0.0', port=5000, reload=True, debug=True)
