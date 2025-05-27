from app.domain.ports.order_port import OrderPort
from app.domain.entities import order_entity, product_entity, ingredient_entity
from app.domain.value_objects import money, status, category, sku
from app.domain.errors.custom_errors import NotFoundError
from app.adapter.outbound.repositories.sql.orm import database
from app.adapter.outbound.repositories.sql.entities import order_sql, product_sql, ingredient_sql


class OrderRepoImpl(OrderPort):

    def __init__(self) -> None:
        self._database = database.get_db()

    @staticmethod
    def _order_entity_to_sql(order: order_entity.Order) -> order_sql.Order:
        
        order_sql_entity = order_sql.Order(
            
            id = order.id,
            customer_id = order.customer_id,
            value = order.value,
#            order_items = order.order_items,
            payment_date = order.payment_date,
            payment_transaction_id = order.payment_transaction_id,
            start_date = order.start_date,
            end_date = order.end_date,
            has_payment_verified = order.has_payment_verified,
            status = order.status 
        )

        return order_sql_entity

    @staticmethod
    def _order_item_entity_to_sql(order: order_entity.Order) -> order_sql.OrderItem:

        order_item_sql = [

            order_sql.OrderItem(
                id = item.id,
                order_id = order.id,
                product_id = item.product.id,
                price = item.price
            ) for item in order.order_items
        ]

        return order_item_sql
    
    @staticmethod
    def _order_item_receipt_entity_to_sql(order: order_entity.Order) -> order_sql.OrderItemReceipt:

        print('****'*20, order.__dict__)
        print('****'*20, order.order_items[0].__dict__)

        order_item_receipt_sql = [
            order_sql.OrderItemReceipt(
                order_id = order.id,
                order_item_id = item.id,
                product_id = item.product.id,
                ingredient_id = receipt.ingredient.id,
                quantity = receipt.quantity
            ) for item in order.order_items
              for receipt in item.get_item_receipt()
        ]

        return order_item_receipt_sql


    def create_order(self, order: order_entity.Order) -> None:

        db_order = self._order_entity_to_sql(order)
        db_order_items = self._order_item_entity_to_sql(order)
        db_order_item_receipts = self._order_item_receipt_entity_to_sql(order)

        self._database.add(db_order)
        self._database.add_all(db_order_items)
        self._database.add_all(db_order_item_receipts)

        self._database.commit()

        self._database.refresh(db_order)
        for item in db_order_items:
            self._database.refresh(item)
        for receipt in db_order_item_receipts:
            self._database.refresh(receipt)

    def update_order(self, search_key, search_value, order: order_entity.Order) -> None:
        pass

    def delete_order(self):
        pass

    def _to_domain_entity(
            self,
            order_sql: order_sql.Order,
            list_order_items_sql: list[order_sql.OrderItem],
            list_order_item_receipts_sql: list[order_sql.OrderItemReceipt]
        ) -> order_entity.Order:
        """"""
        order_items = [
            order_entity.OrderItem(
                order_id=order_sql.id,
                product = product_entity.Product(
                    name = order_items_sql.product.name,
                    price = order_items_sql.product.price,
                    category = order_items_sql.product.category,
                    sku = sku.SKU(sku=order_items_sql.product.sku),
                    default_ingredient = [
                        product_entity.ProductReceiptItem(
                            ingredient = ingredient_entity.Ingredient(
                                id = receipt.ingredient.id,
                                name = receipt.ingredient.name,
                                price = money.Money(amount=receipt.ingredient.price),
                                product_category = product_entity.ProductCategory(
                                    category=receipt.ingredient.product_category
                                ),
                                is_active=receipt.ingredient.is_active
                            ),
                            quantity=receipt.quantity
                        )
                        for receipt in order_items_sql.product.product_receipts
                    ],
                    id = order_items_sql.product.id
                ),
                additional_ingredient = [],
                remove_ingredient = [],
                price = money.Money(amount=order_items_sql.price),
                item_receipt = [
                    product_entity.ProductReceiptItem(
                        ingredient= ingredient_entity.Ingredient(
                            id=receipt.ingredient_id,
                            name=receipt.ingredient.name,
                            price=money.Money(amount=receipt.ingredient.price),
                            product_category=category.ProductCategory(
                                category=receipt.ingredient.product_category
                            ),
                            is_active=receipt.ingredient.is_active
                        ),
                        quantity = receipt.quantity
                    )
                    for receipt in list_order_item_receipts_sql
                    if receipt.order_item_id == order_items_sql.id
                ],
                id = order_items_sql.id
            ) for order_items_sql in list_order_items_sql
        ]

        order = order_entity.Order(
            customer_id = order_sql.customer_id,
            order_items = order_items,
            value  = order_sql.value,
            status = status.OrderStatus(status=status.OrderStatusType(order_sql.status)),
            start_date = order_sql.start_date,
            end_date = order_sql.end_date,
            has_payment_verified = order_sql.has_payment_verified,
            payment_date = order_sql.payment_date,
            payment_transaction_id = order_sql.payment_transaction_id,
            id = order_sql.id
        )

        return order
        """"""

    def read_order(self, search_key, search_value) -> order_entity.Order:
        
        order = self._database.query(
            order_sql.Order
        ).filter_by(
            **{search_key: search_value}
        ).one()

        if not order:
            raise NotFoundError('Order not found')

        list_order_items = self._database.query(
            order_sql.OrderItem
        ).filter(
            order_sql.OrderItem.order_id == order.id
        ).join(
            product_sql.Product,
            order_sql.OrderItem.product_id == product_sql.Product.id
        ).join(
            product_sql.ProductReceipt,
            product_sql.Product.id == product_sql.ProductReceipt.product_id
        ).join(
            ingredient_sql.Ingredient,
            product_sql.ProductReceipt.ingredient_id == ingredient_sql.Ingredient.id
        ).all()

        list_order_item_receipts = self._database.query(
            order_sql.OrderItemReceipt
        ).filter(
            order_sql.OrderItemReceipt.order_id == order.id
        ).join(
            ingredient_sql.Ingredient,
            order_sql.OrderItemReceipt.ingredient_id == ingredient_sql.Ingredient.id
        ).all()

        domain_order = self._to_domain_entity(
            order_sql=order,
            list_order_items_sql=list_order_items,
            list_order_item_receipts_sql=list_order_item_receipts
        )

        return domain_order
 
    
#test = OrderRepoImpl().read_order(
#    'id', 
#    'f80ddf99-245f-455a-8b21-a05cee4195c5'
#)