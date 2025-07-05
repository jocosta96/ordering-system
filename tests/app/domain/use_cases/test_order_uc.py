from app.domain.use_cases.order_uc import OrderCreate, OrderRead, OrderUpdate


class DummyPort:
    def create_order(self, order):
        return 1

    def read_order(self, order_id):
        return 3

    def update_order(self, order_id, status):
        return 4


def test_order_use_cases():
    port = DummyPort()
    assert OrderCreate(port).create_order(None) == 1
    assert OrderRead(port).read_order(None) == 3
    assert OrderUpdate(port).update_order(None, None) == 4
