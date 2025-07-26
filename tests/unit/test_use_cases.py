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
- ProductCreateUseCase
- ProductReadUseCase
- ProductUpdateUseCase
- ProductDeleteUseCase
- ProductListUseCase
- ProductGetActiveUseCase
- ProductReadBySkuUseCase
- ProductListByCategoryUseCase
- ProductListByActiveStatusUseCase
"""

import pytest

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
from src.application.use_cases.product_use_cases import (
    ProductCreateUseCase,
    ProductReadUseCase,
    ProductUpdateUseCase,
    ProductDeleteUseCase,
    ProductListUseCase,
    ProductGetActiveUseCase,
    ProductReadBySkuUseCase,
    ProductListByCategoryUseCase,
    ProductListByActiveStatusUseCase,
)
from src.application.dto import (
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerResponse,
    CustomerListResponse,
    IngredientCreateRequest,
    IngredientUpdateRequest,
    IngredientResponse,
    IngredientListResponse,
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductResponse,
    ProductListResponse,
)
from src.application.exceptions import (
    CustomerNotFoundException,
    CustomerAlreadyExistsException,
    CustomerBusinessRuleException,
    IngredientNotFoundException,
    IngredientAlreadyExistsException,
    ProductNotFoundException,
    ProductAlreadyExistsException,
    ProductBusinessRuleException,
    ProductValidationException,
)
from src.entities.customer import Customer
from src.entities.ingredient import IngredientType
from src.entities.product import ProductCategory, ProductReceiptItem
from src.entities.value_objects.sku import SKU
from src.entities.value_objects.money import Money
from decimal import Decimal
import uuid


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
        result = use_case.execute(sample_customer.id)

        # Assert
        assert isinstance(result, CustomerResponse)
        assert isinstance(result.id, str)
        uuid.UUID(result.id)
        assert result.id == str(sample_customer.id)
        assert result.first_name == "John"
        mock_customer_repository.find_by_id.assert_called_once_with(sample_customer.id)

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
            id=sample_customer.id,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725",  # Valid Brazilian CPF
        )

        # Act
        result = use_case.execute(request)

        # Assert
        assert isinstance(result, CustomerResponse)
        assert isinstance(result.id, str)
        uuid.UUID(result.id)
        assert result.id == str(sample_customer.id)
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
            customer_id=None  # UUID will be auto-generated
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
        result = use_case.execute(sample_customer.id)

        # Assert
        assert result is True
        mock_customer_repository.delete.assert_called_once_with(sample_customer.id)

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
        result = use_case.execute(sample_ingredient.id)

        # Assert
        assert isinstance(result, IngredientResponse)
        assert isinstance(result.id, str)
        uuid.UUID(result.id)
        assert result.name == "Tomato"
        mock_ingredient_repository.find_by_id.assert_called_once_with(sample_ingredient.id)

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
            id=sample_ingredient.id,
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
        assert isinstance(result.id, str)
        uuid.UUID(result.id)
        assert result.id == str(sample_ingredient.id)
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
        result = use_case.execute(sample_ingredient.id)

        # Assert
        assert result is True
        mock_ingredient_repository.delete.assert_called_once_with(sample_ingredient.id)

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
        result = use_case.execute(ProductCategory.BURGER)

        # Assert
        assert isinstance(result, IngredientListResponse)
        assert len(result.ingredients) == 3
        assert result.total_count == 3
        mock_ingredient_repository.find_by_applies_usage.assert_called_once_with(ProductCategory.BURGER)

    def test_list_ingredients_by_applies_to_empty(self, mock_ingredient_repository):
        """Test ingredient listing by applies to when no ingredients exist"""
        # Arrange
        mock_ingredient_repository.find_by_applies_usage.return_value = []
        use_case = IngredientListByAppliesToUseCase(mock_ingredient_repository)

        # Act
        result = use_case.execute(ProductCategory.BURGER)

        # Assert
        assert isinstance(result, IngredientListResponse)
        assert len(result.ingredients) == 0
        assert result.total_count == 0


class TestProductCreateUseCase:
    """Test cases for ProductCreateUseCase"""

    def test_create_product_success(self, mock_product_repository, sample_product):
        """Test successful product creation"""
        # Arrange
        mock_product_repository.save.return_value = sample_product
        use_case = ProductCreateUseCase(mock_product_repository)
        
        # Create test ingredient for the request
        ingredient = sample_product.default_ingredient[0].ingredient
        
        request = ProductCreateRequest(
            name="Classic Burger",
            price=12.99,
            category="burger",
            sku="BURG-2024-CLS",
            default_ingredient=[ProductReceiptItem(ingredient, 1)],
        )

        # Act
        result = use_case.execute(request)

        # Assert
        assert isinstance(result, ProductResponse)
        assert result.name == "Classic Burger"
        assert result.price == 12.99
        assert result.category == "burger"
        assert result.sku == "BURG-2024-CLS"
        mock_product_repository.save.assert_called_once()

    def test_create_product_sku_already_exists(self, mock_product_repository, sample_product):
        """Test product creation fails when SKU already exists"""
        # Arrange
        mock_product_repository.exists_by_sku.return_value = True
        use_case = ProductCreateUseCase(mock_product_repository)
        
        # Create test ingredient
        ingredient = sample_product.default_ingredient[0].ingredient
        
        request = ProductCreateRequest(
            name="Classic Burger",
            price=12.99,
            category="burger",
            sku="BURG-2024-CLS",
            default_ingredient=[ProductReceiptItem(ingredient, 1)],
        )

        # Act & Assert
        with pytest.raises(
            ProductAlreadyExistsException, match="SKU.*already exists"
        ):
            use_case.execute(request)


class TestProductReadUseCase:
    """Test cases for ProductReadUseCase"""

    def test_read_product_success(self, mock_product_repository, sample_product):
        """Test successful product retrieval"""
        # Arrange
        mock_product_repository.find_by_id.return_value = sample_product
        use_case = ProductReadUseCase(mock_product_repository)
        result = use_case.execute(sample_product.id)
        assert isinstance(result.id, str)
        uuid.UUID(result.id)
        assert result.name == sample_product.name.value
        mock_product_repository.find_by_id.assert_called_once_with(sample_product.id)

    def test_read_product_not_found(self, mock_product_repository):
        """Test product retrieval fails when product not found"""
        # Arrange
        mock_product_repository.find_by_id.return_value = None
        use_case = ProductReadUseCase(mock_product_repository)
        product_id = uuid.uuid4()

        # Act & Assert
        with pytest.raises(
            ProductNotFoundException, match="Product with ID.*not found"
        ):
            use_case.execute(product_id)


class TestProductUpdateUseCase:
    """Test cases for ProductUpdateUseCase"""

    def test_update_product_success(self, mock_product_repository, sample_product):
        """Test successful product update"""
        # Arrange
        mock_product_repository.find_by_id.return_value = sample_product
        mock_product_repository.save.return_value = sample_product
        use_case = ProductUpdateUseCase(mock_product_repository)
        
        # Create test ingredient
        ingredient = sample_product.default_ingredient[0].ingredient
        
        request = ProductUpdateRequest(
            id=str(sample_product.id),
            name="Updated Burger",
            price=15.99,
            category="burger",
            sku="BURG-2024-UPD",
            default_ingredient=[ProductReceiptItem(ingredient, 1)],
        )

        # Act
        result = use_case.execute(request)

        # Assert
        assert isinstance(result, ProductResponse)
        assert result.name == "Updated Burger"
        assert result.price == 15.99
        mock_product_repository.find_by_id.assert_called_once_with(sample_product.id)
        mock_product_repository.save.assert_called_once()

    def test_update_product_not_found(self, mock_product_repository):
        """Test product update fails when product not found"""
        # Arrange
        mock_product_repository.find_by_id.return_value = None
        use_case = ProductUpdateUseCase(mock_product_repository)
        
        # Use a valid UUID string
        valid_uuid = "550e8400-e29b-41d4-a716-446655440000"
        
        request = ProductUpdateRequest(
            id=valid_uuid,
            name="Updated Burger",
            price=15.99,
            category="burger",
            sku="BURG-2024-UPD",
            default_ingredient=[],
        )

        # Act & Assert
        with pytest.raises(
            ProductNotFoundException, match="Product with ID.*not found"
        ):
            use_case.execute(request)

    def test_update_product_sku_conflict(self, mock_product_repository, sample_product):
        """Test product update fails when SKU conflicts with existing product"""
        # Arrange
        mock_product_repository.find_by_id.return_value = sample_product
        mock_product_repository.exists_by_sku.return_value = True
        use_case = ProductUpdateUseCase(mock_product_repository)
        
        # Create test ingredient
        ingredient = sample_product.default_ingredient[0].ingredient
        
        request = ProductUpdateRequest(
            id=str(sample_product.id),
            name="Updated Burger",
            price=15.99,
            category="burger",
            sku="BURG-2024-CON",
            default_ingredient=[ProductReceiptItem(ingredient, 1)],
        )

        # Act & Assert
        with pytest.raises(
            ProductAlreadyExistsException, match="SKU.*already exists"
        ):
            use_case.execute(request)


class TestProductDeleteUseCase:
    """Test cases for ProductDeleteUseCase"""

    def test_delete_product_success(self, mock_product_repository, sample_product):
        """Test successful product deletion"""
        # Arrange
        mock_product_repository.find_by_id.return_value = sample_product
        mock_product_repository.delete.return_value = True
        use_case = ProductDeleteUseCase(mock_product_repository)
        product_id = uuid.uuid4()

        # Act
        result = use_case.execute(product_id)

        # Assert
        assert result is True
        mock_product_repository.find_by_id.assert_called_once_with(product_id)
        mock_product_repository.delete.assert_called_once_with(product_id)

    def test_delete_product_not_found(self, mock_product_repository):
        """Test product deletion fails when product not found"""
        # Arrange
        mock_product_repository.find_by_id.return_value = None
        use_case = ProductDeleteUseCase(mock_product_repository)
        product_id = uuid.uuid4()

        # Act & Assert
        with pytest.raises(
            ProductNotFoundException, match="Product with ID.*not found"
        ):
            use_case.execute(product_id)


class TestProductListUseCase:
    """Test cases for ProductListUseCase"""

    def test_list_products_success(self, mock_product_repository, sample_products):
        """Test successful product listing"""
        # Arrange
        mock_product_repository.find_all.return_value = sample_products
        use_case = ProductListUseCase(mock_product_repository)

        # Act
        result = use_case.execute()

        # Assert
        assert isinstance(result, ProductListResponse)
        assert len(result.products) == 4
        assert result.total_count == 4
        mock_product_repository.find_all.assert_called_once()

    def test_list_products_empty(self, mock_product_repository):
        """Test product listing returns empty list"""
        # Arrange
        mock_product_repository.find_all.return_value = []
        use_case = ProductListUseCase(mock_product_repository)

        # Act
        result = use_case.execute()

        # Assert
        assert isinstance(result, ProductListResponse)
        assert len(result.products) == 0
        assert result.total_count == 0


class TestProductGetActiveUseCase:
    """Test cases for ProductGetActiveUseCase"""

    def test_get_active_products_success(self, mock_product_repository, sample_products):
        """Test successful active products retrieval"""
        # Arrange
        mock_product_repository.find_all_active.return_value = sample_products
        use_case = ProductGetActiveUseCase(mock_product_repository)

        # Act
        result = use_case.execute()

        # Assert
        assert isinstance(result, ProductListResponse)
        assert len(result.products) == 4
        assert result.total_count == 4
        mock_product_repository.find_all_active.assert_called_once()

    def test_get_active_products_empty(self, mock_product_repository):
        """Test active products retrieval returns empty list"""
        # Arrange
        mock_product_repository.find_all_active.return_value = []
        use_case = ProductGetActiveUseCase(mock_product_repository)

        # Act
        result = use_case.execute()

        # Assert
        assert isinstance(result, ProductListResponse)
        assert len(result.products) == 0
        assert result.total_count == 0


class TestProductReadBySkuUseCase:
    """Test cases for ProductReadBySkuUseCase"""

    def test_read_product_by_sku_success(self, mock_product_repository, sample_product):
        """Test successful product retrieval by SKU"""
        # Arrange
        mock_product_repository.find_by_sku.return_value = sample_product
        use_case = ProductReadBySkuUseCase(mock_product_repository)
        result = use_case.execute(sample_product.sku.value)
        assert isinstance(result.id, str)
        uuid.UUID(result.id)
        assert result.sku == sample_product.sku.value
        mock_product_repository.find_by_sku.assert_called_once()

    def test_read_product_by_sku_not_found(self, mock_product_repository):
        """Test product retrieval by SKU fails when product not found"""
        # Arrange
        mock_product_repository.find_by_sku.return_value = None
        use_case = ProductReadBySkuUseCase(mock_product_repository)
        sku = "NON-2024-EXI"

        # Act & Assert
        with pytest.raises(
            ProductNotFoundException, match="Product with SKU.*not found"
        ):
            use_case.execute(sku)


class TestProductListByCategoryUseCase:
    """Test cases for ProductListByCategoryUseCase"""

    def test_list_products_by_category_success(self, mock_product_repository, sample_products):
        """Test successful product listing by category"""
        # Arrange
        mock_product_repository.find_all.return_value = sample_products
        use_case = ProductListByCategoryUseCase(mock_product_repository)
        category = "burger"

        # Act
        result = use_case.execute(category)

        # Assert
        assert isinstance(result, ProductListResponse)
        assert len(result.products) == 1
        assert result.total_count == 1
        assert all(p.category == "burger" for p in result.products)
        mock_product_repository.find_all.assert_called_once()

    def test_list_products_by_category_empty(self, mock_product_repository):
        """Test product listing by category returns empty list"""
        # Arrange
        mock_product_repository.find_all.return_value = []
        use_case = ProductListByCategoryUseCase(mock_product_repository)
        category = "non-existent-category"

        # Act & Assert
        with pytest.raises(ProductValidationException, match="Invalid category"):
            use_case.execute(category)


class TestProductListByActiveStatusUseCase:
    """Test cases for ProductListByActiveStatusUseCase"""

    def test_list_products_by_active_status_success(self, mock_product_repository, sample_products):
        """Test successful product listing by active status"""
        # Arrange
        mock_product_repository.find_all_active.return_value = sample_products
        use_case = ProductListByActiveStatusUseCase(mock_product_repository)
        is_active = True

        # Act
        result = use_case.execute(is_active)

        # Assert
        assert isinstance(result, ProductListResponse)
        assert len(result.products) == 4
        assert result.total_count == 4
        mock_product_repository.find_all_active.assert_called_once()

    def test_list_products_by_active_status_empty(self, mock_product_repository):
        """Test product listing by active status returns empty list"""
        # Arrange
        mock_product_repository.find_all.return_value = []
        use_case = ProductListByActiveStatusUseCase(mock_product_repository)
        is_active = False

        # Act
        result = use_case.execute(is_active)

        # Assert
        assert isinstance(result, ProductListResponse)
        assert len(result.products) == 0
        assert result.total_count == 0
