from pydantic import BaseModel, Field, field_validator
from enum import Enum


class OrderStatusType(str, Enum):

    RECEBIDO = "RECEBIDO"
    EM_PREPARACAO = "EM_PREPARACAO"
    PRONTO = "PRONTO"
    FINALIZADO = "FINALIZADO"


class OrderStatus(BaseModel):

    status: str = Field(
        ...,
        description="Order Status",
        examples=["RECEBIDO", "EM_PREPARACAO", "PRONTO", "FINALIZADO"]
    )

    @field_validator("status")
    def validate(cls, value):
        assert OrderStatusType(value)
        return value
    
    def __str__(self) -> str:
        return self.status

    @property
    def value(self) -> str:
        return self.status

