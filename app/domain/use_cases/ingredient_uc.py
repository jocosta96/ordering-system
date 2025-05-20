from app.domain.ports import ingredient_port
from app.domain.entities import ingredient_entity

class BaseIngredientUseCase():

    def __init__(
        self,
        port: ingredient_port.IngredientPort
    ) -> None:
        self.port = port

class IngredientCreate(BaseIngredientUseCase):

    def create_ingredient(self, ingredient: ingredient_entity.Ingredient) -> int:
        return self.port.create_ingredient(ingredient)


class IngredientDelete(BaseIngredientUseCase):

    def check_ingredient():
        pass

    def delete_ingredient(self, ingredient: ingredient_entity.Ingredient) -> int:
        return self.port.delete_ingredient(ingredient)
    
class IngredientRead(BaseIngredientUseCase):

    def read_ingredient(self, seach_key, search_value) -> ingredient_entity.Ingredient:

        key = seach_key.strip().lower()

        return self.port.read_ingredient(key, search_value)
    
class IngredientUpdate(BaseIngredientUseCase):

    def update_ingredient(self, search_key, search_value, ingredient: ingredient_entity.Ingredient) -> None:

        return self.port.update_ingredient(search_key, search_value, ingredient)