import pytest
from unittest.mock import MagicMock, patch
from app.adapter.outbound.repositories.sql.implementation.order_impl import OrderRepoImpl

@pytest.fixture
def mock_sql_impl():
    with patch('app.adapter.outbound.repositories.sql.implementation.order_impl.sql_impl.SQLRepoImpl') as mock:
        yield mock

def test_init_uses_sql_impl(mock_sql_impl):
    repo = OrderRepoImpl()
    assert repo._sql_impl is not None

def test_order_entity_to_sql():
    from app.adapter.outbound.repositories.sql.implementation.order_impl import OrderRepoImpl
    order = MagicMock()
    order.id = 1
    order.customer_id = 2
    order.value = 100.0
    order.payment_date = None
    order.payment_transaction_id = 'txid'
    order.start_date = None
    order.end_date = None
    order.has_payment_verified = False
    order.status = 'pending'
    sql_entity = OrderRepoImpl._order_entity_to_sql(order)
    assert sql_entity.id == 1
    assert sql_entity.customer_id == 2
    assert sql_entity.value == 100.0
    assert sql_entity.payment_transaction_id == 'txid'
    assert sql_entity.status == 'pending'

def test_order_item_entity_to_sql():
    from app.adapter.outbound.repositories.sql.implementation.order_impl import OrderRepoImpl
    order = MagicMock()
    item = MagicMock()
    item.id = 1
    item.product.id = 2
    item.price = 10.0
    order.order_items = [item]
    sql_items = OrderRepoImpl._order_item_entity_to_sql(order)
    assert sql_items[0].id == 1
    assert sql_items[0].product_id == 2
    assert sql_items[0].price == 10.0

def test_order_item_receipt_entity_to_sql():
    from app.adapter.outbound.repositories.sql.implementation.order_impl import OrderRepoImpl
    order = MagicMock()
    item = MagicMock()
    item.id = 1
    item.product.id = 2
    receipt = MagicMock()
    receipt.ingredient.id = 3
    receipt.quantity = 5
    item.get_item_receipt.return_value = [receipt]
    order.order_items = [item]
    with patch('app.adapter.outbound.repositories.sql.implementation.order_impl.order_sql.OrderItemReceipt') as MockReceipt:
        MockReceipt.return_value = MagicMock(ingredient_id=3, quantity=5)
        result = OrderRepoImpl._order_item_receipt_entity_to_sql(order)
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].ingredient_id == 3
        assert result[0].quantity == 5
