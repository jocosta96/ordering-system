from sqlalchemy import Column, DECIMAL, String, Sequence, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.adapter.outbound.repositories.sql.orm import database


class Order(database.Base):
    __tablename__ = "order"
    
    id = Column(
        Integer,
        Sequence('order_id_seq', start=1, increment=1),
        primary_key=True
    ),
    customer_id = Column(Integer, ForeignKey('customer.id'))
    status = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    value = Column(DECIMAL(5,2))
    has_payment_verified = Column(Boolean)

    customer = relationship('Customer', back_populates='customer')
