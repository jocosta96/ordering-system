from src.adapters.gateways.implementations import QRPayment


class QRPaymentRepository():

    def __init__(self, qr_payment: QRPayment):
        self.qr_payment = qr_payment

    def request_payment(self, order_id, amount):
        return self.qr_payment.request_payment(order_id, amount)

