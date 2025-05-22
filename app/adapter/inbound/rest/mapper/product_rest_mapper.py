from app.domain.entities import product_entity
from app.adapter.inbound.rest.entity import product_rest
from app.domain.value_objects import category, name, money, sku, codebar

def to_domain_entity(product: product_rest.Product) -> product_entity.Product:

    print('***'*100, type(product.default_ingredient), product.default_ingredient)

    domain_product = product_entity.Product(
        id = product.id,
        name= product.name,
        price= product.price,
        category= product.category,
        sku= product.sku,
        codebar= product.codebar,
        default_ingredient= product.default_ingredient
    )

    return domain_product


def to_rest_entity(product: product_entity.Product) -> product_rest.Product:

    print('***'*100, product)

    rest_product = product_rest.Product(
        name= product.name,
        price= product.price,
        category= product.category,
        sku= product.sku,
        codebar= product.codebar,
        id=product.id
    )

    return rest_product