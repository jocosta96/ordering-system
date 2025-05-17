from app.domain.use_cases import product_base_uc
from app.domain.entities import product_entity


class ProductDelete(product_base_uc.BaseProductUseCase):

    def delete_product(self, product: product_entity.Product) -> int:
        return self.port.delete_product(product)
