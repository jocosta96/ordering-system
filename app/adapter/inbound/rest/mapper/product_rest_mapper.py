from app.domain.entities import product_entity
from app.adapter.inbound.rest.entity import product_rest
from app.domain.value_objects import category, name, money, sku

def to_domain_entity(product: product_rest.Product) -> product_entity.Product:
    # Convert REST ProductReceiptItem to domain ProductReceiptItem
    domain_default_ingredient = [
        product_entity.ProductReceiptItem(
            ingredient_id=item.ingredient_id,  # Get the id from Ingredient
            quantity=item.quantity
        )
        for item in product.default_ingredient
    ]

    domain_product = product_entity.Product(
        id=product.id,
        name=product.name,
        price=product.price,
        category=product.category,
        sku=product.sku,
        default_ingredient=domain_default_ingredient
    )

    return domain_product


def to_rest_entity(product: product_entity.Product) -> product_rest.Product:

    print('***'*100, product)

    rest_product_receipt = [
        product_rest.ProductReceiptItem(
            ingredient_id=item.ingredient_id,
            quantity=item.quantity
        )
        for item in product.default_ingredient
    ]

    rest_product = product_rest.Product(
        name=product.name,
        price=product.price,
        category=product.category,
        sku=product.sku,
        id=product.id,
        default_ingredient=rest_product_receipt
    )

    return rest_product