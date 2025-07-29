"""
Unit tests for controllers.

Tests cover:
- Customer controller
- Ingredient controller
- Product controller
- Order controller
- Error handling
- Business logic
"""

import pytest
from unittest.mock import Mock

from src.adapters.controllers.customer_controller import CustomerController
from src.adapters.controllers.ingredient_controller import IngredientController
from src.adapters.controllers.product_controller import ProductController
from src.adapters.controllers.order_controller import OrderController
from src.entities.customer import Customer
from src.entities.ingredient import Ingredient, IngredientType
from src.entities.product import Product, ProductCategory, ProductReceiptItem
from src.entities.order import Order, OrderItem
from src.entities.value_objects.money import Money
from src.entities.value_objects.sku import SKU


class TestCustomerController:
    """Test cases for customer controller"""

    @pytest.fixture
    def mock_customer_repository(self):
        """Mock customer repository"""
        return Mock()

    @pytest.fixture
    def mock_presenter(self):
        """Mock presenter"""
        return Mock()

    @pytest.fixture
    def customer_controller(self, mock_customer_repository, mock_presenter):
        """Create customer controller with mocked dependencies"""
        return CustomerController(
            customer_repository=mock_customer_repository,
            presenter=mock_presenter
        )

    @pytest.fixture
    def sample_customer(self):
        """Sample customer for testing"""
        return Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            document="12345678909"  # Valid CPF
        )


class TestIngredientController:
    """Test cases for ingredient controller"""

    @pytest.fixture
    def mock_ingredient_repository(self):
        """Mock ingredient repository"""
        return Mock()

    @pytest.fixture
    def mock_presenter(self):
        """Mock presenter"""
        return Mock()

    @pytest.fixture
    def ingredient_controller(self, mock_ingredient_repository, mock_presenter):
        """Create ingredient controller with mocked dependencies"""
        return IngredientController(
            ingredient_repository=mock_ingredient_repository,
            presenter=mock_presenter
        )

    @pytest.fixture
    def sample_ingredient(self):
        """Sample ingredient for testing"""
        return Ingredient.create(
            name="Cheese",
            price=Money(2.50),
            is_active=True,
            type=IngredientType.CHEESE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )


class TestProductController:
    """Test cases for product controller"""

    @pytest.fixture
    def mock_product_repository(self):
        """Mock product repository"""
        return Mock()

    @pytest.fixture
    def mock_presenter(self):
        """Mock presenter"""
        return Mock()

    @pytest.fixture
    def mock_ingredient_repository(self):
        """Mock ingredient repository"""
        return Mock()

    @pytest.fixture
    def product_controller(self, mock_product_repository, mock_ingredient_repository, mock_presenter):
        """Create product controller with mocked dependencies"""
        return ProductController(
            product_repository=mock_product_repository,
            ingredient_repository=mock_ingredient_repository,
            presenter=mock_presenter
        )

    @pytest.fixture
    def sample_ingredient(self):
        """Sample ingredient for testing"""
        return Ingredient.create(
            name="Cheese",
            price=Money(2.50),
            is_active=True,
            type=IngredientType.CHEESE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )

    @pytest.fixture
    def sample_product(self, sample_ingredient):
        """Sample product for testing"""
        default_ingredients = [ProductReceiptItem(sample_ingredient, 1)]
        return Product.create(
            name="Cheeseburger",
            price=Money(12.99),
            category=ProductCategory.BURGER,
            sku=SKU("BURG-2024-CHS"),
            default_ingredient=default_ingredients,
            is_active=True
        )


class TestOrderController:
    """Test cases for order controller"""

    @pytest.fixture
    def mock_order_repository(self):
        """Mock order repository"""
        return Mock()

    @pytest.fixture
    def mock_customer_repository(self):
        """Mock customer repository"""
        return Mock()

    @pytest.fixture
    def mock_product_repository(self):
        """Mock product repository"""
        return Mock()

    @pytest.fixture
    def mock_ingredient_repository(self):
        """Mock ingredient repository"""
        return Mock()

    @pytest.fixture
    def mock_qr_payment_repository(self):
        """Mock QR payment repository"""
        return Mock()

    @pytest.fixture
    def mock_presenter(self):
        """Mock presenter"""
        return Mock()

    @pytest.fixture
    def order_controller(self, mock_order_repository, mock_customer_repository, mock_product_repository, mock_ingredient_repository, mock_qr_payment_repository, mock_presenter):
        """Create order controller with mocked dependencies"""
        return OrderController(
            order_repository=mock_order_repository,
            customer_repository=mock_customer_repository,
            product_repository=mock_product_repository,
            ingredient_repository=mock_ingredient_repository,
            qr_payment_repository=mock_qr_payment_repository,
            presenter=mock_presenter
        )

    @pytest.fixture
    def sample_customer(self):
        """Sample customer for testing"""
        return Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            document="12345678909"
        )

    @pytest.fixture
    def sample_ingredient(self):
        """Sample ingredient for testing"""
        return Ingredient.create(
            name="Cheese",
            price=Money(2.50),
            is_active=True,
            type=IngredientType.CHEESE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )

    @pytest.fixture
    def sample_product(self, sample_ingredient):
        """Sample product for testing"""
        default_ingredients = [ProductReceiptItem(sample_ingredient, 1)]
        return Product.create(
            name="Cheeseburger",
            price=Money(12.99),
            category=ProductCategory.BURGER,
            sku=SKU("BURG-2024-CHS"),
            default_ingredient=default_ingredients,
            is_active=True
        )

    @pytest.fixture
    def sample_order(self, sample_customer, sample_product):
        """Sample order for testing"""
        order_items = [
            OrderItem(
                order_internal_id=0,
                product=sample_product,
                additional_ingredients=[],
                remove_ingredients=[]
            )
        ]
        return Order.create(
            customer_internal_id=sample_customer.internal_id,
            order_items=order_items
        ) 