import fastapi

from app.adapter.outbound.repositories.sql.implementation import (
    customer_impl,
    product_impl
)
from app.domain.use_cases import (
    customer_uc,
    product_uc
)
from app.adapter.inbound.rest.entity import (
    customer_rest,
    product_rest
)
from app.adapter.inbound.rest.mapper import (
    customer_rest_mapper,
    product_rest_mapper
)


repo_customer = customer_impl.CustomerRepoImpl()
uc_customer_create = customer_uc.CustomerCreate(repo_customer)
uc_customer_delete = customer_uc.CustomerDelete(repo_customer)
uc_customer_read = customer_uc.CustomerRead(repo_customer)
uc_customer_update = customer_uc.CustomerUpdate(repo_customer)

repo_product = product_impl.ProductRepoImpl()
uc_product_create = product_uc.ProductCreate(repo_product)
uc_product_delete = product_uc.ProductDelete(repo_product)
uc_product_read = product_uc.ProductRead(repo_product)
uc_product_update = product_uc.ProductUpdate(repo_product)


app = fastapi.FastAPI()

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


@app.get('/product/')
def product_read(search_key, search_value):
    return uc_product_read.read_product(search_key, search_value)

@app.post('/product/')
def product_create(product_data:product_rest.Product):

    product = product_rest_mapper.to_domain_entity(product_data)

    return uc_product_create.create_product(product)

@app.put('/product/')
def product_update(search_key, search_value, product_data:product_rest.Product):
    
    product = product_rest_mapper.to_domain_entity(product_data)

    return uc_product_update.update_product(search_key, search_value, product)

@app.delete('/product/')
def product_delete():
    pass