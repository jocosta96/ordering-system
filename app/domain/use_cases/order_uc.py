
from app.domain.entities import order_entity
from app.domain.ports import order_port
from app.domain.value_objects import status


class BaseOrderUseCase:
    def __init__(self, port: order_port.OrderPort) -> None:
        self.port = port


class OrderCreate(BaseOrderUseCase):
    def create_order(self, order: order_entity.Order) -> order_entity.Order:
        return self.port.create_order(order)


class OrderRead(BaseOrderUseCase):
    def read_order(self, order_id: str) -> order_entity.Order:
        return self.port.read_order(order_id)


class OrderUpdate(BaseOrderUseCase):
    def update_order(self, order_id: str, status: status.OrderStatus) -> int:
        return self.port.update_order(order_id, status)


class OrderPay(BaseOrderUseCase):
    def pay_order(
        self, order: order_entity.Order
    ) -> int:
        return self.port.pay_order(order)
    

class OrderList(BaseOrderUseCase):
    def list_order(self, search_key=None, search_value=None):
        return self.port.list_order(search_key, search_value)


class OrderDelete(BaseOrderUseCase):
    def delete_order(self, order_id: str) -> int:
        return self.port.delete_order(order_id)
