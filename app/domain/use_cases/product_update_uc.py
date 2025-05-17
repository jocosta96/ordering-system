from app.domain.use_cases import product_base_uc
from app.domain.entities import product_entity


class ProductUpdate(product_base_uc.BaseProductUseCase):

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
