import os
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound

from app.adapter.outbound.repositories.sql.orm.database import get_db

db_name = os.environ['POSTGRES_DB']
usr_pwd = os.environ['POSTGRES_PASSWORD']

with get_db() as session:
    try:
        alembic = session.execute(text(
            "DROP TABLE alembic_version;"
        ))
        session.commit()
        os.system('alembic revision --autogenerate && alembic upgrade head')

    except Exception as e:
        session.rollback()
        raise e
