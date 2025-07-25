"""
Pytest configuration and fixtures for the ordering system tests.

This file provides:
- Test configuration
- Common fixtures for all test layers
- Mock implementations for testing
"""

import pytest
from unittest.mock import Mock, MagicMock
from typing import Generator
from decimal import Decimal

from src.application.repositories.customer_repository import CustomerRepository
from src.application.repositories.ingredient_repository import IngredientRepository
from src.adapters.presenters.interfaces.presenter_interface import PresenterInterface
from src.entities.customer import Customer
from src.entities.ingredient import Ingredient, IngredientType
from src.entities.value_objects.name import Name
from src.entities.value_objects.email import Email
from src.entities.value_objects.document import Document
from src.entities.value_objects.money import Money


@pytest.fixture
def mock_customer_repository() -> Mock:
    """Mock customer repository for testing"""
    mock_repo = Mock(spec=CustomerRepository)

    # Setup default mock behaviors
    mock_repo.save.return_value = None
    mock_repo.find_by_id.return_value = None
    mock_repo.find_by_document.return_value = None
    mock_repo.find_by_email.return_value = None
    mock_repo.find_all.return_value = []
    mock_repo.delete.return_value = False
    mock_repo.exists_by_document.return_value = False
    mock_repo.exists_by_email.return_value = False

    return mock_repo


@pytest.fixture
def mock_ingredient_repository() -> Mock:
    """Mock ingredient repository for testing"""
    mock_repo = Mock(spec=IngredientRepository)

    # Setup default mock behaviors
    mock_repo.save.return_value = None
    mock_repo.find_by_id.return_value = None
    mock_repo.find_by_name.return_value = None
    mock_repo.find_by_type.return_value = []
    mock_repo.find_by_applies_usage.return_value = []
    mock_repo.find_all.return_value = []
    mock_repo.delete.return_value = False
    mock_repo.exists_by_name.return_value = False
    mock_repo.exists_by_type.return_value = False

    return mock_repo


@pytest.fixture
def mock_presenter() -> Mock:
    """Mock presenter for testing"""
    mock_presenter = Mock(spec=PresenterInterface)

    # Setup default mock behaviors
    mock_presenter.present.return_value = {"status": "success"}
    mock_presenter.present_list.return_value = {"data": [], "total_count": 0}
    mock_presenter.present_error.return_value = {"error": "test error"}

    return mock_presenter


@pytest.fixture
def sample_customer() -> Customer:
    """Sample customer entity for testing"""
    return Customer.create_registered(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        document="52998224725",  # Valid Brazilian CPF
        customer_id=1,
    )


@pytest.fixture
def sample_anonymous_customer() -> Customer:
    """Sample anonymous customer entity for testing"""
    return Customer.create_anonymous()


@pytest.fixture
def sample_customers() -> list[Customer]:
    """Sample list of customers for testing"""
    return [
        Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725",  # Valid Brazilian CPF
            customer_id=1,
        ),
        Customer.create_registered(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            document="12345678909",  # Valid Brazilian CPF
            customer_id=2,
        ),
        Customer.create_anonymous(),
    ]


@pytest.fixture
def sample_ingredient() -> Ingredient:
    """Sample ingredient entity for testing"""
    return Ingredient.create(
        name="Tomato",
        price=Money(amount=Decimal("2.50")),
        is_active=True,
        type=IngredientType.VEGETABLE,
        applies_to_burger=True,
        applies_to_side=False,
        applies_to_drink=False,
        applies_to_dessert=False,
        ingredient_id=1,
    )


@pytest.fixture
def sample_ingredients() -> list[Ingredient]:
    """Sample list of ingredients for testing"""
    return [
        Ingredient.create(
            name="Tomato",
            price=Money(amount=Decimal("2.50")),
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
            ingredient_id=1,
        ),
        Ingredient.create(
            name="Lettuce",
            price=Money(amount=Decimal("1.00")),
            is_active=True,
            type=IngredientType.SALAD,
            applies_to_burger=True,
            applies_to_side=True,
            applies_to_drink=False,
            applies_to_dessert=False,
            ingredient_id=2,
        ),
        Ingredient.create(
            name="Cheese",
            price=Money(amount=Decimal("3.00")),
            is_active=True,
            type=IngredientType.CHEESE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
            ingredient_id=3,
        ),
    ]


@pytest.fixture
def valid_name() -> Name:
    """Valid name value object for testing"""
    return Name.create("John")


@pytest.fixture
def valid_email() -> Email:
    """Valid email value object for testing"""
    return Email.create("test@example.com")


@pytest.fixture
def valid_document() -> Document:
    """Valid document value object for testing"""
    return Document.create("52998224725")  # Valid Brazilian CPF


@pytest.fixture
def valid_money() -> Money:
    """Valid money value object for testing"""
    return Money(amount=Decimal("10.00"))


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test"""
    # Set test environment variables
    import os

    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["ANONYMOUS_EMAIL"] = "anonymous@test.local"

    yield

    # Cleanup after each test
    pass
