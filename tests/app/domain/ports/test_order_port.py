from app.domain.ports.order_port import OrderPort


class DummyOrderPort(OrderPort):
    def create_order(self, order):
        return order

    def read_order(self, order_id):
        return order_id

    def update_order(self, order, status=None):
        return order

    def delete_order(self, order_id):
        return order_id

    def pay_order(self, order_id, payment_date, payment_transaction_id):
        return (order_id, payment_date, payment_transaction_id)

    def list_order(self, search_key, search_value):
        return [(search_key, search_value)]


def test_order_port_interface():
    port = DummyOrderPort()
    dummy_order = object()
    assert port.create_order(dummy_order) == dummy_order
    assert port.read_order("id") == "id"
    assert port.update_order(dummy_order) == dummy_order
    assert port.delete_order("id") == "id"
