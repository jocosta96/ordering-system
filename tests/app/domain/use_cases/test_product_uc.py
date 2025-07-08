from app.domain.use_cases.product_uc import (
    ProductCreate,
    ProductDelete,
    ProductRead,
    ProductUpdate,
    ProductRestoreDeleted,
    ProductList,
)


class DummyPort:
    def create_product(self, product):
        return 1

    def delete_product(self, product):
        return 2

    def read_product(self, product_id):
        return 3

    def update_product(self, product):
        return 4

    def restore_deleted_product(self, product):
        return 5

    def list_product(self, search_key=None, search_value=None):
        return [6]


def test_product_use_cases():
    port = DummyPort()
    dummy_product = {}
    dummy_product_id = 1
    assert ProductCreate(port).create_product(dummy_product) == 1
    assert ProductDelete(port).delete_product(dummy_product) == 2
    assert ProductRead(port).read_product(dummy_product_id) == 3
    assert ProductUpdate(port).update_product(dummy_product) == 4
    assert ProductRestoreDeleted(port).restore_deleted_product(dummy_product) == 5
    assert ProductList(port).list_product() == [6]
