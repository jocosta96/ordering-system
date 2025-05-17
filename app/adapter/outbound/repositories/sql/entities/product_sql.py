from sqlalchemy import Column, DECIMAL, String, Sequence, Integer
from app.adapter.outbound.repositories.sql.orm import database

class Product(database.Base):

    __tablename__ = "product"

    id = Column(
        Integer,
        Sequence('product_id_seq', start=1, increment=1),
        primary_key=True
    )
    name = Column(String, unique=True)
    price = Column(DECIMAL(5,2))
    category = Column(String)
    sku = Column(String, unique=True)
    codebar = Column(String, unique=True)
