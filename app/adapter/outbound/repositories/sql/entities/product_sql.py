from sqlalchemy import Column, DECIMAL, String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.adapter.outbound.repositories.sql.orm import database


class ProductReceipt(database.Base):
    __tablename__ = "product_receipt"

    product_id = Column(UUID(as_uuid=True), ForeignKey('product.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'), primary_key=True)
    quantity = Column(Integer)

    ingredient = relationship('Ingredient', back_populates='product_receipts')
    product = relationship('Product', back_populates='product_receipts')


class Product(database.Base):

    __tablename__ = "product"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name = Column(String, unique=True)
    price = Column(DECIMAL(5,2))
    category = Column(String)
    sku = Column(String, unique=True)
    is_active = Column(Boolean, default=True)

    order_item = relationship('OrderItem', back_populates='product')
    order_item_receipts = relationship('OrderItemReceipt', back_populates='product')
    order_items = relationship('OrderItem', back_populates='product')
    product_receipts = relationship('ProductReceipt', back_populates='product')

