from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from typing import List

from app.adapter.outbound.repositories.sql.implementation import customer_impl
from app.domain.use_cases import customer_uc
from app.adapter.inbound.rest.entity import customer_rest
from app.adapter.inbound.rest.mapper import customer_rest_mapper
from app.domain.errors.custom_errors import NotFoundError

repo_customer = customer_impl.CustomerRepoImpl()
uc_customer_create = customer_uc.CustomerCreate(repo_customer)
uc_customer_delete = customer_uc.CustomerDelete(repo_customer)
uc_customer_read = customer_uc.CustomerRead(repo_customer)
uc_customer_update = customer_uc.CustomerUpdate(repo_customer)
uc_customer_list = customer_uc.CustomerList(repo_customer)

customer = APIRouter(tags=["customer"], prefix="/customer")

@customer.get("/list")
async def list_customer(search_key=None, search_value=None) -> List[customer_rest.Customer]:
    try:
        customers = uc_customer_list.list_customer(search_key, search_value)
        return [customer_rest_mapper.to_rest_entity(cust) for cust in customers]
    except NotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not found customers')

@customer.get("/{customer_id}")
async def customer_read(customer_id: int) -> customer_rest.Customer:
    try:
        customer_obj = uc_customer_read.read_customer(customer_id)
        if not customer_obj:
            raise NotFoundError('Customer not found')
        return customer_rest_mapper.to_rest_entity(customer_obj)
    except NotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not found customer')

@customer.post('')
async def customer_create(customer_data: customer_rest.Customer):
    customer = customer_rest_mapper.to_domain_entity(customer_data)
    return uc_customer_create.create_customer(customer)

@customer.put('')
async def customer_update(customer_data: customer_rest.Customer):
    customer = customer_rest_mapper.to_domain_entity(customer_data)
    return uc_customer_update.update_customer(customer)

@customer.delete('/{customer_id}')
async def customer_delete(customer_id: int):
    try:
        return uc_customer_delete.delete_customer(customer_id)
    except NotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Not found customer')

