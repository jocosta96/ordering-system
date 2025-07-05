from app.domain.entities import product_entity
from app.domain.ports import product_port


class BaseProductUseCase:
    def __init__(self, port: product_port.ProductPort) -> None:
        self.port = port


class ProductCreate(BaseProductUseCase):
    def create_product(self, product: product_entity.Product) -> int:
        return self.port.create_product(product)


class ProductDelete(BaseProductUseCase):
    def delete_product(self, product: product_entity.Product) -> int:
        return self.port.delete_product(product)


class ProductRead(BaseProductUseCase):
    def read_product(self, product_id) -> int:
        return self.port.read_product(product_id)


class ProductUpdate(BaseProductUseCase):
    def update_product(self, product: product_entity.Product) -> int:
        return self.port.update_product(product)


class ProductRestoreDeleted(BaseProductUseCase):
    def restore_deleted_product(self, product: product_entity.Product) -> int:
        return self.port.restore_deleted_product(product)


class ProductList(BaseProductUseCase):
    def list_product(self, search_key=None, search_value=None):
        return self.port.list_product(search_key, search_value)
