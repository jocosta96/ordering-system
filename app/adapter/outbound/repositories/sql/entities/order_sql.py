from sqlalchemy import Column, DECIMAL, String, Sequence, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
import uuid
from app.adapter.outbound.repositories.sql.orm import database
from sqlalchemy.dialects.postgresql import UUID


class Order(database.Base):
    __tablename__ = "order"
    
    id:uuid = Column(UUID, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    status = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    value = Column(DECIMAL(5,2))
    payment_date = Column(DateTime)
    payment_transaction_id = Column(String)
    has_payment_verified = Column(Boolean)
    order_number = Column(Integer, Sequence('order_number_seq', start=1, increment=1))
    customer = relationship('Customer', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order')
    order_item_receipts = relationship('OrderItemReceipt', back_populates='order')


class OrderItem(database.Base):
    __tablename__ = "order_item"
    
    id:uuid = Column(
        UUID,
        primary_key=True
    )
    order_id = Column(UUID, ForeignKey('order.id'))
    product_id = Column(UUID, ForeignKey('product.id'))
    price = Column(DECIMAL(5,2))

    order = relationship('Order', back_populates='order_items')
    order_item_receipts = relationship('OrderItemReceipt', back_populates='order_item', cascade="all, delete-orphan")
    product = relationship('Product', back_populates='order_items')


class OrderItemReceipt(database.Base):
    __tablename__ = "order_item_receipt"

    order_id = Column(UUID, ForeignKey('order.id'), primary_key=True)
    order_item_id = Column(UUID, ForeignKey('order_item.id'), primary_key=True)
    product_id = Column(UUID, ForeignKey('product.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'), primary_key=True)
    quantity = Column(Integer)

    ingredient = relationship('Ingredient', back_populates='order_item_receipts')
    order_item = relationship('OrderItem', back_populates='order_item_receipts')
    product = relationship('Product', back_populates='order_item_receipts')
    order = relationship('Order', back_populates='order_item_receipts')
