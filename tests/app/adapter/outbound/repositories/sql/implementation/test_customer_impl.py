import pytest
from unittest.mock import MagicMock, patch
from app.adapter.outbound.repositories.sql.implementation.customer_impl import CustomerRepoImpl
from app.domain.entities.customer_entity import Customer
from app.domain.value_objects.document import Document
from app.domain.value_objects.name import Name
from app.domain.value_objects.email import Email
from sqlalchemy.orm.exc import NoResultFound

TEST_EMAIL = 'test@example.com'

@pytest.fixture
def mock_sql_impl():
    with patch('app.adapter.outbound.repositories.sql.implementation.customer_impl.sql_impl.SQLRepoImpl') as mock:
        yield mock

@pytest.fixture
def customer_entity():
    return Customer(
        document=Document(document='52998224725'),
        email=Email(email=TEST_EMAIL),
        first_name=Name(name='First'),
        last_name=Name(name='Last'),
        id=1
    )

def test_to_sql_entity(customer_entity):
    from app.adapter.outbound.repositories.sql.implementation.customer_impl import CustomerRepoImpl
    sql_customer = CustomerRepoImpl._to_sql_entity(customer_entity)
    assert sql_customer.document == '52998224725'
    assert sql_customer.email == TEST_EMAIL
    assert sql_customer.first_name == 'First'
    assert sql_customer.last_name == 'Last'

def test_init_uses_sql_impl(mock_sql_impl):
    repo = CustomerRepoImpl()
    assert repo._sql_impl is not None

def test_get_anonymous_customer_found(mock_sql_impl):
    repo = CustomerRepoImpl()
    mock_customer = MagicMock()
    mock_customer.document = '52998224725'
    mock_customer.email = TEST_EMAIL
    mock_customer.first_name = 'First'
    mock_customer.last_name = 'Last'
    mock_customer.id = 1
    repo._sql_impl.get_one.return_value = mock_customer
    result = repo.get_anonymous_customer()
    assert result is not None
    repo._sql_impl.get_one.assert_called_once()

def test_get_anonymous_customer_not_found(mock_sql_impl):
    repo = CustomerRepoImpl()
    repo._sql_impl.get_one.side_effect = NoResultFound()
    with patch('app.adapter.outbound.repositories.sql.implementation.customer_impl.customer_sql.Customer') as mock_sql_customer:
        mock_sql_customer.return_value = MagicMock(document='52998224725', email=TEST_EMAIL, first_name='First', last_name='Last', id=1)
        repo._sql_impl.add_one = MagicMock()
        result = repo.get_anonymous_customer()
        assert result is not None
        repo._sql_impl.add_one.assert_called_once()

def test_create_customer(mock_sql_impl, customer_entity):
    repo = CustomerRepoImpl()
    repo._sql_impl.add_one = MagicMock()
    repo.create_customer(customer_entity)
    repo._sql_impl.add_one.assert_called_once()

def test_to_domain_entity_valid():
    from app.adapter.outbound.repositories.sql.implementation.customer_impl import CustomerRepoImpl
    mock_customer = MagicMock()
    mock_customer.document = '52998224725'
    mock_customer.email = TEST_EMAIL
    mock_customer.first_name = 'First'
    mock_customer.last_name = 'Last'
    mock_customer.id = 1
    result = CustomerRepoImpl._to_domain_entity(mock_customer)
    assert result.document.value == '52998224725'
    assert result.email.value == TEST_EMAIL
    assert result.first_name.value == 'First'
    assert result.last_name.value == 'Last'
    assert result.id == 1

def test_update_customer_success(mock_sql_impl, customer_entity):
    repo = CustomerRepoImpl()
    repo._sql_impl.update = MagicMock()
    repo.update_customer(customer_entity)
    repo._sql_impl.update.assert_called_once()


def test_delete_customer_success(mock_sql_impl, customer_entity):
    from app.adapter.outbound.repositories.sql.entities.customer_sql import Customer as RealCustomer
    repo = CustomerRepoImpl()
    repo.read_customer = MagicMock(return_value=customer_entity)
    repo._sql_impl.delete = MagicMock()
    repo.delete_customer(customer_entity.id)
    repo._sql_impl.delete.assert_called_once_with(
        RealCustomer, dict_filter={"id": customer_entity.id}
    )


def test_read_customer_found(mock_sql_impl, customer_entity):
    repo = CustomerRepoImpl()
    mock_customer = MagicMock()
    mock_customer.document = customer_entity.document.value
    mock_customer.email = customer_entity.email.value
    mock_customer.first_name = customer_entity.first_name.value
    mock_customer.last_name = customer_entity.last_name.value
    mock_customer.id = customer_entity.id
    repo._sql_impl.get_one.return_value = mock_customer
    result = repo.read_customer(customer_entity.id)
    assert result.id == customer_entity.id
    repo._sql_impl.get_one.assert_called_once()


def test_read_customer_not_found(mock_sql_impl):
    repo = CustomerRepoImpl()
    repo._sql_impl.get_one.side_effect = NoResultFound()
    result = repo.read_customer(999)
    assert result is None  # Should return None if not found


def test_list_customer_success(mock_sql_impl, customer_entity):
    repo = CustomerRepoImpl()
    mock_customer = MagicMock()
    mock_customer.document = customer_entity.document.value
    mock_customer.email = customer_entity.email.value
    mock_customer.first_name = customer_entity.first_name.value
    mock_customer.last_name = customer_entity.last_name.value
    mock_customer.id = customer_entity.id
    repo._sql_impl.list_all.return_value = [mock_customer]
    result = repo.list_customer()
    assert isinstance(result, list)
    assert result[0].id == customer_entity.id
    repo._sql_impl.list_all.assert_called_once()


def test_list_customer_empty(mock_sql_impl):
    repo = CustomerRepoImpl()
    repo._sql_impl.list_all.return_value = []
    with pytest.raises(Exception):
        repo.list_customer()


def test_list_customer_no_result_found(mock_sql_impl):
    repo = CustomerRepoImpl()
    repo._sql_impl.list_all.side_effect = NoResultFound()
    with pytest.raises(Exception):
        repo.list_customer()
