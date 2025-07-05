import uuid
from app.domain.entities.product_entity import Product, ProductReceiptItem, Ingredient
from app.domain.value_objects.name import Name
from app.domain.value_objects.sku import SKU
from app.domain.value_objects.money import Money
from app.domain.value_objects.category import ProductCategory


class DummyIngredient(Ingredient):
    def __init__(self, id=1, name=None, price=None, product_category=None, is_active=True):
        super().__init__(
            id=id,
            name=name or Name(name="Test Ingredient"),
            price=price or Money(amount=1.0),
            product_category=product_category or ProductCategory(category="LANCHE"),
            is_active=is_active,
        )


def test_product_receipt_item():
    item = ProductReceiptItem(ingredient=DummyIngredient(), quantity=2)
    assert isinstance(item.ingredient, Ingredient)
    assert item.quantity == 2


def test_product_creation():
    name = Name(name="X-Burger")
    price = Money(amount=12.50)
    category = ProductCategory(category="LANCHE")
    sku = SKU(sku="PROD-1234-XYZ")
    ingredients = [ProductReceiptItem(ingredient=DummyIngredient(), quantity=2)]
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
    assert isinstance(product.id, uuid.UUID)
