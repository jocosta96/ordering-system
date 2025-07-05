from pydantic import BaseModel
from typing import Optional
from app.domain.value_objects import name, sku, money, category
from app.adapter.inbound.rest.entity.ingredient_rest import Ingredient
from uuid import UUID


class ProductReceiptItem(BaseModel):
    ingredient: Ingredient
    quantity: int


class Product(BaseModel):
    name: name.Name
    category: category.ProductCategory
    default_ingredient: list[ProductReceiptItem]
    price: money.Money
    sku: sku.SKU
    id: Optional[str | UUID] = None  # Accepts both str and UUID

    model_config = {
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "name": {"name": "X-Burguer"},
                "category": {"category": "LANCHE"},
                "default_ingredient": [
                    {
                        "ingredient": {
                            "id": 1,
                            "name": {"name": "ALFACE"},
                            "price": {"amount": "5.00"},
                            "product_category": {"category": "LANCHE"},
                            "is_active": True,
                        },
                        "quantity": 1,
                    },
                    {
                        "ingredient": {
                            "id": 2,
                            "name": {"name": "PAO"},
                            "price": {"amount": "5.00"},
                            "product_category": {"category": "LANCHE"},
                            "is_active": True,
                        },
                        "quantity": 2,
                    },
                    {
                        "ingredient": {
                            "id": 3,
                            "name": {"name": "QUEIJO"},
                            "price": {"amount": "5.00"},
                            "product_category": {"category": "LANCHE"},
                            "is_active": True,
                        },
                        "quantity": 3,
                    },
                ],
                "price": {"amount": 32.00},
                "sku": {"sku": "PROD-1234-XYZ"},
            }
        },
    }
