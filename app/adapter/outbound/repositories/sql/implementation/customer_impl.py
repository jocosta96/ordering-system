import typing
from sqlalchemy.orm.exc import NoResultFound

from app.domain.ports import customer_port
from app.domain.entities import customer_entity
from app.adapter.outbound.repositories.sql.orm import database
from app.adapter.outbound.repositories.sql.entities import customer_sql
from app.adapter.outbound.repositories.sql.mapper import customer_sql_mapper


class CustomerRepoImpl(customer_port.CustomerPort):

    def __init__(self) -> None:
        self._database = database.get_db()
        self._user_id = None
    
    def create_customer(self, customer: customer_entity.Customer) -> None:

        db_customer = customer_sql_mapper.to_sql_entity(customer)
        self._database.add(db_customer)
        self._database.commit()
        self._database.refresh(db_customer)

    def update_customer(self, search_key, search_value, customer: customer_entity.Customer) -> None:

        self.read_customer(search_key, search_value)

        customer_dict = customer.__dict__.copy()
        customer_dict.pop('id', None)

        self._database.query(
            customer_sql.Customer
        ).filter_by(
            id=self._user_id
        ).update(
            customer_dict
        )

        self._database.commit()

    def delete_customer(self):
        
        self._database.query(
            customer_sql.Customer
        ).filter_by(
            id=self._user_id
        ).delete()
        
        self._database.commit()
        
    def read_customer(self, search_key, search_value) -> customer_entity.Customer:
        
        try:
            data = self._database.query(customer_sql.Customer).filter_by(**{search_key:search_value}).one()
            result = customer_sql_mapper.to_domain_entity(data)
            self._user_id = result.id
        except NoResultFound:
            result = 'User not found'
        return result
