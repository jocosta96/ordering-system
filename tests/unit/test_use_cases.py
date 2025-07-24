"""
Unit tests for use cases.

Tests cover:
- CustomerCreateUseCase
- CustomerReadUseCase
- CustomerUpdateUseCase
- CustomerDeleteUseCase
- CustomerListUseCase
- CustomerGetAnonymousUseCase
"""

import pytest
from unittest.mock import Mock

from src.application.use_cases.customer_use_cases import (
    CustomerCreateUseCase,
    CustomerReadUseCase,
    CustomerUpdateUseCase,
    CustomerDeleteUseCase,
    CustomerListUseCase,
    CustomerGetAnonymousUseCase,
)
from src.application.dto.customer_dto import (
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerResponse,
    CustomerListResponse,
)
from src.application.exceptions import (
    CustomerNotFoundException,
    CustomerAlreadyExistsException,
    CustomerBusinessRuleException,
)
from src.entities.customer import Customer


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
        """Test successful customer read"""
        # Arrange
        mock_customer_repository.find_by_id.return_value = sample_customer
        use_case = CustomerReadUseCase(mock_customer_repository)

        # Act
        result = use_case.execute(1)

        # Assert
        assert isinstance(result, CustomerResponse)
        assert result.id == 1
        mock_customer_repository.find_by_id.assert_called_once_with(1)

    def test_read_customer_not_found(self, mock_customer_repository):
        """Test customer read fails when customer not found"""
        # Arrange
        mock_customer_repository.find_by_id.return_value = None
        use_case = CustomerReadUseCase(mock_customer_repository)

        # Act & Assert
        with pytest.raises(
            CustomerNotFoundException, match="Customer with ID 1 not found"
        ):
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
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            document="12345678909",  # Valid Brazilian CPF
        )

        # Act
        result = use_case.execute(request)

        # Assert
        assert isinstance(result, CustomerResponse)
        mock_customer_repository.find_by_id.assert_called_once_with(1)
        mock_customer_repository.save.assert_called_once()

    def test_update_customer_not_found(self, mock_customer_repository):
        """Test customer update fails when customer not found"""
        # Arrange
        mock_customer_repository.find_by_id.return_value = None
        use_case = CustomerUpdateUseCase(mock_customer_repository)
        request = CustomerUpdateRequest(
            id=1,
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            document="12345678909",  # Valid Brazilian CPF
        )

        # Act & Assert
        with pytest.raises(
            CustomerNotFoundException, match="Customer with ID 1 not found"
        ):
            use_case.execute(request)

    def test_update_customer_document_conflict(
        self, mock_customer_repository, sample_customer
    ):
        """Test customer update fails when document conflicts"""
        # Arrange
        conflicting_customer = Customer.create_registered(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            document="52998224725",  # Valid Brazilian CPF
            customer_id=2,
        )
        mock_customer_repository.find_by_id.return_value = sample_customer
        mock_customer_repository.find_by_document.return_value = conflicting_customer
        use_case = CustomerUpdateUseCase(mock_customer_repository)
        request = CustomerUpdateRequest(
            id=1,
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            document="52998224725",  # Valid Brazilian CPF
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
        mock_customer_repository.find_by_id.assert_called_once_with(1)
        mock_customer_repository.delete.assert_called_once_with(1)

    def test_delete_customer_not_found(self, mock_customer_repository):
        """Test customer deletion fails when customer not found"""
        # Arrange
        mock_customer_repository.find_by_id.return_value = None
        use_case = CustomerDeleteUseCase(mock_customer_repository)

        # Act & Assert
        with pytest.raises(
            CustomerNotFoundException, match="Customer with ID 1 not found"
        ):
            use_case.execute(1)

    def test_delete_anonymous_customer_fails(
        self, mock_customer_repository, sample_anonymous_customer
    ):
        """Test that deleting anonymous customer fails"""
        # Arrange
        mock_customer_repository.find_by_id.return_value = sample_anonymous_customer
        use_case = CustomerDeleteUseCase(mock_customer_repository)

        # Act & Assert
        with pytest.raises(
            CustomerBusinessRuleException, match="Cannot delete anonymous customer"
        ):
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
        mock_customer_repository.get_anonymous_customer.return_value = (
            sample_anonymous_customer
        )
        use_case = CustomerGetAnonymousUseCase(mock_customer_repository)

        # Act
        result = use_case.execute()

        # Assert
        assert isinstance(result, CustomerResponse)
        assert result.is_anonymous is True
        mock_customer_repository.get_anonymous_customer.assert_called_once()
