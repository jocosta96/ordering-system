from app.domain.value_objects import payment
from app.domain.entities import order_entity
from app.domain.ports import payment_port


class BaseOrderUseCase:
    def __init__(self, port: payment_port.PaymentPort) -> None:
        self.port = port


class RequestPayment(BaseOrderUseCase):
    def request_payment(
        self, order: order_entity.Order, value
    ) -> payment.Payment:
        return self.port.request_payment(order, value)