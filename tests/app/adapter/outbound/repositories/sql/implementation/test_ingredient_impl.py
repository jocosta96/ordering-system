import pytest
from unittest.mock import MagicMock, patch
from app.adapter.outbound.repositories.sql.implementation.ingredient_impl import IngredientRepoImpl
from app.domain.entities.ingredient_entity import Ingredient
from app.domain.value_objects.category import ProductCategory, ProductCategoryType
from app.domain.value_objects.money import Money

TEST_INGREDIENT_NAME = 'Test Ingredient'

@pytest.fixture
def mock_sql_impl():
    with patch('app.adapter.outbound.repositories.sql.implementation.ingredient_impl.sql_impl.SQLRepoImpl') as mock:
        yield mock

@pytest.fixture
def ingredient_entity():
    return Ingredient(
        id=1,
        name=TEST_INGREDIENT_NAME,
        price=Money(amount=10.0),
        product_category=ProductCategory(category=ProductCategoryType.LANCHE),
        is_active=True
    )

def test_to_sql_entity(ingredient_entity):
    from app.adapter.outbound.repositories.sql.implementation.ingredient_impl import IngredientRepoImpl
    sql_ingredient = IngredientRepoImpl._to_sql_entity(ingredient_entity)
    assert sql_ingredient.name == TEST_INGREDIENT_NAME
    assert sql_ingredient.price == 10.0 or float(sql_ingredient.price) == 10.0
    assert str(sql_ingredient.product_category) == 'LANCHE'
    assert sql_ingredient.is_active is True

def test_init_uses_sql_impl(mock_sql_impl):
    repo = IngredientRepoImpl()
    assert repo._sql_impl is not None

def test_create_ingredient(mock_sql_impl, ingredient_entity):
    repo = IngredientRepoImpl()
    repo._sql_impl.add_one = MagicMock()
    repo.create_ingredient(ingredient_entity)
    repo._sql_impl.add_one.assert_called_once()

def test_update_ingredient(mock_sql_impl, ingredient_entity):
    repo = IngredientRepoImpl()
    repo._sql_impl.update = MagicMock()
    repo.update_ingredient(ingredient_entity)
    repo._sql_impl.update.assert_called_once()

def test_to_domain_entity_valid():
    from app.adapter.outbound.repositories.sql.implementation.ingredient_impl import IngredientRepoImpl
    mock_ingredient = MagicMock()
    mock_ingredient.id = 1
    mock_ingredient.name = TEST_INGREDIENT_NAME
    mock_ingredient.price = 10.0
    mock_ingredient.product_category = 'LANCHE'
    mock_ingredient.is_active = True
    result = IngredientRepoImpl._to_domain_entity(mock_ingredient)
    assert result.name == TEST_INGREDIENT_NAME
    assert result.price == 10.0
    assert str(result.product_category) == 'LANCHE'
    assert result.is_active is True

def test_update_ingredient_calls_update(mock_sql_impl, ingredient_entity):
    repo = IngredientRepoImpl()
    repo._sql_impl.update = MagicMock()
    repo.update_ingredient(ingredient_entity)
    repo._sql_impl.update.assert_called_once()

# Add more tests for methods as needed, mocking DB as required
