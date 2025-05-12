from app.domain.entities import customer_entity
from app.adapter.outbound.repositories.sql.entities import customer_sql

def to_domain_entity(customer: customer_sql.Customer) -> customer_entity.Customer:

    domain_customer = customer_entity.Customer(
        document = customer.document,
        email = customer.email,
        name = customer.name,
        id = customer.id
    )

    return domain_customer


def to_sql_entity(customer: customer_entity.Customer) -> customer_sql.Customer:

    sql_customer = customer_sql.Customer(
        document = customer.document,
        email = customer.email,
        name = customer.name,
        id = customer.id
    )

    return sql_customer