from app.adapter.outbound.repositories.sql.entities.order_sql import Order, OrderItem


def test_order_sql_fields():
    assert hasattr(Order, "id")
    assert hasattr(Order, "customer_id")
    assert hasattr(Order, "value")
    assert hasattr(Order, "status")
    assert hasattr(Order, "order_items")


def test_order_item_sql_fields():
    assert hasattr(OrderItem, "id")
    assert hasattr(OrderItem, "order_id")
    assert hasattr(OrderItem, "product_id")
    assert hasattr(OrderItem, "price")
    assert hasattr(OrderItem, "order")
    assert hasattr(OrderItem, "product")
