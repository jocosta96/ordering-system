from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.domain.value_objects import name, sku, money, codebar, category
from app.adapter.inbound.rest.entity.ingredient_rest import Ingredient
from uuid import UUID

class ProductReceiptItem(BaseModel):
    ingredient_id: int
    quantity: int

class Product(BaseModel):

    name: name.Name
    category: category.ProductCategory
    default_ingredient: list[ProductReceiptItem]
    price: money.Money
    sku: sku.SKU
    codebar: codebar.Codebar
    id: Optional[str | UUID] = None  # Accepts both str and UUID

    class Config:
        schema_extra = {
            "example": {
                "name": { "name": "X-Burger" },
                "category": { "category": "LANCHE" },
                "default_ingredient": [
                    { "ingredient_id": 1, "quantity": 2 },
                    { "ingredient_id": 2, "quantity": 1 }
                ],
                "price": { "amount": 12.5 },
                "sku": { "sku": "PROD-1238-XYZ" },
                "codebar": { "code": "4006381333931" }
            }
        }
