from app.adapter.outbound.repositories.sql.implementation.order_impl import (
    OrderRepoImpl,
)


def test_order_repo_impl_methods():
    assert hasattr(OrderRepoImpl, "_to_domain_entity")
    assert hasattr(OrderRepoImpl, "_to_sql_entity")
    assert hasattr(OrderRepoImpl, "create_order")
    assert hasattr(OrderRepoImpl, "read_order")
    assert hasattr(OrderRepoImpl, "update_order")
    assert hasattr(OrderRepoImpl, "delete_order")
