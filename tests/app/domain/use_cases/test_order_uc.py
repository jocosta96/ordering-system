from app.domain.use_cases.order_uc import OrderCreate, OrderRead, OrderUpdate


class DummyPort:
    def create_order(self, order):
        return 1

    def read_order(self, seach_key, search_value):
        return 3

    def update_order(self, search_key, search_value, order):
        return 4


def test_order_use_cases():
    port = DummyPort()
    assert OrderCreate(port).create_order(None) == 1
    assert OrderRead(port).read_order(None, None) == 3
    assert OrderUpdate(port).update_order(None, None, None) == 4
