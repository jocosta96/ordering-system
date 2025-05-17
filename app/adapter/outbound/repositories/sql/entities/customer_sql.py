from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship

from app.adapter.outbound.repositories.sql.orm import database

class Customer(database.Base):

    __tablename__ = "customer"

    id = Column(
        Integer,
        Sequence('customer_id_seq', start=1, increment=1),
        primary_key=True
    )
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    document = Column(String, unique=True)


    orders = relationship('Order', back_populates='order')
