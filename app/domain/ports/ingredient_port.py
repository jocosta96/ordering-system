import abc

from app.domain.entities import ingredient_entity


class IngredientPort(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_ingredient(self, ingredient: ingredient_entity.Ingredient) -> ingredient_entity.Ingredient:
        raise NotImplementedError

    @abc.abstractmethod
    def read_ingredient(self, ingredient_id: int) -> ingredient_entity.Ingredient:
        raise NotImplementedError

    @abc.abstractmethod
    def update_ingredient(self, ingredient: ingredient_entity.Ingredient) -> ingredient_entity.Ingredient:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_ingredient(self, ingredient_id: int) -> ingredient_entity.Ingredient:
        raise NotImplementedError

    @abc.abstractmethod
    def restore_deleted_ingredient(self, ingredient: ingredient_entity.Ingredient) -> ingredient_entity.Ingredient:
        raise NotImplementedError

    @abc.abstractmethod
    def list_ingredient(self, search_key, search_value) -> list[ingredient_entity.Ingredient]:
        raise NotImplementedError
