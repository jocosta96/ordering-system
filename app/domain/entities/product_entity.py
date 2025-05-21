from app.domain.value_objects.name import Name
from app.domain.value_objects.sku import SKU
from app.domain.value_objects.money import Money
from app.domain.value_objects.codebar import Codebar
from app.domain.value_objects.category import ProductCategory
from app.domain.entities.ingredient_entity import Ingredient


class Product:

    def __init__(
        self,
        name: Name,
        price: Money,
        category: ProductCategory,
        sku: SKU,
        codebar: Codebar,
        default_ingredient: list[Ingredient],
        id:int=None
    ):
        
        self.name = name
        self.price = price
        self.category = category
        self.sku = sku
        self.codebar =codebar
        self.id = id
        self.default_ingredient = default_ingredient
