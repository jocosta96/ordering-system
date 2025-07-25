"""
Unit tests for use cases.

Tests cover:
- CustomerCreateUseCase
- CustomerReadUseCase
- CustomerUpdateUseCase
- CustomerDeleteUseCase
- CustomerListUseCase
- CustomerGetAnonymousUseCase
- IngredientCreateUseCase
- IngredientReadUseCase
- IngredientUpdateUseCase
- IngredientDeleteUseCase
- IngredientListUseCase
- IngredientListByTypeUseCase
- IngredientListByAppliesToUseCase
"""

import pytest
from unittest.mock import Mock
from decimal import Decimal

from src.application.use_cases.customer_use_cases import (
    CustomerCreateUseCase,
    CustomerReadUseCase,
    CustomerUpdateUseCase,
    CustomerDeleteUseCase,
    CustomerListUseCase,
    CustomerGetAnonymousUseCase,
)
from src.application.use_cases.ingredient_use_cases import (
    IngredientCreateUseCase,
    IngredientReadUseCase,
    IngredientUpdateUseCase,
    IngredientDeleteUseCase,
    IngredientListUseCase,
    IngredientListByTypeUseCase,
    IngredientListByAppliesToUseCase,
)
from src.application.dto.customer_dto import (
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerResponse,
    CustomerListResponse,
)
from src.application.dto.ingredient_dto import (
    IngredientCreateRequest,
    IngredientUpdateRequest,
    IngredientResponse,
    IngredientListResponse,
)
from src.application.exceptions import (
    CustomerNotFoundException,
    CustomerAlreadyExistsException,
    CustomerBusinessRuleException,
    IngredientNotFoundException,
    IngredientAlreadyExistsException,
    IngredientValidationException,
    IngredientBusinessRuleException,
)
from src.entities.customer import Customer
from src.entities.ingredient import Ingredient, IngredientType
from src.entities.value_objects.money import Money


class TestCustomerCreateUseCase:
    """Test cases for CustomerCreateUseCase"""

    def test_create_customer_success(self, mock_customer_repository, sample_customer):
        """Test successful customer creation"""
        # Arrange
        mock_customer_repository.save.return_value = sample_customer
        use_case = CustomerCreateUseCase(mock_customer_repository)
        request = CustomerCreateRequest(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725",  # Valid Brazilian CPF
        )

        # Act
        result = use_case.execute(request)

        # Assert
        assert isinstance(result, CustomerResponse)
        assert result.first_name == "John"
        assert result.last_name == "Doe"
        assert result.email == "john.doe@example.com"
        assert result.document == "52998224725"  # Valid Brazilian CPF
        mock_customer_repository.save.assert_called_once()

    def test_create_customer_document_already_exists(self, mock_customer_repository):
        """Test customer creation fails when document already exists"""
        # Arrange
        mock_customer_repository.exists_by_document.return_value = True
        use_case = CustomerCreateUseCase(mock_customer_repository)
        request = CustomerCreateRequest(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725",  # Valid Brazilian CPF
        )

        # Act & Assert
        with pytest.raises(
            CustomerAlreadyExistsException, match="document.*already exists"
        ):
            use_case.execute(request)

    def test_create_customer_email_already_exists(self, mock_customer_repository):
        """Test customer creation fails when email already exists"""
        # Arrange
        mock_customer_repository.exists_by_email.return_value = True
        use_case = CustomerCreateUseCase(mock_customer_repository)
        request = CustomerCreateRequest(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725",  # Valid Brazilian CPF
        )

        # Act & Assert
        with pytest.raises(
            CustomerAlreadyExistsException, match="email.*already exists"
        ):
            use_case.execute(request)


class TestCustomerReadUseCase:
    """Test cases for CustomerReadUseCase"""

    def test_read_customer_success(self, mock_customer_repository, sample_customer):
        """Test successful customer retrieval"""
        # Arrange
        mock_customer_repository.find_by_id.return_value = sample_customer
        use_case = CustomerReadUseCase(mock_customer_repository)

        # Act
        result = use_case.execute(1)

        # Assert
        assert isinstance(result, CustomerResponse)
        assert result.id == 1
        assert result.first_name == "John"
        mock_customer_repository.find_by_id.assert_called_once_with(1)

    def test_read_customer_not_found(self, mock_customer_repository):
        """Test customer retrieval fails when customer not found"""
        # Arrange
        mock_customer_repository.find_by_id.return_value = None
        use_case = CustomerReadUseCase(mock_customer_repository)

        # Act & Assert
        with pytest.raises(CustomerNotFoundException, match="not found"):
            use_case.execute(1)


class TestCustomerUpdateUseCase:
    """Test cases for CustomerUpdateUseCase"""

    def test_update_customer_success(self, mock_customer_repository, sample_customer):
        """Test successful customer update"""
        # Arrange
        mock_customer_repository.find_by_id.return_value = sample_customer
        mock_customer_repository.save.return_value = sample_customer
        use_case = CustomerUpdateUseCase(mock_customer_repository)
        request = CustomerUpdateRequest(
            id=1,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725",  # Valid Brazilian CPF
        )

        # Act
        result = use_case.execute(request)

        # Assert
        assert isinstance(result, CustomerResponse)
        assert result.id == 1
        mock_customer_repository.save.assert_called_once()

    def test_update_customer_not_found(self, mock_customer_repository):
        """Test customer update fails when customer not found"""
        # Arrange
        mock_customer_repository.find_by_id.return_value = None
        use_case = CustomerUpdateUseCase(mock_customer_repository)
        request = CustomerUpdateRequest(
            id=1,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725",  # Valid Brazilian CPF
        )

        # Act & Assert
        with pytest.raises(CustomerNotFoundException, match="not found"):
            use_case.execute(request)

    def test_update_customer_document_conflict(
        self, mock_customer_repository, sample_customer
    ):
        """Test customer update fails when new document conflicts"""
        # Arrange
        mock_customer_repository.find_by_id.return_value = sample_customer
        # Mock find_by_document to return a different customer (conflict)
        conflicting_customer = Customer.create_registered(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            document="12345678909",
            customer_id=2
        )
        mock_customer_repository.find_by_document.return_value = conflicting_customer
        use_case = CustomerUpdateUseCase(mock_customer_repository)
        request = CustomerUpdateRequest(
            id=1,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="12345678909",  # Different document
        )

        # Act & Assert
        with pytest.raises(
            CustomerAlreadyExistsException, match="Document.*already used"
        ):
            use_case.execute(request)


class TestCustomerDeleteUseCase:
    """Test cases for CustomerDeleteUseCase"""

    def test_delete_customer_success(self, mock_customer_repository, sample_customer):
        """Test successful customer deletion"""
        # Arrange
        mock_customer_repository.find_by_id.return_value = sample_customer
        mock_customer_repository.delete.return_value = True
        use_case = CustomerDeleteUseCase(mock_customer_repository)

        # Act
        result = use_case.execute(1)

        # Assert
        assert result is True
        mock_customer_repository.delete.assert_called_once_with(1)

    def test_delete_customer_not_found(self, mock_customer_repository):
        """Test customer deletion fails when customer not found"""
        # Arrange
        mock_customer_repository.find_by_id.return_value = None
        use_case = CustomerDeleteUseCase(mock_customer_repository)

        # Act & Assert
        with pytest.raises(CustomerNotFoundException, match="not found"):
            use_case.execute(1)

    def test_delete_anonymous_customer_fails(
        self, mock_customer_repository, sample_anonymous_customer
    ):
        """Test that deleting anonymous customer fails"""
        # Arrange
        mock_customer_repository.find_by_id.return_value = sample_anonymous_customer
        use_case = CustomerDeleteUseCase(mock_customer_repository)

        # Act & Assert
        with pytest.raises(CustomerBusinessRuleException, match="Cannot delete anonymous customer"):
            use_case.execute(1)


class TestCustomerListUseCase:
    """Test cases for CustomerListUseCase"""

    def test_list_customers_success(self, mock_customer_repository, sample_customers):
        """Test successful customer listing"""
        # Arrange
        mock_customer_repository.find_all.return_value = sample_customers
        use_case = CustomerListUseCase(mock_customer_repository)

        # Act
        result = use_case.execute()

        # Assert
        assert isinstance(result, CustomerListResponse)
        assert len(result.customers) == 3
        assert result.total_count == 3
        mock_customer_repository.find_all.assert_called_once()

    def test_list_customers_empty(self, mock_customer_repository):
        """Test customer listing when no customers exist"""
        # Arrange
        mock_customer_repository.find_all.return_value = []
        use_case = CustomerListUseCase(mock_customer_repository)

        # Act
        result = use_case.execute()

        # Assert
        assert isinstance(result, CustomerListResponse)
        assert len(result.customers) == 0
        assert result.total_count == 0


class TestCustomerGetAnonymousUseCase:
    """Test cases for CustomerGetAnonymousUseCase"""

    def test_get_anonymous_customer_success(
        self, mock_customer_repository, sample_anonymous_customer
    ):
        """Test successful anonymous customer retrieval"""
        # Arrange
        mock_customer_repository.get_anonymous_customer.return_value = sample_anonymous_customer
        use_case = CustomerGetAnonymousUseCase(mock_customer_repository)

        # Act
        result = use_case.execute()

        # Assert
        assert isinstance(result, CustomerResponse)
        assert result.is_anonymous is True
        mock_customer_repository.get_anonymous_customer.assert_called_once()


class TestIngredientCreateUseCase:
    """Test cases for IngredientCreateUseCase"""

    def test_create_ingredient_success(self, mock_ingredient_repository, sample_ingredient):
        """Test successful ingredient creation"""
        # Arrange
        mock_ingredient_repository.save.return_value = sample_ingredient
        use_case = IngredientCreateUseCase(mock_ingredient_repository)
        request = IngredientCreateRequest(
            name="Tomato",
            price=2.50,
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
        )

        # Act
        result = use_case.execute(request)

        # Assert
        assert isinstance(result, IngredientResponse)
        assert result.name == "Tomato"
        assert result.price == 2.50
        assert result.type == IngredientType.VEGETABLE
        assert result.applies_to_burger is True
        mock_ingredient_repository.save.assert_called_once()

    def test_create_ingredient_name_already_exists(self, mock_ingredient_repository):
        """Test ingredient creation fails when name already exists"""
        # Arrange
        mock_ingredient_repository.exists_by_name.return_value = True
        use_case = IngredientCreateUseCase(mock_ingredient_repository)
        request = IngredientCreateRequest(
            name="Tomato",
            price=2.50,
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
        )

        # Act & Assert
        with pytest.raises(
            IngredientAlreadyExistsException, match="name.*already exists"
        ):
            use_case.execute(request)


class TestIngredientReadUseCase:
    """Test cases for IngredientReadUseCase"""

    def test_read_ingredient_success(self, mock_ingredient_repository, sample_ingredient):
        """Test successful ingredient retrieval"""
        # Arrange
        mock_ingredient_repository.find_by_id.return_value = sample_ingredient
        use_case = IngredientReadUseCase(mock_ingredient_repository)

        # Act
        result = use_case.execute(1)

        # Assert
        assert isinstance(result, IngredientResponse)
        assert result.id == 1
        assert result.name == "Tomato"
        mock_ingredient_repository.find_by_id.assert_called_once_with(1)

    def test_read_ingredient_not_found(self, mock_ingredient_repository):
        """Test ingredient retrieval fails when ingredient not found"""
        # Arrange
        mock_ingredient_repository.find_by_id.return_value = None
        use_case = IngredientReadUseCase(mock_ingredient_repository)

        # Act & Assert
        with pytest.raises(IngredientNotFoundException, match="not found"):
            use_case.execute(1)


class TestIngredientUpdateUseCase:
    """Test cases for IngredientUpdateUseCase"""

    def test_update_ingredient_success(self, mock_ingredient_repository, sample_ingredient):
        """Test successful ingredient update"""
        # Arrange
        mock_ingredient_repository.find_by_id.return_value = sample_ingredient
        mock_ingredient_repository.save.return_value = sample_ingredient
        use_case = IngredientUpdateUseCase(mock_ingredient_repository)
        request = IngredientUpdateRequest(
            id=1,
            name="Tomato",
            price=2.50,
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
        )

        # Act
        result = use_case.execute(request)

        # Assert
        assert isinstance(result, IngredientResponse)
        assert result.id == 1
        mock_ingredient_repository.save.assert_called_once()

    def test_update_ingredient_not_found(self, mock_ingredient_repository):
        """Test ingredient update fails when ingredient not found"""
        # Arrange
        mock_ingredient_repository.find_by_id.return_value = None
        use_case = IngredientUpdateUseCase(mock_ingredient_repository)
        request = IngredientUpdateRequest(
            id=1,
            name="Tomato",
            price=2.50,
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
        )

        # Act & Assert
        with pytest.raises(IngredientNotFoundException, match="not found"):
            use_case.execute(request)

    def test_update_ingredient_name_conflict(
        self, mock_ingredient_repository, sample_ingredient
    ):
        """Test ingredient update fails when new name conflicts"""
        # Arrange
        mock_ingredient_repository.find_by_id.return_value = sample_ingredient
        mock_ingredient_repository.exists_by_name.return_value = True
        use_case = IngredientUpdateUseCase(mock_ingredient_repository)
        request = IngredientUpdateRequest(
            id=1,
            name="Lettuce",  # Different name
            price=2.50,
            is_active=True,
            type=IngredientType.VEGETABLE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
        )

        # Act & Assert
        with pytest.raises(
            IngredientAlreadyExistsException, match="name.*already exists"
        ):
            use_case.execute(request)


class TestIngredientDeleteUseCase:
    """Test cases for IngredientDeleteUseCase"""

    def test_delete_ingredient_success(self, mock_ingredient_repository, sample_ingredient):
        """Test successful ingredient deletion"""
        # Arrange
        mock_ingredient_repository.find_by_id.return_value = sample_ingredient
        mock_ingredient_repository.delete.return_value = True
        use_case = IngredientDeleteUseCase(mock_ingredient_repository)

        # Act
        result = use_case.execute(1)

        # Assert
        assert result is True
        mock_ingredient_repository.delete.assert_called_once_with(1)

    def test_delete_ingredient_not_found(self, mock_ingredient_repository):
        """Test ingredient deletion fails when ingredient not found"""
        # Arrange
        mock_ingredient_repository.find_by_id.return_value = None
        use_case = IngredientDeleteUseCase(mock_ingredient_repository)

        # Act & Assert
        with pytest.raises(IngredientNotFoundException, match="not found"):
            use_case.execute(1)


class TestIngredientListUseCase:
    """Test cases for IngredientListUseCase"""

    def test_list_ingredients_success(self, mock_ingredient_repository, sample_ingredients):
        """Test successful ingredient listing"""
        # Arrange
        mock_ingredient_repository.find_all.return_value = sample_ingredients
        use_case = IngredientListUseCase(mock_ingredient_repository)

        # Act
        result = use_case.execute()

        # Assert
        assert isinstance(result, IngredientListResponse)
        assert len(result.ingredients) == 3
        assert result.total_count == 3
        mock_ingredient_repository.find_all.assert_called_once()

    def test_list_ingredients_empty(self, mock_ingredient_repository):
        """Test ingredient listing when no ingredients exist"""
        # Arrange
        mock_ingredient_repository.find_all.return_value = []
        use_case = IngredientListUseCase(mock_ingredient_repository)

        # Act
        result = use_case.execute()

        # Assert
        assert isinstance(result, IngredientListResponse)
        assert len(result.ingredients) == 0
        assert result.total_count == 0


class TestIngredientListByTypeUseCase:
    """Test cases for IngredientListByTypeUseCase"""

    def test_list_ingredients_by_type_success(self, mock_ingredient_repository, sample_ingredients):
        """Test successful ingredient listing by type"""
        # Arrange
        mock_ingredient_repository.find_by_type.return_value = sample_ingredients
        use_case = IngredientListByTypeUseCase(mock_ingredient_repository)

        # Act
        result = use_case.execute(IngredientType.VEGETABLE)

        # Assert
        assert isinstance(result, IngredientListResponse)
        assert len(result.ingredients) == 3
        assert result.total_count == 3
        mock_ingredient_repository.find_by_type.assert_called_once_with(IngredientType.VEGETABLE)

    def test_list_ingredients_by_type_empty(self, mock_ingredient_repository):
        """Test ingredient listing by type when no ingredients exist"""
        # Arrange
        mock_ingredient_repository.find_by_type.return_value = []
        use_case = IngredientListByTypeUseCase(mock_ingredient_repository)

        # Act
        result = use_case.execute(IngredientType.VEGETABLE)

        # Assert
        assert isinstance(result, IngredientListResponse)
        assert len(result.ingredients) == 0
        assert result.total_count == 0


class TestIngredientListByAppliesToUseCase:
    """Test cases for IngredientListByAppliesToUseCase"""

    def test_list_ingredients_by_applies_to_success(self, mock_ingredient_repository, sample_ingredients):
        """Test successful ingredient listing by applies to"""
        # Arrange
        mock_ingredient_repository.find_by_applies_usage.return_value = sample_ingredients
        use_case = IngredientListByAppliesToUseCase(mock_ingredient_repository)

        # Act
        result = use_case.execute(
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
        )

        # Assert
        assert isinstance(result, IngredientListResponse)
        assert len(result.ingredients) == 3
        assert result.total_count == 3
        mock_ingredient_repository.find_by_applies_usage.assert_called_once_with(
            True, False, False, False
        )

    def test_list_ingredients_by_applies_to_empty(self, mock_ingredient_repository):
        """Test ingredient listing by applies to when no ingredients exist"""
        # Arrange
        mock_ingredient_repository.find_by_applies_usage.return_value = []
        use_case = IngredientListByAppliesToUseCase(mock_ingredient_repository)

        # Act
        result = use_case.execute(
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
        )

        # Assert
        assert isinstance(result, IngredientListResponse)
        assert len(result.ingredients) == 0
        assert result.total_count == 0
