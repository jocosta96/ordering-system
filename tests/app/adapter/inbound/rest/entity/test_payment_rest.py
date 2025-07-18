from app.adapter.inbound.rest.entity.payment_rest import Payment
from datetime import datetime

def test_payment_creation():
    payment = Payment(
        date=datetime(2025, 7, 8, 12, 0, 0),
        transaction_id="txn-123",
        order_id="order-1"
    )
    assert payment.date == datetime(2025, 7, 8, 12, 0, 0)
    assert payment.transaction_id == "txn-123"
    assert payment.order_id == "order-1"
