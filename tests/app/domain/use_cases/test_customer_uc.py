import pytest
from unittest.mock import MagicMock
from app.domain.use_cases.customer_uc import (
    CustomerCreate, CustomerDelete, CustomerRead, CustomerUpdate, CustomerList, CustomerAnonymous
)
from app.domain.entities.customer_entity import Customer
from app.domain.value_objects.document import Document
from app.domain.value_objects.email import Email
from app.domain.value_objects.name import Name

@pytest.fixture
def mock_port():
    return MagicMock()

def test_create_customer(mock_port):
    use_case = CustomerCreate(mock_port)
    customer = Customer(id=1, document=Document(document="52998224725"), email=Email(email="john@example.com"), first_name=Name(name="John"), last_name=Name(name="Doe"))
    mock_port.create_customer.return_value = 42
    result = use_case.create_customer(customer)
    mock_port.create_customer.assert_called_once_with(customer)
    assert result == 42

def test_delete_customer(mock_port):
    use_case = CustomerDelete(mock_port)
    mock_port.delete_customer.return_value = "deleted"
    result = use_case.delete_customer(1)
    mock_port.delete_customer.assert_called_once_with(1)
    assert result == "deleted"

def test_read_customer(mock_port):
    use_case = CustomerRead(mock_port)
    customer = Customer(id=1, document=Document(document="52998224725"), email=Email(email="john@example.com"), first_name=Name(name="John"), last_name=Name(name="Doe"))
    mock_port.read_customer.return_value = customer
    result = use_case.read_customer(1)
    mock_port.read_customer.assert_called_once_with(1)
    assert result == customer

def test_update_customer(mock_port):
    use_case = CustomerUpdate(mock_port)
    customer = Customer(id=1, document=Document(document="52998224725"), email=Email(email="john@example.com"), first_name=Name(name="John"), last_name=Name(name="Doe"))
    mock_port.update_customer.return_value = 1
    result = use_case.update_customer(customer)
    mock_port.update_customer.assert_called_once_with(customer)
    assert result == 1

def test_list_customer(mock_port):
    use_case = CustomerList(mock_port)
    mock_port.list_customer.return_value = ["a", "b"]
    result = use_case.list_customer()
    mock_port.list_customer.assert_called_once_with(None, None)
    assert result == ["a", "b"]

def test_get_anonymous_customer(mock_port):
    use_case = CustomerAnonymous(mock_port)
    customer = Customer(id=0, document=Document(document="00000000000"), email=Email(email=""), first_name=Name(name="Anonymous"), last_name=Name(name=""))
    mock_port.get_anonymous_customer.return_value = customer
    result = use_case.get_anonymous_customer()
    mock_port.get_anonymous_customer.assert_called_once_with()
    assert result == customer
