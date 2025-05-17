from app.domain.value_objects.name import Name
from app.domain.value_objects.sku import SKU
from app.domain.value_objects.money import Money
from app.domain.value_objects.codebar import Codebar


class Product:

    def __init__(
        self,
        name: Name,
        price: Money,
        category: Name,
        sku: SKU,
        codebar: Codebar,
        id:int=None
    ):
        
        self.name = name
        self.price = price
        self.category = category
        self.sku = sku
        self.codebar =codebar
        self.id = id
