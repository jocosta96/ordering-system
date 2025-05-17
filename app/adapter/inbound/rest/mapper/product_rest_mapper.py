from decimal import Decimal

from app.domain.entities import product_entity
from app.adapter.inbound.rest.entity import product_rest

def to_domain_entity(product: product_rest.Product) -> product_entity.Product:

    domain_product = product_entity.Product(
        id = product.id,
        name= str(product.name),
        price= Decimal(product.price),
        category= str(product.category),
        sku= str(product.sku),
        codebar= str(product.codebar)
    )

    return domain_product


def to_sql_entity(product: product_entity.Product) -> product_rest.Product:

    rest_product = product_rest.Product(
        name= product.name.get(),
        price= product.price.get(),
        category= product.category.get(),
        sku= product.sku.get(),
        codebar= product.codebar.get()
    )

    return rest_product