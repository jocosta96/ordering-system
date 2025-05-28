import uuid
from datetime import datetime
from collections import Counter

from app.domain.value_objects.money import Money
from app.domain.value_objects.status import OrderStatus, OrderStatusType
from app.domain.entities.product_entity import Product, ProductReceiptItem
from app.domain.entities.ingredient_entity import Ingredient

class OrderItem:

    def __init__(
        self,
        order_id: str,
        product: Product,
        additional_ingredient: list[Ingredient],
        remove_ingredient: list[Ingredient],
        item_receipt: list[ProductReceiptItem] = [],
        price: Money = Money(amount=0.0), 
        id: str=None
    ):
        self.id = id
        self.order_id = order_id
        self.product = product
        self.additional_ingredient = additional_ingredient
        self.remove_ingredient = remove_ingredient
        self.item_receipt = item_receipt
        self.price = price

        self._check_or_create_uuid()
        self._generate_item_receipt()
        self._calculate_price()

    def _check_or_create_uuid(self):
        if not self.id:
            self.id = uuid.uuid4()


    def _serialize_default_ingredients(self):
        result = []
        for item in self.product.default_ingredient:
            if item.quantity > 1:
                result.extend([item.ingredient] * item.quantity)
            else:
                result.append(item.ingredient)
        return result
    

    def _generate_item_receipt(self):

        if self.item_receipt:
            return

        default_ingredient = self._serialize_default_ingredients()
        additional_ingredient = self.additional_ingredient
        remove_ingredient = self.remove_ingredient

        # Only keep default ingredients not in remove_ingredient
        filtered_default = [item for item in default_ingredient if item not in remove_ingredient]

        # Combine all ingredients (filtered default + additional)
        full_list = filtered_default + additional_ingredient

        # Use id for grouping to avoid duplicate objects with same id
        ingredient_map = {}
        for ingredient in full_list:

            key = getattr(ingredient, "id", id(ingredient))
            if key in ingredient_map:
                ingredient_map[key]["quantity"] += 1
            else:
                ingredient_map[key] = {"ingredient": ingredient, "quantity": 1}

        self.item_receipt = [
            ProductReceiptItem(
                ingredient=entry["ingredient"],
                quantity=entry["quantity"]
            )
            for entry in ingredient_map.values()
        ]


    def get_item_receipt(self):
        if self.item_receipt is None:
            self.update_ingredient()
        return self.item_receipt

    def _calculate_price(self):
        if not self.price.amount == Money(amount=0.0).amount:
            return

        total_price = self.product.price
        for ingredient in self.additional_ingredient:
            total_price += ingredient.price
        self.price = total_price


class Order:

    def __init__(
        self,

        customer_id: int,
        order_items: list[OrderItem],
        value: Money = Money(amount=0.0),
        status: OrderStatus = None,
        start_date = None,
        end_date = None,
        has_payment_verified = False,
        payment_date: datetime = None,
        payment_transaction_id: str = '',
        id: str = None,
        order_number: int = None,
    ):
        
        self.id = id
        self.customer_id = customer_id
        self.value = value
        self.order_items = order_items
        self.payment_date = payment_date
        self.payment_transaction_id = payment_transaction_id

        self.start_date = start_date
        self.end_date = end_date
        self.has_payment_verified = has_payment_verified
        self.status = status

        self.order_number = order_number
        self.order_display_id: str = ''

        self._check_or_create_uuid()
        self._check_or_create_status()
        self.calculate_value()
        self._set_display_id()

    def _set_display_id(self):
        if self.order_number:
            self.order_display_id = str(self.order_number).zfill(3)[:3]
        return self.order_display_id

    def _check_or_create_status(self):
        if not self.status:
            self.status = OrderStatus(status=OrderStatusType.RECEBIDO)

    def _check_or_create_uuid(self):
        if not self.id:
            self.id = uuid.uuid4()

    def set_start_date(self):
        self.start_date = datetime.now()

    def set_end_date(self):
        self.end_date = datetime.now()

    def execute_payment(self, payment_date, transaction_id):
        self.has_payment_verified = True
        self.payment_date = payment_date,
        self.payment_transaction_id = transaction_id

    def next_status(self):
        self.status.next_status()

    def calculate_value(self):

        total_value = Money(amount=0.0)

        for item in self.order_items:
            total_value += Money(amount=item.price) if not isinstance(item.price, Money) else item.price

        self.value = total_value