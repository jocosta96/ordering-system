import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

host = os.environ["db_host"]
database = os.environ["db_database"]
user = os.environ["db_user"]
password = os.environ["db_password"]

connection_string = f"postgresql://{user}:{password}@{host}/{database}"

engine = create_engine(
    connection_string,  # os.environ['SQLALCHEMY_DATABASE_URL'],
    # connect_args={'check_same_thread': False},
    echo=True,
    pool_pre_ping=True,
    pool_recycle=600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
