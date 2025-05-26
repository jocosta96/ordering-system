from app.domain.value_objects.money import Money
from app.domain.value_objects.name import Name
from app.domain.value_objects.category import ProductCategory
from pydantic_core import core_schema

class Ingredient:

    def __init__(
        self,
        id: int,
        name: Name,
        price: Money,
        product_category: ProductCategory,
        is_active: bool
    ):
        self.id = id
        self.name = name
        self.price = price
        self.product_category = product_category
        self._is_active = is_active

    @property
    def is_active(self) -> bool:
        """Check if the ingredient is active."""
        return self._is_active
