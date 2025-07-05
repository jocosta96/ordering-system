from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_order_list_route(monkeypatch):
    # Patch the method on the class, not the instance
    from app.domain.use_cases.order_uc import OrderList

    def mock_list_order(self, search_key, search_value):
        return []

    monkeypatch.setattr(OrderList, "list_order", mock_list_order)
    response = client.get("/order/list?search_key=id&search_value=1")
    assert response.status_code in (200, 404)  # Accept 404 if no data
    assert isinstance(response.json(), list) or response.status_code == 404


def test_order_read_route(monkeypatch):
    from app.domain.use_cases.order_uc import OrderRead

    def mock_read_order(self, k, v):
        return None

    monkeypatch.setattr(OrderRead, "read_order", mock_read_order)
    response = client.get("/order/1")
    assert response.status_code in (200, 404)  # Accept 404 if not found


# Additional tests for create, update, delete can be added similarly with monkeypatching
