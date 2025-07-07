import pytest
from unittest.mock import MagicMock
from app.domain.use_cases.ingredient_uc import (
    IngredientCreate, IngredientDelete, IngredientRead, IngredientUpdate, IngredientRestoreDeleted, IngredientList
)
from app.domain.entities.ingredient_entity import Ingredient
from app.domain.value_objects.name import Name
from app.domain.value_objects.money import Money
from app.domain.value_objects.category import ProductCategory

@pytest.fixture
def mock_port():
    return MagicMock()

def make_ingredient():
    return Ingredient(id=1, name=Name(name="Tomato"), price=Money(amount=2.5), product_category=ProductCategory(category="LANCHE"), is_active=True)

def test_create_ingredient(mock_port):
    use_case = IngredientCreate(mock_port)
    ingredient = make_ingredient()
    mock_port.create_ingredient.return_value = 42
    result = use_case.create_ingredient(ingredient)
    mock_port.create_ingredient.assert_called_once_with(ingredient)
    assert result == 42

def test_delete_ingredient(mock_port):
    use_case = IngredientDelete(mock_port)
    mock_port.delete_ingredient.return_value = 1
    result = use_case.delete_ingredient(1)
    mock_port.delete_ingredient.assert_called_once_with(1)
    assert result == 1

def test_read_ingredient(mock_port):
    use_case = IngredientRead(mock_port)
    ingredient = make_ingredient()
    mock_port.read_ingredient.return_value = ingredient
    result = use_case.read_ingredient(1)
    mock_port.read_ingredient.assert_called_once_with(1)
    assert result == ingredient

def test_update_ingredient(mock_port):
    use_case = IngredientUpdate(mock_port)
    ingredient = make_ingredient()
    mock_port.update_ingredient.return_value = 1
    result = use_case.update_ingredient(ingredient)
    mock_port.update_ingredient.assert_called_once_with(ingredient)
    assert result == 1

def test_restore_deleted_ingredient(mock_port):
    use_case = IngredientRestoreDeleted(mock_port)
    ingredient = make_ingredient()
    mock_port.restore_deleted_ingredient.return_value = 1
    result = use_case.restore_deleted_ingredient(ingredient)
    mock_port.restore_deleted_ingredient.assert_called_once_with(ingredient)
    assert result == 1

def test_list_ingredient(mock_port):
    use_case = IngredientList(mock_port)
    mock_port.list_ingredient.return_value = ["a", "b"]
    result = use_case.list_ingredient()
    mock_port.list_ingredient.assert_called_once_with(None, None)
    assert result == ["a", "b"]
