import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from psycopg2.extensions import register_adapter, AsIs, QuotedString

from app.domain.value_objects import (
    name,
    document,
    email
)

register_adapter(document.Document, lambda document: QuotedString(str(document)))
register_adapter(name.Name, lambda name: QuotedString(str(name)))
register_adapter(email.Email, lambda email: QuotedString(str(email)))

host = os.environ["POSTGRES_HOST"]
database = os.environ["POSTGRES_DB"]
user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]

connection_string = f"postgresql://{user}:{password}@{host}/{database}"

engine = create_engine(
    connection_string,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()