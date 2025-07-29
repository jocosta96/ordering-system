from abc import ABC, abstractmethod


class PaymentFactory(ABC):

    @abstractmethod
    def request_payment(self, order_id):
        raise NotImplementedError