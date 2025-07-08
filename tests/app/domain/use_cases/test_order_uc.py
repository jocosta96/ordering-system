from app.domain.use_cases.order_uc import OrderCreate, OrderRead, OrderUpdate, OrderPay, OrderList, OrderDelete


class DummyPort:
    def create_order(self, order):
        return 1

    def read_order(self, order_id):
        return 3

    def update_order(self, order_id, status):
        return 4

    def pay_order(self, order_id, payment_date, payment_transaction_id):
        return 5

    def list_order(self, search_key=None, search_value=None):
        return [6]

    def delete_order(self, order_id):
        return 7


def test_order_use_cases():
    port = DummyPort()
    assert OrderCreate(port).create_order(None) == 1
    assert OrderRead(port).read_order(None) == 3
    assert OrderUpdate(port).update_order(None, None) == 4
    assert OrderPay(port).pay_order(None, None, None) == 5
    assert OrderList(port).list_order() == [6]
    assert OrderDelete(port).delete_order(None) == 7
