from decimal import Decimal

from app.domain.entities import product_entity
from app.adapter.inbound.rest.entity import product_rest

def to_domain_entity(product: product_rest.Product) -> product_entity.Product:

    domain_product = product_entity.Product(
        id = product.id,
        name= product.name,
        price= product.price,
        category= product.category,
        sku= product.sku,
        codebar= product.codebar
    )

    return domain_product


def to_sql_entity(product: product_entity.Product) -> product_rest.Product:

    rest_product = product_rest.Product(
        name= product.name.value,
        price= product.price.value,
        category= product.category.value,
        sku= product.sku.value,
        codebar= product.codebar.value
    )

    return rest_product