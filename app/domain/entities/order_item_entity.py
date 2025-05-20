from app.domain.entities.product_entity import Product

class OrderItem:

    def __init__(
        self,
        order_id: int,
        product: list[Product],
        
        id: int=None
    ):
        self.id = id,
        self.order_id = order_id,
        self.product = product
