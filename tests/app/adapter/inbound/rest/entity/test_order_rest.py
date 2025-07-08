from app.adapter.inbound.rest.entity.order_rest import Order, OrderItem, SimpleOrderReader
from app.adapter.inbound.rest.entity.product_rest import Product, ProductReceiptItem
from app.adapter.inbound.rest.entity.ingredient_rest import Ingredient
from app.domain.value_objects.money import Money
from app.domain.value_objects.name import Name
from app.domain.value_objects.sku import SKU
from app.domain.value_objects.category import ProductCategory
from app.domain.value_objects.status import OrderStatus, OrderStatusType
from datetime import datetime


def make_product():
    ingredient = Ingredient(
        id=1,
        name=Name(name="ALFACE"),
        price=Money(amount=5.00),
        product_category=ProductCategory(category="LANCHE"),
        is_active=True,
    )
    return Product(
        name=Name(name="X-Burger"),
        price=Money(amount=12.50),
        category=ProductCategory(category="LANCHE"),
        sku=SKU(sku="PROD-1234-XYZ"),
        default_ingredient=[ProductReceiptItem(ingredient=ingredient, quantity=2)],
    )


def test_order_item_rest_creation():
    product = make_product()
    order_item = OrderItem(
        order_id="order-1",
        product=product,
        additional_ingredient=[],
        remove_ingredient=[],
        price=Money(amount=12.50),
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
        price=Money(amount=12.50),
    )
    order = Order(customer_id=1, order_items=[order_item], value=Money(amount=12.50))
    assert order.customer_id == 1
    assert order.value.amount == 12.50


def test_simple_order_reader():
    simple_order = SimpleOrderReader(
        id="order-1",
        customer_id=1,
        value=Money(amount=32.00),
        status=OrderStatus(status=OrderStatusType.RECEBIDO),
        order_display_id="ORD-001",
        order_start_date=datetime(2025, 7, 8, 12, 0, 0),
    )
    assert simple_order.id == "order-1"
    assert simple_order.customer_id == 1
    assert simple_order.value.amount == 32.00
    assert simple_order.status.status == OrderStatusType.RECEBIDO
    assert simple_order.order_display_id == "ORD-001"
    assert simple_order.order_start_date == datetime(2025, 7, 8, 12, 0, 0)
