from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.domain.value_objects import name, sku, money, codebar

class Product(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        title="Product",
        json_schema_extra={
            "example": {
                "name": "T-Shirt",
                "category": "Clothing",
                "price": "129.99",
                "sku": "PROD-1234-XYZ",
                "codebar": "7891234567895",
                "id": 1
            }
        }
    )

    name: name.Name
    category: str
    price: money.Money
    sku: sku.SKU
    codebar: codebar.Codebar
    id: Optional[int] = None

