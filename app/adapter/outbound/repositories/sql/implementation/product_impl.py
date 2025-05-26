from sqlalchemy.orm.exc import NoResultFound

from app.domain.ports import product_port
from app.domain.entities import product_entity
from app.adapter.outbound.repositories.sql.orm import database
from app.adapter.outbound.repositories.sql.entities import product_sql
from app.domain.value_objects import name, sku, money, category
from app.adapter.outbound.repositories.sql.entities import product_sql
from app.domain.errors.custom_errors import NotFoundError

class ProductRepoImpl(product_port.ProductPort):

    @staticmethod
    def _to_domain_entity(
        product: product_sql.Product,
        receipt: list[product_sql.ProductReceipt]
    ) -> product_entity.Product:
        
        default_ingredient = [

            product_entity.ProductReceiptItem(
                ingredient_id= item.ingredient.id,
                quantity= item.quantity
            )
            for item in receipt
        ]
        

        domain_product = product_entity.Product(
            id = product.id,
            name= name.Name(name=str(product.name)),
            price= money.Money(amount=float(product.price)),
            category= category.ProductCategory(category=str(product.category)),
            sku= sku.SKU(sku=str(product.sku)),
            default_ingredient= default_ingredient
        )
        return domain_product

    @staticmethod
    def _to_sql_entity(product: product_entity.Product) -> product_sql.Product:
        sql_product = product_sql.Product(
            id=product.id,
            name= product.name.value,
            price= product.price.value,
            category= product.category.value,
            sku= product.sku.value
        )
        return sql_product

    @staticmethod
    def _to_sql_receipt_entity(product: product_entity.Product) -> product_sql.ProductReceipt:
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

    def update_product(self, product: product_entity.Product) -> None:

        product_dict = product.__dict__.copy()
        product_dict.pop('default_ingredient', None)
        product_dict.pop('id', None)

        db_receip = self._to_sql_receipt_entity(product)

        self._database.query(
            product_sql.ProductReceipt
        ).filter_by(
            product_id=product.id
        ).delete()

        self._database.add_all(db_receip)

        self._database.query(
            product_sql.Product
        ).filter_by(
            id=product.id
        ).update(
            product_dict
        )

        self._database.commit()

    def delete_product(self, product_id: str) -> None:

        self._database.query(
            product_sql.Product
        ).filter_by(
            id=product_id
        ).update(
            {'is_active': False}
        )
        
        self._database.commit()
        
    def restore_deleted_product(self, product_id: str) -> None:

        self._database.query(
            product_sql.Product
        ).filter_by(
            id=product_id
        ).update(
            {'is_active': True}
        )
        
        self._database.commit()


    def read_product(self, product_id) -> product_entity.Product:

        try:

            product = self._database.query(
                product_sql.Product
            ).filter_by(
                id=product_id
            ).filter_by(
                is_active = True
            ).one()

            if not product:
                raise NotFoundError('Product not found')

            receipt = self._database.query(
                product_sql.ProductReceipt
            ).filter_by(
                product_id=product.id
            ).all()

            if not receipt:
                raise NotFoundError('Product receipt not found')

            result = self._to_domain_entity(product, receipt)

            return result
        
        except NoResultFound:
            raise NotFoundError('Product not found')


    def list_product(self, search_key=None, search_value=None) -> list[product_entity.Product]:

        try:
            products = self._database.query(
                product_sql.Product
            ).filter_by(
                is_active = True
            ).filter_by(
                **{search_key: search_value}
            ).all()

            result = []

            if not products:
                raise NotFoundError('No products found')
            
            for product in products:

                receipts = self._database.query(
                    product_sql.ProductReceipt
                ).filter_by(
                    product_id=product.id
                ).all()

                if not receipts:
                    raise NotFoundError(f'Receipt for product {product.id} not found')
                
                result.append(self._to_domain_entity(product, receipts))
            
            return result

        except NoResultFound:
            raise NotFoundError('Product not found')
