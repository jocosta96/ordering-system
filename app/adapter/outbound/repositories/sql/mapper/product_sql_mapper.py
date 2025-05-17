from decimal import Decimal

from app.domain.entities import product_entity
from app.domain.value_objects import name, sku, codebar, money
from app.adapter.outbound.repositories.sql.entities import product_sql

def to_domain_entity(product: product_sql.Product) -> product_entity.Product:

    domain_product = product_entity.Product(
        id = product.id,
        name= name.Name(str(product.name)),
        price= money(float(product.price)),
        category= name.Name(str(product.category)),
        sku= sku.SKU(str(product.sku)),
        codebar= codebar.Codebar(str(product.codebar))
    )

    return domain_product


def to_sql_entity(product: product_entity.Product) -> product_sql.Product:

    sql_product = product_sql.Product(
        name= product.name.value,
        price= product.price.value,
        category= product.category,
        sku= product.sku.value,
        codebar= product.codebar.value
    )

    return sql_product