

from email.policy import default
from .config import settings
import sqlalchemy
import databases
from sqlalchemy.ext.declarative import declarative_base
DATABASE_URL = settings.db_url

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)

image_table = sqlalchemy.Table(
    "image_table",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("address", sqlalchemy.String),
    sqlalchemy.Column("date", sqlalchemy.DateTime),
    sqlalchemy.Column("result", sqlalchemy.String, default=""),


)
metadata.create_all(engine)