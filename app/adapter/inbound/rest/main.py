import typing
import fastapi

from app.adapter.outbound.repositories.sql.implementation import customer_impl
from app.domain.use_cases import (
    customer_create_uc,
    customer_delete_uc,
    customer_read_uc,
    customer_update_uc
)
from app.domain.entities import customer_entity
from app.adapter.inbound.rest.entity import customer_rest
from app.adapter.inbound.rest.mapper import customer_rest_mapper 


app = fastapi.FastAPI()

repo_customer = customer_impl.CustomerRepoImpl()

uc_customer_create = customer_create_uc.CustomerCreate(repo_customer)
uc_customer_delete = customer_delete_uc.CustomerDelete(repo_customer)
uc_customer_read = customer_read_uc.CustomerRead(repo_customer)
uc_customer_update = customer_update_uc.CustomerUpdate(repo_customer)

@app.get('/customer/')
def customer_read(search_key, search_value):
    return uc_customer_read.read_customer(search_key, search_value)

@app.post('/customer/')
def customer_create(customer_data:customer_rest.Customer):

    customer = customer_rest_mapper.to_domain_entity(customer_data)

    return uc_customer_create.create_customer(customer)

@app.put('/customer/')
def customer_update(search_key, search_value, customer_data:customer_rest.Customer):
    
    customer = customer_rest_mapper.to_domain_entity(customer_data)

    return uc_customer_update.update_customer(search_key, search_value, customer)

@app.delete('/customer/')
def customer_delete():
    pass