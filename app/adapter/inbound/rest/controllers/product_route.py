from fastapi import APIRouter

from app.adapter.outbound.repositories.sql.implementation import product_impl
from app.domain.use_cases import product_uc
from app.adapter.inbound.rest.entity import product_rest
from app.adapter.inbound.rest.mapper import product_rest_mapper


repo_product = product_impl.ProductRepoImpl()
uc_product_create = product_uc.ProductCreate(repo_product)
uc_product_delete = product_uc.ProductDelete(repo_product)
uc_product_read = product_uc.ProductRead(repo_product)
uc_product_update = product_uc.ProductUpdate(repo_product)

product = APIRouter(tags=["product"], prefix="/product")

@product.get('')
def product_read(search_key, search_value):

    product_rest = uc_product_read.read_product(search_key, search_value)

    product = product_rest_mapper.to_domain_entity(product_rest)

    return product

@product.post('')
def product_create(product_data:product_rest.Product):

    product = product_rest_mapper.to_domain_entity(product_data)

    return uc_product_create.create_product(product)

@product.put('')
def product_update(search_key, search_value, product_data:product_rest.Product):
    
    product = product_rest_mapper.to_domain_entity(product_data)

    return uc_product_update.update_product(search_key, search_value, product)

@product.delete('')
def product_delete():
    pass
