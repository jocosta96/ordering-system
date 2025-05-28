from app.domain.entities import order_entity
from app.adapter.inbound.rest.entity import order_rest, product_rest
from app.domain.value_objects.status import OrderStatus, OrderStatusType
from app.domain.value_objects.money import Money
from app.adapter.inbound.rest.mapper import product_rest_mapper, ingredient_rest_mapper

def to_domain_entity(
    order:order_rest.Order
) -> order_entity.Order:
    
    order_items = [
        order_entity.OrderItem(
            id=item.id,
            order_id=order.id,
            product=product_rest_mapper.to_domain_entity(item.product),  # <-- FIXED
            additional_ingredient=[
                ingredient_rest_mapper.to_domain_entity(ing) for ing in item.additional_ingredient
            ],
            remove_ingredient=[
                ingredient_rest_mapper.to_domain_entity(ing) for ing in item.remove_ingredient
            ],
            price=item.price
        )
        for item in order.order_items
    ]

    return order_entity.Order(
        id=order.id,
        customer_id=order.customer_id,
        value=order.value,
        status=order.status,
        payment_date=order.payment_date,
        payment_transaction_id=order.payment_transaction_id,
        has_payment_verified=order.has_payment_verified,
        order_items=order_items
    )

def to_rest_entity(
    order: order_entity.Order
) -> order_rest.Order:
    order_items = [
        order_rest.OrderItem(
            id=str(item.id),
            product=product_rest_mapper.to_rest_entity(item.product),
            additional_ingredient=[
                ingredient_rest_mapper.to_rest_entity(ing) for ing in item.additional_ingredient
            ],
            remove_ingredient=[
                ingredient_rest_mapper.to_rest_entity(ing) for ing in item.remove_ingredient
            ],
            item_receipt=[
                product_rest.ProductReceiptItem(
                    ingredient=ingredient_rest_mapper.to_rest_entity(receipt.ingredient),
                    quantity=receipt.quantity
                )
                for receipt in item.item_receipt
            ],
            price=item.price
        )
        for item in order.order_items
    ]

    return order_rest.Order(
        id=str(order.id),
        customer_id=order.customer_id,
        value=Money(amount=str(order.value)),
        status=OrderStatus(status=str(order.status)),
        payment_date=order.payment_date,
        payment_transaction_id=order.payment_transaction_id,
        has_payment_verified=order.has_payment_verified,
        order_items=order_items
    )


def to_simple_reader(
    order: order_entity.Order
) -> order_rest.SimpleOrderReader:
    
    print('*****'*20, order.__dict__)

    return order_rest.SimpleOrderReader(
        id=str(order.id),
        customer_id=order.customer_id,
        value=Money(amount=str(order.value)),
        status=OrderStatus(status=str(order.status)),
        order_display_id=order.order_display_id,
        order_start_date=order.start_date
    )
