from pydantic import BaseModel
import datetime

class ImageIn(BaseModel):
    name: str
    address: str
    date: datetime.date
    result: str

class Image(BaseModel):
    id: int
    name: str
    address: str
    date: datetime.date
    result: str
