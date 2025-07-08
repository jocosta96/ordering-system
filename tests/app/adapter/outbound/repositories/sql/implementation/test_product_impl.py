import pytest
from unittest.mock import MagicMock, patch
from app.adapter.outbound.repositories.sql.implementation.product_impl import ProductRepoImpl
from app.domain.entities.product_entity import Product
from app.domain.value_objects.name import Name
from app.domain.value_objects.money import Money
from app.domain.value_objects.category import ProductCategory, ProductCategoryType
from app.domain.value_objects.sku import SKU

@pytest.fixture
def mock_sql_impl():
    with patch('app.adapter.outbound.repositories.sql.implementation.product_impl.sql_impl.SQLRepoImpl') as mock:
        yield mock

@pytest.fixture
def product_entity():
    return Product(
        id="123e4567-e89b-12d3-a456-426614174000",
        name=Name(name='Test Product'),
        price=Money(amount=10.0),
        category=ProductCategory(category=ProductCategoryType.LANCHE),
        sku=SKU(sku='PROD-1234-XYZ'),
        default_ingredient=[]
    )

def test_to_sql_entity(product_entity):
    from app.adapter.outbound.repositories.sql.implementation.product_impl import ProductRepoImpl
    sql_product = ProductRepoImpl._to_sql_entity(product_entity)
    assert sql_product.name == 'Test Product'
    assert sql_product.price == 10.0
    assert sql_product.category == 'LANCHE'
    assert sql_product.sku == 'PROD-1234-XYZ'

def test_init_uses_sql_impl(mock_sql_impl):
    repo = ProductRepoImpl()
    assert repo._sql_impl is not None

def test_to_sql_receipt_entity(product_entity):
    from app.adapter.outbound.repositories.sql.implementation.product_impl import ProductRepoImpl
    # Mock a product with default_ingredient
    product = product_entity
    ingredient = MagicMock()
    ingredient.ingredient.id = 2
    ingredient.quantity = 3
    product.default_ingredient = [ingredient]
    receipts = ProductRepoImpl._to_sql_receipt_entity(product)
    assert receipts[0].ingredient_id == 2
    assert receipts[0].quantity == 3

# Add more tests for methods as needed, mocking DB as required
