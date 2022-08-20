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

async def post(payload: ImageIn):
    query = images.insert().values(name=payload.name, address=payload.address, date=payload.date)
    return await database.execute(query=query)

async def get_all():
    query = images.select()
    return await database.fetch_all(query=query)

async def put(id: int, payload: ImageIn):
    query = (
        images
        .update()
        .where(id == images.c.id)
        .values(name=payload.name, address=payload.address, date=payload.date)
        .returning(images.c.id)
    )
    return await database.execute(query=query)

async def delete(id: int):
    query = images.delete().where(id == images.c.id)
    return await database.execute(query=query)