import typing
import fastapi

from app.adapter.outbound.repositories.sql.implementation import customer_impl
from app.domain.use_cases import customer_create_uc
from app.domain.use_cases import customer_read_uc
from app.domain.use_cases import customer_delete_uc
from app.domain.use_cases import customer_update_uc
from app.adapter.inbound.rest.v1.entity import customer_rest
from app.adapter.inbound.rest.v1.mapper import customer_rest_mapper

app = fastapi.FastAPI()

repository = customer_impl.CustomerRepoImpl()
uc_customer_create = customer_create_uc.CustomerCreate()
uc_customer_read = customer_read_uc.CustomerRead()
uc_customer_update = customer_update_uc.CustomerUpdate()
uc_customer_delete = customer_delete_uc.CustomerDelete()

@app.post('/customer/')
def create():
    pass #implementar UC

@app.patch('/customer/')
def update():
    pass

@app.delete('/customer')
def delete():
    pass

@app.get('/customer/')
def read():
    pass