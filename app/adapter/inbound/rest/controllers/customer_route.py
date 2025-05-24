from fastapi import APIRouter

from app.adapter.outbound.repositories.sql.implementation import customer_impl
from app.domain.use_cases import customer_uc
from app.adapter.inbound.rest.entity import customer_rest
from app.adapter.inbound.rest.mapper import customer_rest_mapper


repo_customer = customer_impl.CustomerRepoImpl()
uc_customer_create = customer_uc.CustomerCreate(repo_customer)
uc_customer_delete = customer_uc.CustomerDelete(repo_customer)
uc_customer_read = customer_uc.CustomerRead(repo_customer)
uc_customer_update = customer_uc.CustomerUpdate(repo_customer)

customer = APIRouter(tags=["customer"], prefix="/customer")

@customer.get('', response_model=customer_rest.Customer)
def customer_read(search_key, search_value):
    customer_rest_obj = uc_customer_read.read_customer(search_key, search_value)
    customer = customer_rest_mapper.to_domain_entity(customer_rest_obj)
    return customer

@customer.post('')
def customer_create(customer_data:customer_rest.Customer):

    customer = customer_rest_mapper.to_domain_entity(customer_data)

    return uc_customer_create.create_customer(customer)

@customer.put('')
def customer_update(search_key, search_value, customer_data:customer_rest.Customer):
    
    customer = customer_rest_mapper.to_domain_entity(customer_data)

    return uc_customer_update.update_customer(search_key, search_value, customer)

@customer.delete('')
def customer_delete(search_key, search_value):
    
    return uc_customer_delete.delete_customer(search_key, search_value)

