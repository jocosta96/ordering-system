import pytest
from app.adapter.inbound.rest.entity.order_rest import Order, OrderItem
from app.domain.value_objects.money import Money
from app.domain.value_objects.status import OrderStatus
from app.domain.entities.product_entity import Product, ProductReceiptItem
from app.domain.value_objects.name import Name
from app.domain.value_objects.sku import SKU
from app.domain.value_objects.category import ProductCategory

def make_product():
    return Product(
        name=Name(name="X-Burger"),
        price=Money(amount=12.50),
        category=ProductCategory(category="LANCHE"),
        sku=SKU(sku="PROD-1234-XYZ"),
        default_ingredient=[ProductReceiptItem(ingredient_id=1, quantity=2)]
    )

def test_order_item_rest_creation():
    product = make_product()
    order_item = OrderItem(
        order_id="order-1",
        product=product,
        additional_ingredient=[],
        remove_ingredient=[],
        price=Money(amount=12.50)
    )
    assert order_item.product == product
    assert order_item.order_id == "order-1"

def test_order_rest_creation():
    product = make_product()
    order_item = OrderItem(
        order_id="order-1",
        product=product,
        additional_ingredient=[],
        remove_ingredient=[],
        price=Money(amount=12.50)
    )
    order = Order(
        customer_id=1,
        order_items=[order_item],
        value=Money(amount=12.50)
    )
    assert order.customer_id == 1
    assert order.value.amount == 12.50
