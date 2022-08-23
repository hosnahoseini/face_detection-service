from src.db.schema import ImageIn
from src.db.db import image_table, database

async def get(id: int):
    query = image_table.select().where(image_table.c.id == id)
    res = await database.fetch_one(query)
    return res

async def post(payload: ImageIn):
    query = image_table.insert().values(name=payload.name, address=payload.address, date=payload.date, result=payload.result)
    res = await database.execute(query=query)
    return res

async def get_all():
    query = image_table.select()
    return await database.fetch_all(query=query)

async def put(id: int, payload: ImageIn):
    query = (
        image_table
        .update()
        .where(id == image_table.c.id)
        .values(name=payload.name, address=payload.address, date=payload.date, result=payload.result)
        .returning(image_table.c.id)
    )
    return await database.execute(query=query)

async def delete(id: int):
    query = image_table.delete().where(id == image_table.c.id)
    return await database.execute(query=query)