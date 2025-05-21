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
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    price = Column(DECIMAL(5,2))

    order = relationship('Order', back_populates='order_item')
    product = relationship('Product', back_populates='order_item')


class OrderItemReceipt(database.Base):
    __tablename__ = "order_item_receipt"

    product_id = Column(Integer, ForeignKey('product.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'))
    quantity = Column(Integer)
