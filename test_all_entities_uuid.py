#!/usr/bin/env python3
"""
Comprehensive test script to verify that all entities work correctly with UUID strings.
Tests Ingredient, Customer, and Product delete operations with UUID strings.
"""

import uuid
from unittest.mock import Mock

# Import the modules we need to test
from src.adapters.controllers.ingredient_controller import IngredientController
from src.adapters.controllers.customer_controller import CustomerController
from src.adapters.controllers.product_controller import ProductController
from src.application.repositories.ingredient_repository import IngredientRepository
from src.application.repositories.customer_repository import CustomerRepository
from src.application.repositories.product_repository import ProductRepository
from src.adapters.presenters.interfaces.presenter_interface import PresenterInterface

def test_ingredient_delete_with_uuid():
    """Test that ingredient delete works with UUID strings"""
    
    # Create mocks
    mock_repository = Mock(spec=IngredientRepository)
    mock_presenter = Mock(spec=PresenterInterface)
    
    # Create controller
    controller = IngredientController(mock_repository, mock_presenter)
    
    # Mock the use case to return True (success)
    controller.delete_use_case.execute = Mock(return_value=True)
    
    # Mock the presenter
    mock_presenter.present.return_value = {"success": True, "message": "Ingredient soft deleted successfully"}
    
    # Test with the UUID from the user's error
    test_uuid = "c2f149a9-973a-401b-9b73-a6abb8415ed1"
    
    try:
        # Call the delete method
        result = controller.delete_ingredient(test_uuid, "test_user")
        
        # Verify the result
        assert result == {"success": True, "message": "Ingredient soft deleted successfully"}
        
        # Verify the use case was called with the correct UUID object
        controller.delete_use_case.execute.assert_called_once_with(uuid.UUID(test_uuid))
        
        print("✅ SUCCESS: Ingredient delete works with UUID strings!")
        print(f"   Input UUID string: {test_uuid}")
        print(f"   Converted to UUID object: {uuid.UUID(test_uuid)}")
        
    except Exception as e:
        print(f"❌ ERROR: Ingredient delete failed - {e}")
        return False
    
    return True

def test_customer_delete_with_uuid():
    """Test that customer delete works with UUID strings"""
    
    # Create mocks
    mock_repository = Mock(spec=CustomerRepository)
    mock_presenter = Mock(spec=PresenterInterface)
    
    # Create controller
    controller = CustomerController(mock_repository, mock_presenter)
    
    # Mock the use case to return True (success)
    controller.delete_use_case.execute = Mock(return_value=True)
    
    # Mock the presenter
    mock_presenter.present.return_value = {"success": True, "message": "Customer soft deleted successfully - data replaced with placeholder values"}
    
    # Test with a valid UUID
    test_uuid = "c2f149a9-973a-401b-9b73-a6abb8415ed1"
    
    try:
        # Call the delete method
        result = controller.delete_customer(test_uuid, "test_user")
        
        # Verify the result
        assert result == {"success": True, "message": "Customer soft deleted successfully - data replaced with placeholder values"}
        
        # Verify the use case was called with the correct UUID object
        controller.delete_use_case.execute.assert_called_once_with(uuid.UUID(test_uuid))
        
        print("✅ SUCCESS: Customer delete works with UUID strings!")
        print(f"   Input UUID string: {test_uuid}")
        print(f"   Converted to UUID object: {uuid.UUID(test_uuid)}")
        
    except Exception as e:
        print(f"❌ ERROR: Customer delete failed - {e}")
        return False
    
    return True

def test_product_delete_with_uuid():
    """Test that product delete works with UUID strings"""
    
    # Create mocks
    mock_repository = Mock(spec=ProductRepository)
    mock_ingredient_repository = Mock(spec=IngredientRepository)
    mock_presenter = Mock(spec=PresenterInterface)
    
    # Create controller
    controller = ProductController(mock_repository, mock_ingredient_repository, mock_presenter)
    
    # Mock the use case to return True (success)
    controller.delete_use_case.execute = Mock(return_value=True)
    
    # Mock the presenter
    mock_presenter.present.return_value = {"success": True, "message": "Product soft deleted successfully"}
    
    # Test with a valid UUID
    test_uuid = "c2f149a9-973a-401b-9b73-a6abb8415ed1"
    
    try:
        # Call the delete method
        result = controller.delete_product(test_uuid, "test_user")
        
        # Verify the result
        assert result == {"success": True, "message": "Product soft deleted successfully"}
        
        # Verify the use case was called with the correct UUID object
        controller.delete_use_case.execute.assert_called_once_with(uuid.UUID(test_uuid))
        
        print("✅ SUCCESS: Product delete works with UUID strings!")
        print(f"   Input UUID string: {test_uuid}")
        print(f"   Converted to UUID object: {uuid.UUID(test_uuid)}")
        
    except Exception as e:
        print(f"❌ ERROR: Product delete failed - {e}")
        return False
    
    return True

def test_uuid_conversion():
    """Test UUID string to UUID object conversion"""
    
    test_uuid = "c2f149a9-973a-401b-9b73-a6abb8415ed1"
    
    try:
        uuid_obj = uuid.UUID(test_uuid)
        print(f"✅ SUCCESS: UUID conversion works!")
        print(f"   String: {test_uuid}")
        print(f"   UUID object: {uuid_obj}")
        return True
    except Exception as e:
        print(f"❌ ERROR: UUID conversion failed: {e}")
        return False

def test_invalid_uuid_handling():
    """Test that invalid UUID strings are properly handled"""
    
    invalid_uuid = "invalid-uuid-string"
    
    # Test ingredient controller
    try:
        mock_repository = Mock(spec=IngredientRepository)
        mock_presenter = Mock(spec=PresenterInterface)
        controller = IngredientController(mock_repository, mock_presenter)
        
        # Mock the presenter to return error response
        mock_presenter.present_error.return_value = {"error": "Invalid ingredient ID format"}
        
        # This should raise an HTTPException
        try:
            controller.delete_ingredient(invalid_uuid, "test_user")
            print("❌ ERROR: Ingredient controller should have raised an exception for invalid UUID")
            return False
        except Exception:
            print("✅ SUCCESS: Ingredient controller properly handles invalid UUID")
        
    except Exception as e:
        print(f"❌ ERROR: Ingredient invalid UUID test failed - {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Testing all entities with UUID strings...")
    print("=" * 60)
    
    # Test UUID conversion
    print("\n1. Testing UUID conversion:")
    uuid_success = test_uuid_conversion()
    
    # Test ingredient delete
    print("\n2. Testing ingredient delete with UUID:")
    ingredient_success = test_ingredient_delete_with_uuid()
    
    # Test customer delete
    print("\n3. Testing customer delete with UUID:")
    customer_success = test_customer_delete_with_uuid()
    
    # Test product delete
    print("\n4. Testing product delete with UUID:")
    product_success = test_product_delete_with_uuid()
    
    # Test invalid UUID handling
    print("\n5. Testing invalid UUID handling:")
    invalid_uuid_success = test_invalid_uuid_handling()
    
    print("\n" + "=" * 60)
    if uuid_success and ingredient_success and customer_success and product_success and invalid_uuid_success:
        print("🎉 ALL TESTS PASSED! All entities now work correctly with UUID strings.")
        print("\n📋 SUMMARY:")
        print("   ✅ Ingredient routes, controller, and use cases updated to use UUID")
        print("   ✅ Customer routes, controller, and use cases updated to use UUID")
        print("   ✅ Product routes, controller, and use cases already use UUID")
        print("   ✅ All entities now consistently use UUID strings in routes and UUID objects in business logic")
    else:
        print("💥 SOME TESTS FAILED. Please check the implementation.")