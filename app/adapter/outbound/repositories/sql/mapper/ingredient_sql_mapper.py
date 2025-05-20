from decimal import Decimal

from app.domain.entities import ingredient_entity
from app.domain.value_objects import name, sku, codebar, money, category
from app.adapter.outbound.repositories.sql.entities import ingredient_sql

def to_domain_entity(ingredient: ingredient_sql.Ingredient) -> ingredient_entity.Ingredient:

    print('*'*100, ingredient)

    domain_ingredient = ingredient_entity.Ingredient(
        id = ingredient.id,
        name = ingredient.name,
        price = ingredient.price,
        product_category = ingredient.product_category,
        is_active = ingredient.is_active
    )

    return domain_ingredient


def to_sql_entity(ingredient: ingredient_entity.Ingredient) -> ingredient_sql.Ingredient:

    sql_ingredient = ingredient_sql.Ingredient(
        name = ingredient.name,
        price = Decimal(ingredient.price.amount),
        product_category = ingredient.product_category,
        is_active = ingredient.is_active
    )

    return sql_ingredient