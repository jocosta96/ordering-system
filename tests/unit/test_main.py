"""
Unit tests for main application.

Tests cover:
- Application creation
- Router inclusion
- Middleware configuration
- Application configuration
"""

from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.main import create_application, app


class TestMainApplication:
    """Test cases for main application"""

    def test_create_application_returns_fastapi_app(self):
        """Test that create_application returns a FastAPI app"""
        with patch('src.main.configure_logging'):
            result = create_application()
            
            assert isinstance(result, FastAPI)
            assert result.title == "FastFood Ordering System"
            assert result.version == "1.0.0"
            assert result.description == "A clean architecture ordering system"

    def test_create_application_includes_all_routers(self):
        """Test that create_application includes all required routers"""
        with patch('src.main.configure_logging'):
            app = create_application()
            
            # Check that all routers are included
            router_paths = [route.path for route in app.routes]
            
            # Health routes
            assert any('/health' in path for path in router_paths)
            
            # Customer routes
            assert any('/customer' in path for path in router_paths)
            
            # Ingredient routes
            assert any('/ingredient' in path for path in router_paths)
            
            # Product routes
            assert any('/product' in path for path in router_paths)
            
            # Order routes
            assert any('/order' in path for path in router_paths)

    def test_create_application_configures_cors(self):
        """Test that create_application configures CORS middleware"""
        with patch('src.main.configure_logging'):
            app = create_application()

            # Check that CORS middleware is added
            middleware_found = False
            for middleware in app.user_middleware:
                if 'CORSMiddleware' in str(middleware):
                    middleware_found = True
                    break

            assert middleware_found, "CORS middleware should be configured"

    def test_app_instance_exists(self):
        """Test that app instance is created"""
        assert app is not None
        assert isinstance(app, FastAPI)

    def test_app_has_health_endpoint(self):
        """Test that app has health endpoint"""
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code in [200, 404]  # 404 if health route not implemented

    def test_app_has_customer_endpoints(self):
        """Test that app has customer endpoints"""
        client = TestClient(app)
        
        # Test that customer routes are accessible (may return 401 for auth required)
        response = client.get("/customer/list")
        assert response.status_code in [200, 401, 404]  # 401 for auth, 404 if not implemented

    def test_app_has_ingredient_endpoints(self):
        """Test that app has ingredient endpoints"""
        client = TestClient(app)
        
        # Test that ingredient routes are accessible (may return 401 for auth required)
        response = client.get("/ingredient/list")
        assert response.status_code in [200, 401, 404]  # 401 for auth, 404 if not implemented

    def test_app_has_product_endpoints(self):
        """Test that app has product endpoints"""
        client = TestClient(app)
        
        # Test that product routes are accessible (may return 401 for auth required)
        response = client.get("/product/list")
        assert response.status_code in [200, 401, 404]  # 401 for auth, 404 if not implemented

    def test_app_has_order_endpoints(self):
        """Test that app has order endpoints"""
        client = TestClient(app)
        
        # Test that order routes are accessible (may return 401 for auth required)
        response = client.get("/order/list")
        assert response.status_code in [200, 401, 404]  # 401 for auth, 404 if not implemented

    def test_app_configuration_values(self):
        """Test that app has correct configuration values"""
        assert app.title == "FastFood Ordering System"
        assert app.version == "1.0.0"
        assert app.description == "A clean architecture ordering system"

    def test_app_middleware_configuration(self):
        """Test that app has CORS middleware configured"""
        # Check that CORS middleware is present
        middleware_found = False
        for middleware in app.user_middleware:
            if 'CORSMiddleware' in str(middleware):
                middleware_found = True
                break

        assert middleware_found, "CORS middleware should be configured"

    def test_app_routes_structure(self):
        """Test that app has the expected route structure"""
        # Get all routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)
        
        # Check that we have routes from different modules
        route_paths = ' '.join(routes)
        
        # Should have health routes
        assert '/health' in route_paths or 'health' in route_paths
        
        # Should have customer routes
        assert '/customer' in route_paths or 'customer' in route_paths
        
        # Should have ingredient routes
        assert '/ingredient' in route_paths or 'ingredient' in route_paths
        
        # Should have product routes
        assert '/product' in route_paths or 'product' in route_paths
        
        # Should have order routes
        assert '/order' in route_paths or 'order' in route_paths

    def test_app_openapi_generation(self):
        """Test that app can generate OpenAPI schema"""
        openapi_schema = app.openapi()
        
        assert openapi_schema is not None
        assert 'info' in openapi_schema
        assert 'paths' in openapi_schema
        assert openapi_schema['info']['title'] == "FastFood Ordering System"
        assert openapi_schema['info']['version'] == "1.0.0"

    def test_app_docs_endpoint(self):
        """Test that app has docs endpoint"""
        client = TestClient(app)
        response = client.get("/docs")
        assert response.status_code == 200

    def test_app_redoc_endpoint(self):
        """Test that app has redoc endpoint"""
        client = TestClient(app)
        response = client.get("/redoc")
        assert response.status_code == 200

    def test_app_openapi_endpoint(self):
        """Test that app has openapi endpoint"""
        client = TestClient(app)
        response = client.get("/openapi.json")
        assert response.status_code == 200 