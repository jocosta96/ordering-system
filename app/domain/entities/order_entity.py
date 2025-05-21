from datetime import datetime
from app.domain.value_objects.money import Money
from app.domain.value_objects.status import OrderStatus, OrderStatusType
from app.domain.entities.order_item_entity import OrderItem


class Order:

    def __init__(
        self,
        id: int,
        customer_id: int,
        order_item: list[OrderItem],
        value: Money = 0.00,
        status: OrderStatus = None,
        start_date = None,
        end_date = None,
        has_payment_verified = False
    ):
        
        self.id = id
        self.customer_id = customer_id
        self.value = value
        self.order_item = order_item

        self.start_date = start_date
        self.end_date = end_date
        self.has_payment_verified = has_payment_verified
        self.status = status or OrderStatus(status=OrderStatusType.RECEBIDO)

    def set_start_date(self):
        self.start_date = datetime.now()

    def set_end_date(self):
        self.end_date = datetime.now()

    def update_payment_flag(self):
        self.has_payment_verified = True

    def next_status(self):
        self.status.next_status()
