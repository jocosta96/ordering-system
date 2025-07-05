from app.domain.entities import ingredient_entity
from app.adapter.inbound.rest.entity import ingredient_rest
from app.domain.value_objects.money import Money
from app.domain.value_objects.name import Name


def to_domain_entity(
    ingredient: ingredient_rest.Ingredient,
) -> ingredient_entity.Ingredient:
    domain_ingredient = ingredient_entity.Ingredient(
        id=ingredient.id,
        name=ingredient.name,
        price=ingredient.price,
        product_category=ingredient.product_category,
        is_active=ingredient.is_active,
    )

    return domain_ingredient


def to_rest_entity(
    ingredient: ingredient_entity.Ingredient,
) -> ingredient_rest.Ingredient:
    print("*" * 100, ingredient.__dict__)

    rest_ingredient = ingredient_rest.Ingredient(
        id=ingredient.id,
        name=Name(name=str(ingredient.name)),
        price=Money(amount=str(ingredient.price)),
        product_category=ingredient.product_category,
        is_active=ingredient.is_active,
    )

    return rest_ingredient
