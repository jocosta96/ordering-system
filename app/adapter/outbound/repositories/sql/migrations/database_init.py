import os
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound

from app.adapter.outbound.repositories.sql.orm.database import get_db

db_name = os.environ["POSTGRES_DB"]
usr_pwd = os.environ["POSTGRES_PASSWORD"]

with get_db() as session:
    try:
        alembic = session.execute(
            text(
                "SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND tablename  = 'alembic_version'"
            )
        ).one()
        if not alembic:
            os.system("alembic revision --autogenerate && alembic upgrade head")
        else:
            print("database already initalized")

    except NoResultFound:
        session.rollback()
        os.system("alembic revision --autogenerate && alembic upgrade head")

    except Exception as e:
        session.rollback()
        print(e)

with get_db() as session:
    try:
        session.execute(
            text(f"""
            DO $$
            BEGIN
            IF NOT EXISTS (
                SELECT FROM pg_catalog.pg_roles WHERE rolname = '{db_name}'
            ) THEN
                CREATE ROLE {db_name} WITH LOGIN PASSWORD '{usr_pwd}';
            END IF;
            END $$;

            GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_name};
        """)
        )
        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error during database initialization: {e}")
