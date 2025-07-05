from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Payment(BaseModel):
    payment_date: Optional[datetime] = None
    payment_transaction_id: Optional[str] = None
    order_id: str
