from sqlalchemy import Column, DECIMAL, String, Sequence, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship


from app.adapter.outbound.repositories.sql.orm import database


class OrderItem(database.Base):
    __tablename__ = "order_item"
    
    id = Column(
        Integer,
        Sequence('order_item_id_seq', start=1, increment=1),
        primary_key=True
    )
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    custom_lunch = Column(String)
    type = Column(String)
    quantity = Column(Integer)
    unity_price = Column(DECIMAL(5,2))

    order = relationship('Order', back_populates='order_item')
    product = relationship('Product', back_populates='order_item')
