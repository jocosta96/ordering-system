from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.domain.value_objects.money import Money
from app.domain.value_objects.status import OrderStatus, OrderStatusType
from app.adapter.inbound.rest.entity.ingredient_rest import Ingredient
from app.adapter.inbound.rest.entity.product_rest import Product, ProductReceiptItem


class OrderItem(BaseModel):
    id: Optional[str] = None
    order_id: Optional[str] = None
    product: Product
    additional_ingredient: list[Ingredient] = []
    remove_ingredient: list[Ingredient] = []
    item_receipt: list[ProductReceiptItem] = []
    price: Money= Money(amount=0.00)

    model_config = {
        "arbitrary_types_allowed": True
    }


class Order(BaseModel):
    id: Optional[str] = None
    customer_id: int
    value: Money = Money(amount=0.00)
    status: OrderStatus = OrderStatus(status=OrderStatusType.RECEBIDO)
    payment_date: Optional[datetime] = None
    payment_transaction_id: Optional[str] = None
    has_payment_verified: bool
    order_items: list[OrderItem]

    model_config = {
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "customer_id": 1,
                "payment_date": "2025-05-26T18:25:01.962Z",
                "payment_transaction_id": "string",
                "has_payment_verified": True,
                "order_items": [
                    {
                        "product": {
                            "name": {
                                "name": "X-Bullgerrrrrr"
                            },
                            "category": {
                                "category": "LANCHE"
                            },
                            "default_ingredient": [
                                {
                                    "ingredient": {
                                        "id": 1,
                                        "name": {
                                            "name": "QUEIJO PRATO"
                                        },
                                        "price": {
                                            "amount": "0.0"
                                        },
                                        "product_category": {
                                            "category": "LANCHE"
                                        },
                                        "is_active": True
                                    },
                                    "quantity": 3
                                },
                                {
                                    "ingredient": {
                                        "id": 2,
                                        "name": {
                                            "name": "ALFACE"
                                        },
                                        "price": {
                                            "amount": "0.0"
                                        },
                                        "product_category": {
                                            "category": "LANCHE"
                                        },
                                        "is_active": True
                                    },
                                    "quantity": 1
                                }
                            ],
                            "price": {
                                "amount": "12.5"
                            },
                            "sku": {
                                "sku": "PROD-1238-XYZ"
                            },
                            "id": "5bc76687-014a-4950-8a23-999959157630"
                        },
                        "additional_ingredient": [
                            {
                                "id": 1,
                                "name": {
                                    "name": "QUEIJO PRATO"
                                },
                                "price": {
                                    "amount": "0.00"
                                },
                                "product_category": {
                                    "category": "LANCHE"
                                },
                                "is_active": True
                            }
                        ],
                        "remove_ingredient": []
                    }
                ]
            }
        }
    }
