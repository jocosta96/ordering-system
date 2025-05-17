from app.domain.use_cases import product_base_uc
from app.domain.entities import product_entity


class ProductRead(product_base_uc.BaseProductUseCase):

    def read_product(self, seach_key, search_value) -> int:
        return self.port.read_product(seach_key, search_value)
    
