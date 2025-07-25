"""
Integration tests for controllers.

Tests cover:
- CustomerController integration with use cases
- IngredientController integration with use cases
- Error handling and presentation
- Authentication handling
"""

import pytest
from unittest.mock import Mock

from src.adapters.controllers.customer_controller import CustomerController
from src.adapters.controllers.ingredient_controller import IngredientController
from src.application.dto import CustomerResponse, CustomerListResponse, IngredientResponse, IngredientListResponse
from src.application.exceptions import (
    CustomerNotFoundException,
    CustomerAlreadyExistsException,
    IngredientNotFoundException,
    IngredientAlreadyExistsException,
)
from src.entities.ingredient import IngredientType


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
        """Test customer retrieval fails when customer not found"""
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
        mock_presenter.present.return_value = {"id": 1, "first_name": "John"}

        # Mock the use case instance directly
        controller.update_use_case.execute = Mock(
            return_value=CustomerResponse.from_entity(sample_customer)
        )

        customer_data = {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "document": "52998224725",  # Valid Brazilian CPF
        }

        # Act
        result = controller.update_customer(customer_data, "authenticated_user")

        # Assert
        assert result == {"id": 1, "first_name": "John"}
        controller.update_use_case.execute.assert_called_once()
        mock_presenter.present.assert_called_once()

    def test_delete_customer_success(self, mock_customer_repository, mock_presenter):
        """Test successful customer deletion"""
        # Arrange
        controller = CustomerController(mock_customer_repository, mock_presenter)
        mock_presenter.present.return_value = {"success": True, "message": "Customer deleted successfully"}

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
        mock_presenter.present.return_value = {"customers": [], "total_count": 0}

        # Mock the use case instance directly
        controller.list_use_case.execute = Mock(
            return_value=CustomerListResponse(customers=[], total_count=0)
        )

        # Act
        result = controller.list_customers("authenticated_user")

        # Assert
        assert result == {"customers": [], "total_count": 0}
        controller.list_use_case.execute.assert_called_once()
        mock_presenter.present.assert_called_once()


class TestIngredientController:
    """Test cases for IngredientController"""

    def test_create_ingredient_success(
        self, mock_ingredient_repository, mock_presenter, sample_ingredient
    ):
        """Test successful ingredient creation"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present.return_value = {"id": 1, "name": "Tomato"}

        # Mock the use case instance directly
        controller.create_use_case.execute = Mock(
            return_value=IngredientResponse.from_entity(sample_ingredient)
        )

        ingredient_data = {
            "name": "Tomato",
            "price": 2.50,
            "is_active": True,
            "type": IngredientType.VEGETABLE,
            "applies_to_burger": True,
            "applies_to_side": False,
            "applies_to_drink": False,
            "applies_to_dessert": False,
        }

        # Act
        result = controller.create_ingredient(ingredient_data, "authenticated_user")

        # Assert
        assert result == {"id": 1, "name": "Tomato"}
        controller.create_use_case.execute.assert_called_once()
        mock_presenter.present.assert_called_once()

    def test_create_ingredient_authentication_required(
        self, mock_ingredient_repository, mock_presenter
    ):
        """Test ingredient creation fails without authentication"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present_error.return_value = {"error": "Authentication required"}

        ingredient_data = {
            "name": "Tomato",
            "price": 2.50,
            "is_active": True,
            "type": IngredientType.VEGETABLE,
            "applies_to_burger": True,
            "applies_to_side": False,
            "applies_to_drink": False,
            "applies_to_dessert": False,
        }

        # Act & Assert
        with pytest.raises(Exception):  # HTTPException will be raised
            controller.create_ingredient(ingredient_data, "")

    def test_create_ingredient_already_exists(
        self, mock_ingredient_repository, mock_presenter
    ):
        """Test ingredient creation fails when ingredient already exists"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present_error.return_value = {"error": "Ingredient already exists"}

        # Mock the use case to raise exception
        controller.create_use_case.execute = Mock(
            side_effect=IngredientAlreadyExistsException("Ingredient already exists")
        )

        ingredient_data = {
            "name": "Tomato",
            "price": 2.50,
            "is_active": True,
            "type": IngredientType.VEGETABLE,
            "applies_to_burger": True,
            "applies_to_side": False,
            "applies_to_drink": False,
            "applies_to_dessert": False,
        }

        # Act & Assert
        with pytest.raises(Exception):  # HTTPException will be raised
            controller.create_ingredient(ingredient_data, "authenticated_user")

    def test_get_ingredient_success(
        self, mock_ingredient_repository, mock_presenter, sample_ingredient
    ):
        """Test successful ingredient retrieval"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present.return_value = {"id": 1, "name": "Tomato"}

        # Mock the use case instance directly
        controller.read_use_case.execute = Mock(
            return_value=IngredientResponse.from_entity(sample_ingredient)
        )

        # Act
        result = controller.get_ingredient(1, "authenticated_user")

        # Assert
        assert result == {"id": 1, "name": "Tomato"}
        controller.read_use_case.execute.assert_called_once_with(1)
        mock_presenter.present.assert_called_once()

    def test_get_ingredient_authentication_required(
        self, mock_ingredient_repository, mock_presenter
    ):
        """Test ingredient retrieval fails without authentication"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present_error.return_value = {"error": "Authentication required"}

        # Act & Assert
        with pytest.raises(Exception):  # HTTPException will be raised
            controller.get_ingredient(1, "")

    def test_get_ingredient_not_found(self, mock_ingredient_repository, mock_presenter):
        """Test ingredient retrieval fails when ingredient not found"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present_error.return_value = {"error": "Ingredient not found"}

        # Mock the use case to raise exception
        controller.read_use_case.execute = Mock(
            side_effect=IngredientNotFoundException("Ingredient not found")
        )

        # Act & Assert
        with pytest.raises(Exception):  # HTTPException will be raised
            controller.get_ingredient(1, "authenticated_user")

    def test_update_ingredient_success(
        self, mock_ingredient_repository, mock_presenter, sample_ingredient
    ):
        """Test successful ingredient update"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present.return_value = {"id": 1, "name": "Tomato"}

        # Mock the use case instance directly
        controller.update_use_case.execute = Mock(
            return_value=IngredientResponse.from_entity(sample_ingredient)
        )

        ingredient_data = {
            "id": 1,
            "name": "Tomato",
            "price": 2.50,
            "is_active": True,
            "type": IngredientType.VEGETABLE,
            "applies_to_burger": True,
            "applies_to_side": False,
            "applies_to_drink": False,
            "applies_to_dessert": False,
        }

        # Act
        result = controller.update_ingredient(ingredient_data, "authenticated_user")

        # Assert
        assert result == {"id": 1, "name": "Tomato"}
        controller.update_use_case.execute.assert_called_once()
        mock_presenter.present.assert_called_once()

    def test_update_ingredient_authentication_required(
        self, mock_ingredient_repository, mock_presenter
    ):
        """Test ingredient update fails without authentication"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present_error.return_value = {"error": "Authentication required"}

        ingredient_data = {
            "id": 1,
            "name": "Tomato",
            "price": 2.50,
            "is_active": True,
            "type": IngredientType.VEGETABLE,
            "applies_to_burger": True,
            "applies_to_side": False,
            "applies_to_drink": False,
            "applies_to_dessert": False,
        }

        # Act & Assert
        with pytest.raises(Exception):  # HTTPException will be raised
            controller.update_ingredient(ingredient_data, "")

    def test_update_ingredient_not_found(self, mock_ingredient_repository, mock_presenter):
        """Test ingredient update fails when ingredient not found"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present_error.return_value = {"error": "Ingredient not found"}

        # Mock the use case to raise exception
        controller.update_use_case.execute = Mock(
            side_effect=IngredientNotFoundException("Ingredient not found")
        )

        ingredient_data = {
            "id": 1,
            "name": "Tomato",
            "price": 2.50,
            "is_active": True,
            "type": IngredientType.VEGETABLE,
            "applies_to_burger": True,
            "applies_to_side": False,
            "applies_to_drink": False,
            "applies_to_dessert": False,
        }

        # Act & Assert
        with pytest.raises(Exception):  # HTTPException will be raised
            controller.update_ingredient(ingredient_data, "authenticated_user")

    def test_delete_ingredient_success(self, mock_ingredient_repository, mock_presenter):
        """Test successful ingredient deletion"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present.return_value = {"success": True, "message": "Ingredient deleted successfully"}

        # Mock the use case instance directly
        controller.delete_use_case.execute = Mock(return_value=True)

        # Act
        result = controller.delete_ingredient(1, "authenticated_user")

        # Assert
        assert result == {"success": True, "message": "Ingredient deleted successfully"}
        controller.delete_use_case.execute.assert_called_once_with(1)
        mock_presenter.present.assert_called_once()

    def test_delete_ingredient_authentication_required(
        self, mock_ingredient_repository, mock_presenter
    ):
        """Test ingredient deletion fails without authentication"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present_error.return_value = {"error": "Authentication required"}

        # Act & Assert
        with pytest.raises(Exception):  # HTTPException will be raised
            controller.delete_ingredient(1, "")

    def test_delete_ingredient_not_found(self, mock_ingredient_repository, mock_presenter):
        """Test ingredient deletion fails when ingredient not found"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present_error.return_value = {"error": "Ingredient not found"}

        # Mock the use case to raise exception
        controller.delete_use_case.execute = Mock(
            side_effect=IngredientNotFoundException("Ingredient not found")
        )

        # Act & Assert
        with pytest.raises(Exception):  # HTTPException will be raised
            controller.delete_ingredient(1, "authenticated_user")

    def test_list_ingredients_success(self, mock_ingredient_repository, mock_presenter):
        """Test successful ingredient listing"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present.return_value = {"ingredients": [], "total_count": 0}

        # Mock the use case instance directly
        controller.list_use_case.execute = Mock(
            return_value=IngredientListResponse(ingredients=[], total_count=0)
        )

        # Act
        result = controller.list_ingredients("authenticated_user")

        # Assert
        assert result == {"ingredients": [], "total_count": 0}
        controller.list_use_case.execute.assert_called_once()
        mock_presenter.present.assert_called_once()

    def test_list_ingredients_authentication_required(
        self, mock_ingredient_repository, mock_presenter
    ):
        """Test ingredient listing fails without authentication"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present_error.return_value = {"error": "Authentication required"}

        # Act & Assert
        with pytest.raises(Exception):  # HTTPException will be raised
            controller.list_ingredients("")

    def test_list_ingredients_by_type_success(self, mock_ingredient_repository, mock_presenter):
        """Test successful ingredient listing by type"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present.return_value = {"ingredients": [], "total_count": 0}

        # Mock the use case instance directly
        controller.list_by_type_use_case.execute = Mock(
            return_value=IngredientListResponse(ingredients=[], total_count=0)
        )

        # Act
        result = controller.list_ingredients_by_type(IngredientType.VEGETABLE, "authenticated_user")

        # Assert
        assert result == {"ingredients": [], "total_count": 0}
        controller.list_by_type_use_case.execute.assert_called_once_with(IngredientType.VEGETABLE)
        mock_presenter.present.assert_called_once()

    def test_list_ingredients_by_type_authentication_required(
        self, mock_ingredient_repository, mock_presenter
    ):
        """Test ingredient listing by type fails without authentication"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present_error.return_value = {"error": "Authentication required"}

        # Act & Assert
        with pytest.raises(Exception):  # HTTPException will be raised
            controller.list_ingredients_by_type(IngredientType.VEGETABLE, "")

    def test_list_ingredients_by_applies_to_success(self, mock_ingredient_repository, mock_presenter):
        """Test successful ingredient listing by applies to"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present.return_value = {"ingredients": [], "total_count": 0}

        # Mock the use case instance directly
        controller.list_by_applies_to_use_case.execute = Mock(
            return_value=IngredientListResponse(ingredients=[], total_count=0)
        )

        # Act
        result = controller.list_ingredients_by_applies_to(
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
            login="authenticated_user"
        )

        # Assert
        assert result == {"ingredients": [], "total_count": 0}
        controller.list_by_applies_to_use_case.execute.assert_called_once_with(
            True, False, False, False
        )
        mock_presenter.present.assert_called_once()

    def test_list_ingredients_by_applies_to_authentication_required(
        self, mock_ingredient_repository, mock_presenter
    ):
        """Test ingredient listing by applies to fails without authentication"""
        # Arrange
        controller = IngredientController(mock_ingredient_repository, mock_presenter)
        mock_presenter.present_error.return_value = {"error": "Authentication required"}

        # Act & Assert
        with pytest.raises(Exception):  # HTTPException will be raised
            controller.list_ingredients_by_applies_to(
                applies_to_burger=True,
                applies_to_side=False,
                applies_to_drink=False,
                applies_to_dessert=False,
                login=""
            )
