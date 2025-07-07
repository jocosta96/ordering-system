from app.domain.entities.ingredient_entity import Ingredient
from app.domain.value_objects.money import Money
from app.domain.value_objects.name import Name
from app.domain.value_objects.category import ProductCategory

def test_ingredient_creation():
    ingredient = Ingredient(
        id=1,
        name=Name(name="Tomato"),
        price=Money(amount=2.5),
        product_category=ProductCategory(category="LANCHE"),  # valid category
        is_active=True
    )
    assert ingredient.id == 1
    assert ingredient.name.value == "Tomato"
    assert ingredient.price.amount == 2.5
    assert ingredient.product_category.category == "LANCHE"
    assert ingredient.is_active is True
