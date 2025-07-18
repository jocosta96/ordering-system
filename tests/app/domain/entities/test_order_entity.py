import uuid
from datetime import datetime
from app.domain.entities.order_entity import Order, OrderItem
from app.domain.value_objects.money import Money
from app.domain.entities.product_entity import Product, ProductReceiptItem
from app.domain.entities.ingredient_entity import Ingredient
from app.domain.value_objects.name import Name
from app.domain.value_objects.sku import SKU
from app.domain.value_objects.category import ProductCategory


class DummyIngredient(Ingredient):
    def __init__(
        self, id=1, name=None, price=None, product_category=None, is_active=True
    ):
        super().__init__(
            id=id,
            name=name or Name(name="Test Ingredient"),
            price=price or Money(amount=1.0),
            product_category=product_category or ProductCategory(category="LANCHE"),
            is_active=is_active,
        )


def make_product():
    return Product(
        name=Name(name="X-Burger"),
        price=Money(amount=12.50),
        category=ProductCategory(category="LANCHE"),
        sku=SKU(sku="PROD-1234-XYZ"),
        default_ingredient=[ProductReceiptItem(ingredient=DummyIngredient(), quantity=2)],
    )


def test_order_item_creation():
    product = make_product()
    ingredient = DummyIngredient()
    order_item = OrderItem(
        order_id="order-1",
        product=product,
        additional_ingredient=[ingredient],
        remove_ingredient=[],
        price=Money(amount=12.50),
    )
    assert order_item.product == product
    assert order_item.order_id == "order-1"
    assert isinstance(order_item.id, uuid.UUID)


def test_order_creation():
    product = make_product()
    ingredient = DummyIngredient()
    order_item = OrderItem(
        order_id="order-1",
        product=product,
        additional_ingredient=[ingredient],
        remove_ingredient=[],
        price=Money(amount=12.50),
    )
    order = Order(customer_id=1, order_items=[order_item], value=Money(amount=12.50))
    assert order.customer_id == 1
    assert order.value.amount == 12.50
    assert isinstance(order.id, uuid.UUID)
    assert order.status.status == "RECEBIDO"
    order.set_start_date()
    assert isinstance(order.start_date, datetime)
    order.set_end_date()
    assert isinstance(order.end_date, datetime)
    
    # Test payment processing
    payment_data = {
        'transaction_id': 'txid123',
        'date': datetime.now(),
        'message': 'Payment successful',
        'approval_status': True
    }
    order.process_payment(payment_data)
    assert order.has_payment_verified
    assert order.payment_transaction_id == "txid123"
    # After payment processing, status should be EM_PREPARACAO
    assert order.status.status == "EM_PREPARACAO"
    order.next_status()
    # After next_status, status should be PRONTO
    assert order.status.status == "PRONTO"
