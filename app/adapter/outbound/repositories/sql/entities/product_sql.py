from sqlalchemy import Column, DECIMAL, String, Sequence, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.adapter.outbound.repositories.sql.orm import database


class ProductReceipt(database.Base):
    __tablename__ = "product_receipt"

    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'), primary_key=True)
    quantity = Column(Integer)

    ingredient = relationship('Ingredient', back_populates='product_receipts')
    product = relationship('Product', back_populates='product_receipts')


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

    order_item = relationship('OrderItem', back_populates='product')
    order_item_receipts = relationship('OrderItemReceipt', back_populates='product')
    order_items = relationship('OrderItem', back_populates='product')
    product_receipts = relationship('ProductReceipt', back_populates='product')

