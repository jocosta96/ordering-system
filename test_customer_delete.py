from src.application.dto.implementation.customer_dto import CustomerResponse
from datetime import datetime

# Mock the use case to return a customer response
mock_customer_response = CustomerResponse(
    id="c2f149a9-973a-401b-9b73-a6abb8415ed1",
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com",
    document="12345678901",
    full_name="John Doe",
    is_anonymous=False,
    is_registered=True,
    is_active=True,
    created_at=datetime(2024, 1, 1)
)