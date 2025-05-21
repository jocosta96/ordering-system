from app.domain.entities.product_entity import Product
from app.domain.entities.ingredient_entity import Ingredient
from app.domain.value_objects.money import Money

class OrderItem:

    def __init__(
        self,
        order_id: int,
        product: Product,
        additional_ingredient: list[Ingredient],
        remove_ingredient: list[Ingredient],
        price: Money, 
        id: int=None
    ):
        self.id = id,
        self.order_id = order_id,
        self.product = product,
        self.additional_ingredient = additional_ingredient
        self.remove_ingredient = remove_ingredient
        self.price = price

    def update_ingredient(self):
        # TODO cria a receita do item pega o default que esta dentro de produtos remove a lista em remove_ingredient e adiciona additional_ingredient
        pass

    def calculate_price(self):
        # TODO pega o preço default e adiciona o preço dos itens adicionais additional_ingredient
        pass