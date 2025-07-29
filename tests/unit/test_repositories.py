"""
Unit tests for repository implementations.

Tests cover:
- SQLProductRepository
- Database model conversions
- CRUD operations
- Error handling
"""

import pytest
from unittest.mock import Mock
from decimal import Decimal

from src.adapters.gateways.sql_product_repository import SQLProductRepository, ProductModel
from src.entities.product import Product, ProductCategory
from src.entities.ingredient import Ingredient, IngredientType
from src.entities.value_objects.money import Money
from src.entities.value_objects.sku import SKU


class TestSQLProductRepository:
    """Test cases for SQLProductRepository"""

    @pytest.fixture
    def mock_database(self):
        """Mock database interface"""
        mock_db = Mock()
        mock_db.get_session.return_value = Mock()
        mock_db.find_by_id.return_value = None
        mock_db.find_by_field.return_value = None
        mock_db.find_by_sku.return_value = None
        mock_db.find_all.return_value = []
        mock_db.find_all_by_boolean_field.return_value = []
        mock_db.find_all_by_field.return_value = []
        mock_db.add.return_value = None
        mock_db.update.return_value = None
        mock_db.delete.return_value = True
        mock_db.commit.return_value = None
        mock_db.rollback.return_value = None
        mock_db.close_session.return_value = None
        mock_db.exists_by_field.return_value = False
        mock_db.exists_by_sku.return_value = False
        mock_db.exists_by_id.return_value = False
        mock_db.exists_by_name.return_value = False
        mock_db.exists_by_category.return_value = False
        return mock_db

    @pytest.fixture
    def mock_ingredient_repository(self):
        """Mock ingredient repository for testing"""
        mock_repo = Mock()
        
        # Create a sample ingredient for testing
        sample_ingredient = Ingredient.create(
            name="Test Ingredient",
            price=Money(amount=Decimal("1.00")),
            is_active=True,
            type=IngredientType.SAUCE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
            internal_id=1,  # Set to match product model expectation
        )
        
        mock_repo.find_by_id.return_value = sample_ingredient
        return mock_repo

    @pytest.fixture
    def sample_product_model(self):
        """Sample ProductModel for testing"""
        model = ProductModel()
        model.internal_id = 1  # Use internal_id instead of UUID
        model.name = "Test Product"
        model.price = 10.00
        model.category = "burger"
        model.sku = "TEST-2024-ABC"
        model.default_ingredient = [
            {
                "ingredient_internal_id": 1,  # Use internal_id instead of UUID
                "quantity": 1
            }
        ]
        model.is_active = True
        model.created_at = "2024-01-01T00:00:00"
        return model

    def test_init_does_not_create_tables(self, mock_database):
        """Test that repository initialization does not create tables"""
        # Act
        repository = SQLProductRepository(mock_database)

        # Assert
        # No table creation should happen - tables are managed by migrations
        assert repository is not None

    def test_to_entity_conversion(self, mock_database, mock_ingredient_repository, sample_product_model):
        """Test conversion from database model to entity"""
        # Arrange
        repository = SQLProductRepository(mock_database, mock_ingredient_repository)

        # Act
        entity = repository._to_entity(sample_product_model)

        # Assert
        assert isinstance(entity, Product)
        # UUID assertion removed - using internal_id now
        assert entity.name.value == "Test Product"
        assert entity.price.amount == Decimal("10.00")
        assert entity.category == ProductCategory.BURGER
        assert entity.sku.value == "TEST-2024-ABC"
        assert entity.is_active is True
        assert len(entity.default_ingredient) == 1
        assert entity.default_ingredient[0].ingredient.name.value == "Test Ingredient"

    def test_to_model_conversion(self, mock_database, sample_product):
        """Test conversion from entity to database model"""
        # Arrange
        repository = SQLProductRepository(mock_database)

        # Act
        model = repository._to_model(sample_product)

        # Assert
        assert isinstance(model, ProductModel)
        assert model.internal_id == sample_product.internal_id
        assert model.name == sample_product.name.value
        assert model.price == float(sample_product.price.amount)
        assert model.category == sample_product.category.value
        assert model.sku == sample_product.sku.value
        assert model.is_active == sample_product.is_active

    def test_save_new_product(self, mock_database, mock_ingredient_repository, sample_product):
        """Test saving a new product"""
        # Arrange
        repository = SQLProductRepository(mock_database, mock_ingredient_repository)
        sample_product.internal_id = None  # New product
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session

        # Act
        repository.save(sample_product)

        # Assert
        # Check that add was called with a ProductModel object
        add_call_args = mock_database.add.call_args
        assert add_call_args is not None
        assert len(add_call_args[0]) == 2
        assert add_call_args[0][0] == mock_session
        assert isinstance(add_call_args[0][1], ProductModel)
        mock_database.commit.assert_called_once_with(mock_session)
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_save_existing_product(self, mock_database, mock_ingredient_repository, sample_product, sample_product_model):
        """Test updating an existing product"""
        # Arrange
        repository = SQLProductRepository(mock_database, mock_ingredient_repository)
        sample_product.internal_id = 1  # Set to simulate existing product
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.find_by_field.return_value = sample_product_model

        # Act
        repository.save(sample_product)

        # Assert
        mock_database.find_by_field.assert_called_once_with(mock_session, ProductModel, "internal_id", sample_product.internal_id)
        mock_database.update.assert_called_once_with(mock_session, sample_product_model)
        mock_database.commit.assert_called_once_with(mock_session)
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_save_existing_product_not_found(self, mock_database, mock_ingredient_repository, sample_product):
        """Test saving existing product that doesn't exist - should create new product"""
        # Arrange
        repository = SQLProductRepository(mock_database, mock_ingredient_repository)
        sample_product.internal_id = 999  # Set to simulate product that should exist but doesn't
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.find_by_field.return_value = None

        # Act
        repository.save(sample_product)

        # Assert
        mock_database.find_by_field.assert_called_once_with(mock_session, ProductModel, "internal_id", sample_product.internal_id)
        mock_database.add.assert_called_once()
        mock_database.commit.assert_called_once_with(mock_session)
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_save_rollback_on_error(self, mock_database, sample_product):
        """Test that rollback is called on error during save"""
        # Arrange
        repository = SQLProductRepository(mock_database)
        sample_product.internal_id = None  # New product
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.add.side_effect = Exception("Database error")

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            repository.save(sample_product)

        mock_database.rollback.assert_called_once_with(mock_session)
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_find_by_id_success(self, mock_database, mock_ingredient_repository, sample_product_model):
        """Test finding product by ID successfully"""
        # Arrange
        repository = SQLProductRepository(mock_database, mock_ingredient_repository)
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.find_by_field.return_value = sample_product_model
        product_id = 1

        # Act
        result = repository.find_by_id(product_id)

        # Assert
        assert isinstance(result, Product)
        assert result.internal_id is not None
        mock_database.find_by_field.assert_called_once_with(mock_session, ProductModel, "internal_id", product_id)
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_find_by_id_not_found(self, mock_database):
        """Test finding product by ID when not found"""
        # Arrange
        repository = SQLProductRepository(mock_database)
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.find_by_field.return_value = None
        product_id = 999

        # Act
        result = repository.find_by_id(product_id)

        # Assert
        assert result is None
        mock_database.find_by_field.assert_called_once_with(mock_session, ProductModel, "internal_id", product_id)
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_find_by_sku_success(self, mock_database, mock_ingredient_repository, sample_product_model):
        """Test finding product by SKU successfully"""
        # Arrange
        repository = SQLProductRepository(mock_database, mock_ingredient_repository)
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.find_by_field.return_value = sample_product_model
        sku = SKU.create("TEST-2024-ABC")

        # Act
        result = repository.find_by_sku(sku)

        # Assert
        assert isinstance(result, Product)
        assert result.sku.value == "TEST-2024-ABC"
        mock_database.find_by_field.assert_called_once_with(mock_session, ProductModel, "sku", "TEST-2024-ABC")
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_find_by_sku_not_found(self, mock_database):
        """Test finding product by SKU when not found"""
        # Arrange
        repository = SQLProductRepository(mock_database)
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.find_by_field.return_value = None
        sku = SKU.create("TEST-2024-XYZ")

        # Act
        result = repository.find_by_sku(sku)

        # Assert
        assert result is None
        mock_database.find_by_field.assert_called_once_with(mock_session, ProductModel, "sku", "TEST-2024-XYZ")
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_find_all_success(self, mock_database, mock_ingredient_repository, sample_product_model):
        """Test finding all products successfully"""
        # Arrange
        repository = SQLProductRepository(mock_database, mock_ingredient_repository)
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.find_all_by_boolean_field.return_value = [sample_product_model]

        # Act
        result = repository.find_all()

        # Assert
        assert len(result) == 1
        assert isinstance(result[0], Product)
        mock_database.find_all_by_boolean_field.assert_called_once_with(mock_session, ProductModel, "is_active", True)
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_find_all_empty(self, mock_database):
        """Test finding all products when none exist"""
        # Arrange
        repository = SQLProductRepository(mock_database)
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.find_all.return_value = []

        # Act
        result = repository.find_all()

        # Assert
        assert len(result) == 0
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_delete_success(self, mock_database, mock_ingredient_repository, sample_product_model):
        """Test deleting product successfully"""
        # Arrange
        repository = SQLProductRepository(mock_database, mock_ingredient_repository)
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.find_by_field.return_value = sample_product_model
        product_id = 1

        # Act
        result = repository.delete(product_id)

        # Assert
        assert result is True
        mock_database.find_by_field.assert_called_once_with(mock_session, ProductModel, "internal_id", product_id)
        mock_database.update.assert_called_once_with(mock_session, sample_product_model)
        mock_database.commit.assert_called_once_with(mock_session)
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_delete_not_found(self, mock_database):
        """Test deleting product that doesn't exist"""
        # Arrange
        repository = SQLProductRepository(mock_database)
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.find_by_field.return_value = None
        product_id = 999

        # Act
        result = repository.delete(product_id)

        # Assert
        assert result is False
        mock_database.find_by_field.assert_called_once_with(mock_session, ProductModel, "internal_id", product_id)
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_exists_by_sku_true(self, mock_database):
        """Test checking if product exists by SKU when it does"""
        # Arrange
        repository = SQLProductRepository(mock_database)
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.find_by_field.return_value = Mock(is_active=True)
        sku = SKU.create("TEST-2024-ABC")

        # Act
        result = repository.exists_by_sku(sku)

        # Assert
        assert result is True
        mock_database.find_by_field.assert_called_once_with(mock_session, ProductModel, "sku", "TEST-2024-ABC")
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_exists_by_sku_false(self, mock_database):
        """Test checking if product exists by SKU when it doesn't"""
        # Arrange
        repository = SQLProductRepository(mock_database)
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.find_by_field.return_value = None
        sku = SKU.create("TEST-2024-XYZ")

        # Act
        result = repository.exists_by_sku(sku)

        # Assert
        assert result is False
        mock_database.find_by_field.assert_called_once_with(mock_session, ProductModel, "sku", "TEST-2024-XYZ")
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_exists_by_id_true(self, mock_database):
        """Test checking if product exists by ID when it does"""
        # Arrange
        repository = SQLProductRepository(mock_database)
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.find_by_field.return_value = Mock()  # Return a mock object to indicate existence
        product_id = 1

        # Act
        result = repository.exists_by_id(product_id)

        # Assert
        assert result is True
        mock_database.find_by_field.assert_called_once_with(mock_session, ProductModel, "internal_id", product_id)
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_exists_by_name_true(self, mock_database):
        """Test checking if product exists by name when it does"""
        # Arrange
        repository = SQLProductRepository(mock_database)
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.find_by_field.return_value = Mock(is_active=True)
        name = "Test Product"

        # Act
        result = repository.exists_by_name(name)

        # Assert
        assert result is True
        mock_database.find_by_field.assert_called_once_with(mock_session, ProductModel, "name", name)
        mock_database.close_session.assert_called_once_with(mock_session)

    def test_exists_by_category_true(self, mock_database):
        """Test checking if product exists by category when it does"""
        # Arrange
        repository = SQLProductRepository(mock_database)
        mock_session = Mock()
        mock_database.get_session.return_value = mock_session
        mock_database.find_all_by_field.return_value = [Mock(is_active=True)]
        category = ProductCategory.BURGER

        # Act
        result = repository.exists_by_category(category)

        # Assert
        assert result is True
        mock_database.find_all_by_field.assert_called_once_with(mock_session, ProductModel, "category", category.value)
        mock_database.close_session.assert_called_once_with(mock_session)

 