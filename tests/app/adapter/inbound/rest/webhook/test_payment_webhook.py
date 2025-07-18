from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.adapter.inbound.webhook import payment
import httpx

client = TestClient(payment.webhook)


def test_new_payment_success():
    payment_data = {
        "order_id": "123",  # must be a string to match the Pydantic model
        # Add other required fields for Payment here
    }
    with patch("httpx.AsyncClient.patch", new_callable=AsyncMock) as mock_patch:
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.raise_for_status = lambda: None
        response = client.post("/webhook/mercadopago", json=payment_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Notification received, processing payment..."


def test_new_payment_failure():
    payment_data = {
        "order_id": "123",  # must be a string to match the Pydantic model
        # Add other required fields for Payment here
    }
    with patch("httpx.AsyncClient.patch", new_callable=AsyncMock) as mock_patch:
        mock_patch.side_effect = httpx.RequestError("Connection error", request=None)
        response = client.post("/webhook/mercadopago", json=payment_data)
        assert response.status_code == 200  # The webhook always returns 200, even on failure
        assert response.json()["message"] == "Notification received, processing payment..."
