from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import Annotated
from pydantic import BaseModel, validator
from typing import Optional
import uuid

from src.adapters.controllers.customer_controller import CustomerController
from src.security.http_auth import check_credentials


# Pydantic models for request/response validation
class CustomerCreateModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    document: str


class CustomerUpdateModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    document: str


class CustomerResponseModel(BaseModel):
    id: Optional[str]
    first_name: str
    last_name: str
    email: str
    document: str
    full_name: str
    is_anonymous: bool
    is_registered: bool
    is_active: bool
    created_at: Optional[str]


class CustomerListResponseModel(BaseModel):
    data: list[CustomerResponseModel]
    total_count: int
    timestamp: str


# UUID validation function
def validate_uuid(customer_id: str) -> str:
    """Validate that customer_id is a valid UUID format"""
    try:
        uuid.UUID(customer_id)
        return customer_id
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "message": f"Invalid customer ID format: '{customer_id}'. Customer ID must be a valid UUID (e.g., '550e8400-e29b-41d4-a716-446655440000').",
                    "type": "CustomerValidationException",
                    "status_code": 400
                }
            }
        )


# Dependency injection function
def get_customer_controller() -> CustomerController:
    """Dependency injection for customer controller"""
    from src.adapters.di.container import container
    from src.adapters.presenters.implementations.json_presenter import JSONPresenter

    return CustomerController(container.customer_repository, JSONPresenter())


# Create router
customer_router = APIRouter(tags=["customer"], prefix="/customer")


@customer_router.get("/anonymous", response_model=CustomerResponseModel)
def get_anonymous_customer(
    controller: Annotated[CustomerController, Depends(get_customer_controller)]
):
    """Get anonymous customer endpoint"""
    return controller.get_anonymous_customer()


@customer_router.get("/list", response_model=CustomerListResponseModel)
def list_customers(
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[CustomerController, Depends(get_customer_controller)],
    include_inactive: bool = False,
):
    """List all customers endpoint"""
    return controller.list_customers(login, include_inactive=include_inactive)


@customer_router.get("/by-id/{customer_id}", response_model=CustomerResponseModel)
def get_customer(
    customer_id: str,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[CustomerController, Depends(get_customer_controller)],
    include_inactive: bool = False,
):
    """Get customer by ID endpoint"""
    # Validate UUID format before passing to controller
    validate_uuid(customer_id)
    return controller.get_customer(customer_id, login, include_inactive=include_inactive)


@customer_router.post("/create", response_model=CustomerResponseModel)
def create_customer(
    customer_data: CustomerCreateModel,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[CustomerController, Depends(get_customer_controller)],
):
    """Create customer endpoint"""
    return controller.create_customer(customer_data.dict(), login)


@customer_router.put("/update", response_model=CustomerResponseModel)
def update_customer(
    customer_data: CustomerUpdateModel,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[CustomerController, Depends(get_customer_controller)],
):
    """Update customer endpoint"""
    return controller.update_customer(customer_data.dict(), login)


@customer_router.delete("/delete/{customer_id}")
def delete_customer(
    customer_id: str,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[CustomerController, Depends(get_customer_controller)],
):
    """Delete customer endpoint"""
    # Validate UUID format before passing to controller
    validate_uuid(customer_id)
    return controller.delete_customer(customer_id, login)
