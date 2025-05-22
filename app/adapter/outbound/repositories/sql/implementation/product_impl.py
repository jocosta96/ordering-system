import typing
from sqlalchemy.orm.exc import NoResultFound

from app.domain.ports import product_port
from app.domain.entities import product_entity
from app.adapter.outbound.repositories.sql.orm import database
from app.adapter.outbound.repositories.sql.entities import product_sql
from app.domain.value_objects import name, sku, codebar, money, category
from app.adapter.outbound.repositories.sql.entities import product_sql

class ProductRepoImpl(product_port.ProductPort):


    @staticmethod
    def _to_domain_entity(product: product_sql.Product) -> product_entity.Product:

        domain_product = product_entity.Product(
            id = product.id,
            name= name.Name(name=str(product.name)),
            price= money.Money(amount=float(product.price)),
            category= category.ProductCategory(category=str(product.category)),
            sku= sku.SKU(sku=str(product.sku)),
            codebar= codebar.Codebar(code=str(product.codebar))
        )

        return domain_product

    @staticmethod
    def _to_sql_entity(product: product_entity.Product) -> product_sql.Product:

        sql_product = product_sql.Product(
            name= product.name.value,
            price= product.price.value,
            category= product.category.value,
            sku= product.sku.value,
            codebar= product.codebar.value
        )

        return sql_product


    @staticmethod
    def _to_sql_receipt_entity(product: product_entity.Product) -> product_sql.ProductReceipt:

        print('****'*20, len(product.default_ingredient), "INGREDIENTS")

        sql_product = [
            product_sql.ProductReceipt(
                product_id= product.id,
                ingredient_id= ingredient.ingredient_id,
                quantity= ingredient.quantity,
            )
            for ingredient in product.default_ingredient
        ]

        return sql_product

    def __init__(self) -> None:
        self._database = database.get_db()
        self._user_id = None
    
    def create_product(self, product: product_entity.Product) -> None:

        db_receip = self._to_sql_receipt_entity(product)
        db_product = self._to_sql_entity(product)

        self._database.add_all(db_receip)
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
            result = self._to_domain_entity(data)
            self._user_id = result.id
        except NoResultFound:
            result = 'User not found'
        return result
