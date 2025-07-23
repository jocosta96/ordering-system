from datetime import datetime
from typing import Any, Dict, List
from http import HTTPStatus

from src.adapters.presenters.interfaces.presenter_interface import PresenterInterface
from src.application.dto.customer_dto import CustomerResponse, CustomerListResponse


class JSONPresenter(PresenterInterface):
    """
    JSON presenter for REST API responses.

    In Clean Architecture:
    - This is part of the Interface Adapters layer
    - It formats data for JSON responses
    - It handles error formatting
    - It provides consistent API response structure
    """

    def present(self, data: Any) -> dict:
        """Present single data item as JSON"""
        if isinstance(data, CustomerResponse):
            return self._present_customer(data)
        elif isinstance(data, CustomerListResponse):
            return self._present_customer_list(data)
        else:
            return self._present_generic(data)

    def present_list(self, data_list: list) -> dict:
        """Present list of data as JSON"""
        if not data_list:
            return {"data": [], "total_count": 0, "timestamp": self._get_timestamp()}

        # Handle different types of lists
        if all(isinstance(item, CustomerResponse) for item in data_list):
            return {
                "data": [self._present_customer(item) for item in data_list],
                "total_count": len(data_list),
                "timestamp": self._get_timestamp(),
            }
        else:
            return {
                "data": [self._present_generic(item) for item in data_list],
                "total_count": len(data_list),
                "timestamp": self._get_timestamp(),
            }

    def present_error(self, error: Exception) -> dict:
        """Present error as JSON"""
        error_response = {
            "error": {
                "message": str(error),
                "type": type(error).__name__,
                "timestamp": self._get_timestamp(),
            }
        }

        # Add HTTP status code if available
        if hasattr(error, "status_code"):
            error_response["error"]["status_code"] = error.status_code
        else:
            # Map common exceptions to HTTP status codes
            if isinstance(error, ValueError):
                error_response["error"]["status_code"] = HTTPStatus.BAD_REQUEST
            elif isinstance(error, FileNotFoundError):
                error_response["error"]["status_code"] = HTTPStatus.NOT_FOUND
            else:
                error_response["error"]["status_code"] = (
                    HTTPStatus.INTERNAL_SERVER_ERROR
                )

        return error_response

    def _present_customer(self, customer: CustomerResponse) -> dict:
        """Present customer data in JSON format"""
        return {
            "id": customer.id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "document": customer.document,
            "full_name": customer.full_name,
            "is_anonymous": customer.is_anonymous,
            "is_registered": customer.is_registered,
            "created_at": self._get_timestamp(),
        }

    def _present_customer_list(self, customer_list: CustomerListResponse) -> dict:
        """Present customer list data in JSON format"""
        return {
            "data": [
                self._present_customer(customer) for customer in customer_list.customers
            ],
            "total_count": customer_list.total_count,
            "timestamp": self._get_timestamp(),
        }

    def _present_generic(self, data: Any) -> dict:
        """Present generic data in JSON format"""
        if hasattr(data, "__dict__"):
            return {"data": data.__dict__, "timestamp": self._get_timestamp()}
        else:
            return {"data": str(data), "timestamp": self._get_timestamp()}

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.utcnow().isoformat() + "Z"
