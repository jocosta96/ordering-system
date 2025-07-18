import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

from app.adapter.outbound.repositories.sql.orm.database import Base

from app.adapter.outbound.repositories.sql.entities.customer_sql import Customer
from app.adapter.outbound.repositories.sql.entities.ingredient_sql import Ingredient
from app.adapter.outbound.repositories.sql.entities.order_sql import Order, OrderItem, OrderItemReceipt
from app.adapter.outbound.repositories.sql.entities.product_sql import ProductReceipt, Product

load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

usr = os.getenv

# Set your DATABASE_URL from environment
host = os.environ["POSTGRES_HOST"]
database = os.environ["POSTGRES_DB"]
user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
driver = os.environ["DRIVER_NAME"]

connection_string = f"{driver}://{user}:{password}@{host}/{database}"

config.set_main_option("sqlalchemy.url", connection_string)

target_metadata = Base.metadata


def count_entities():
    entity_list = [Customer, Ingredient, Order, OrderItem, OrderItemReceipt, ProductReceipt, Product]
    print(len(entity_list), 'tables found')


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,  # detects column type changes
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
