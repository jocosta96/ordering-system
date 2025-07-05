from typing import Type
from app.adapter.outbound.repositories.sql.implementation.factory.sql_repo import (
    SQLRepository,
)
from app.adapter.outbound.repositories.sql.orm import database
from sqlalchemy import case


class SQLRepoImpl(SQLRepository):
    def __init__(self) -> None:
        self._database = database.get_db()

    def try_commit(self) -> None:
        try:
            self._database.commit()
        except Exception as e:
            self._database.rollback()
            raise e

    def get_one(self, entity: Type[database.Base], dict_filter: dict) -> database.Base:
        sql_entity = self._database.query(entity).filter_by(**dict_filter).one()
        return sql_entity

    def add_one(self, entity: Type[database.Base]) -> None:
        self._database.add(entity)
        self.try_commit()
        self._database.refresh(entity)

    def add_all(self, entities: list[Type[database.Base]]) -> None:
        self._database.add_all(entities)
        self.try_commit()
        for entity in entities:
            self._database.refresh(entity)

    def list_all(
        self,
        entity: Type[database.Base],
        dict_filter: dict = None,
        order_by_column=None,
    ) -> list[Type[database.Base]]:
        """Returns a list of all entities in the database."""
        query = self._database.query(entity)
        if dict_filter:
            query = query.filter_by(**dict_filter)
        if order_by_column is not None:
            query = query.order_by(order_by_column)
        return query.all()

    def update(
        self, entity: Type[database.Base], entity_dict: dict, dict_filter: dict
    ) -> None:
        self._database.query(entity).filter_by(**dict_filter).update(entity_dict)
        self.try_commit()

    def delete(self, entity: Type[database.Base], dict_filter: dict) -> None:
        self._database.query(entity).filter_by(**dict_filter).delete()
        self.try_commit()

    def list_order_items(
        self,
        order_sql_entity: Type[database.Base],
        ingredient_sql_entity: Type[database.Base],
        order_id: str,
        product_sql_entity: Type[database.Base],
    ) -> list[Type[database.Base]]:
        list_order_items = (
            self._database.query(order_sql_entity.OrderItem)
            .filter(order_sql_entity.OrderItem.order_id == order_id)
            .join(
                product_sql_entity.Product,
                order_sql_entity.OrderItem.product_id == product_sql_entity.Product.id,
            )
            .join(
                product_sql_entity.ProductReceipt,
                product_sql_entity.Product.id
                == product_sql_entity.ProductReceipt.product_id,
            )
            .join(
                ingredient_sql_entity.Ingredient,
                product_sql_entity.ProductReceipt.ingredient_id
                == ingredient_sql_entity.Ingredient.id,
            )
            .all()
        )
        return list_order_items

    def list_order_item_receipts(
        self,
        order_sql_entity: Type[database.Base],
        ingredient_sql_entity: Type[database.Base],
        order_id: str,
    ) -> list[Type[database.Base]]:
        list_order_item_receipts = (
            self._database.query(order_sql_entity.OrderItemReceipt)
            .filter(order_sql_entity.OrderItemReceipt.order_id == order_id)
            .join(
                ingredient_sql_entity.Ingredient,
                order_sql_entity.OrderItemReceipt.ingredient_id
                == ingredient_sql_entity.Ingredient.id,
            )
            .all()
        )
        return list_order_item_receipts

    def list_product_receipts(
        self,
        product_sql_entity: Type[database.Base],
        ingredient_sql_entity: Type[database.Base],
        product_id: str,
    ) -> list[Type[database.Base]]:
        list_receipts = (
            self._database.query(product_sql_entity.ProductReceipt)
            .filter(product_sql_entity.ProductReceipt.product_id == product_id)
            .join(
                ingredient_sql_entity.Ingredient,
                product_sql_entity.ProductReceipt.ingredient_id
                == ingredient_sql_entity.Ingredient.id,
            )
            .all()
        )
        return list_receipts

    def list_order(
        self, 
        order_sql_entity: Type[database.Base],
        dict_filter: dict = None
    ) -> list[Type[database.Base]]:
        status_order = case(
            (order_sql_entity.Order.status == "PRONTO", 1),
            (order_sql_entity.Order.status == "EM_PREPARACAO", 2),
            (order_sql_entity.Order.status == "RECEBIDO", 3),
            else_=4
        )

        if dict_filter is None:
            statuses_to_exclude = ["FINALIZADO", "CANCELADO"]

            orders = self._database.query(
                order_sql_entity.Order
            ).filter(
                order_sql_entity.Order.status.notin_(statuses_to_exclude)
            ).order_by(
                status_order.asc(),
                order_sql_entity.Order.internal_id.asc()
            ).all()

        orders = self._database.query(
           order_sql_entity.Order
        ).filter_by(
            **dict_filter if dict_filter else {}
        ).order_by(
            status_order.asc(),
            order_sql_entity.Order.internal_id.asc()
        ).all()
        return orders
