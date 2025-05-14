import typing
import fastapi

from app.adapter.outbound.repositories.sql.implementation import customer_impl
from app.domain.use_cases import (
    customer_create_uc,
    customer_delete_uc,
    customer_read_uc,
    customer_update_uc
)
from app.adapter.inbound.rest.entity import customer_rest
from app.adapter.inbound.rest.mapper import customer_rest_mapper 


app = fastapi.FastAPI()

repo_customer = customer_impl.CustomerRepoImpl()

uc_customer_create = customer_create_uc.CustomerCreate(repo_customer)
uc_customer_delete = customer_delete_uc.CustomerDelete(repo_customer)
uc_customer_read = customer_read_uc.CustomerRead(repo_customer)
uc_customer_update = customer_update_uc.CustomerUpdate(repo_customer)

@app.get('/customer/')
def customer_read(login_type, login_key):
    return uc_customer_read.read_customer(login_type, login_key)

@app.post('/customer/')
def customer_create():
    pass

@app.patch('/customer/')
def customer_update():
    pass

@app.delete('/customer/')
def customer_delete():
    pass