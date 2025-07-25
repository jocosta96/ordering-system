from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from pydantic import BaseModel

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
    email: str
    document: str
    full_name: str


class CustomerListResponseModel(BaseModel):
    data: list[CustomerResponseModel]
    total_count: int
    timestamp: str


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


@customer_router.get("/{customer_id}", response_model=CustomerResponseModel)
def get_customer(
    customer_id: int,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[CustomerController, Depends(get_customer_controller)],
):
    """Get customer by ID endpoint"""
    return controller.get_customer(customer_id, login)


@customer_router.post("", response_model=CustomerResponseModel)
def create_customer(
    customer_data: CustomerCreateModel,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[CustomerController, Depends(get_customer_controller)],
):
    """Create customer endpoint"""
    return controller.create_customer(customer_data.dict(), login)


@customer_router.put("", response_model=CustomerResponseModel)
def update_customer(
    customer_data: CustomerUpdateModel,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[CustomerController, Depends(get_customer_controller)],
):
    """Update customer endpoint"""
    return controller.update_customer(customer_data.dict(), login)


@customer_router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[CustomerController, Depends(get_customer_controller)],
):
    """Delete customer endpoint"""
    return controller.delete_customer(customer_id, login)


@customer_router.get("", response_model=CustomerListResponseModel)
def list_customers(
    login: Annotated[str, Depends(check_credentials)],
    controller: Annotated[CustomerController, Depends(get_customer_controller)],
):
    """List all customers endpoint"""
    return controller.list_customers(login)
