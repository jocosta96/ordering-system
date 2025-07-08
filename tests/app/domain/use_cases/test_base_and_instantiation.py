import pytest
from app.domain.use_cases.product_uc import BaseProductUseCase, ProductCreate, ProductDelete, ProductRead, ProductUpdate, ProductRestoreDeleted, ProductList
from app.domain.use_cases.order_uc import BaseOrderUseCase, OrderCreate, OrderRead, OrderUpdate, OrderPay, OrderList, OrderDelete
from app.domain.use_cases.customer_uc import BaseCustomerUseCase, CustomerCreate, CustomerDelete, CustomerRead, CustomerUpdate, CustomerList, CustomerAnonymous

# Dummy port classes for instantiation
def make_dummy_product_port():
    class DummyProductPort:
        pass
    return DummyProductPort()

def make_dummy_order_port():
    class DummyOrderPort:
        pass
    return DummyOrderPort()

def make_dummy_customer_port():
    class DummyCustomerPort:
        pass
    return DummyCustomerPort()


def test_base_product_use_case_instantiation():
    base = BaseProductUseCase(make_dummy_product_port())
    assert isinstance(base, BaseProductUseCase)

def test_product_use_cases_instantiation():
    port = make_dummy_product_port()
    assert isinstance(ProductCreate(port), ProductCreate)
    assert isinstance(ProductDelete(port), ProductDelete)
    assert isinstance(ProductRead(port), ProductRead)
    assert isinstance(ProductUpdate(port), ProductUpdate)
    assert isinstance(ProductRestoreDeleted(port), ProductRestoreDeleted)
    assert isinstance(ProductList(port), ProductList)

def test_base_order_use_case_instantiation():
    base = BaseOrderUseCase(make_dummy_order_port())
    assert isinstance(base, BaseOrderUseCase)

def test_order_use_cases_instantiation():
    port = make_dummy_order_port()
    assert isinstance(OrderCreate(port), OrderCreate)
    assert isinstance(OrderRead(port), OrderRead)
    assert isinstance(OrderUpdate(port), OrderUpdate)
    assert isinstance(OrderPay(port), OrderPay)
    assert isinstance(OrderList(port), OrderList)
    assert isinstance(OrderDelete(port), OrderDelete)

def test_base_customer_use_case_instantiation():
    base = BaseCustomerUseCase(make_dummy_customer_port())
    assert isinstance(base, BaseCustomerUseCase)

def test_customer_use_cases_instantiation():
    port = make_dummy_customer_port()
    assert isinstance(CustomerCreate(port), CustomerCreate)
    assert isinstance(CustomerDelete(port), CustomerDelete)
    assert isinstance(CustomerRead(port), CustomerRead)
    assert isinstance(CustomerUpdate(port), CustomerUpdate)
    assert isinstance(CustomerList(port), CustomerList)
    assert isinstance(CustomerAnonymous(port), CustomerAnonymous)
