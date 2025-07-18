import abc

from app.domain.entities import order_entity


class PaymentPort(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def request_payment(
        self, order_id: dict, value
    ) -> order_entity.Order:
        raise NotImplementedError