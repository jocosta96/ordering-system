from fastapi import APIRouter
from app.adapter.outbound.repositories.sql.implementation import product_impl
from app.domain.use_cases import product_uc
from app.adapter.inbound.rest.entity import product_rest
from app.adapter.inbound.rest.mapper import product_rest_mapper


repo_product = product_impl.ProductRepoImpl()
uc_product_create = product_uc.ProductCreate(repo_product)
uc_product_delete = product_uc.ProductDelete(repo_product)
uc_product_restore = product_uc.ProductRestoreDeleted(repo_product)
uc_product_read = product_uc.ProductRead(repo_product)
uc_product_update = product_uc.ProductUpdate(repo_product)
uc_product_list = product_uc.ProductList(repo_product)

product = APIRouter(prefix="/product", tags=["product"])

@product.get("/list")
async def product_list(search_key, search_value):
    products = uc_product_list.list_product(
        search_key=search_key, 
        search_value=search_value
    )
    return [product_rest_mapper.to_rest_entity(p) for p in products]

@product.get("/{product_id}")
async def product_read(product_id):
    product = uc_product_read.read_product(product_id)
    return product_rest_mapper.to_rest_entity(product)

@product.post('')
async def product_create(product_data:product_rest.Product):
    product = product_rest_mapper.to_domain_entity(product_data)
    return uc_product_create.create_product(product)

@product.put('')
async def product_update(product_data:product_rest.Product):
    product = product_rest_mapper.to_domain_entity(product_data)
    return uc_product_update.update_product(product)

@product.delete('/{product_id}')
async def product_delete(product_id: str):
    return uc_product_delete.delete_product(product_id)

@product.patch('/restore/{product_id}')
async def product_restore_deleted(product_id: str):
    return uc_product_restore.restore_deleted_product(product_id)
