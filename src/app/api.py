from fastapi import APIRouter, HTTPException, status

from src.app import crud
from src.db.schema import Image, ImageIn

router = APIRouter()

@router.post("/image/", response_model=Image, status_code = status.HTTP_201_CREATED)
async def create_image(image: ImageIn):
    last_record_id = crud.post(image)
    print(last_record_id, type(last_record_id))
    return {**image.dict(), "id": 100}


@router.get("/image/{id}/", response_model=Image, status_code = status.HTTP_200_OK)
async def read_image(id: int):
    res = await crud.get(id)
    if not res:
        raise HTTPException(status_code=404, detail="Image not found")
    return image