"""
Unit tests for order use cases.

Tests cover:
- OrderCreateUseCase
- OrderReadUseCase
- OrderListUseCase
- OrderUpdateUseCase
- OrderStatusUpdateUseCase
- OrderPaymentProcessUseCase
- OrderPaymentStatusUseCase
- OrderPaymentRequestUseCase
- OrderCancelUseCase
- OrderByStatusUseCase
"""

import pytest
from unittest.mock import Mock
from decimal import Decimal
from datetime import datetime

from src.application.use_cases.order_use_cases import (
    OrderCreateUseCase,
    OrderReadUseCase,
    OrderListUseCase,
    OrderUpdateUseCase,
    OrderStatusUpdateUseCase,
    OrderPaymentProcessUseCase,
    OrderPaymentStatusUseCase,
    OrderPaymentRequestUseCase,
    OrderCancelUseCase,
    OrderByStatusUseCase
)
from src.application.dto.implementation.order_dto import (
    OrderCreateRequest,
    OrderUpdateRequest,
    PaymentRequest,
    PaymentRequestDTO,
    OrderResponse,
    OrderListResponse,
    PaymentStatusResponse,
    PaymentRequestResponse,
    OrderItemRequest
)
from src.entities.order import Order, OrderItem
from src.entities.customer import Customer
from src.entities.product import Product, ProductCategory, ProductReceiptItem
from src.entities.ingredient import Ingredient, IngredientType
from src.entities.value_objects.money import Money
from src.entities.value_objects.sku import SKU


class TestOrderCreateUseCase:
    """Test cases for OrderCreateUseCase"""

    @pytest.fixture
    def mock_repositories(self):
        """Mock repositories"""
        order_repo = Mock()
        product_repo = Mock()
        ingredient_repo = Mock()
        customer_repo = Mock()
        
        return order_repo, product_repo, ingredient_repo, customer_repo

    @pytest.fixture
    def sample_customer(self):
        """Sample customer for testing"""
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725"
        )
        customer.internal_id = 1
        return customer

    @pytest.fixture
    def sample_product(self):
        """Sample product for testing"""
        ingredient = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Test Burger",
            price=Money(amount=Decimal("10.00")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-TST"),
            default_ingredient=[ProductReceiptItem(ingredient, 1)],
            is_active=True
        )
        product.internal_id = 1
        return product

    @pytest.fixture
    def sample_ingredient(self):
        """Sample ingredient for testing"""
        ingredient = Ingredient.create(
            name="Cheese",
            price=Money(amount=Decimal("1.50")),
            is_active=True,
            type=IngredientType.CHEESE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        ingredient.internal_id = 1
        return ingredient

    def test_create_order_success(self, mock_repositories, sample_customer, sample_product):
        """Test successful order creation"""
        order_repo, product_repo, ingredient_repo, customer_repo = mock_repositories
        
        # Setup mocks
        customer_repo.find_by_id.return_value = sample_customer
        product_repo.find_by_id.return_value = sample_product
        ingredient_repo.find_by_id.return_value = None  # No additional ingredients
        
        # Mock order creation
        created_order = Order.create(
            customer_internal_id=sample_customer.internal_id,
            order_items=[OrderItem(
                order_internal_id=0,
                product=sample_product,
                additional_ingredient=[],
                remove_ingredient=[]
            )]
        )
        created_order.internal_id = 1
        order_repo.create.return_value = created_order
        
        use_case = OrderCreateUseCase(order_repo, product_repo, ingredient_repo, customer_repo)
        
        request = OrderCreateRequest(
            customer_internal_id=1,
            order_items=[
                OrderItemRequest(
                    product_internal_id=1,
                    additional_ingredient_internal_ids=[],
                    remove_ingredient_internal_ids=[]
                )
            ]
        )
        
        result = use_case.execute(request)
        
        assert isinstance(result, OrderResponse)
        assert result.customer_internal_id == 1
        customer_repo.find_by_id.assert_called_once_with(1)
        product_repo.find_by_id.assert_called_once_with(1, include_inactive=False)
        order_repo.create.assert_called_once()

    def test_create_order_customer_not_found(self, mock_repositories):
        """Test order creation fails when customer not found"""
        order_repo, product_repo, ingredient_repo, customer_repo = mock_repositories
        
        customer_repo.find_by_id.return_value = None
        
        use_case = OrderCreateUseCase(order_repo, product_repo, ingredient_repo, customer_repo)
        
        request = OrderCreateRequest(
            customer_internal_id=999,
            order_items=[]
        )
        
        with pytest.raises(ValueError, match="Customer with ID 999 not found"):
            use_case.execute(request)

    def test_create_order_customer_cannot_place_order(self, mock_repositories, sample_customer):
        """Test order creation fails when customer cannot place orders"""
        order_repo, product_repo, ingredient_repo, customer_repo = mock_repositories
        
        # Mock customer that cannot place orders (inactive)
        sample_customer.is_active = False
        customer_repo.find_by_id.return_value = sample_customer
        
        use_case = OrderCreateUseCase(order_repo, product_repo, ingredient_repo, customer_repo)
        
        request = OrderCreateRequest(
            customer_internal_id=1,
            order_items=[]
        )
        
        with pytest.raises(ValueError, match="Customer does not meet requirements to place orders"):
            use_case.execute(request)

    def test_create_order_product_not_found(self, mock_repositories, sample_customer):
        """Test order creation fails when product not found"""
        order_repo, product_repo, ingredient_repo, customer_repo = mock_repositories
        
        customer_repo.find_by_id.return_value = sample_customer
        product_repo.find_by_id.return_value = None
        
        use_case = OrderCreateUseCase(order_repo, product_repo, ingredient_repo, customer_repo)
        
        request = OrderCreateRequest(
            customer_internal_id=1,
            order_items=[
                OrderItemRequest(
                    product_internal_id=999,
                    additional_ingredient_internal_ids=[],
                    remove_ingredient_internal_ids=[]
                )
            ]
        )
        
        with pytest.raises(ValueError, match="Product with ID 999 not found or is deactivated"):
            use_case.execute(request)

    def test_create_order_inactive_product(self, mock_repositories, sample_customer, sample_product):
        """Test order creation fails when product is inactive"""
        order_repo, product_repo, ingredient_repo, customer_repo = mock_repositories
        
        customer_repo.find_by_id.return_value = sample_customer
        sample_product.is_active = False
        product_repo.find_by_id.return_value = sample_product
        
        use_case = OrderCreateUseCase(order_repo, product_repo, ingredient_repo, customer_repo)
        
        request = OrderCreateRequest(
            customer_internal_id=1,
            order_items=[
                OrderItemRequest(
                    product_internal_id=1,
                    additional_ingredient_internal_ids=[],
                    remove_ingredient_internal_ids=[]
                )
            ]
        )
        
        with pytest.raises(ValueError, match="Product with ID 1 is deactivated and cannot be added to new orders"):
            use_case.execute(request)


class TestOrderReadUseCase:
    """Test cases for OrderReadUseCase"""

    @pytest.fixture
    def mock_order_repository(self):
        """Mock order repository"""
        return Mock()

    def test_read_order_success(self, mock_order_repository):
        """Test successful order read"""
        # Create a sample order with at least one item
        ingredient = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Test Burger",
            price=Money(amount=Decimal("10.00")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-TST"),
            default_ingredient=[ProductReceiptItem(ingredient, 1)],
            is_active=True
        )
        
        order = Order.create(
            customer_internal_id=1,
            order_items=[OrderItem(
                order_internal_id=0,
                product=product,
                additional_ingredient=[],
                remove_ingredient=[]
            )]
        )
        order.internal_id = 1
        
        mock_order_repository.get_by_id.return_value = order
        
        use_case = OrderReadUseCase(mock_order_repository)
        
        result = use_case.execute(1)
        
        assert isinstance(result, OrderResponse)
        assert result.customer_internal_id == 1
        mock_order_repository.get_by_id.assert_called_once_with(1)

    def test_read_order_not_found(self, mock_order_repository):
        """Test order read when order not found"""
        mock_order_repository.get_by_id.return_value = None
        
        use_case = OrderReadUseCase(mock_order_repository)
        
        result = use_case.execute(999)
        
        assert result is None


class TestOrderListUseCase:
    """Test cases for OrderListUseCase"""

    @pytest.fixture
    def mock_order_repository(self):
        """Mock order repository"""
        return Mock()

    def test_list_orders_success(self, mock_order_repository):
        """Test successful order listing"""
        # Create sample orders with at least one item each
        ingredient = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Test Burger",
            price=Money(amount=Decimal("10.00")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-TST"),
            default_ingredient=[ProductReceiptItem(ingredient, 1)],
            is_active=True
        )
        
        orders = [
            Order.create(
                customer_internal_id=1,
                order_items=[OrderItem(
                    order_internal_id=0,
                    product=product,
                    additional_ingredient=[],
                    remove_ingredient=[]
                )]
            ),
            Order.create(
                customer_internal_id=2,
                order_items=[OrderItem(
                    order_internal_id=0,
                    product=product,
                    additional_ingredient=[],
                    remove_ingredient=[]
                )]
            )
        ]
        
        mock_order_repository.list_all.return_value = orders
        
        use_case = OrderListUseCase(mock_order_repository)
        
        result = use_case.execute(skip=0, limit=10)
        
        assert isinstance(result, OrderListResponse)
        assert len(result.orders) == 2
        mock_order_repository.list_all.assert_called_once_with(skip=0, limit=10)


class TestOrderUpdateUseCase:
    """Test cases for OrderUpdateUseCase"""

    @pytest.fixture
    def mock_order_repository(self):
        """Mock order repository"""
        return Mock()

    def test_update_order_success(self, mock_order_repository):
        """Test successful order update"""
        # Create a sample order with at least one item
        ingredient = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Test Burger",
            price=Money(amount=Decimal("10.00")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-TST"),
            default_ingredient=[ProductReceiptItem(ingredient, 1)],
            is_active=True
        )
        
        order = Order.create(
            customer_internal_id=1,
            order_items=[OrderItem(
                order_internal_id=0,
                product=product,
                additional_ingredient=[],
                remove_ingredient=[]
            )]
        )
        order.internal_id = 1
        
        mock_order_repository.get_by_id.return_value = order
        mock_order_repository.update.return_value = order
        
        use_case = OrderUpdateUseCase(mock_order_repository)
        
        request = OrderUpdateRequest(status="EM_PREPARACAO")
        
        result = use_case.execute(1, request)
        
        assert isinstance(result, OrderResponse)
        mock_order_repository.get_by_id.assert_called_once_with(1)
        mock_order_repository.update.assert_called_once()

    def test_update_order_not_found(self, mock_order_repository):
        """Test order update when order not found"""
        mock_order_repository.get_by_id.return_value = None
        
        use_case = OrderUpdateUseCase(mock_order_repository)
        
        request = OrderUpdateRequest(status="EM_PREPARACAO")
        
        result = use_case.execute(999, request)
        
        assert result is None


class TestOrderStatusUpdateUseCase:
    """Test cases for OrderStatusUpdateUseCase"""

    @pytest.fixture
    def mock_order_repository(self):
        """Mock order repository"""
        return Mock()

    def test_update_order_status_success(self, mock_order_repository):
        """Test successful order status update"""
        # Create a sample order with at least one item
        ingredient = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Test Burger",
            price=Money(amount=Decimal("10.00")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-TST"),
            default_ingredient=[ProductReceiptItem(ingredient, 1)],
            is_active=True
        )
        
        order = Order.create(
            customer_internal_id=1,
            order_items=[OrderItem(
                order_internal_id=0,
                product=product,
                additional_ingredient=[],
                remove_ingredient=[]
            )]
        )
        order.internal_id = 1
        
        mock_order_repository.update_status.return_value = order
        
        use_case = OrderStatusUpdateUseCase(mock_order_repository)
        
        result = use_case.execute(1, "EM_PREPARACAO")
        
        assert isinstance(result, OrderResponse)
        mock_order_repository.update_status.assert_called_once_with(1, "EM_PREPARACAO")

    def test_update_order_status_not_found(self, mock_order_repository):
        """Test order status update when order not found"""
        mock_order_repository.update_status.return_value = None
        
        use_case = OrderStatusUpdateUseCase(mock_order_repository)
        
        result = use_case.execute(999, "EM_PREPARACAO")
        
        assert result is None


class TestOrderPaymentProcessUseCase:
    """Test cases for OrderPaymentProcessUseCase"""

    @pytest.fixture
    def mock_order_repository(self):
        """Mock order repository"""
        return Mock()

    def test_process_payment_success(self, mock_order_repository):
        """Test successful payment processing"""
        # Create a sample order with at least one item
        ingredient = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Test Burger",
            price=Money(amount=Decimal("10.00")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-TST"),
            default_ingredient=[ProductReceiptItem(ingredient, 1)],
            is_active=True
        )
        
        order = Order.create(
            customer_internal_id=1,
            order_items=[OrderItem(
                order_internal_id=0,
                product=product,
                additional_ingredient=[],
                remove_ingredient=[]
            )]
        )
        order.internal_id = 1
        
        mock_order_repository.process_payment.return_value = order
        
        use_case = OrderPaymentProcessUseCase(mock_order_repository)
        
        payment_request = PaymentRequest(
            transaction_id="TXN123",
            approval_status=True,
            date=datetime.now(),
            message="Payment approved"
        )
        
        result = use_case.execute(1, payment_request)
        
        assert isinstance(result, OrderResponse)
        mock_order_repository.process_payment.assert_called_once()

    def test_process_payment_not_found(self, mock_order_repository):
        """Test payment processing when order not found"""
        mock_order_repository.process_payment.return_value = None
        
        use_case = OrderPaymentProcessUseCase(mock_order_repository)
        
        payment_request = PaymentRequest(
            transaction_id="TXN123",
            approval_status=True,
            date=datetime.now(),
            message="Payment approved"
        )
        
        result = use_case.execute(999, payment_request)
        
        assert result is None


class TestOrderPaymentStatusUseCase:
    """Test cases for OrderPaymentStatusUseCase"""

    @pytest.fixture
    def mock_order_repository(self):
        """Mock order repository"""
        return Mock()

    def test_get_payment_status_success(self, mock_order_repository):
        """Test successful payment status retrieval"""
        # Create a sample order with at least one item
        ingredient = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Test Burger",
            price=Money(amount=Decimal("10.00")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-TST"),
            default_ingredient=[ProductReceiptItem(ingredient, 1)],
            is_active=True
        )
        
        order = Order.create(
            customer_internal_id=1,
            order_items=[OrderItem(
                order_internal_id=0,
                product=product,
                additional_ingredient=[],
                remove_ingredient=[]
            )]
        )
        order.internal_id = 1
        
        mock_order_repository.get_by_id.return_value = order
        
        use_case = OrderPaymentStatusUseCase(mock_order_repository)
        
        result = use_case.execute(1)
        
        assert isinstance(result, PaymentStatusResponse)
        mock_order_repository.get_by_id.assert_called_once_with(1)

    def test_get_payment_status_not_found(self, mock_order_repository):
        """Test payment status retrieval when order not found"""
        mock_order_repository.get_by_id.return_value = None
        
        use_case = OrderPaymentStatusUseCase(mock_order_repository)
        
        result = use_case.execute(999)
        
        assert result is None


class TestOrderPaymentRequestUseCase:
    """Test cases for OrderPaymentRequestUseCase"""

    @pytest.fixture
    def mock_order_repository(self):
        """Mock order repository"""
        return Mock()

    @pytest.fixture
    def mock_qr_payment_repository(self):
        """Mock QR payment repository"""
        return Mock()

    def test_request_payment_success(self, mock_order_repository, mock_qr_payment_repository):
        """Test successful payment request"""
        # Create a sample order with at least one item
        ingredient = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Test Burger",
            price=Money(amount=Decimal("10.00")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-TST"),
            default_ingredient=[ProductReceiptItem(ingredient, 1)],
            is_active=True
        )
        
        order = Order.create(
            customer_internal_id=1,
            order_items=[OrderItem(
                order_internal_id=0,
                product=product,
                additional_ingredient=[],
                remove_ingredient=[]
            )]
        )
        order.internal_id = 1
        
        mock_order_repository.get_by_id.return_value = order
        mock_qr_payment_repository.request_payment.return_value = Mock(
            status_code=200,
            content=b'{"status": "success"}'
        )
        
        use_case = OrderPaymentRequestUseCase(mock_order_repository, mock_qr_payment_repository)
        
        payment_request = PaymentRequestDTO(order_internal_id=1)
        
        result = use_case.execute(1, payment_request)
        
        assert isinstance(result, PaymentRequestResponse)
        assert result.order_id == 1
        mock_order_repository.get_by_id.assert_called_once_with(1)
        mock_qr_payment_repository.request_payment.assert_called_once()

    def test_request_payment_order_not_found(self, mock_order_repository, mock_qr_payment_repository):
        """Test payment request when order not found"""
        mock_order_repository.get_by_id.return_value = None
        
        use_case = OrderPaymentRequestUseCase(mock_order_repository, mock_qr_payment_repository)
        
        payment_request = PaymentRequestDTO(order_internal_id=999)
        
        with pytest.raises(ValueError, match="Order with ID 999 not found"):
            use_case.execute(999, payment_request)

    def test_request_payment_already_paid(self, mock_order_repository, mock_qr_payment_repository):
        """Test payment request when order already paid"""
        # Create a sample order with at least one item
        ingredient = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Test Burger",
            price=Money(amount=Decimal("10.00")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-TST"),
            default_ingredient=[ProductReceiptItem(ingredient, 1)],
            is_active=True
        )
        
        order = Order.create(
            customer_internal_id=1,
            order_items=[OrderItem(
                order_internal_id=0,
                product=product,
                additional_ingredient=[],
                remove_ingredient=[]
            )]
        )
        order.internal_id = 1
        order.has_payment_verified = True  # Already paid
        
        mock_order_repository.get_by_id.return_value = order
        
        use_case = OrderPaymentRequestUseCase(mock_order_repository, mock_qr_payment_repository)
        
        payment_request = PaymentRequestDTO(order_internal_id=1)
        
        with pytest.raises(ValueError, match="Order has already been paid"):
            use_case.execute(1, payment_request)


class TestOrderCancelUseCase:
    """Test cases for OrderCancelUseCase"""

    @pytest.fixture
    def mock_order_repository(self):
        """Mock order repository"""
        return Mock()

    def test_cancel_order_success(self, mock_order_repository):
        """Test successful order cancellation"""
        mock_order_repository.cancel.return_value = True
        
        use_case = OrderCancelUseCase(mock_order_repository)
        
        result = use_case.execute(1)
        
        assert result is True
        mock_order_repository.cancel.assert_called_once_with(1)

    def test_cancel_order_failure(self, mock_order_repository):
        """Test order cancellation failure"""
        mock_order_repository.cancel.return_value = False
        
        use_case = OrderCancelUseCase(mock_order_repository)
        
        result = use_case.execute(1)
        
        assert result is False


class TestOrderByStatusUseCase:
    """Test cases for OrderByStatusUseCase"""

    @pytest.fixture
    def mock_order_repository(self):
        """Mock order repository"""
        return Mock()

    def test_get_orders_by_status_success(self, mock_order_repository):
        """Test successful order retrieval by status"""
        # Create sample orders with at least one item each
        ingredient = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Test Burger",
            price=Money(amount=Decimal("10.00")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-TST"),
            default_ingredient=[ProductReceiptItem(ingredient, 1)],
            is_active=True
        )
        
        orders = [
            Order.create(
                customer_internal_id=1,
                order_items=[OrderItem(
                    order_internal_id=0,
                    product=product,
                    additional_ingredient=[],
                    remove_ingredient=[]
                )]
            ),
            Order.create(
                customer_internal_id=2,
                order_items=[OrderItem(
                    order_internal_id=0,
                    product=product,
                    additional_ingredient=[],
                    remove_ingredient=[]
                )]
            )
        ]
        
        mock_order_repository.get_by_status.return_value = orders
        
        use_case = OrderByStatusUseCase(mock_order_repository)
        
        result = use_case.execute("RECEBIDO")
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(order, OrderResponse) for order in result)
        mock_order_repository.get_by_status.assert_called_once_with("RECEBIDO")

    def test_get_orders_by_status_empty(self, mock_order_repository):
        """Test order retrieval by status when no orders found"""
        mock_order_repository.get_by_status.return_value = []
        
        use_case = OrderByStatusUseCase(mock_order_repository)
        
        result = use_case.execute("FINALIZADO")
        
        assert isinstance(result, list)
        assert len(result) == 0 