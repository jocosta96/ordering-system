import pytest
from app.domain.ports.ingredient_port import IngredientPort
from app.domain.entities.ingredient_entity import Ingredient
from app.domain.value_objects.name import Name
from app.domain.value_objects.money import Money
from app.domain.value_objects.category import ProductCategory

class DummyIngredientPort(IngredientPort):
    def create_ingredient(self, ingredient):
        return ingredient
    def read_ingredient(self, ingredient_id):
        return Ingredient(id=ingredient_id, name=Name(name="Test"), price=Money(amount=1.0), product_category=ProductCategory(category="LANCHE"), is_active=True)
    def update_ingredient(self, ingredient):
        return ingredient
    def delete_ingredient(self, ingredient_id):
        return Ingredient(id=ingredient_id, name=Name(name="Deleted"), price=Money(amount=0.0), product_category=ProductCategory(category="LANCHE"), is_active=False)
    def restore_deleted_ingredient(self, ingredient):
        return ingredient
    def list_ingredient(self, search_key, search_value):
        return [Ingredient(id=1, name=Name(name="A"), price=Money(amount=1.0), product_category=ProductCategory(category="LANCHE"), is_active=True)]

def make_ingredient():
    return Ingredient(id=1, name=Name(name="Tomato"), price=Money(amount=2.5), product_category=ProductCategory(category="LANCHE"), is_active=True)

def test_create_ingredient():
    port = DummyIngredientPort()
    ingredient = make_ingredient()
    result = port.create_ingredient(ingredient)
    assert result == ingredient

def test_read_ingredient():
    port = DummyIngredientPort()
    result = port.read_ingredient(1)
    assert result.id == 1
    assert result.name.value == "Test"

def test_update_ingredient():
    port = DummyIngredientPort()
    ingredient = make_ingredient()
    result = port.update_ingredient(ingredient)
    assert result == ingredient

def test_delete_ingredient():
    port = DummyIngredientPort()
    result = port.delete_ingredient(2)
    assert result.id == 2
    assert result.name.value == "Deleted"
    assert result.is_active is False

def test_restore_deleted_ingredient():
    port = DummyIngredientPort()
    ingredient = make_ingredient()
    result = port.restore_deleted_ingredient(ingredient)
    assert result == ingredient

def test_list_ingredient():
    port = DummyIngredientPort()
    result = port.list_ingredient(None, None)
    assert isinstance(result, list)
    assert result[0].name.value == "A"
