import typing
from sqlalchemy.orm.exc import NoResultFound

from app.domain.ports import customer_port
from app.domain.entities import customer_entity
from app.adapter.outbound.repositories.sql.orm import database
from app.adapter.outbound.repositories.sql.entities import customer_sql
from app.domain.value_objects import document, name, email
from app.domain.errors.custom_errors import NotFoundError

from app.adapter.outbound.repositories.sql.implementation import sql_impl

class CustomerRepoImpl(customer_port.CustomerPort):
    
    def __init__(self) -> None:
        self._customer_id = None
        self._sql_impl = sql_impl.SQLRepoImpl()

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

    def get_anonymous_customer(self) -> customer_entity.Customer:

        try:
            sql_customer = self._sql_impl.get_one(
                customer_sql.Customer,
                dict_filter={'id': -1}
            )
        except NoResultFound:
            sql_customer = customer_sql.Customer(
                document='',
                email='',
                first_name='',
                last_name='',
                id=-1
            )
            self._sql_impl.add_one(sql_customer)
        finally:
            domain_customer = self._to_domain_entity(sql_customer)
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
        self._sql_impl.add_one(db_customer)

    def update_customer(self, customer: customer_entity.Customer) -> None:
        customer_dict = customer.__dict__.copy()
        self._sql_impl.update(
            customer_sql.Customer,
            entity_dict=customer_dict,
            dict_filter={
                'id': customer_dict['id']
            }
        )

    def delete_customer(self, customer_id: int):
        self.read_customer(customer_id)
        self._sql_impl.delete(
            customer_sql.Customer,
            dict_filter={
                'id': customer_id
            }
        )

    def read_customer(self, customer_id: int) -> customer_entity.Customer:
        try:
            customer = self._sql_impl.get_one(
                customer_sql.Customer,
                dict_filter={
                    'id': customer_id
                }
            )
            if not customer:
                raise NoResultFound('Customer not found')
            result = self._to_domain_entity(customer)
            self._customer_id = result.id
            return result
        except NoResultFound:
            NotFoundError('Customer not found')

    def list_customer(self, search_key=None, search_value=None) -> list[customer_entity.Customer]:
        try:
            customers = self._sql_impl.list_all(
                customer_sql.Customer,
                dict_filter={
                    search_key: search_value
                } if search_key and search_value else {}
            )
            if not customers:
                raise NoResultFound('Customers not found')
            result = [self._to_domain_entity(cust) for cust in customers]
            return result
        except NoResultFound:
            raise NotFoundError('Customers not found')
