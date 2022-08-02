# build a schema using pydantic
from pydantic import BaseModel
import datetime

class ImageIn(BaseModel):
    name: str
    address: str
    date: datetime.date

class Image(BaseModel):
    id: int
    name: str
    address: str
    date: datetime.date
