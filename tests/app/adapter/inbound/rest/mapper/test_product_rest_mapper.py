from app.adapter.inbound.rest.mapper import product_rest_mapper
from app.adapter.inbound.rest.entity.product_rest import Product, ProductReceiptItem
from app.domain.entities.product_entity import (
    Product as DomainProduct,
    ProductReceiptItem as DomainReceiptItem,
)
from app.domain.value_objects.name import Name
from app.domain.value_objects.sku import SKU
from app.domain.value_objects.money import Money
from app.domain.value_objects.category import ProductCategory


def test_to_domain_entity():
    from app.adapter.inbound.rest.entity.ingredient_rest import Ingredient

    ingredient = Ingredient(
        id=1,
        name=Name(name="ALFACE"),
        price=Money(amount=5.00),
        product_category=ProductCategory(category="LANCHE"),
        is_active=True,
    )
    rest_product = Product(
        name=Name(name="X-Burger"),
        price=Money(amount=12.50),
        category=ProductCategory(category="LANCHE"),
        sku=SKU(sku="PROD-1234-XYZ"),
        default_ingredient=[ProductReceiptItem(ingredient=ingredient, quantity=2)],
    )
    domain_product = product_rest_mapper.to_domain_entity(rest_product)
    assert isinstance(domain_product, DomainProduct)
    assert domain_product.name.value == "X-Burger"
    assert domain_product.price.value == 12.5
    assert domain_product.category.value == "LANCHE"
    assert domain_product.sku.value == "PROD-1234-XYZ"
    assert len(domain_product.default_ingredient) == 1


def test_to_rest_entity():
    from app.domain.entities.ingredient_entity import Ingredient

    ingredient = Ingredient(
        id=1,
        name=Name(name="ALFACE"),
        price=Money(amount=5.00),
        product_category=ProductCategory(category="LANCHE"),
        is_active=True,
    )
    domain_product = DomainProduct(
        name=Name(name="X-Burger"),
        price=Money(amount=12.50),
        category=ProductCategory(category="LANCHE"),
        sku=SKU(sku="PROD-1234-XYZ"),
        default_ingredient=[DomainReceiptItem(ingredient=ingredient, quantity=2)],
    )
    rest_product = product_rest_mapper.to_rest_entity(domain_product)
    assert isinstance(rest_product, Product)
    assert rest_product.name.value == "X-Burger"
    assert rest_product.price.value == 12.5
    assert rest_product.category.value == "LANCHE"
    assert rest_product.sku.value == "PROD-1234-XYZ"
    assert len(rest_product.default_ingredient) == 1
