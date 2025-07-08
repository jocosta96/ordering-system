from fastapi import APIRouter, HTTPException, Depends
from http import HTTPStatus
from typing_extensions import Annotated

from app.adapter.outbound.repositories.sql.implementation import customer_impl
from app.domain.use_cases import customer_uc
from app.adapter.inbound.rest.entity import customer_rest
from app.adapter.inbound.rest.mapper import customer_rest_mapper
from app.domain.errors.custom_errors import NotFoundError
from app.adapter.inbound.rest.controllers.security import check_credentials, raise_not_authorized

repo_customer = customer_impl.CustomerRepoImpl()
uc_customer_create = customer_uc.CustomerCreate(repo_customer)
uc_customer_delete = customer_uc.CustomerDelete(repo_customer)
uc_customer_read = customer_uc.CustomerRead(repo_customer)
uc_customer_update = customer_uc.CustomerUpdate(repo_customer)
uc_customer_list = customer_uc.CustomerList(repo_customer)

customer = APIRouter(tags=["customer"], prefix="/customer")

@customer.get("/anonymous")
def get_anonymous_customer() -> customer_rest.Customer:
    try:
        customer_obj = repo_customer.get_anonymous_customer()
        return customer_rest_mapper.to_rest_entity(customer_obj)
    except NotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Not found anonymous customer"
        )


@customer.get("/{customer_id}")
async def customer_read(
    customer_id: int, login: Annotated['str', Depends(check_credentials)]
) -> customer_rest.Customer:

    if not login:
        raise_not_authorized()

    try:
        customer_obj = uc_customer_read.read_customer(customer_id)
        if not customer_obj:
            raise NotFoundError("Customer not found")
        return customer_rest_mapper.to_rest_entity(customer_obj)
    except NotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Not found customer"
        )


@customer.post("")
async def customer_create(
    customer_data: customer_rest.Customer,
    login: Annotated['str', Depends(check_credentials)]
):
    if not login:
        raise_not_authorized()

    customer = customer_rest_mapper.to_domain_entity(customer_data)
    return uc_customer_create.create_customer(customer)


@customer.put("")
async def customer_update(
    customer_data: customer_rest.Customer,
    login: Annotated['str', Depends(check_credentials)]
):
    if not login:
        raise_not_authorized()

    customer = customer_rest_mapper.to_domain_entity(customer_data)
    return uc_customer_update.update_customer(customer)


@customer.delete("/{customer_id}")
async def customer_delete(
    customer_id: int,
    login: Annotated['str', Depends(check_credentials)]
):
    
    if not login:
        raise_not_authorized()

    try:
        return uc_customer_delete.delete_customer(customer_id)
    except NotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Not found customer"
        )
