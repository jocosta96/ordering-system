import typing
from sqlalchemy.orm.exc import NoResultFound

from app.domain.ports import customer_port
from app.domain.entities import customer_entity
from app.adapter.outbound.repositories.sql.orm import database
from app.adapter.outbound.repositories.sql.entities import customer_sql
from app.domain.value_objects import document, name, email
from app.domain.errors.custom_errors import NotFoundError


class CustomerRepoImpl(customer_port.CustomerPort):

    def __init__(self) -> None:
        self._database = database.get_db()
        self._customer_id = None

    @staticmethod
    def _to_domain_entity(customer: customer_sql.Customer) -> customer_entity.Customer:

        domain_customer = customer_entity.Customer(
            document=document.Document(document=str(customer.document)),
            email=email.Email(email=customer.email),
            first_name=name.Name(name=str(customer.first_name)),
            last_name=name.Name(name=str(customer.last_name)),
            id=int(customer.id)  # Assuming id is just an integer
        )

        return domain_customer

    @staticmethod
    def _to_sql_entity(customer: customer_entity.Customer) -> customer_sql.Customer:

        sql_customer = customer_sql.Customer(
            document=customer.document.value,
            email=customer.email.value,
            first_name=customer.first_name.value,
            last_name=customer.last_name.value
        )

        return sql_customer

    def create_customer(self, customer: customer_entity.Customer) -> None:

        db_customer = self._to_sql_entity(customer)
        self._database.add(db_customer)
        self._database.commit()
        self._database.refresh(db_customer)

    def update_customer(self, customer: customer_entity.Customer) -> None:

        customer_dict = customer.__dict__.copy()

        self._database.query(
            customer_sql.Customer
        ).filter_by(
            id=customer_dict['id']
        ).update(
            customer_dict
        )

        self._database.commit()

    def delete_customer(self, customer_id: int):
        self.read_customer(customer_id)
        self._database.query(
            customer_sql.Customer
        ).filter_by(
            id=self._customer_id
        ).delete()
        self._database.commit()

    def read_customer(self, customer_id: int) -> customer_entity.Customer:
        try:
            customer = self._database.query(
                customer_sql.Customer
            ).filter_by(
                id=customer_id
            ).one()
            if not customer:
                raise NoResultFound('Customer not found')
            result = self._to_domain_entity(customer)
            self._customer_id = result.id
            return result
        except NoResultFound:
            NotFoundError('Customer not found')

    def list_customer(self, search_key=None, search_value=None) -> list[customer_entity.Customer]:
        try:
            query = self._database.query(customer_sql.Customer).filter_by()
            if search_key and search_value is not None:
                query = query.filter_by(**{search_key: search_value})
            customers = query.all()
            if not customers:
                raise NoResultFound('Customers not found')
            result = [self._to_domain_entity(cust) for cust in customers]
            return result
        except NoResultFound:
            raise NotFoundError('Customers not found')
