import uuid
from datetime import datetime

from app.domain.value_objects.money import Money
from app.domain.value_objects.status import OrderStatus, OrderStatusType
from app.domain.entities.product_entity import Product
from app.domain.entities.ingredient_entity import Ingredient


class OrderItem:

    def __init__(
        self,
        order_id: str,
        product: Product,
        additional_ingredient: list[Ingredient],
        remove_ingredient: list[Ingredient],
        price: Money, 
        id: str=None
    ):
        self.id = id
        self.order_id = order_id
        self.product = product
        self.additional_ingredient = additional_ingredient
        self.remove_ingredient = remove_ingredient
        self.item_receipt = None
        self.price = price

        self._check_or_create_uuid()

    def _check_or_create_uuid(self):
        if not self.id:
            self.id = uuid.uuid4()

    def update_ingredient(self):
        default_ingredient = self.product.default_ingredient
        additional_ingredient = self.additional_ingredient
        remove_ingredient = self.remove_ingredient

        item_receipt = [ing for ing in default_ingredient if ing not in remove_ingredient]
        for ing in additional_ingredient:
            if ing not in item_receipt:
                item_receipt.append(ing)

        self.final_ingredient = item_receipt
        self.item_receipt = item_receipt

    def get_item_receipt(self):
        if self.item_receipt is None:
            self.update_ingredient()
        return self.item_receipt

    def calculate_price(self):
        total_price = self.product.price
        for ingredient in self.additional_ingredient:
            total_price += ingredient.price
        self.price = total_price


class Order:

    def __init__(
        self,

        customer_id: int,
        order_items: list[OrderItem],
        value: Money = 0.00,
        status: OrderStatus = None,
        start_date = None,
        end_date = None,
        has_payment_verified = False,
        payment_date: datetime = None,
        payment_transaction_id: str = '',
        id: str = None
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

        self._check_or_create_uuid()
        self._check_or_create_status()


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
