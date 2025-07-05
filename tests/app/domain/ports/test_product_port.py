from app.domain.ports.product_port import ProductPort


class DummyProductPort(ProductPort):
    def create_product(self, product):
        return 1

    def delete_product(self, product):
        return 1

    def read_product(self, product_id):
        return 1

    def update_product(self, product):
        return 1

    def restore_deleted_product(self, product):
        return 1

    def list_product(self, search_key=None, search_value=None):
        return []


def test_product_port_interface():
    port = DummyProductPort()
    assert port.create_product(None) == 1
    assert port.delete_product(None) == 1
    assert port.read_product(1) == 1
    assert port.update_product(None) == 1
    assert port.restore_deleted_product(None) == 1
    assert port.list_product() == []
