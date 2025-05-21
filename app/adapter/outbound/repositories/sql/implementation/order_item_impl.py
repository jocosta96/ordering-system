from app.domain.ports import order_item_port
from app.domain.entities import order_item_entity
from app.adapter.outbound.repositories.sql.orm import database
from app.adapter.outbound.repositories.sql.entities import order_item_sql
from app.adapter.outbound.repositories.sql.mapper import order_item_sql_mapper


class OrderItemRepoImpl(order_item_port.OrderItemPort):
    def __init__(self) -> None:
        self._database = database.get_db()
        self._ordem_item_id = None

    def create_order_item(self, order_item: order_item_entity.OrderItem) -> None:
        db_order_item, db_order_item_receipt = order_item_sql_mapper.to_sql_entity(order_item)
        self._database.add(db_order_item)
        self._database.commit()
        self._database.refresh(db_order_item)

        for item in db_order_item_receipt:
            self._database.add(item)
            self._database.commit()
            self._database.refresh(item)

    def read_order_item(self, search_key, search_value) -> order_item_entity.OrderItem:
        order_item = self._database.query(
            order_item_sql.OrderItem
        ).filter_by(
            **{search_key: search_value}
        ).first()

        if not order_item:
            raise Exception("Order item not found")
        self._user_id = order_item.id
        return order_item
    
    def update_order_item(self, search_key, search_value, order_item: order_item_entity.OrderItem) -> None:
        self.read_order_item(search_key, search_value)

        order_item_dict = order_item.__dict__.copy()
        order_item_dict.pop('id', None)

        self._database.query(
            order_item_sql.OrderItem
        ).filter_by(
            id=self._ordem_item_id
        ).update(
            order_item_dict
        )

        self._database.commit()