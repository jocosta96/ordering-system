from app.adapter.inbound.rest.entity.product_rest import Product, ProductReceiptItem
from app.adapter.inbound.rest.entity.ingredient_rest import Ingredient
from app.domain.value_objects.name import Name
from app.domain.value_objects.sku import SKU
from app.domain.value_objects.money import Money
from app.domain.value_objects.category import ProductCategory


def test_product_receipt_item_rest():
    ingredient = Ingredient(
        id=1,
        name=Name(name="ALFACE"),
        price=Money(amount=5.00),
        product_category=ProductCategory(category="LANCHE"),
        is_active=True,
    )
    item = ProductReceiptItem(ingredient=ingredient, quantity=2)
    assert item.ingredient == ingredient
    assert item.quantity == 2


def test_product_rest_creation():
    name = Name(name="X-Burger")
    price = Money(amount=12.50)
    category = ProductCategory(category="LANCHE")
    sku = SKU(sku="PROD-1234-XYZ")
    ingredient = Ingredient(
        id=1,
        name=Name(name="ALFACE"),
        price=Money(amount=5.00),
        product_category=ProductCategory(category="LANCHE"),
        is_active=True,
    )
    ingredients = [ProductReceiptItem(ingredient=ingredient, quantity=2)]
    product = Product(
        name=name,
        price=price,
        category=category,
        sku=sku,
        default_ingredient=ingredients,
    )
    assert product.name == name
    assert product.price == price
    assert product.category == category
    assert product.sku == sku
    assert product.default_ingredient == ingredients
