from app.domain.entities import product_entity, ingredient_entity
from app.adapter.inbound.rest.entity import product_rest
from app.domain.value_objects import category, name, money, sku

def to_domain_entity(product: product_rest.Product) -> product_entity.Product:

    domain_default_ingredient = [
        product_entity.ProductReceiptItem(
            ingredient=ingredient_entity.Ingredient(
                id=item.ingredient.id,
                name=name.Name(name=str(item.ingredient.name)), 
                price=money.Money(amount=str(item.ingredient.price)),
                product_category=category.ProductCategory(
                    category=str(item.ingredient.product_category)
                ),
                is_active=item.ingredient.is_active  
            ),
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

    rest_product_receipt = [
        product_rest.ProductReceiptItem(
            ingredient=product_rest.Ingredient(
                id=item.ingredient.id,
                name=name.Name(name=str(item.ingredient.name)),
                price=money.Money(amount=str(item.ingredient.price)),
                product_category=category.ProductCategory(
                    category=str(item.ingredient.product_category)
                ),
                is_active=item.ingredient.is_active
            ),
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