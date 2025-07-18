import abc
from datetime import datetime

from app.domain.entities import order_entity
from app.domain.value_objects import status


class PaymentPort(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def request_payment(
        self, order_id: dict, value
    ) -> order_entity.Order:
        raise NotImplementedError