from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Payment(BaseModel):

    date: Optional[datetime] = None
    transaction_id: Optional[str] = None
    approval_status: Optional[bool] = None
    message: Optional[str] = None
    order_id: str