import typing
from sqlalchemy.orm.exc import NoResultFound

from app.domain.ports import order_port
from app.domain.entities import order_entity
from app.adapter.outbound.repositories.sql.orm import database
from app.adapter.outbound.repositories.sql.entities import order_sql
from app.adapter.outbound.repositories.sql.mapper import order_sql_mapper


class OrderRepoImpl(order_port.OrderPort):

    def __init__(self) -> None:
        self._database = database.get_db()
        self._user_id = None
    
    def create_order(self, order: order_entity.Order) -> None:

        db_order = order_sql_mapper.to_sql_entity(order)
        self._database.add(db_order)
        self._database.commit()
        self._database.refresh(db_order)

    def update_order(self, search_key, search_value, order: order_entity.Order) -> None:

        self.read_order(search_key, search_value)

        order_dict = order.__dict__.copy()
        order_dict.pop('id', None)

        self._database.query(
            order_sql.Order
        ).filter_by(
            id=self._user_id
        ).update(
            order_dict
        )

        self._database.commit()

    def end_order(self, search_key, search_value, order: order_entity.Order) -> None:

        self.read_order(search_key, search_value)

        order_dict = order.__dict__.copy()
        order_dict.pop('id', None)

        self._database.query(
            order_sql.Order
        ).filter_by(
            id=self._user_id
        ).update(
            order_dict
        )

        self._database.commit()

    def delete_order(self):
        
        self._database.query(
            order_sql.Order
        ).filter_by(
            id=self._user_id
        ).delete()
        
        self._database.commit()
        
    def read_order(self, search_key, search_value) -> order_entity.Order:
        
        try:
            data = self._database.query(order_sql.Order).filter_by(**{search_key:search_value}).one()
            result = order_sql_mapper.to_domain_entity(data)
            self._user_id = result.id
        except NoResultFound:
            result = 'User not found'
        return result
