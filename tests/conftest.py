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

from src.application.repositories.customer_repository import CustomerRepository
from src.adapters.presenters.interfaces.presenter_interface import PresenterInterface
from src.entities.customer import Customer
from src.entities.value_objects.name import Name
from src.entities.value_objects.email import Email
from src.entities.value_objects.document import Document


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
