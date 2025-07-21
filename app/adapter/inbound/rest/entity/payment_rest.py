from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Payment(BaseModel):

    date: Optional[datetime] = None
    transaction_id: Optional[str] = None
    approval_status: Optional[bool] = None
    message: Optional[str] = None
    order_id: str


class PaymentStatus(BaseModel):
    order_id: str
    has_payment_verified: bool
    payment_date: Optional[datetime] = None
    payment_transaction_id: Optional[str] = None
    payment_message: Optional[str] = None
    order_status: str
    order_value: float 