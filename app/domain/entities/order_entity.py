from datetime import datetime
from app.domain.value_objects.money import Money


class Order:

    def __init__(
        self,
        id: int,
        customer_id: int,
        status: str, #(RECEBIDO, EM_PREPARACAO, PRONTO, FINALIZADO)
        start_date: datetime,
        end_date: datetime,
        value: Money,
        has_payment_verified: bool
    ):
        
        self.id = id
        self.customer_id = customer_id,
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.value = value
        self.has_payment_verified = has_payment_verified