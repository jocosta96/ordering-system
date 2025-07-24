"""
Integration tests for controllers.

Tests cover:
- CustomerController integration with use cases
- Error handling and presentation
- Authentication handling
"""

import pytest
from unittest.mock import Mock, patch

from src.adapters.controllers.customer_controller import CustomerController
from src.application.dto.customer_dto import CustomerResponse
from src.application.exceptions import (
    CustomerNotFoundException,
    CustomerAlreadyExistsException,
    CustomerBusinessRuleException,
    AuthenticationException,
)
from src.application.dto.customer_dto import CustomerListResponse


class TestCustomerController:
    """Test cases for CustomerController"""

    def test_get_anonymous_customer_success(
        self, mock_customer_repository, mock_presenter, sample_anonymous_customer
    ):
        """Test successful anonymous customer retrieval"""
        # Arrange
        controller = CustomerController(mock_customer_repository, mock_presenter)
        mock_presenter.present.return_value = {"id": None, "is_anonymous": True}

        # Mock the use case instance directly
        controller.anonymous_use_case.execute = Mock(
            return_value=CustomerResponse.from_entity(sample_anonymous_customer)
        )

        # Act
        result = controller.get_anonymous_customer()

        # Assert
        assert result == {"id": None, "is_anonymous": True}
        controller.anonymous_use_case.execute.assert_called_once()
        mock_presenter.present.assert_called_once()

    def test_get_anonymous_customer_not_found(
        self, mock_customer_repository, mock_presenter
    ):
        """Test anonymous customer retrieval when not found"""
        # Arrange
        controller = CustomerController(mock_customer_repository, mock_presenter)
        mock_presenter.present_error.return_value = {
            "error": "Anonymous customer not found"
        }

        # Mock the use case to raise exception
        controller.anonymous_use_case.execute = Mock(
            side_effect=CustomerNotFoundException("Anonymous customer not found")
        )

        # Act & Assert
        with pytest.raises(Exception):  # HTTPException will be raised
            controller.get_anonymous_customer()

    def test_get_customer_success(
        self, mock_customer_repository, mock_presenter, sample_customer
    ):
        """Test successful customer retrieval"""
        # Arrange
        controller = CustomerController(mock_customer_repository, mock_presenter)
        mock_presenter.present.return_value = {"id": 1, "first_name": "John"}

        # Mock the use case instance directly
        controller.read_use_case.execute = Mock(
            return_value=CustomerResponse.from_entity(sample_customer)
        )

        # Act
        result = controller.get_customer(1, "authenticated_user")

        # Assert
        assert result == {"id": 1, "first_name": "John"}
        controller.read_use_case.execute.assert_called_once_with(1)
        mock_presenter.present.assert_called_once()

    def test_get_customer_authentication_required(
        self, mock_customer_repository, mock_presenter
    ):
        """Test customer retrieval fails without authentication"""
        # Arrange
        controller = CustomerController(mock_customer_repository, mock_presenter)
        mock_presenter.present_error.return_value = {"error": "Authentication required"}

        # Act & Assert
        with pytest.raises(Exception):  # HTTPException will be raised
            controller.get_customer(1, "")

    def test_get_customer_not_found(self, mock_customer_repository, mock_presenter):
        """Test customer retrieval when customer not found"""
        # Arrange
        controller = CustomerController(mock_customer_repository, mock_presenter)
        mock_presenter.present_error.return_value = {"error": "Customer not found"}

        # Mock the use case to raise exception
        controller.read_use_case.execute = Mock(
            side_effect=CustomerNotFoundException("Customer not found")
        )

        # Act & Assert
        with pytest.raises(Exception):  # HTTPException will be raised
            controller.get_customer(1, "authenticated_user")

    def test_create_customer_success(
        self, mock_customer_repository, mock_presenter, sample_customer
    ):
        """Test successful customer creation"""
        # Arrange
        controller = CustomerController(mock_customer_repository, mock_presenter)
        mock_presenter.present.return_value = {"id": 1, "first_name": "John"}

        # Mock the use case instance directly
        controller.create_use_case.execute = Mock(
            return_value=CustomerResponse.from_entity(sample_customer)
        )

        customer_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "document": "52998224725",  # Valid Brazilian CPF
        }

        # Act
        result = controller.create_customer(customer_data, "authenticated_user")

        # Assert
        assert result == {"id": 1, "first_name": "John"}
        controller.create_use_case.execute.assert_called_once()
        mock_presenter.present.assert_called_once()

    def test_create_customer_already_exists(
        self, mock_customer_repository, mock_presenter
    ):
        """Test customer creation fails when customer already exists"""
        # Arrange
        controller = CustomerController(mock_customer_repository, mock_presenter)
        mock_presenter.present_error.return_value = {"error": "Customer already exists"}

        # Mock the use case to raise exception
        controller.create_use_case.execute = Mock(
            side_effect=CustomerAlreadyExistsException("Customer already exists")
        )

        customer_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "document": "52998224725",  # Valid Brazilian CPF
        }

        # Act & Assert
        with pytest.raises(Exception):  # HTTPException will be raised
            controller.create_customer(customer_data, "authenticated_user")

    def test_update_customer_success(
        self, mock_customer_repository, mock_presenter, sample_customer
    ):
        """Test successful customer update"""
        # Arrange
        controller = CustomerController(mock_customer_repository, mock_presenter)
        mock_presenter.present.return_value = {"id": 1, "first_name": "Jane"}

        # Mock the use case instance directly
        controller.update_use_case.execute = Mock(
            return_value=CustomerResponse.from_entity(sample_customer)
        )

        customer_data = {
            "id": 1,
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "document": "12345678909",  # Valid Brazilian CPF
        }

        # Act
        result = controller.update_customer(customer_data, "authenticated_user")

        # Assert
        assert result == {"id": 1, "first_name": "Jane"}
        controller.update_use_case.execute.assert_called_once()
        mock_presenter.present.assert_called_once()

    def test_delete_customer_success(self, mock_customer_repository, mock_presenter):
        """Test successful customer deletion"""
        # Arrange
        controller = CustomerController(mock_customer_repository, mock_presenter)
        mock_presenter.present.return_value = {
            "success": True,
            "message": "Customer deleted successfully",
        }

        # Mock the use case instance directly
        controller.delete_use_case.execute = Mock(return_value=True)

        # Act
        result = controller.delete_customer(1, "authenticated_user")

        # Assert
        assert result == {"success": True, "message": "Customer deleted successfully"}
        controller.delete_use_case.execute.assert_called_once_with(1)
        mock_presenter.present.assert_called_once()

    def test_list_customers_success(self, mock_customer_repository, mock_presenter):
        """Test successful customer listing"""
        # Arrange
        controller = CustomerController(mock_customer_repository, mock_presenter)
        mock_presenter.present.return_value = {"data": [], "total_count": 0}

        # Mock the use case instance directly
        controller.list_use_case.execute = Mock(
            return_value=CustomerListResponse(customers=[], total_count=0)
        )

        # Act
        result = controller.list_customers("authenticated_user")

        # Assert
        assert result == {"data": [], "total_count": 0}
        controller.list_use_case.execute.assert_called_once()
        mock_presenter.present.assert_called_once()
