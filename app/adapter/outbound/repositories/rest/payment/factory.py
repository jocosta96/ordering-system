import abc
from app.domain.ports.payment_port import PaymentPort 

class PaymentFactory(PaymentPort, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def request_payment(self, order_id):
        raise NotImplementedError
