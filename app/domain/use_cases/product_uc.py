from app.domain.entities import product_entity
from app.domain.ports import product_port


class BaseProductUseCase():

    def __init__(
        self,
        port: product_port.ProductPort
    ) -> None:
        self.port = port


class ProductCreate(BaseProductUseCase):

    def create_product(self, product: product_entity.Product) -> int:

        product.category.fix()
        product.category.validate()

        product.name.fix()
        product.name.validate()

        product.price.fix()
        product.price.validate()

        product.sku.fix()
        product.sku.validate()

        product.codebar.fix()
        product.codebar.validate()

        return self.port.create_product(product)


class ProductDelete(BaseProductUseCase):

    def delete_product(self, product: product_entity.Product) -> int:
        return self.port.delete_product(product)


class ProductRead(BaseProductUseCase):

    def read_product(self, seach_key, search_value) -> int:
        return self.port.read_product(seach_key, search_value)


class ProductUpdate(BaseProductUseCase):

    def update_product(self, search_key, search_value, product: product_entity.Product) -> int:

        product.category.fix()
        product.category.validate()

        product.name.fix()
        product.name.validate()

        product.price.fix()
        product.price.validate()

        product.sku.fix()
        product.sku.validate()

        product.codebar.fix()
        product.codebar.validate()

        return self.port.update_product(search_key, search_value, product)