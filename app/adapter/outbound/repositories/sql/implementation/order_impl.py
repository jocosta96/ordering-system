from app.domain.ports.order_port import OrderPort
from app.domain.entities import order_entity
from app.adapter.outbound.repositories.sql.orm import database
from app.adapter.outbound.repositories.sql.entities import order_sql

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
                order_id = receipt.order_id,
                order_item_id = receipt.order_item_id,
                product_id = receipt.product_id,
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
        
    def read_order(self, search_key, search_value) -> order_entity.Order:
        pass