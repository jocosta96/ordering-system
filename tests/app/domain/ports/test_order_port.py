import pytest
from app.domain.ports.order_port import OrderPort
from app.domain.entities.order_entity import Order

class DummyOrderPort(OrderPort):
    def create_order(self, order): return order
    def read_order(self, order_id): return order_id
    def update_order(self, order): return order
    def delete_order(self, order_id): return order_id

def test_order_port_interface():
    port = DummyOrderPort()
    dummy_order = object()
    assert port.create_order(dummy_order) == dummy_order
    assert port.read_order("id") == "id"
    assert port.update_order(dummy_order) == dummy_order
    assert port.delete_order("id") == "id"
