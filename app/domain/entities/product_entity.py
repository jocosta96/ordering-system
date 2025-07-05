from app.domain.value_objects.name import Name
from app.domain.value_objects.sku import SKU
from app.domain.value_objects.money import Money
from app.domain.value_objects.category import ProductCategory
from app.domain.entities.ingredient_entity import Ingredient
import uuid


class ProductReceiptItem:
    def __init__(self, ingredient: Ingredient, quantity: int):
        self.ingredient = ingredient
        self.quantity = quantity

    def __tuple__(self):
        return self.ingredient, self.quantity


class Product:
    def __init__(
        self,
        name: Name,
        price: Money,
        category: ProductCategory,
        sku: SKU,
        default_ingredient: list[ProductReceiptItem],
        id: str | uuid.UUID = None,
    ):
        self.id = uuid.UUID(str(id)) if id else uuid.uuid4()
        self.name = name
        self.price = price
        self.category = category
        self.sku = sku
        self.default_ingredient = default_ingredient
