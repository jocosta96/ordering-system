import os
import base64
import dotenv
import pytest
from fastapi.testclient import TestClient
from app.main import app

dotenv.load_dotenv()
client = TestClient(app)

def get_basic_auth_header(username=None, password=None):
    username = username or os.environ.get("API_USER", "user")
    password = password or os.environ.get("API_PWD", "pass")
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}

def test_check_credentials_success(monkeypatch):
    from app.domain.use_cases import customer_uc
    from app.adapter.inbound.rest.mapper import customer_rest_mapper
    from app.domain.entities.customer_entity import Customer
    from app.domain.value_objects.document import Document
    from app.domain.value_objects.email import Email
    from app.domain.value_objects.name import Name

    def mock_read_customer(self, customer_id):
        return Customer(
            id=1,
            document=Document(document="83904593021"),
            email=Email(email="email@domain.com"),
            first_name=Name(name="PRIM"),
            last_name=Name(name="SEC")
        )

    monkeypatch.setattr(customer_uc.CustomerRead, "read_customer", mock_read_customer)
    monkeypatch.setattr(customer_rest_mapper, "to_rest_entity", lambda x: {
        "id": x.id,
        "document": {"document": x.document.value},
        "email": {"email": x.email.value},
        "first_name": {"name": x.first_name.value},
        "last_name": {"name": x.last_name.value},
    })
    headers = get_basic_auth_header()
    response = client.get("/customer/1", headers=headers)
    assert response.status_code in (200, 404)

def test_check_credentials_fail():
    headers = get_basic_auth_header(username="wrong", password="wrong")
    response = client.get("/customer/1", headers=headers)
    assert response.status_code == 401
