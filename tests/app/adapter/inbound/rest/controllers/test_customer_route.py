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

def test_get_anonymous_customer(monkeypatch):
    from app.adapter.outbound.repositories.sql.implementation import customer_impl
    from app.adapter.inbound.rest.mapper import customer_rest_mapper

    class DummyCustomer:
        pass

    def mock_get_anonymous_customer(self):
        return DummyCustomer()

    def mock_to_rest_entity(customer):
        return {
            "id": 1,
            "document": {"document": "39053344705"},
            "email": {"email": "anon@example.com"},
            "first_name": {"name": ""},
            "last_name": {"name": ""}
        }

    monkeypatch.setattr(customer_impl.CustomerRepoImpl, "get_anonymous_customer", mock_get_anonymous_customer)
    monkeypatch.setattr(customer_rest_mapper, "to_rest_entity", mock_to_rest_entity)
    response = client.get("/customer/anonymous")
    assert response.status_code == 200
    assert response.json()["first_name"]["name"] == ""
    assert response.json()["last_name"]["name"] == ""

def test_get_anonymous_customer_not_found(monkeypatch):
    from app.adapter.outbound.repositories.sql.implementation import customer_impl
    from app.domain.errors.custom_errors import NotFoundError

    def mock_get_anonymous_customer(self):
        raise NotFoundError()

    monkeypatch.setattr(customer_impl.CustomerRepoImpl, "get_anonymous_customer", mock_get_anonymous_customer)
    response = client.get("/customer/anonymous")
    assert response.status_code == 404

def test_customer_read_found(monkeypatch):
    from app.domain.use_cases import customer_uc
    from app.adapter.inbound.rest.mapper import customer_rest_mapper

    class DummyCustomer:
        pass

    def mock_read_customer(self, customer_id):
        return DummyCustomer()

    def mock_to_rest_entity(customer):
        return {
            "id": 1,
            "document": {"document": "39053344705"},
            "email": {"email": "test@example.com"},
            "first_name": {"name": "Test"},
            "last_name": {"name": "Customer"}
        }

    monkeypatch.setattr(customer_uc.CustomerRead, "read_customer", mock_read_customer)
    monkeypatch.setattr(customer_rest_mapper, "to_rest_entity", mock_to_rest_entity)
    headers = get_basic_auth_header()
    response = client.get("/customer/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["first_name"]["name"] == "Test"
    assert response.json()["last_name"]["name"] == "Customer"

def test_customer_read_not_found(monkeypatch):
    from app.domain.use_cases import customer_uc
    from app.domain.errors.custom_errors import NotFoundError

    def mock_read_customer(self, customer_id):
        raise NotFoundError()

    monkeypatch.setattr(customer_uc.CustomerRead, "read_customer", mock_read_customer)
    headers = get_basic_auth_header()
    response = client.get("/customer/1", headers=headers)
    assert response.status_code == 404

def test_customer_create(monkeypatch):
    from app.domain.use_cases import customer_uc
    from app.adapter.inbound.rest.mapper import customer_rest_mapper

    def mock_create_customer(self, customer):
        return {
            "id": 1,
            "document": {"document": "39053344705"},
            "email": {"email": "created@example.com"},
            "first_name": {"name": "Created"},
            "last_name": {"name": "Customer"}
        }

    monkeypatch.setattr(customer_uc.CustomerCreate, "create_customer", mock_create_customer)
    monkeypatch.setattr(customer_rest_mapper, "to_domain_entity", lambda x: x)
    headers = get_basic_auth_header()
    data = {
        "id": 1,
        "document": {"document": "39053344705"},
        "email": {"email": "created@example.com"},
        "first_name": {"name": "Created"},
        "last_name": {"name": "Customer"}
    }
    response = client.post("/customer", json=data, headers=headers)
    assert response.status_code in (200, 201)
