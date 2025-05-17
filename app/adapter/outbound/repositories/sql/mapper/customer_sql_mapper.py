from app.domain.entities import customer_entity
from app.adapter.outbound.repositories.sql.entities import customer_sql

def to_domain_entity(customer: customer_sql.Customer) -> customer_entity.Customer:

    domain_customer = customer_entity.Customer(
        document = str(customer.document),
        email = str(customer.email),
        first_name = str(customer.first_name),
        last_name = str(customer.last_name),
        id = customer.id
    )

    return domain_customer


def to_sql_entity(customer: customer_entity.Customer) -> customer_sql.Customer:

    sql_customer = customer_sql.Customer(
        document = customer.document.get(),
        email = customer.email.get(),
        first_name = customer.first_name.get(),
        last_name = customer.last_name.get()
        #id = customer.id
    )

    return sql_customer