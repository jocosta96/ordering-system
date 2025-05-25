from app.domain.entities import order_entity
from app.adapter.inbound.rest.entity import order_rest
from app.domain.value_objects.status import OrderStatus
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
):
    
    pass
