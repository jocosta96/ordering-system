from app.domain.entities import customer_entity
from app.adapter.inbound.rest.entity import customer_rest

def to_domain_entity(
    customer:customer_rest.Customer
) -> customer_entity.Customer:
    
    domain_customer = customer_entity.Customer(
        document = customer.document,
        email = customer.email,
        first_name = customer.first_name,
        last_name = customer.last_name
        #id = customer.id
    )

    return domain_customer

def to_rest_entity(
    customer: customer_entity.Customer
) -> customer_rest.Customer:
    
    rest_customer = customer_rest.Customer(
        document = customer.document,
        email = customer.email,
        first_name = customer.first_name,
        last_name = customer.last_name
        #id = customer.id
    )

    return rest_customer
