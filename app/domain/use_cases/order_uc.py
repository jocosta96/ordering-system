from app.domain.entities import order_entity
from app.domain.ports import order_port


class BaseOrderUseCase():

    def __init__(
        self,
        port: order_port.OrderPort
    ) -> None:
        self.port = port


class OrderCreate(BaseOrderUseCase):

    def create_order(self, order: order_entity.Order) -> int:

        return self.port.create_order(order)


class OrderDelete(BaseOrderUseCase):

    def delete_order(self, order: order_entity.Order) -> int:
        return self.port.delete_order(order)


class OrderRead(BaseOrderUseCase):

    def read_order(self, seach_key, search_value) -> int:
        return self.port.read_order(seach_key, search_value)


class OrderUpdate(BaseOrderUseCase):

    def update_order(self, search_key, search_value, order: order_entity.Order) -> int:

        return self.port.update_order(search_key, search_value, order)