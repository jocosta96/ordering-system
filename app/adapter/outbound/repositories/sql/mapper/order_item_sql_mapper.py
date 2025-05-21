from app.domain.entities import order_item_entity
from app.adapter.outbound.repositories.sql.entities import order_item_sql


def to_sql_entity(order_item: order_item_entity.OrderItem) -> order_item_sql.OrderItem:
    sql_order_item = order_item_sql.OrderItem(
        id=order_item.id,
        order_id=order_item.order_id,
        product_id=order_item.product_id,
        quantity=order_item.quantity,
        price=order_item.price
    )

    sql_order_item_receipt = (
        order_item_sql.OrderItemReceipt(
            product_id=order_item.product_id,
            ingredient_id=ingredient.id,
            quantity=ingredient.quantity
        ) for ingredient in order_item.final_ingredient
    )

    return sql_order_item, sql_order_item_receipt
