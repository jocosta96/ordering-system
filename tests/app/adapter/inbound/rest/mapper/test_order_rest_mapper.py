from app.adapter.inbound.rest.mapper import order_rest_mapper
from app.adapter.inbound.rest.entity.order_rest import Order
from app.domain.entities.order_entity import (
    Order as DomainOrder,
)
from app.domain.value_objects.money import Money
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
        default_ingredient=[ProductReceiptItem(ingredient_id=1, quantity=2)],
    )


def test_to_domain_entity():
    rest_order = Order(customer_id=1, order_items=[], value=Money(amount=12.50))
    domain_order = order_rest_mapper.to_domain_entity(rest_order)
    assert isinstance(domain_order, DomainOrder)
    assert domain_order.customer_id == 1
    assert domain_order.value.amount == 12.50


def test_to_rest_entity():
    domain_order = DomainOrder(customer_id=1, order_items=[], value=Money(amount=12.50))
    rest_order = order_rest_mapper.to_rest_entity(domain_order)
    assert isinstance(rest_order, Order)
    assert rest_order.customer_id == 1
    assert rest_order.value.amount == 12.50
