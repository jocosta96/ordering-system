from datetime import datetime
from typing import Any, Dict, List
from http import HTTPStatus

from src.adapters.presenters.interfaces.presenter_interface import PresenterInterface


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
        return self._present_generic(data)

    def present_list(self, data_list: list) -> dict:
        """Present list of data as JSON"""
        if not data_list:
            return {"data": [], "total_count": 0, "timestamp": self._get_timestamp()}

        # Handle different types of lists
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

    def _present_generic(self, data: Any) -> dict:
        """Present generic data in JSON format"""
        if hasattr(data, "to_dict"):
            return data.to_dict()
        elif hasattr(data, "__dict__"):
            return data.__dict__
        else:
            return {"data": str(data), "timestamp": self._get_timestamp()}

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.utcnow().isoformat() + "Z"
