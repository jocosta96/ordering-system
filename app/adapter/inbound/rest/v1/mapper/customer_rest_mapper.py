from app.domain.entities import customer_entity
from app.adapter.inbound.rest.v1.entity import customer_rest

def to_domain_entity(
    customer:customer_rest.Customer
) -> customer_entity.Customer:
    
    domain_customer = customer_entity.Customer(
        document = customer.document,
        email = customer.email,
        name = customer.name,
        id = customer.id
    )

    return domain_customer

def to_rest_entity(
    customer: customer_entity.Customer
) -> customer_rest.Customer:
    
    rest_customer = customer_rest.Customer(
        document = customer.document,
        email = customer.email,
        name = customer.name,
        id = customer.id
    )

    return rest_customer
