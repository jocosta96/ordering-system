from app.domain.ports import ingredient_port
from app.domain.entities import ingredient_entity


class BaseIngredientUseCase:
    def __init__(self, port: ingredient_port.IngredientPort) -> None:
        self.port = port


class IngredientCreate(BaseIngredientUseCase):
    def create_ingredient(self, ingredient: ingredient_entity.Ingredient) -> int:
        return self.port.create_ingredient(ingredient)


class IngredientDelete(BaseIngredientUseCase):
    def delete_ingredient(self, ingredient_id) -> int:
        return self.port.delete_ingredient(ingredient_id)


class IngredientRead(BaseIngredientUseCase):
    def read_ingredient(self, ingredient_id: int) -> ingredient_entity.Ingredient:
        return self.port.read_ingredient(ingredient_id)


class IngredientUpdate(BaseIngredientUseCase):
    def update_ingredient(self, ingredient: ingredient_entity.Ingredient) -> int:
        return self.port.update_ingredient(ingredient)


class IngredientRestoreDeleted(BaseIngredientUseCase):
    def restore_deleted_ingredient(
        self, ingredient: ingredient_entity.Ingredient
    ) -> int:
        return self.port.restore_deleted_ingredient(ingredient)


class IngredientList(BaseIngredientUseCase):
    def list_ingredient(self, search_key=None, search_value=None):
        return self.port.list_ingredient(search_key, search_value)
