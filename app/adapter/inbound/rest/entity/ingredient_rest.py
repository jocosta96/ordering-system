from pydantic import BaseModel
from typing import Optional

from app.domain.value_objects import money, category, name


class Ingredient(BaseModel):

    id: Optional[int] = None
    name: name.Name
    price: money.Money
    product_category: category.ProductCategory
    is_active: bool = True

    model_config = {
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example":   {
                "name": {
                    "name": "ALFACE"
                },
                "price": {
                    "amount": "5.00"
                },
                "product_category": {
                    "category": "LANCHE"
                },
                "is_active": True
  
            }
        }
    }   