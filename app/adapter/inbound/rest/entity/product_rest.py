from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.domain.value_objects import name, sku, money, codebar, category
from app.adapter.inbound.rest.entity.ingredient_rest import Ingredient

class ProductReceiptItem(BaseModel):
    default_ingredient: Ingredient
    quantity: int

class Product(BaseModel):

    name: name.Name
    category: category.ProductCategory
    default_ingredient: list[ProductReceiptItem]
    price: money.Money
    sku: sku.SKU
    codebar: codebar.Codebar
    id: Optional[int] = None

