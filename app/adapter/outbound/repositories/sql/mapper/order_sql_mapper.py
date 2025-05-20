from datetime import datetime

from app.domain.entities import order_entity
from app.adapter.outbound.repositories.sql.entities import order_sql
from app.domain.value_objects import name, status

def to_domain_entity(order: order_sql.Order) -> order_entity.Order:

    domain_order = order_entity.Order(
        id = int(order.id),
        customer_id = int(order.customer_id),
        status = str(order.status),
        start_date = order.start_date,
        end_date = order.end_date,
        value = order.value,
        has_payment_verified = bool(order.has_payment_verified)
    )


    return domain_order


def to_sql_entity(order: order_entity.Order) -> order_sql.Order:

    sql_order = order_sql.Order(
#        id = order.id,
        customer_id = order.customer_id,
        status = order.status.value,
        start_date = order.start_date,
        end_date = order.end_date,
        value = order.value.value,
        has_payment_verified = order.has_payment_verified
    )

    return sql_order