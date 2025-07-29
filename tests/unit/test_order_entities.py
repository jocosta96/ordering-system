"""
Unit tests for Order and OrderItem entities.

Tests cover:
- Order and OrderItem creation and validation
- Business rules
- Factory methods
- Properties and methods
- DTO conversions
"""

import pytest
from decimal import Decimal
from datetime import datetime
from src.entities.order import Order, OrderItem
from src.entities.customer import Customer
from src.entities.ingredient import Ingredient, IngredientType
from src.entities.product import Product, ProductCategory, ProductReceiptItem
from src.entities.value_objects.money import Money
from src.entities.value_objects.sku import SKU
from src.entities.value_objects.order_status import OrderStatusType
from src.application.dto.implementation.order_dto import OrderResponse, OrderItemResponse


def create_test_product(name="Test Burger", price=Decimal("10.00"), sku="BURG-2024-TST"):
    """Helper function to create a test product with default ingredients"""
    # Create test ingredient
    bread = Ingredient.create(
        name="Burger Bun",
        price=Money(amount=Decimal("2.00")),
        is_active=True,
        type=IngredientType.BREAD,
        applies_to_burger=True,
        applies_to_side=False,
        applies_to_drink=False,
        applies_to_dessert=False
    )
    
    return Product.create(
        name=name,
        price=Money(amount=price),
        category=ProductCategory.BURGER,
        sku=SKU.create(sku),
        default_ingredient=[ProductReceiptItem(bread, 1)],
        is_active=True
    )


class TestOrderItemEntity:
    """Test cases for OrderItem entity"""

    def test_create_order_item_with_id(self):
        """Test creating an order item with ID"""
        # Create test product
        bread = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        meat = Ingredient.create(
            name="Beef Patty",
            price=Money(amount=Decimal("8.00")),
            is_active=True,
            type=IngredientType.MEAT,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Classic Burger",
            price=Money(amount=Decimal("12.99")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-CLS"),
            default_ingredient=[
                ProductReceiptItem(bread, 1),
                ProductReceiptItem(meat, 1)
            ],
            is_active=True
        )
        
        order_id = 0
        item_id = 0
        
        order_item = OrderItem(
            order_internal_id=0,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[],
            internal_id=item_id
        )
        
        assert order_item.internal_id == item_id
        assert order_item.order_internal_id == order_id
        assert order_item.product == product
        assert len(order_item.additional_ingredient) == 0
        assert len(order_item.remove_ingredient) == 0
        assert order_item.price.amount == Decimal("12.99")  # Base product price

    def test_create_order_item_without_id(self):
        """Test creating an order item without ID (auto-generated)"""
        # Create test product
        cheese = Ingredient.create(
            name="Cheddar Cheese",
            price=Money(amount=Decimal("1.50")),
            is_active=True,
            type=IngredientType.CHEESE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Cheese Burger",
            price=Money(amount=Decimal("14.49")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-CHS"),
            default_ingredient=[ProductReceiptItem(cheese, 1)],
            is_active=True
        )
        
        order_id = 0
        
        order_item = OrderItem(
            order_internal_id=0,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        assert order_item.internal_id is None  # New entity
        # UUID assertion removed - using internal_id now
        assert order_item.order_internal_id == order_id
        assert order_item.product == product
        assert order_item.price.amount == Decimal("14.49")

    def test_order_item_with_additional_ingredients(self):
        """Test order item with additional ingredients"""
        # Create test ingredients
        bread = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        meat = Ingredient.create(
            name="Beef Patty",
            price=Money(amount=Decimal("8.00")),
            is_active=True,
            type=IngredientType.MEAT,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        cheese = Ingredient.create(
            name="Cheddar Cheese",
            price=Money(amount=Decimal("1.50")),
            is_active=True,
            type=IngredientType.CHEESE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        bacon = Ingredient.create(
            name="Bacon",
            price=Money(amount=Decimal("2.50")),
            is_active=True,
            type=IngredientType.MEAT,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Classic Burger",
            price=Money(amount=Decimal("12.99")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-CLS"),
            default_ingredient=[
                ProductReceiptItem(bread, 1),
                ProductReceiptItem(meat, 1)
            ],
            is_active=True
        )
        
        order_item = OrderItem(
            order_internal_id=0,
            product=product,
            additional_ingredient=[cheese, bacon],
            remove_ingredient=[]
        )
        
        assert len(order_item.additional_ingredient) == 2
        assert cheese in order_item.additional_ingredient
        assert bacon in order_item.additional_ingredient
        # Price should be base product price + additional ingredients
        expected_price = Decimal("12.99") + Decimal("1.50") + Decimal("2.50")
        assert order_item.price.amount == expected_price

    def test_order_item_with_removed_ingredients(self):
        """Test order item with removed ingredients"""
        # Create test ingredients
        bread = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        meat = Ingredient.create(
            name="Beef Patty",
            price=Money(amount=Decimal("8.00")),
            is_active=True,
            type=IngredientType.MEAT,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        cheese = Ingredient.create(
            name="Cheddar Cheese",
            price=Money(amount=Decimal("1.50")),
            is_active=True,
            type=IngredientType.CHEESE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Classic Burger",
            price=Money(amount=Decimal("12.99")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-CLS"),
            default_ingredient=[
                ProductReceiptItem(bread, 1),
                ProductReceiptItem(meat, 1),
                ProductReceiptItem(cheese, 1)
            ],
            is_active=True
        )
        
        order_item = OrderItem(
            order_internal_id=0,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[cheese]
        )
        
        assert len(order_item.remove_ingredient) == 1
        assert cheese in order_item.remove_ingredient
        
        # Check that cheese is not in the final receipt
        receipt = order_item.get_item_receipt()
        cheese_in_receipt = any(item.ingredient == cheese for item in receipt)
        assert not cheese_in_receipt

    def test_order_item_receipt_generation(self):
        """Test order item receipt generation"""
        # Create test ingredients
        bread = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
            internal_id=1
        )
        
        meat = Ingredient.create(
            name="Beef Patty",
            price=Money(amount=Decimal("8.00")),
            is_active=True,
            type=IngredientType.MEAT,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
            internal_id=2
        )
        
        cheese = Ingredient.create(
            name="Cheddar Cheese",
            price=Money(amount=Decimal("1.50")),
            is_active=True,
            type=IngredientType.CHEESE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False,
            internal_id=3
        )
        
        product = Product.create(
            name="Classic Burger",
            price=Money(amount=Decimal("12.99")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-CLS"),
            default_ingredient=[
                ProductReceiptItem(bread, 1),
                ProductReceiptItem(meat, 1),
                ProductReceiptItem(cheese, 2)  # Double cheese
            ],
            is_active=True
        )
        
        order_item = OrderItem(
            order_internal_id=0,
            product=product,
            additional_ingredient=[cheese],  # Add one more cheese
            remove_ingredient=[]
        )
        
        receipt = order_item.get_item_receipt()
        
        # Should have 3 cheeses total (2 default + 1 additional)
        cheese_items = [item for item in receipt if item.ingredient == cheese]
        assert len(cheese_items) == 1
        assert cheese_items[0].quantity == 3

    def test_order_item_string_representation(self):
        """Test order item string representation"""
        # Create test product
        product = create_test_product()
        
        item_id = 0
        
        order_item = OrderItem(
            order_internal_id=0,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[],
            internal_id=item_id
        )
        
        expected = f"OrderItem(internal_id={item_id}, product={product.name}, price={order_item.price})"
        assert str(order_item) == expected

    def test_order_item_repr_representation(self):
        """Test order item repr representation"""
        # Create test product
        product = create_test_product()
        
        item_id = 0
        
        order_item = OrderItem(
            order_internal_id=0,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[],
            internal_id=item_id
        )
        
        expected = f"OrderItem(internal_id={item_id}, product={product.name}, price={order_item.price})"
        assert repr(order_item) == expected


class TestOrderEntity:
    """Test cases for Order entity"""

    def test_create_order_with_id(self):
        """Test creating an order with ID"""
        # Create test customer
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725"
        )
        customer.internal_id = 1  # Set for testing
        
        # Create test order item
        bread = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        meat = Ingredient.create(
            name="Beef Patty",
            price=Money(amount=Decimal("8.00")),
            is_active=True,
            type=IngredientType.MEAT,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Classic Burger",
            price=Money(amount=Decimal("12.99")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-CLS"),
            default_ingredient=[
                ProductReceiptItem(bread, 1),
                ProductReceiptItem(meat, 1)
            ],
            is_active=True
        )
        
        order_id = 0
        
        order_item = OrderItem(
            order_internal_id=0,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        order = Order.create(
            customer_internal_id=customer.internal_id,
            order_items=[order_item],
            internal_id=0
        )
        
        assert order.internal_id == order_id
        assert order.customer_internal_id == customer.internal_id
        assert len(order.order_items) == 1
        assert order.order_items[0] == order_item
        assert order.status.status == OrderStatusType.RECEBIDO
        assert order.value.amount == Decimal("12.99")
        assert order.has_payment_verified is False

    def test_create_order_without_id(self):
        """Test creating an order without ID (auto-generated)"""
        # Create test customer
        customer = Customer.create_registered(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            document="98765432100"
        )
        customer.internal_id = 1  # Set for testing
        
        # Create test order item
        cheese = Ingredient.create(
            name="Cheddar Cheese",
            price=Money(amount=Decimal("1.50")),
            is_active=True,
            type=IngredientType.CHEESE,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        product = Product.create(
            name="Cheese Burger",
            price=Money(amount=Decimal("14.49")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-CHS"),
            default_ingredient=[ProductReceiptItem(cheese, 1)],
            is_active=True
        )
        
        order_item = OrderItem(
            order_internal_id=1,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        order = Order.create(
            customer_internal_id=customer.internal_id,
            order_items=[order_item]
        )
        
        assert order.internal_id is None  # New entity
        # UUID assertion removed - using internal_id now
        assert order.customer_internal_id == customer.internal_id
        assert len(order.order_items) == 1
        assert order.value.amount == Decimal("14.49")

    def test_create_order_with_multiple_items(self):
        """Test creating an order with multiple items"""
        # Create test customer
        customer = Customer.create_registered(
            first_name="Bob",
            last_name="Johnson",
            email="bob.johnson@example.com",
            document="52998224725"  # Valid Brazilian CPF
        )
        customer.internal_id = 1  # Set for testing
        
        # Create test products
        bread = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        meat = Ingredient.create(
            name="Beef Patty",
            price=Money(amount=Decimal("8.00")),
            is_active=True,
            type=IngredientType.MEAT,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        burger_product = Product.create(
            name="Classic Burger",
            price=Money(amount=Decimal("12.99")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-CLS"),
            default_ingredient=[
                ProductReceiptItem(bread, 1),
                ProductReceiptItem(meat, 1)
            ],
            is_active=True
        )
        
        milk = Ingredient.create(
            name="Whole Milk",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.MILK,
            applies_to_burger=False,
            applies_to_side=False,
            applies_to_drink=True,
            applies_to_dessert=False
        )
        
        drink_product = Product.create(
            name="Milk Shake",
            price=Money(amount=Decimal("4.99")),
            category=ProductCategory.DRINK,
            sku=SKU.create("DRNK-2024-MLK"),
            default_ingredient=[ProductReceiptItem(milk, 1)],
            is_active=True
        )
        
        order_item1 = OrderItem(
            order_internal_id=1,
            product=burger_product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        order_item2 = OrderItem(
            order_internal_id=1,
            product=drink_product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        order = Order.create(
            customer_internal_id=customer.internal_id,
            order_items=[order_item1, order_item2]
        )
        
        assert len(order.order_items) == 2
        expected_total = Decimal("12.99") + Decimal("4.99")
        assert order.value.amount == expected_total

    def test_order_business_rules_without_customer_id(self):
        """Test that order without customer ID raises error"""
        # Create test order item
        product = create_test_product()
        
        order_item = OrderItem(
            order_internal_id=1,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        with pytest.raises(ValueError, match="Order must have a customer internal ID"):
            Order(
                customer_internal_id=None,
                order_items=[order_item]
            )

    def test_order_business_rules_without_items(self):
        """Test that order without items raises error"""
        customer_id = 1  # Valid customer ID
        
        with pytest.raises(ValueError, match="Order must have at least one item"):
            Order(
                customer_internal_id=customer_id,
                order_items=[]
            )

    def test_order_business_rules_with_inactive_product(self):
        """Test that order with inactive product raises error"""
        # Create test customer
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725"
        )
        customer.internal_id = 1  # Set for testing
        
        # Create test ingredient
        bread = Ingredient.create(
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
            name="Inactive Burger",
            price=Money(amount=Decimal("10.00")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-INA"),
            default_ingredient=[ProductReceiptItem(bread, 1)],
            is_active=False
        )
        
        order_item = OrderItem(
            order_internal_id=1,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        with pytest.raises(ValueError, match="Order items must have active products"):
            Order(
                customer_internal_id=customer.internal_id,
                order_items=[order_item]
            )

    def test_order_status_flow(self):
        """Test order status flow"""
        # Create test customer and order
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725"
        )
        customer.internal_id = 1  # Set for testing
        
        product = create_test_product()
        
        order_item = OrderItem(
            order_internal_id=1,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        order = Order.create(
            customer_internal_id=customer.internal_id,
            order_items=[order_item]
        )
        
        # Initial status should be RECEBIDO
        assert str(order.status) == "RECEBIDO"
        
        # Move to next status
        order.next_status()
        assert str(order.status) == "EM_PREPARACAO"
        
        # Move to next status
        order.next_status()
        assert str(order.status) == "PRONTO"
        
        # Move to next status
        order.next_status()
        assert str(order.status) == "FINALIZADO"
        
        # Should not be able to move further
        order.next_status()
        assert str(order.status) == "FINALIZADO"

    def test_order_payment_processing(self):
        """Test order payment processing"""
        # Create test customer and order
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725"
        )
        customer.internal_id = 1  # Set for testing
        
        product = create_test_product()
        
        order_item = OrderItem(
            order_internal_id=1,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        order = Order.create(
            customer_internal_id=customer.internal_id,
            order_items=[order_item]
        )
        
        # Process successful payment
        payment_data = {
            'transaction_id': 'TXN123456',
            'approval_status': True,
            'date': datetime.now(),
            'message': 'Payment approved'
        }
        
        order.process_payment(payment_data)
        
        assert order.has_payment_verified is True
        assert order.payment_transaction_id == 'TXN123456'
        assert order.payment_message == 'Payment approved'
        assert str(order.status) == "EM_PREPARACAO"
        
        # Try to process payment again (should fail)
        with pytest.raises(ValueError, match="Payment has already been verified for this order"):
            order.process_payment(payment_data)

    def test_order_payment_processing_failed(self):
        """Test order payment processing with failed payment"""
        # Create test customer and order
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725"
        )
        customer.internal_id = 1  # Set for testing
        
        product = create_test_product()
        
        order_item = OrderItem(
            order_internal_id=1,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        order = Order.create(
            customer_internal_id=customer.internal_id,
            order_items=[order_item]
        )
        
        # Process failed payment
        payment_data = {
            'transaction_id': 'TXN123456',
            'approval_status': False,
            'date': datetime.now(),
            'message': 'Payment declined'
        }
        
        order.process_payment(payment_data)
        
        assert order.has_payment_verified is False
        assert order.payment_transaction_id == 'TXN123456'
        assert order.payment_message == 'Payment declined'
        assert str(order.status) == "CANCELADO"

    def test_order_can_be_cancelled(self):
        """Test order cancellation rules"""
        # Create test customer and order
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725"
        )
        customer.internal_id = 1  # Set for testing
        
        product = create_test_product()
        
        order_item = OrderItem(
            order_internal_id=1,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        order = Order.create(
            customer_internal_id=customer.internal_id,
            order_items=[order_item]
        )
        
        # Should be able to cancel when status is RECEBIDO
        assert order.can_be_cancelled() is True
        
        # Move to EM_PREPARACAO
        order.next_status()
        assert order.can_be_cancelled() is True
        
        # Move to PRONTO
        order.next_status()
        assert order.can_be_cancelled() is False
        
        # Move to FINALIZADO
        order.next_status()
        assert order.can_be_cancelled() is False

    def test_order_can_be_finalized(self):
        """Test order finalization rules"""
        # Create test customer and order
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725"
        )
        customer.internal_id = 1  # Set for testing
        
        product = create_test_product()
        
        order_item = OrderItem(
            order_internal_id=1,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        order = Order.create(
            customer_internal_id=customer.internal_id,
            order_items=[order_item]
        )
        
        # Should not be able to finalize when status is RECEBIDO
        assert order.can_be_finalized() is False
        
        # Move to EM_PREPARACAO
        order.next_status()
        assert order.can_be_finalized() is False
        
        # Move to PRONTO
        order.next_status()
        assert order.can_be_finalized() is True
        
        # Move to FINALIZADO
        order.next_status()
        assert order.can_be_finalized() is False

    def test_order_get_total_items(self):
        """Test getting total number of items in order"""
        # Create test customer
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725"
        )
        customer.internal_id = 1  # Set for testing
        
        # Create test ingredients
        bread = Ingredient.create(
            name="Burger Bun",
            price=Money(amount=Decimal("2.00")),
            is_active=True,
            type=IngredientType.BREAD,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        meat = Ingredient.create(
            name="Beef Patty",
            price=Money(amount=Decimal("8.00")),
            is_active=True,
            type=IngredientType.MEAT,
            applies_to_burger=True,
            applies_to_side=False,
            applies_to_drink=False,
            applies_to_dessert=False
        )
        
        # Create test products
        product1 = Product.create(
            name="Classic Burger",
            price=Money(amount=Decimal("10.00")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-CLS"),
            default_ingredient=[ProductReceiptItem(bread, 1), ProductReceiptItem(meat, 1)],
            is_active=True
        )
        
        product2 = Product.create(
            name="Deluxe Burger",
            price=Money(amount=Decimal("12.00")),
            category=ProductCategory.BURGER,
            sku=SKU.create("BURG-2024-DLX"),
            default_ingredient=[ProductReceiptItem(bread, 1), ProductReceiptItem(meat, 1)],
            is_active=True
        )
        
        order_item1 = OrderItem(
            order_internal_id=1,
            product=product1,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        order_item2 = OrderItem(
            order_internal_id=1,
            product=product2,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        order = Order.create(
            customer_internal_id=customer.internal_id,
            order_items=[order_item1, order_item2]
        )
        
        assert order.get_total_items() == 2

    def test_order_string_representation(self):
        """Test order string representation"""
        # Create test customer and order
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725"
        )
        customer.internal_id = 1  # Set for testing
        
        product = create_test_product()
        
        order_item = OrderItem(
            order_internal_id=1,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        order_id = 0
        order = Order.create(
            customer_internal_id=customer.internal_id,
            order_items=[order_item],
            internal_id=0
        )
        
        expected = f"Order(internal_id={order_id}, customer_id={customer.internal_id}, status={order.status}, value={order.value})"
        assert str(order) == expected

    def test_order_repr_representation(self):
        """Test order repr representation"""
        # Create test customer and order
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725"
        )
        customer.internal_id = 1  # Set for testing
        
        product = create_test_product()
        
        order_item = OrderItem(
            order_internal_id=1,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        order_id = 0
        order = Order.create(
            customer_internal_id=customer.internal_id,
            order_items=[order_item],
            internal_id=0
        )
        
        expected = f"Order(internal_id={order_id}, customer_id={customer.internal_id}, status={order.status}, value={order.value})"
        assert repr(order) == expected

    def test_order_dto_conversion(self):
        """Test order to DTO conversion"""
        # Create test customer and order
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725"
        )
        customer.internal_id = 1  # Set for testing
        
        product = create_test_product()
        
        order_item = OrderItem(
            order_internal_id=1,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        order = Order.create(
            customer_internal_id=customer.internal_id,
            order_items=[order_item]
        )
        
        dto = OrderResponse.from_entity(order)
        
        # UUID assertion removed - using internal_id now
        assert dto.customer_internal_id == customer.internal_id
        assert len(dto.order_items) == 1
        assert dto.value == 10.00
        assert dto.status == "RECEBIDO"
        assert dto.has_payment_verified is False
        assert dto.payment_transaction_id == ""
        assert dto.payment_message == ""

    def test_order_item_dto_conversion(self):
        """Test order item to DTO conversion"""
        # Create test product
        product = create_test_product()
        
        item_id = 0
        
        order_item = OrderItem(
            order_internal_id=0,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[],
            internal_id=item_id
        )
        
        dto = OrderItemResponse.from_entity(order_item)
        
        # UUID assertion removed - using internal_id now
        assert dto.internal_id == item_id
        assert dto.product_internal_id == product.internal_id
        assert dto.product_name == "Test Burger"
        assert dto.product_price == 10.00
        assert len(dto.additional_ingredients) == 0
        assert len(dto.remove_ingredients) == 0
        assert dto.price == 10.00 

    def test_order_payment_request_validation(self):
        """Test order payment request validation"""
        # Create test customer and order
        customer = Customer.create_registered(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            document="52998224725"
        )
        customer.internal_id = 1  # Set for testing
        
        product = create_test_product()
        
        order_item = OrderItem(
            order_internal_id=1,
            product=product,
            additional_ingredient=[],
            remove_ingredient=[]
        )
        
        order = Order.create(
            customer_internal_id=customer.internal_id,
            order_items=[order_item]
        )
        
        # Set internal_id for testing (normally set by repository)
        order.internal_id = 1
        
        # Test that order can be used for payment request
        assert order.has_payment_verified is False
        assert order.value.value > 0
        assert order.internal_id is not None 