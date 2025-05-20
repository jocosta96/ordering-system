from app.domain.entities import order_entity
from app.adapter.inbound.rest.entity import order_rest
from app.domain.value_objects.status import OrderStatus
from app.domain.value_objects.money import Money

def to_domain_entity(
    order:order_rest.BaseOrder
) -> order_entity.Order:
    
    domain_order = order_entity.Order(
        id = order.id,
        customer_id = order.customer_id,
        value = order.value
    )

    return domain_order

def to_rest_entity(
    order: order_entity.Order
) -> order_rest.FullOrder:
    
    print('*'*100, order.__dict__)
    
    rest_order = order_rest.FullOrder(
        id = order.id,
        customer_id = order.customer_id,
        status = OrderStatus(status=order.status),
        start_date = order.start_date,
        end_date = order.end_date,
        value = Money(amount=order.value),
        has_payment_verified = order.has_payment_verified
    )

    return rest_order
