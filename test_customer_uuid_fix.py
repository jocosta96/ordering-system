#!/usr/bin/env python3
"""
Test script to verify the customer delete fix with the specific UUID that was failing.
"""

import uuid
from unittest.mock import Mock

# Import the modules we need to test
from src.adapters.controllers.customer_controller import CustomerController
from src.application.repositories.customer_repository import CustomerRepository
from src.adapters.presenters.interfaces.presenter_interface import PresenterInterface

def test_customer_delete_with_specific_uuid():
    """Test that customer delete works with the specific UUID that was failing"""
    
    # Create mocks
    mock_repository = Mock(spec=CustomerRepository)
    mock_presenter = Mock(spec=PresenterInterface)
    
    # Create controller
    controller = CustomerController(mock_repository, mock_presenter)
    
    # Mock the use case to return True (success)
    controller.delete_use_case.execute = Mock(return_value=True)
    
    # Mock the presenter
    mock_presenter.present.return_value = {"success": True, "message": "Customer soft deleted successfully - data replaced with placeholder values"}
    
    # Test with the specific UUID that was failing
    test_uuid = "c92796a8-19f3-4d19-ba70-1c9279820c20"
    
    try:
        # Call the delete method
        result = controller.delete_customer(test_uuid, "test_user")
        
        # Verify the result
        assert result == {"success": True, "message": "Customer soft deleted successfully - data replaced with placeholder values"}
        
        # Verify the use case was called with the correct UUID object
        controller.delete_use_case.execute.assert_called_once_with(uuid.UUID(test_uuid))
        
        print("✅ SUCCESS: Customer delete works with the specific UUID!")
        print(f"   Input UUID string: {test_uuid}")
        print(f"   Converted to UUID object: {uuid.UUID(test_uuid)}")
        print(f"   Result: {result}")
        
    except Exception as e:
        print(f"❌ ERROR: Customer delete failed - {e}")
        return False
    
    return True

def test_uuid_conversion():
    """Test UUID string to UUID object conversion"""
    
    test_uuid = "c92796a8-19f3-4d19-ba70-1c9279820c20"
    
    try:
        uuid_obj = uuid.UUID(test_uuid)
        print(f"✅ SUCCESS: UUID conversion works!")
        print(f"   String: {test_uuid}")
        print(f"   UUID object: {uuid_obj}")
        return True
    except Exception as e:
        print(f"❌ ERROR: UUID conversion failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing customer delete with the specific UUID that was failing...")
    print("=" * 70)
    
    # Test UUID conversion
    print("\n1. Testing UUID conversion:")
    uuid_success = test_uuid_conversion()
    
    # Test customer delete
    print("\n2. Testing customer delete with the specific UUID:")
    delete_success = test_customer_delete_with_specific_uuid()
    
    print("\n" + "=" * 70)
    if uuid_success and delete_success:
        print("🎉 ALL TESTS PASSED! The fix is working correctly.")
        print("   The customer delete should now work with the UUID from your curl command.")
    else:
        print("💥 SOME TESTS FAILED. Please check the implementation.")