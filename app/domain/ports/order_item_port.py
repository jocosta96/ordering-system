import abc

from app.domain.entities import order_item_entity


class OrderItemPort(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_order_item(self) -> order_item_entity.OrderItem:
        raise NotImplementedError
    
    @abc.abstractmethod
    def read_order_item(self) -> order_item_entity.OrderItem:
        raise NotImplementedError
    
    @abc.abstractmethod
    def update_order_item(self) -> order_item_entity.OrderItem:
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete_order_item(self) -> order_item_entity.OrderItem:
        raise NotImplementedError