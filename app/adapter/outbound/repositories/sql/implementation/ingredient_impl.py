import typing
from sqlalchemy.orm.exc import NoResultFound

from app.domain.ports import ingredient_port
from app.domain.entities import ingredient_entity
from app.adapter.outbound.repositories.sql.orm import database
from app.adapter.outbound.repositories.sql.entities import ingredient_sql
from app.adapter.outbound.repositories.sql.mapper import ingredient_sql_mapper


class IngredientRepoImpl(ingredient_port.IngredientPort):

    def __init__(self) -> None:
        self._database = database.get_db()
        self._user_id = None
    
    def create_ingredient(self, ingredient: ingredient_entity.Ingredient) -> None:

        db_ingredient = ingredient_sql_mapper.to_sql_entity(ingredient)
        self._database.add(db_ingredient)
        self._database.commit()
        self._database.refresh(db_ingredient)

    def update_ingredient(self, search_key, search_value, ingredient: ingredient_entity.Ingredient) -> None:

        self.read_ingredient(search_key, search_value)

        ingredient_dict = ingredient.__dict__.copy()
        ingredient_dict.pop('id', None)

        self._database.query(
            ingredient_sql.Ingredient
        ).filter_by(
            id=self._user_id
        ).update(
            ingredient_dict
        )

        self._database.commit()

    def delete_ingredient(self):
        
        self._database.query(
            ingredient_sql.Ingredient
        ).filter_by(
            id=self._user_id
        ).delete()
        
        self._database.commit()
        
    def read_ingredient(self, search_key, search_value) -> ingredient_entity.Ingredient:
        
        try:
            data = self._database.query(ingredient_sql.Ingredient).filter_by(**{search_key:search_value}).one()
            result = ingredient_sql_mapper.to_domain_entity(data)
            self._user_id = result.id
        except NoResultFound:
            result = 'User not found'
        return result
