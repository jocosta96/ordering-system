from app.domain.value_objects.name import Name
from app.domain.value_objects.sku import SKU
from app.domain.value_objects.money import Money
from app.domain.value_objects.codebar import Codebar


class Product:

    def __init__(
        self,
        name: str,
        price: float,
        category: str,
        sku: str,
        codebar: str,
        id:int=None
    ):
        
        self.name = Name(name)
        self.price = Money(price)
        self.category = Name(category)
        self.sku = SKU(sku)
        self.codebar = Codebar(codebar)
        self.id = id
