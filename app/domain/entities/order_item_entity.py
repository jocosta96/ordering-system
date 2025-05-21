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
        self.final_ingredient = None
        self.price = price

    def update_ingredient(self):
        default_ingredient = self.product.default_ingredient
        additional_ingredient = self.additional_ingredient
        remove_ingredient = self.remove_ingredient

        final_ingredient = [ing for ing in default_ingredient if ing not in remove_ingredient]
        for ing in additional_ingredient:
            if ing not in final_ingredient:
                final_ingredient.append(ing)

        self.final_ingredient = final_ingredient
        

    def calculate_price(self):
        total_price = self.product.price
        for ingredient in self.additional_ingredient:
            total_price += ingredient.price
        self.price = total_price
