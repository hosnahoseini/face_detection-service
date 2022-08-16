from src.db.schema import ImageIn, Image
from src.db.db import images, database

async def post(image: ImageIn):
    query = images.insert().values(name=image.name, address=image.address, date=datetime.now())
    last_record_id = await database.execute(query)
    return last_record_id

async def get(id: int):
    query = images.select().where(images.c.id == id)
    res = await database.fetch_one(query)
    return res