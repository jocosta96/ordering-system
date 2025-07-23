from fastapi import APIRouter, HTTPException, Depends
from http import HTTPStatus
from typing_extensions import Annotated

from src.application.use_cases.customer_use_cases import (
    CustomerCreateUseCase,
    CustomerReadUseCase,
    CustomerUpdateUseCase,
    CustomerDeleteUseCase,
    CustomerListUseCase,
    CustomerGetAnonymousUseCase,
)
from src.application.dto.customer_dto import (
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerResponse,
    CustomerListResponse,
)
from src.application.repositories.customer_repository import CustomerRepository
from src.adapters.presenters.interfaces.presenter_interface import PresenterInterface


class CustomerController:
    """
    Customer controller that handles HTTP requests.

    In Clean Architecture:
    - This is part of the Interface Adapters layer
    - It handles HTTP-specific concerns
    - It delegates business logic to use cases
    - It converts between HTTP data and application DTOs
    """

    def __init__(
        self, customer_repository: CustomerRepository, presenter: PresenterInterface
    ):
        self.customer_repository = customer_repository
        self.presenter = presenter
        self.create_use_case = CustomerCreateUseCase(customer_repository)
        self.read_use_case = CustomerReadUseCase(customer_repository)
        self.update_use_case = CustomerUpdateUseCase(customer_repository)
        self.delete_use_case = CustomerDeleteUseCase(customer_repository)
        self.list_use_case = CustomerListUseCase(customer_repository)
        self.anonymous_use_case = CustomerGetAnonymousUseCase(customer_repository)

    def get_anonymous_customer(self) -> dict:
        """Get anonymous customer endpoint"""
        try:
            customer = self.anonymous_use_case.execute()
            return self.presenter.present(customer)
        except ValueError as e:
            error_response = self.presenter.present_error(e)
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=error_response)

    def get_customer(self, customer_id: int, login: str) -> dict:
        """Get customer by ID endpoint"""
        if not login:
            error_response = self.presenter.present_error(
                ValueError("Authentication required")
            )
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail=error_response
            )

        try:
            customer = self.read_use_case.execute(customer_id)
            return self.presenter.present(customer)
        except ValueError as e:
            error_response = self.presenter.present_error(e)
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=error_response)

    def create_customer(self, customer_data: dict, login: str) -> dict:
        """Create customer endpoint"""
        if not login:
            error_response = self.presenter.present_error(
                ValueError("Authentication required")
            )
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail=error_response
            )

        try:
            request = CustomerCreateRequest(
                first_name=customer_data.get("first_name", ""),
                last_name=customer_data.get("last_name", ""),
                email=customer_data.get("email", ""),
                document=customer_data.get("document", ""),
            )
            customer = self.create_use_case.execute(request)
            return self.presenter.present(customer)
        except ValueError as e:
            error_response = self.presenter.present_error(e)
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail=error_response
            )

    def update_customer(self, customer_data: dict, login: str) -> dict:
        """Update customer endpoint"""
        if not login:
            error_response = self.presenter.present_error(
                ValueError("Authentication required")
            )
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail=error_response
            )

        try:
            request = CustomerUpdateRequest(
                id=customer_data.get("id"),
                first_name=customer_data.get("first_name", ""),
                last_name=customer_data.get("last_name", ""),
                email=customer_data.get("email", ""),
                document=customer_data.get("document", ""),
            )
            customer = self.update_use_case.execute(request)
            return self.presenter.present(customer)
        except ValueError as e:
            error_response = self.presenter.present_error(e)
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail=error_response
            )

    def delete_customer(self, customer_id: int, login: str) -> dict:
        """Delete customer endpoint"""
        if not login:
            error_response = self.presenter.present_error(
                ValueError("Authentication required")
            )
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail=error_response
            )

        try:
            success = self.delete_use_case.execute(customer_id)
            return self.presenter.present(
                {"success": success, "message": "Customer deleted successfully"}
            )
        except ValueError as e:
            error_response = self.presenter.present_error(e)
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=error_response)

    def list_customers(self, login: str) -> dict:
        """List all customers endpoint"""
        if not login:
            error_response = self.presenter.present_error(
                ValueError("Authentication required")
            )
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail=error_response
            )

        try:
            customer_list = self.list_use_case.execute()
            return self.presenter.present(customer_list)
        except Exception as e:
            error_response = self.presenter.present_error(e)
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=error_response
            )
