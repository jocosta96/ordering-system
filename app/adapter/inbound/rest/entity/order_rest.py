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


class BaseOrder(BaseModel):
    customer_id: int
    value: Money


class FullOrder(BaseModel):
    """Used in API responses — includes system-generated fields."""
    id: int
    status: Optional[OrderStatus]
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    has_payment_verified: bool
    customer_id: int
    value: Money
