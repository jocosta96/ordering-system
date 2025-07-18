import abc

from app.domain.entities import order_entity
from app.domain.value_objects import status


class OrderPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_order(self, order: order_entity.Order) -> order_entity.Order:
        raise NotImplementedError

    @abc.abstractmethod
    def read_order(self, order_id: str) -> order_entity.Order:
        raise NotImplementedError

    @abc.abstractmethod
    def update_order(
        self, order_id: str, status: status.OrderStatus
    ) -> order_entity.Order:
        raise NotImplementedError

    @abc.abstractmethod
    def pay_order(
        self, payment: dict
    ) -> order_entity.Order:
        raise NotImplementedError

    @abc.abstractmethod
    def list_order(self, search_key=None, search_value=None) -> list[order_entity.Order]:
        raise NotImplementedError

