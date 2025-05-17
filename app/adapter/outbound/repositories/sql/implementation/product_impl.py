import typing
from sqlalchemy.orm.exc import NoResultFound

from app.domain.ports import product_port
from app.domain.entities import product_entity
from app.adapter.outbound.repositories.sql.orm import database
from app.adapter.outbound.repositories.sql.entities import product_sql
from app.adapter.outbound.repositories.sql.mapper import product_sql_mapper


class ProductRepoImpl(product_port.ProductPort):

    def __init__(self) -> None:
        self._database = database.get_db()
        self._user_id = None
    
    def create_product(self, product: product_entity.Product) -> None:

        db_product = product_sql_mapper.to_sql_entity(product)
        self._database.add(db_product)
        self._database.commit()
        self._database.refresh(db_product)

    def update_product(self, search_key, search_value, product: product_entity.Product) -> None:

        self.read_product(search_key, search_value)

        product_dict = product.__dict__.copy()
        product_dict.pop('id', None)

        self._database.query(
            product_sql.Product
        ).filter_by(
            id=self._user_id
        ).update(
            product_dict
        )

        self._database.commit()

    def delete_product(self):
        
        self._database.query(
            product_sql.Product
        ).filter_by(
            id=self._user_id
        ).delete()
        
        self._database.commit()
        
    def read_product(self, search_key, search_value) -> product_entity.Product:
        
        try:
            data = self._database.query(product_sql.Product).filter_by(**{search_key:search_value}).one()
            result = product_sql_mapper.to_domain_entity(data)
            self._user_id = result.id
        except NoResultFound:
            result = 'User not found'
        return result
