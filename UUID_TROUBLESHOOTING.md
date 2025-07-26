# UUID Validation and Soft Delete Troubleshooting Guide

## Problem 1: UUID Validation Error
You're getting a 400 Bad Request error with the message:
```
"Invalid customer ID format: 'c92796a8-19f3-4d19-ba70-1c9279820c20'. Customer ID must be a valid UUID (e.g., '550e8400-e29b-41d4-a716-446655440000')."
```

## Problem 2: Soft Delete Error
You're getting a 500 Internal Server Error with the message:
```
"Anonymous customers must have anonymous email"
```

Or:
```
"Cannot delete anonymous customer"
```

## Root Cause Analysis

### UUID Issue
The UUID `c92796a8-19f3-4d19-ba70-1c9279820c20` is actually **valid**. The error was occurring due to:
1. **Status Code Mismatch**: The error response showed `"status_code": 500` instead of `400`
2. **Customer Not Found**: The most likely cause is that the customer with this UUID doesn't exist in the database

### Soft Delete Issue
The soft delete error was occurring because:
1. **Business Rule Violation**: The system was trying to make soft-deleted customers anonymous but with non-anonymous emails
2. **Concept Confusion**: Active anonymous customers and inactive customers were being treated the same way
3. **Incorrect Anonymous Detection**: The system was using document status instead of the `is_anonymous` flag to determine if a customer is anonymous

## Solution Implemented

### 1. Fixed Error Status Codes
- Updated the `JSONPresenter` to properly map `CustomerValidationException` to HTTP 400 (Bad Request)
- All validation exceptions now return the correct HTTP status codes

### 2. Updated Business Rules
- **Active anonymous customers** (is_anonymous=True + active) must have anonymous email
- **Inactive customers** can have any email
- This allows soft-deleted customers to become inactive and anonymous with unique emails

### 3. Fixed Soft Delete Method
- Soft-deleted customers become **inactive** and **anonymous**
- They get unique deleted emails: `deleted.{customer_id}@fastfood.local`
- This maintains email uniqueness while allowing proper soft deletion

### 4. Fixed Repository Integration
- Updated `CustomerDeleteUseCase` to use the repository's dedicated `delete` method
- This method updates the database directly without recreating the entity
- Prevents validation errors when the customer is recreated from the database
- Modified `_to_entity` method to create Customer objects without triggering validation

### 5. Fixed Anonymous Detection
- Added `is_anonymous` field to Customer entity
- Updated `is_anonymous` property to use the flag instead of document status
- Updated business rules to use `is_anonymous` flag instead of `document.is_empty`
- This properly separates anonymous customers from customers with empty documents

## Business Rules Clarification

### Customer Types
1. **Active Registered Customer**: Has document, has email, is_active=True, is_anonymous=False
2. **Active Anonymous Customer**: No document, has anonymous email, is_active=True, is_anonymous=True
3. **Inactive Registered Customer**: Empty document, unique deleted email, is_active=False, is_anonymous=False
4. **Inactive Anonymous Customer**: Empty document, anonymous email, is_active=False, is_anonymous=True

### Soft Delete Behavior
When a registered customer is soft-deleted:
- **Status**: `is_active` becomes `False`
- **Name**: Changed to "Deleted Customer"
- **Email**: Changed to `deleted.{customer_id}@fastfood.local` (unique)
- **Document**: Changed to empty string
- **Anonymous**: `is_anonymous` remains `False` (stays registered)
- **Business Rules**: No longer violated because customer is inactive

### Anonymous vs Empty Document
- **Anonymous Customer**: `is_anonymous=True` (regardless of document status)
- **Customer with Empty Document**: `document.is_empty=True` but `is_anonymous=False`
- **Soft-Deleted Customer**: `document.is_empty=True`, `is_anonymous=False`, `is_active=False`
- **Key Difference**: Only the `is_anonymous` flag determines if a customer is anonymous, not the document status

## Valid UUID Formats
Customer IDs must be in valid UUID format:
- `550e8400-e29b-41d4-a716-446655440000` (with hyphens)
- `550e8400e29b41d4a716446655440000` (without hyphens)

## Common Issues and Solutions

### Issue 1: "Invalid customer ID format" for a valid UUID
**Cause**: The customer doesn't exist in the database
**Solution**: 
1. Check if the customer exists using `GET /customer/list`
2. Create a new customer if needed using `POST /customer/create`

### Issue 2: "Anonymous customers must have anonymous email" during soft delete
**Cause**: This was a business rule violation (now fixed)
**Solution**: The system now correctly handles soft deletion by making customers inactive

### Issue 3: "Cannot delete anonymous customer" during soft delete
**Cause**: The customer is already anonymous (is_anonymous=True) and active
**Solution**: The system now properly distinguishes between active anonymous customers (protected) and inactive anonymous customers (can be deleted)

### Issue 4: Status code 500 instead of 400
**Cause**: This was a bug in error handling (now fixed)
**Solution**: The system now correctly returns 400 for validation errors

## How to Get a Valid Customer ID

### Option A: Create a New Customer
```bash
curl -X POST "http://localhost:8000/customer/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <your-auth>" \
  -d '{
    "first_name": "John",
    "last_name": "Doe", 
    "email": "john@example.com",
    "document": "12345678901"
  }'
```

### Option B: List All Customers
```bash
curl -X GET "http://localhost:8000/customer/list" \
  -H "Authorization: Basic <your-auth>"
```

### Option C: Get Anonymous Customer
```bash
curl -X GET "http://localhost:8000/customer/anonymous"
```

## Example Valid Requests

### Get Customer by ID
```bash
curl -X GET "http://localhost:8000/customer/by-id/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Basic <your-auth>"
```

### Delete Customer
```bash
curl -X DELETE "http://localhost:8000/customer/delete/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Basic <your-auth>"
```

## Debugging Tips

### Check the Logs
The application logs UUID validation attempts. Look for:
- `INFO: Attempting to get customer with ID: <customer_id>`
- `WARNING: Customer not found with ID: <customer_id>`

### Test UUID Format
You can test if a UUID is valid using Python:
```python
import uuid
try:
    uuid.UUID("your-customer-id-here")
    print("Valid UUID")
except ValueError:
    print("Invalid UUID")
```

## Recent Improvements
- **Route-level validation**: Invalid UUIDs are caught before reaching the controller
- **Better error messages**: More descriptive error messages with examples
- **Enhanced logging**: Detailed logs for debugging UUID issues
- **Consistent validation**: Both GET and DELETE endpoints validate UUIDs
- **Correct status codes**: Validation errors now return 400 instead of 500
- **Fixed business rules**: Proper separation of active anonymous vs inactive customers
- **Fixed soft delete**: Customers become inactive and anonymous with unique emails
- **Fixed anonymous detection**: Uses `is_anonymous` flag instead of document status
- **Proper entity design**: Added `is_anonymous` field to Customer entity

## API Endpoints That Require UUID
- `GET /customer/by-id/{customer_id}`
- `DELETE /customer/delete/{customer_id}`

## Still Having Issues?
1. **Check that you're using the correct customer ID** from the database
2. **Ensure the customer exists** in the database
3. **Verify the customer hasn't been soft-deleted** (check `is_active` field)
4. **Check the application logs** for detailed error messages
5. **Test the UUID format** using the Python code above

## Example Valid UUIDs for Testing
- `550e8400-e29b-41d4-a716-446655440000`
- `c92796a8-19f3-4d19-ba70-1c9279820c20`
- `123e4567-e89b-12d3-a456-426614174000`

## Expected Error Responses

### Valid UUID, Customer Not Found (404)
```json
{
  "detail": {
    "error": {
      "message": "Customer with ID c92796a8-19f3-4d19-ba70-1c9279820c20 not found",
      "type": "CustomerNotFoundException",
      "timestamp": "2025-07-26T18:34:16.163397Z",
      "status_code": 404
    }
  }
}
```

### Invalid UUID Format (400)
```json
{
  "detail": {
    "error": {
      "message": "Invalid customer ID format: 'not-a-uuid'. Customer ID must be a valid UUID (e.g., '550e8400-e29b-41d4-a716-446655440000').",
      "type": "CustomerValidationException",
      "timestamp": "2025-07-26T18:34:16.163397Z",
      "status_code": 400
    }
  }
}
```

### Successful Soft Delete (200)
```json
{
  "success": true,
  "message": "Customer soft deleted successfully - data replaced with placeholder values"
}
``` 