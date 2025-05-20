from pydantic import BaseModel
from typing import Optional

from app.domain.value_objects import money, category, name


class Ingredient(BaseModel):

    id: Optional[int] 
    name: name.Name
    price: money.Money
    product_category: category.ProductCategory
    is_active: bool