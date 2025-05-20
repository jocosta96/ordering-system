from app.domain.entities import order_item_entity
from app.domain.ports import order_item_port


class BaseOrderItemUseCase():

    def __init__(
        self,
        port: order_item_port.OrderItemPort
    ) -> None:
        self.port = port


class OrderItemCreate(BaseOrderItemUseCase):

    def create_order_item(self, order: order_item_entity.OrderItem) -> int:

        return self.port.create_order_item(order)


class OrderItemDelete(BaseOrderItemUseCase):

    def delete_order_item(self, order: order_item_entity.OrderItem) -> int:
        return self.port.delete_order_item(order)


class OrderItemRead(BaseOrderItemUseCase):

    def read_order_item(self, seach_key, search_value) -> int:
        return self.port.read_order_item(seach_key, search_value)


class OrderItemUpdate(BaseOrderItemUseCase):

    def update_order_item(self, search_key, search_value, order: order_item_entity.OrderItem) -> int:

        return self.port.update_order_item(search_key, search_value, order)