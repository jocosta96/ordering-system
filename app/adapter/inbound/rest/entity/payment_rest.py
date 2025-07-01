from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.domain.value_objects import money

class Payment(BaseModel):

    payment_date: Optional[datetime] = None
    payment_transaction_id: Optional[str] = None
    has_payment_verified: bool