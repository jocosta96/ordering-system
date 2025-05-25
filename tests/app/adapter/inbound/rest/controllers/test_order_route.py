import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_order_list_route(monkeypatch):
    monkeypatch.setattr("app.domain.use_cases.order_uc.OrderRead.read_order", lambda self, k, v: [])
    response = client.get("/order/list?search_key=id&search_value=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_order_read_route(monkeypatch):
    monkeypatch.setattr("app.domain.use_cases.order_uc.OrderRead.read_order", lambda self, k, v: None)
    response = client.get("/order/1")
    assert response.status_code == 200

# Additional tests for create, update, delete can be added similarly with monkeypatching
