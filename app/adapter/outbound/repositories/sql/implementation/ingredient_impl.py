import typing

from sqlalchemy.orm.exc import NoResultFound
from decimal import Decimal

from app.domain.ports import ingredient_port
from app.domain.entities import ingredient_entity
from app.adapter.outbound.repositories.sql.orm import database
from app.adapter.outbound.repositories.sql.entities import ingredient_sql
from app.domain.value_objects import name, sku, codebar, money, category
from app.domain.errors.custom_errors import NotFoundError

from app.adapter.outbound.repositories.sql.implementation import sql_impl

class IngredientRepoImpl(ingredient_port.IngredientPort):

    @staticmethod
    def _to_domain_entity(ingredient: ingredient_sql.Ingredient) -> ingredient_entity.Ingredient:

        domain_ingredient = ingredient_entity.Ingredient(
            id=ingredient.id,
            name=ingredient.name,
            price=ingredient.price,
            product_category=category.ProductCategory(category=str(ingredient.product_category)),
            is_active=ingredient.is_active
        )

        return domain_ingredient

    @staticmethod
    def _to_sql_entity(ingredient: ingredient_entity.Ingredient) -> ingredient_sql.Ingredient:

        sql_ingredient = ingredient_sql.Ingredient(
            name=ingredient.name,
            price=Decimal(ingredient.price.amount),
            product_category=ingredient.product_category,
            is_active=ingredient.is_active
        )

        return sql_ingredient

    def __init__(self) -> None:
        self._sql_impl = sql_impl.SQLRepoImpl()
        self._ingredient_id = None

    def create_ingredient(self, ingredient: ingredient_entity.Ingredient) -> None:
        db_ingredient = self._to_sql_entity(ingredient)
        self._sql_impl.add_one(db_ingredient)

    def update_ingredient(self, ingredient: ingredient_entity.Ingredient) -> None:
        ingredient_dict = ingredient.__dict__.copy()
        self._sql_impl.update(
            entity=ingredient_sql.Ingredient,
            entity_dict=ingredient_dict,
            dict_filter={
                'id': ingredient_dict['id']
            }
        )

    def delete_ingredient(self, ingredient_id: int):
        self.read_ingredient(ingredient_id)
        self._sql_impl.update(
            entity=ingredient_sql.Ingredient,
            entity_dict={'is_active': False},
            dict_filter={
                'id': ingredient_id
            }
        )

    def read_ingredient(self, ingredient_id: int) -> ingredient_entity.Ingredient:
        try:
            ingredient = self._sql_impl.get_one(
                entity=ingredient_sql.Ingredient,
                dict_filter={
                    'id': ingredient_id,
                    'is_active': True
                }
            )
            if not ingredient:
                raise NoResultFound('Ingredient not found')
            result = self._to_domain_entity(ingredient)
            self._ingredient_id = result.id
            return result
        except NoResultFound:
            NotFoundError('Ingredient not found')

    def restore_deleted_ingredient(self, ingredient_id: int) -> None:
        self.read_ingredient(ingredient_id)
        self._sql_impl.update(
            entity=ingredient_sql.Ingredient,
            entity_dict={'is_active': True},
            dict_filter={
                'id': ingredient_id
            }
        )

    def list_ingredient(self, search_key=None, search_value=None) -> list[ingredient_entity.Ingredient]:
        try:
            if search_key and search_value:
                dict_filter = {
                    'is_active': True,
                    search_key: search_value
                }
            else:
                dict_filter = {'is_active': True}
            ingredients = self._sql_impl.list_all(
                entity=ingredient_sql.Ingredient,
                dict_filter=dict_filter
            )
            if not ingredients:
                raise NoResultFound('Ingredients not found')
            return [self._to_domain_entity(ing) for ing in ingredients]
        except NoResultFound:
            raise NotFoundError('Ingredients not found')
