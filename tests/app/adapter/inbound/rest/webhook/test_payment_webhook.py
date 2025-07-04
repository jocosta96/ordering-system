import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.adapter.inbound.webhook import payment

client = TestClient(payment.webhook)

def test_new_payment_success():
    payment_data = {
        "order_id": 123,
        # Add other required fields for Payment here
    }
    with patch('app.adapter.inbound.rest.webhook.payment.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.raise_for_status = lambda: None
        response = client.post('/payment', json=payment_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Payment processed and forwarded."

def test_new_payment_failure():
    payment_data = {
        "order_id": 123,
        # Add other required fields for Payment here
    }
    with patch('app.adapter.inbound.rest.webhook.payment.requests.post') as mock_post:
        mock_post.side_effect = Exception("Connection error")
        response = client.post('/payment', json=payment_data)
        assert response.status_code == 502
        assert "error" in response.json()
