import typing

from sqlalchemy.orm.exc import NoResultFound
from decimal import Decimal

from app.domain.ports import ingredient_port
from app.domain.entities import ingredient_entity
from app.adapter.outbound.repositories.sql.orm import database
from app.adapter.outbound.repositories.sql.entities import ingredient_sql
from app.domain.value_objects import name, sku, codebar, money, category
from app.domain.errors.custom_errors import NotFoundError

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
        self._database = database.get_db()
        self._ingredient_id = None

    def try_commit(self) -> None:
        try:
            self._database.commit()
        except Exception as e:
            self._database.rollback()
            raise e

    def create_ingredient(self, ingredient: ingredient_entity.Ingredient) -> None:

        db_ingredient = self._to_sql_entity(ingredient)
        self._database.add(db_ingredient)
        self._database.commit()
        self._database.refresh(db_ingredient)

    def update_ingredient(self, ingredient: ingredient_entity.Ingredient) -> None:

        ingredient_dict = ingredient.__dict__.copy()

        self._database.query(
            ingredient_sql.Ingredient
        ).filter_by(
            id=ingredient_dict['id']
        ).update(
            ingredient_dict
        )

        self.try_commit()

    def delete_ingredient(self, ingredient_id: int):
        self.read_ingredient(ingredient_id)
        self._database.query(
            ingredient_sql.Ingredient
        ).filter_by(
            id=ingredient_id
        ).update(
            {'is_active': False}
        )

        self.try_commit()

    def read_ingredient(self, ingredient_id: int) -> ingredient_entity.Ingredient:
        try:
            ingredient = self._database.query(
                ingredient_sql.Ingredient
            ).filter_by(
                id=ingredient_id
            ).filter_by(
                is_active=True
            ).one()
            if not ingredient:
                raise NoResultFound('Ingredient not found')
            result = self._to_domain_entity(ingredient)
            self._ingredient_id = result.id
            return result
        except NoResultFound:
            NotFoundError('Ingredient not found')

    def restore_deleted_ingredient(self, ingredient_id: int) -> None:
        self.read_ingredient(ingredient_id)
        self._database.query(
            ingredient_sql.Ingredient
        ).filter_by(
            id=ingredient_id
        ).update(
            {'is_active': True}
        )

        self.try_commit()

    def list_ingredient(self, search_key=None, search_value=None) -> list[ingredient_entity.Ingredient]:
        try:
            ingredients = self._database.query(
                ingredient_sql.Ingredient
            ).filter_by(
                is_active=True
            ).filter_by(
                **{search_key: search_value}
            ).all()

            result = [self._to_domain_entity(ing) for ing in ingredients]
            return result
        except NoResultFound:
            NotFoundError('Ingredients not found')
