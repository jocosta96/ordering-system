"""
Custom exceptions for the application layer.

In Clean Architecture:
- These exceptions are part of the Application Business Rules layer
- They provide specific error types for different business scenarios
- They help standardize error handling across use cases
"""


class ApplicationException(Exception):
    """Base exception for application layer errors"""

    pass


class CustomerNotFoundException(ApplicationException):
    """Raised when a customer is not found"""

    pass


class CustomerAlreadyExistsException(ApplicationException):
    """Raised when trying to create a customer that already exists"""

    pass


class CustomerValidationException(ApplicationException):
    """Raised when customer data validation fails"""

    pass


class CustomerBusinessRuleException(ApplicationException):
    """Raised when a business rule is violated"""

    pass


class CustomerOperationException(ApplicationException):
    """Raised when a customer operation fails"""

    pass


class AuthenticationException(ApplicationException):
    """Raised when authentication fails"""

    pass


class AuthorizationException(ApplicationException):
    """Raised when authorization fails"""

    pass


class DatabaseException(ApplicationException):
    """Raised when database operations fail"""

    pass
