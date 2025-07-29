"""
Unit tests for API routes.

Tests cover:
- Route endpoints
- Request/response handling
- Authentication
- Error handling
"""

import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient

from src.main import create_application


class TestIngredientRoutes:
    """Test cases for ingredient routes"""

    @pytest.fixture
    def app(self):
        """Create test app"""
        app = create_application()
        return app

    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return TestClient(app)

    @pytest.fixture
    def mock_ingredient_controller(self):
        """Mock ingredient controller"""
        mock_controller = Mock()
        
        # Mock successful responses
        mock_controller.create_ingredient.return_value = {
            "internal_id": 1,
            "name": "Test Ingredient",
            "price": 5.50,
            "type": "MEAT",
            "is_active": True
        }
        
        mock_controller.list_ingredients.return_value = {
            "ingredients": [
                {
                    "internal_id": 1,
                    "name": "Test Ingredient",
                    "price": 5.50,
                    "type": "MEAT",
                    "is_active": True
                }
            ],
            "total_count": 1
        }
        
        mock_controller.get_ingredient.return_value = {
            "internal_id": 1,
            "name": "Test Ingredient",
            "price": 5.50,
            "type": "MEAT",
            "is_active": True
        }
        
        mock_controller.update_ingredient.return_value = {
            "internal_id": 1,
            "name": "Updated Ingredient",
            "price": 6.50,
            "type": "MEAT",
            "is_active": True
        }
        
        mock_controller.delete_ingredient.return_value = {
            "success": True,
            "message": "Ingredient deleted"
        }
        
        mock_controller.list_ingredients_by_type.return_value = {
            "ingredients": [
                {
                    "internal_id": 1,
                    "name": "Test Ingredient",
                    "price": 5.50,
                    "type": "MEAT",
                    "is_active": True
                }
            ],
            "total_count": 1
        }
        
        mock_controller.list_ingredients_by_applies_to.return_value = {
            "ingredients": [
                {
                    "internal_id": 1,
                    "name": "Test Ingredient",
                    "price": 5.50,
                    "type": "MEAT",
                    "is_active": True
                }
            ],
            "total_count": 1
        }
        
        mock_controller.list_ingredient_types.return_value = {
            "ingredient_types": [
                {"value": "MEAT", "name": "MEAT"},
                {"value": "VEGETABLE", "name": "VEGETABLE"}
            ],
            "total_count": 2
        }
        
        return mock_controller


class TestProductRoutes:
    """Test cases for product routes"""

    @pytest.fixture
    def app(self):
        """Create test app"""
        app = create_application()
        return app

    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return TestClient(app)

    @pytest.fixture
    def mock_product_controller(self):
        """Mock product controller"""
        mock_controller = Mock()
        
        # Mock successful responses
        mock_controller.create_product.return_value = {
            "internal_id": 1,
            "name": "Test Product",
            "description": "Test Description",
            "price": 10.50,
            "category": "BURGER",
            "sku": "TEST-001",
            "is_active": True
        }
        
        mock_controller.list_products.return_value = {
            "products": [
                {
                    "internal_id": 1,
                    "name": "Test Product",
                    "description": "Test Description",
                    "price": 10.50,
                    "category": "BURGER",
                    "sku": "TEST-001",
                    "is_active": True
                }
            ],
            "total_count": 1
        }
        
        mock_controller.get_product.return_value = {
            "internal_id": 1,
            "name": "Test Product",
            "description": "Test Description",
            "price": 10.50,
            "category": "BURGER",
            "sku": "TEST-001",
            "is_active": True
        }
        
        mock_controller.get_product_by_sku.return_value = {
            "internal_id": 1,
            "name": "Test Product",
            "description": "Test Description",
            "price": 10.50,
            "category": "BURGER",
            "sku": "TEST-001",
            "is_active": True
        }
        
        mock_controller.update_product.return_value = {
            "internal_id": 1,
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 12.50,
            "category": "BURGER",
            "sku": "TEST-001",
            "is_active": True
        }
        
        mock_controller.delete_product.return_value = {
            "success": True,
            "message": "Product deleted"
        }
        
        mock_controller.list_products_by_category.return_value = {
            "products": [
                {
                    "internal_id": 1,
                    "name": "Test Product",
                    "description": "Test Description",
                    "price": 10.50,
                    "category": "BURGER",
                    "sku": "TEST-001",
                    "is_active": True
                }
            ],
            "total_count": 1
        }
        
        return mock_controller


class TestOrderRoutes:
    """Test cases for order routes"""

    @pytest.fixture
    def app(self):
        """Create test app"""
        app = create_application()
        return app

    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return TestClient(app)

    @pytest.fixture
    def mock_order_controller(self):
        """Mock order controller"""
        mock_controller = Mock()
        
        # Mock successful responses
        mock_controller.create_order.return_value = {
            "internal_id": 1,
            "customer_internal_id": 1,
            "status": "PENDING",
            "total_amount": 25.50,
            "created_at": "2023-01-01T00:00:00",
            "is_active": True
        }
        
        mock_controller.get_order.return_value = {
            "internal_id": 1,
            "customer_internal_id": 1,
            "status": "PENDING",
            "total_amount": 25.50,
            "created_at": "2023-01-01T00:00:00",
            "is_active": True
        }
        
        mock_controller.list_orders.return_value = {
            "orders": [
                {
                    "internal_id": 1,
                    "customer_internal_id": 1,
                    "status": "PENDING",
                    "total_amount": 25.50,
                    "created_at": "2023-01-01T00:00:00",
                    "is_active": True
                }
            ],
            "total_count": 1
        }
        
        mock_controller.update_order_status.return_value = {
            "internal_id": 1,
            "customer_internal_id": 1,
            "status": "CONFIRMED",
            "total_amount": 25.50,
            "created_at": "2023-01-01T00:00:00",
            "is_active": True
        }
        
        mock_controller.cancel_order.return_value = {
            "internal_id": 1,
            "customer_internal_id": 1,
            "status": "CANCELLED",
            "total_amount": 25.50,
            "created_at": "2023-01-01T00:00:00",
            "is_active": True
        }
        
        mock_controller.process_payment.return_value = {
            "payment_id": "PAY-001",
            "status": "PROCESSED",
            "amount": 25.50
        }
        
        mock_controller.request_payment.return_value = {
            "payment_id": "PAY-001",
            "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
            "status": "PENDING"
        }
        
        mock_controller.get_payment_status.return_value = {
            "payment_id": "PAY-001",
            "status": "PENDING"
        }
        
        mock_controller.get_orders_by_status.return_value = [
            {
                "internal_id": 1,
                "customer_internal_id": 1,
                "status": "PENDING",
                "total_amount": 25.50,
                "created_at": "2023-01-01T00:00:00",
                "is_active": True
            }
        ]
        
        return mock_controller 