from unittest.mock import MagicMock
from app.adapter.outbound.repositories.sql.implementation.product_impl import (
    ProductRepoImpl,
)
from app.domain.entities.product_entity import Product, ProductReceiptItem
from app.domain.value_objects.name import Name
from app.domain.value_objects.sku import SKU
from app.domain.value_objects.money import Money
from app.domain.value_objects.category import ProductCategory


class DummySQLProduct:
    def __init__(self):
        self.id = "123e4567-e89b-12d3-a456-426614174000"
        self.name = "X-Burger"
        self.price = 12.5
        self.category = "LANCHE"
        self.sku = "PROD-1234-XYZ"


class DummyReceipt:
    def __init__(self):
        self.ingredient = MagicMock(id=1)
        self.quantity = 2


def test_to_domain_entity():
    sql_product = DummySQLProduct()
    receipt = [DummyReceipt()]
    product = ProductRepoImpl._to_domain_entity(sql_product, receipt)
    assert isinstance(product, Product)
    assert product.name.value == "X-Burger"
    assert product.price.value == 12.5
    assert product.category.value == "LANCHE"
    assert product.sku.value == "PROD-1234-XYZ"
    assert len(product.default_ingredient) == 1


def test_to_sql_entity():
    name = Name(name="X-Burger")
    price = Money(amount=12.50)
    category = ProductCategory(category="LANCHE")
    sku = SKU(sku="PROD-1234-XYZ")
    ingredients = [ProductReceiptItem(ingredient_id=1, quantity=2)]
    product = Product(
        name=name,
        price=price,
        category=category,
        sku=sku,
        default_ingredient=ingredients,
    )
    sql_entity = ProductRepoImpl._to_sql_entity(product)
    assert sql_entity.name == "X-Burger"
    assert sql_entity.price == 12.5
    assert sql_entity.category == "LANCHE"
    assert sql_entity.sku == "PROD-1234-XYZ"
