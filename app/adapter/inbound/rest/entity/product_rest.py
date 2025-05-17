from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.domain.value_objects import name, sku, money, codebar

class Product(BaseModel):

    name: name.Name
    category: str
    price: money.Money
    sku: sku.SKU
    codebar: codebar.Codebar
    id: Optional[int] = None

