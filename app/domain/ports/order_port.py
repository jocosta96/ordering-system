import abc

from app.domain.entities import order_entity


class OrderPort(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_order(self) -> order_entity.Order:
        raise NotImplementedError
    
    @abc.abstractmethod
    def read_order(self) -> order_entity.Order:
        raise NotImplementedError
    
    @abc.abstractmethod
    def update_order(self) -> order_entity.Order:
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete_order(self) -> order_entity.Order:
        raise NotImplementedError