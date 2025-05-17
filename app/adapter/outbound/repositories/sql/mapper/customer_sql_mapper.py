from app.domain.entities import customer_entity
from app.adapter.outbound.repositories.sql.entities import customer_sql
from app.domain.value_objects import document, name, email

def to_domain_entity(customer: customer_sql.Customer) -> customer_entity.Customer:

    domain_customer = customer_entity.Customer(
        document = document.Document(document=str(customer.document)),
        email = email.Email(email=str(customer.email)),
        first_name = name.Name(name=str(customer.first_name)),
        last_name = name.Name(name=str(customer.last_name)),
        id = int(customer.id)  # Assuming id is just an integer
    )

    return domain_customer


def to_sql_entity(customer: customer_entity.Customer) -> customer_sql.Customer:

    sql_customer = customer_sql.Customer(
        document = customer.document.value,
        email = customer.email.value,
        first_name = customer.first_name.value,
        last_name = customer.last_name.value
    )

    return sql_customer