class NotFoundError(Exception):
    """Exception raised when a requested resource is not found."""
    def __init__(self, message="Resource not found"):
        super().__init__(message)

class DuplicatedPaymentError(Exception):
    """Exception raised when a requested payment already exist."""
    def __init__(self, message="Duplicated Payment"):
        super().__init__(message)