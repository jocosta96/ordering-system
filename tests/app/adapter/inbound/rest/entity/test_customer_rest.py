from app.adapter.inbound.rest.entity.customer_rest import Customer
from app.domain.value_objects.document import Document
from app.domain.value_objects.email import Email
from app.domain.value_objects.name import Name

def test_customer_creation():
    customer = Customer(
        id=1,
        document=Document(document="83904593021"),
        email=Email(email="email@domain.com"),
        first_name=Name(name="PRIM"),
        last_name=Name(name="SEC")
    )
    assert customer.id == 1
    assert customer.document.document == "83904593021"
    assert customer.email.email == "email@domain.com"
    assert customer.first_name.name == "PRIM"
    assert customer.last_name.name == "SEC"
