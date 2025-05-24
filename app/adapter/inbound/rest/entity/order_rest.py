from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.domain.value_objects.money import Money
from app.domain.value_objects.status import OrderStatus


from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.domain.value_objects.money import Money
from app.domain.value_objects.status import OrderStatus
from app.adapter.inbound.rest.entity.ingredient_rest import Ingredient
from app.adapter.inbound.rest.entity.product_rest import Product


class OrderItem(BaseModel):
    id: Optional[str] = None
    order_id: Optional[str] = None
    product: Product
    additional_ingredient: list[Ingredient]
    remove_ingredient: list[Ingredient]
    price: Money

    model_config = {
        "arbitrary_types_allowed": True
    }


class Order(BaseModel):
    id: Optional[str] = None
    customer_id: int
    value: Money
    status: OrderStatus
    payment_date: Optional[datetime] = None
    payment_transaction_id: Optional[str] = None
    has_payment_verified: bool
    order_items: list[OrderItem]

    model_config = {
        "arbitrary_types_allowed": True
    }