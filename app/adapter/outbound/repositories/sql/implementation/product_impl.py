from sqlalchemy.orm.exc import NoResultFound

from app.domain.ports import product_port
from app.domain.entities import product_entity, ingredient_entity
from app.adapter.outbound.repositories.sql.orm import database
from app.domain.value_objects import name, sku, money, category
from app.adapter.outbound.repositories.sql.entities import product_sql, ingredient_sql
from app.domain.errors.custom_errors import NotFoundError

from app.adapter.outbound.repositories.sql.implementation import sql_impl

class ProductRepoImpl(product_port.ProductPort):

    def __init__(self) -> None:
        self._sql_impl = sql_impl.SQLRepoImpl()
        self._user_id = None

    @staticmethod
    def _to_domain_entity(
        product: product_sql.Product,
        receipt: list[product_sql.ProductReceipt]
    ) -> product_entity.Product:
        
        print('****'*20, product.__dict__)
        print('****'*20, receipt[0].__dict__)
        
        default_ingredient = [

            product_entity.ProductReceiptItem(
                ingredient = ingredient_entity.Ingredient(
                    id = item.ingredient_id,
                    name = name.Name(
                        name=str(item.ingredient.name)
                    ),
                    price = money.Money(
                        amount=float(item.ingredient.price)
                    ),
                    product_category = category.ProductCategory(
                        category=str(item.ingredient.product_category)
                    ),
                    is_active = item.ingredient.is_active,
                ),
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
                product_id=product.id,
                ingredient_id=ingredient.ingredient.id,
                quantity=ingredient.quantity,
            )
            for ingredient in product.default_ingredient
        ]
        return sql_product

    
    def create_product(self, product: product_entity.Product) -> None:
        
        print('***'*100, product.__dict__)

        db_receip = self._to_sql_receipt_entity(product)
        db_product = self._to_sql_entity(product)

        self._sql_impl.add_one(db_product)
        self._sql_impl.add_all(db_receip)

    def update_product(self, product: product_entity.Product) -> None:

        product_dict = product.__dict__.copy()
        product_dict.pop('default_ingredient', None)
        product_dict.pop('id', None)

        db_receip = self._to_sql_receipt_entity(product)

        self._sql_impl.delete(
            entity=product_sql.ProductReceipt,
            dict_filter={
                'product_id': product.id
            }
        )

        self._sql_impl.add_all(
            entities=db_receip
        )

        self._sql_impl.update(
            entity=product_sql.Product,
            entity_dict=product_dict,
            dict_filter={
                'id': product.id
            }
        )

    def delete_product(self, product_id: str) -> None:
        self._sql_impl.update(
            entity=product_sql.Product,
            entity_dict={'is_active': False},
            dict_filter={
                'id': product_id
            }
        )
        
    def restore_deleted_product(self, product_id: str) -> None:

        self._sql_impl.update(
            entity=product_sql.Product,
            entity_dict={'is_active': True},
            dict_filter={
                'id': product_id
            }
        )

    def read_product(self, product_id) -> product_entity.Product:

        try:
            
            product = self._sql_impl.get_one(
                entity=product_sql.Product,
                dict_filter={
                    'id': product_id,
                    'is_active': True
                }
            )

            if not product:
                raise NotFoundError('Product not found')

            receipt = self._sql_impl.list_product_receipts(
                product_sql_entity=product_sql.ProductReceipt,
                ingredient_sql_entity=ingredient_sql.Ingredient,
                product_id=product.id
            )

            if not receipt:
                raise NotFoundError('Product receipt not found')

            result = self._to_domain_entity(product, receipt)

            return result
        
        except NoResultFound:
            raise NotFoundError('Product not found')


    def list_product(self, search_key=None, search_value=None) -> list[product_entity.Product]:

        try:

            products = self._sql_impl.list_all(
                entity=product_sql.Product,
                dict_filter={
                    'is_active': True,
                    search_key: search_value
                }
            )


            result = []

            if not products:
                raise NotFoundError('No products found')
            
            for product in products:

                receipts = self._sql_impl.list_product_receipts(
                    product_sql_entity=product_sql,
                    ingredient_sql_entity=ingredient_sql,
                    product_id=product.id
                )

                if not receipts:
                    raise NotFoundError(f'Receipt for product {product.id} not found')
                
                result.append(self._to_domain_entity(product, receipts))
            
            return result

        except NoResultFound:
            raise NotFoundError('Product not found')
