import abc

from app.domain.entities import ingredient_entity


class IngredientPort(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_ingredient(self) -> ingredient_entity.Ingredient:
        raise NotImplementedError
    
    @abc.abstractmethod
    def read_ingredient(self) -> ingredient_entity.Ingredient:
        raise NotImplementedError
    
    @abc.abstractmethod
    def update_ingredient(self) -> ingredient_entity.Ingredient:
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete_ingredient(self) -> ingredient_entity.Ingredient:
        raise NotImplementedError