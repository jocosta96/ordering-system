import pytest
from app.adapter.inbound.rest.entity.ingredient_rest import Ingredient
from app.domain.value_objects.money import Money
from app.domain.value_objects.category import ProductCategory
from app.domain.value_objects.name import Name


def test_ingredient_creation():
    ingredient = Ingredient(
        id=1,
        name=Name(name="ALFACE"),
        price=Money(amount=5.00),
        product_category=ProductCategory(category="LANCHE"),
        is_active=True
    )
    assert ingredient.id == 1
    assert ingredient.name.name == "ALFACE"
    assert ingredient.price.amount == 5.00
    assert ingredient.product_category.category == "LANCHE"
    assert ingredient.is_active is True
