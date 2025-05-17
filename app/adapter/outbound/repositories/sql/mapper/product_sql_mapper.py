from decimal import Decimal

from app.domain.entities import product_entity
from app.adapter.outbound.repositories.sql.entities import product_sql

def to_domain_entity(product: product_sql.Product) -> product_entity.Product:

    domain_product = product_entity.Product(
        id = product.id,
        name= str(product.name),
        price= Decimal(product.price),
        category= str(product.category),
        sku= str(product.sku),
        codebar= str(product.codebar)
    )

    return domain_product


def to_sql_entity(product: product_entity.Product) -> product_sql.Product:

    sql_product = product_sql.Product(
        name= product.name.get(),
        price= product.price.get(),
        category= product.category.get(),
        sku= product.sku.get(),
        codebar= product.codebar.get()
    )

    return sql_product