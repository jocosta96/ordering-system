from app.domain.entities.customer_entity import Customer
from app.domain.value_objects.document import Document
from app.domain.value_objects.email import Email
from app.domain.value_objects.name import Name

def test_customer_creation():
    customer = Customer(
        id=1,
        document=Document(document="52998224725"),  # valid CPF
        email=Email(email="john@example.com"),
        first_name=Name(name="John"),
        last_name=Name(name="Doe")
    )
    assert customer.id == 1
    assert customer.document.value == "52998224725"
    assert customer.email.value == "john@example.com"
    assert customer.first_name.value == "John"
    assert customer.last_name.value == "Doe"
