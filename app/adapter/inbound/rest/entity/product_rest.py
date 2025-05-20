from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.domain.value_objects import name, sku, money, codebar, category


class Product(BaseModel):

    name: name.Name
    category: category.ProductCategory
    price: money.Money
    sku: sku.SKU
    codebar: codebar.Codebar
    id: Optional[int] = None

