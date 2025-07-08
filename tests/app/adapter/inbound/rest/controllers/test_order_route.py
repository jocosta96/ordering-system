import os
import base64
import dotenv

from fastapi.testclient import TestClient
from app.main import app

dotenv.load_dotenv()
client = TestClient(app)


def get_basic_auth_header():
    username = os.environ.get("API_USER", "user")
    password = os.environ.get("API_PWD", "pass")
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}


def test_order_list_route(monkeypatch):
    from app.domain.use_cases.order_uc import OrderList

    def mock_list_order(self, search_key, search_value):
        return []

    monkeypatch.setattr(OrderList, "list_order", mock_list_order)
    headers = get_basic_auth_header()
    response = client.get("/order/list?search_key=id&search_value=1", headers=headers)
    assert response.status_code in (200, 404)
    assert isinstance(response.json(), list) or response.status_code == 404


def test_order_read_route_not_found(monkeypatch):
    from app.domain.use_cases.order_uc import OrderRead
    from app.adapter.inbound.rest.mapper import order_rest_mapper

    def mock_read_order(self, order_id):
        return None

    def mock_to_rest_entity(order):
        # Simulate what happens if order is None
        if order is None:
            raise AttributeError("Order is None")
        return {}

    monkeypatch.setattr(OrderRead, "read_order", mock_read_order)
    monkeypatch.setattr(order_rest_mapper, "to_rest_entity", mock_to_rest_entity)
    headers = get_basic_auth_header()
    response = client.get("/order/read/1", headers=headers)
    # Should be 404 now that controller handles None
    assert response.status_code == 404


def test_order_read_route_found(monkeypatch):
    from app.domain.use_cases.order_uc import OrderRead
    from app.adapter.inbound.rest.mapper import order_rest_mapper

    class DummyOrder:
        def __init__(self):
            self.id = "1"
            self.status = "RECEBIDO"
            self.created_at = "2024-01-01T00:00:00"
            self.updated_at = "2024-01-01T00:00:00"
            self.items = []
            self.customer_id = 1
            self.value = {"amount": "0.00"}
            self.payment_date = None
            self.payment_transaction_id = None
            self.has_payment_verified = False
            self.order_items = []
        def validate_duplicated_payment(self):
            # This is a dummy method for test purposes; no implementation needed.
            pass

    def mock_read_order(self, order_id):
        return DummyOrder()

    def mock_to_rest_entity(order):
        # Return all required fields for pydantic validation
        return {
            "id": str(order.id),
            "customer_id": order.customer_id,
            "value": {"amount": "0.00"},
            "status": {"status": "RECEBIDO"},
            "payment_date": order.payment_date,
            "payment_transaction_id": order.payment_transaction_id,
            "has_payment_verified": order.has_payment_verified,
            "order_items": [],
        }

    monkeypatch.setattr(OrderRead, "read_order", mock_read_order)
    monkeypatch.setattr(order_rest_mapper, "to_rest_entity", mock_to_rest_entity)
    headers = get_basic_auth_header()
    response = client.get("/order/read/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == "1"
    assert response.json()["status"]["status"] == "RECEBIDO"


def test_order_update_status_route(monkeypatch):
    from app.domain.use_cases.order_uc import OrderUpdate

    def mock_update_order(self, order_id, status):
        # status is an OrderStatus object
        return {"id": order_id, "status": status.status}

    monkeypatch.setattr(OrderUpdate, "update_order", mock_update_order)
    headers = get_basic_auth_header()
    # Use a valid status value to avoid pydantic validation error
    response = client.patch("/order/update/1?status=RECEBIDO", headers=headers)
    assert response.status_code == 200
    assert response.json().get("status") == "RECEBIDO"


def test_order_update_status_route_invalid_status(monkeypatch):
    import pytest
    from app.domain.use_cases.order_uc import OrderUpdate

    def mock_update_order(self, order_id, status):
        return {"id": order_id, "status": status.status}

    monkeypatch.setattr(OrderUpdate, "update_order", mock_update_order)
    headers = get_basic_auth_header()
    # Use an invalid status value to trigger validation error
    with pytest.raises(Exception) as excinfo:
        client.patch("/order/update/1?status=INVALID_STATUS", headers=headers)
    assert "is not a valid OrderStatusType" in str(excinfo.value)


def test_order_create_route_missing_fields(monkeypatch):
    from app.domain.use_cases.order_uc import OrderCreate
    from app.adapter.inbound.rest.mapper import order_rest_mapper

    def mock_create_order(self, order):
        class DummyOrder:
            id = 1
            status = "NEW"
        return DummyOrder()

    monkeypatch.setattr(OrderCreate, "create_order", mock_create_order)
    monkeypatch.setattr(order_rest_mapper, "to_domain_entity", lambda x: x)
    monkeypatch.setattr(order_rest_mapper, "to_simple_reader", lambda x: {"id": 1, "status": "NEW"})

    headers = get_basic_auth_header()
    # Missing required fields
    data = {"status": "NEW"}
    response = client.post("/order", json=data, headers=headers)
    assert response.status_code == 422


def test_order_payment_route_invalid(monkeypatch):
    from app.domain.use_cases.order_uc import OrderPay, OrderRead

    class DummyOrder:
        def validate_duplicated_payment(self):
            # This is a dummy method for test purposes; no implementation needed.
            pass

    def mock_read_order(self, order_id):
        return DummyOrder()

    def mock_pay_order(self, order_id, payment_date, payment_transaction_id):
        return {"order_id": order_id, "payment_date": payment_date, "payment_transaction_id": payment_transaction_id}

    monkeypatch.setattr(OrderRead, "read_order", mock_read_order)
    monkeypatch.setattr(OrderPay, "pay_order", mock_pay_order)

    headers = get_basic_auth_header()
    # Missing required payment fields
    data = {
        "order_id": 1,
        "payment_transaction_id": "txn_123"
    }
    response = client.patch("/order/pay/1", json=data, headers=headers)
    assert response.status_code == 422
